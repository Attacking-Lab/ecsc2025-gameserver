import json
from typing import Any

from controlserver.models import Service, Team
from gamelib import flag_ids, get_flag_regex
from saarctf_commons.config import config
from saarctf_commons.redis import get_redis_connection


class FlagIDFileGenerator:
    def generate(self, teams: list[Team], services: list[Service], tick: int) -> dict:
        from controlserver.timer import Timer

        data: dict[str, Any] = {
            "flag_regex": get_flag_regex().pattern,
            "teams": [
                {
                    "id": team.id,
                    "name": team.name,
                    "affiliation": team.affiliation,
                    "logo": team.logo,
                    "ip": team.vulnbox_ip,
                    "online": team.vpn_connected or team.vpn2_connected,
                }
                for team in teams
            ],
            "attack_info": {},
            "current_tick": Timer.current_tick,
            "current_tick_start": Timer.tick_start,
            "current_tick_until": Timer.tick_end,
        }

        for service in services:
            if service.flag_ids:
                data["attack_info"][service.name] = self.get_service_flag_ids(
                    service, teams, tick
                )

        return data

    def get_service_flag_ids(
        self, service: Service, teams: list[Team], latest_tick: int
    ) -> dict:
        data: dict = {}
        flag_id_types = service.flag_ids.split(",") if service.flag_ids else []
        min_tick = max(1, latest_tick - config.SCORING.flags_rounds_valid)

        if "custom" in flag_id_types:
            custom_flag_ids = self._load_custom_flag_ids(service, min_tick, latest_tick)
        else:
            custom_flag_ids = {}

        for team in teams:
            data[team.vulnbox_ip] = {}
            for tick in range(min_tick, latest_tick):
                ids = {
                    i: (
                        custom_flag_ids.get((tick, team.id, i), None)
                        if flag_id_type == "custom"
                        else flag_ids.generate_flag_id(
                            flag_id_type, service.id, team.id, tick, i
                        )
                    )
                    for i, flag_id_type in enumerate(flag_id_types)
                }
                data[team.vulnbox_ip][tick] = ids
        return data

    def generate_and_save(
        self, teams: list[Team], services: list[Service], tick: int
    ) -> None:
        data = self.generate(teams, services, tick)
        for path in (config.PUBLIC_SCOREBOARD_PATH, config.INTERNAL_SCOREBOARD_PATH):
            (path / "api" / f"attack_round_{tick}.json").write_text(json.dumps(data))
            (path / "api" / "attack.json").write_text(json.dumps(data))

    def _load_custom_flag_ids(
        self, service: Service, min_tick: int, latest_tick: int
    ) -> dict[tuple[int, int, int], str | None]:
        result = {}
        with get_redis_connection() as conn:
            for tick in range(min_tick, latest_tick):
                keys = conn.keys(f"custom_flag_ids:{service.id}:{tick}:*")
                for k, v in zip(keys, conn.mget(keys)):
                    _, _, tck, teamid, idx = k.decode().split(":")
                    result[(int(tck), int(teamid), int(idx))] = (
                        v.decode("utf-8") if v else None
                    )
        return result
