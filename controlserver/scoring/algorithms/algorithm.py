from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from typing import Collection, Mapping, TypeAlias
import sys

from controlserver.logger import log
from controlserver.models import (
    Service,
    TeamPointsLite,
    SubmittedFlag,
    LogMessage,
)
from saarctf_commons.config import ScoringConfig


TeamServicePair: TypeAlias = tuple[int, int]
TickTeamPair: TypeAlias = tuple[int, int]
ServiceTickPair: TypeAlias = tuple[int, int]
ServicePayloadPair: TypeAlias = tuple[int, int]


class FlagSet:
    def __init__(self) -> None:
        self._set: set[tuple[int, int, int, int]] = (
            set()
        )  # service, team, tick_issued, payload

    def is_new(self, flag: SubmittedFlag) -> bool:
        """
        Return True if this flag was not seen by this set before.
        Submitter is ignored, thus similar to "flag string".
        """
        key = (flag.service_id, flag.team_id, flag.tick_issued, flag.payload)
        if key in self._set:
            return False
        self._set.add(key)
        return True


@dataclass(frozen=True)
class StolenFlag:
    flag: SubmittedFlag
    num_previous_submissions: int
    num_submissions: int
    previous_submitter_ids: Collection[int]



class ScoreTickAlgorithm(ABC):
    """
    Scoring algorithm interface, which also implements most of the boilerplate to get/set results.
    """

    def __init__(
        self, config: ScoringConfig, team_ids: list[int], services: list[Service]
    ) -> None:
        self.config = config
        self.team_ids = team_ids
        self.services = services
        self.services_by_id = {service.id: service for service in services}

    @abstractmethod
    def calculate_scoring_for_tick(
        self,
        current_tick: int,
        checker_results: Mapping[int, Mapping[TeamServicePair, tuple[str, Mapping | None]]],
        last_tick_points: dict[TeamServicePair, TeamPointsLite],
        prev_attacking: Mapping[tuple[int, int, int], Mapping[int, set[int]]],
        num_active: Mapping[int, set[int]],
        flags: list[StolenFlag],
    ) -> dict[TeamServicePair, TeamPointsLite]:
        raise NotImplementedError()


class ScoreTickAlgorithmAtklab(
    ScoreTickAlgorithm, ABC
):
    BASE_POINTS: float = 10.0

    def _jeopardy_scaling(self, captures: int) -> float:
        return int(10*(30/(29+max(captures,1)))**3)

    def calculate_scoring_for_tick(
        self,
        current_tick: int,
        checker_results: Mapping[int, Mapping[TeamServicePair, tuple[str, Mapping | None]]],
        last_tick_points: dict[TeamServicePair, TeamPointsLite],
        prev_attacking: Mapping[tuple[int, int, int], Mapping[int, set[int]]],
        num_active: Mapping[int, set[int]],
        flags: list[StolenFlag],
    ) -> dict[TeamServicePair, TeamPointsLite]:
        """
        Calculate the results for one tick
        """

        # 1. Spaces for results
        new_tick_points: dict[TeamServicePair, TeamPointsLite] = {}
        for team_id in self.team_ids:
            for service in self.services:
                new_tick_points[(team_id, service.id)] = TeamPointsLite(
                    team_id=team_id, service_id=service.id, tick=current_tick
                )

        # 2. Calculate SLA and number of active teams
        def sla(status: str, getflags: Mapping[str, str] | None, flags_per_tick: int) -> float:
            if status == "SUCCESS":
                return self.BASE_POINTS * flags_per_tick
            elif status == "RECOVERING":
                flag_ticks = 0
                if getflags is not None:
                    for related_tick in range(current_tick - self.config.flags_rounds_valid + 1, current_tick + 1):
                        for flagstore_id in range(int(flags_per_tick)):
                            related_round_result = getflags.get(f"{related_tick}_{flagstore_id}")
                            flag_ticks += related_round_result == "OK"
                return flag_ticks / (self.config.flags_rounds_valid * flags_per_tick) \
                    * self.BASE_POINTS * flags_per_tick
            else:
                return 0
        for (team_id, service_id), teampoints in new_tick_points.items():
            status, getflags = checker_results[current_tick][(team_id, service_id)]
            teampoints.sla_delta = sla(status, getflags,
                            self.services_by_id[service_id].flags_per_tick)

        # 3. Distribute points for all flags submitted this tick
        stolen_flags = FlagSet()
        new_attacking: dict[tuple[int, int, int], dict[int, set[int]]] = defaultdict(lambda: defaultdict(lambda: set()))
        for flag in flags:
            if flag.flag.team_id == self.config.nop_team_id or \
                    flag.flag.submitted_by == self.config.nop_team_id:
                continue
            if flag.flag.tick_issued <= current_tick - self.config.flags_rounds_valid:
                continue

            try:
                # Mark flag as newly stolen and update victim mapping
                flag_key = flag.flag.tick_issued, flag.flag.service_id, flag.flag.payload
                # Was this team previously attacked by the attacker
                if flag.flag.team_id not in prev_attacking[flag_key].get(flag.flag.submitted_by, set()):
                    new_attacking_tick = new_attacking[flag_key]
                    new_attacking_tick[flag.flag.submitted_by].add(flag.flag.team_id)
                victim = new_tick_points[flag.flag.team_id, flag.flag.service_id]

                def offense(num_submissions: int):
                    return self._jeopardy_scaling(num_submissions)

                # Give new attacker points
                attacker = new_tick_points[(flag.flag.submitted_by, flag.flag.service_id)]
                attacker.flag_captured_count += 1
                num_total_submissions = flag.num_previous_submissions + flag.num_submissions
                attacker.off_points += offense(num_total_submissions)

                # Reduce points of previous attackers
                if stolen_flags.is_new(flag.flag): # once per flag
                    if flag.num_previous_submissions == 0:
                        victim.flag_stolen_count += 1
                    elif flag.num_previous_submissions > 0: # quirk of query
                        assert len(flag.previous_submitter_ids) == flag.num_previous_submissions
                        for ps in flag.previous_submitter_ids:
                            new_tick_points[(ps, flag.flag.service_id)].off_points += (
                                offense(num_total_submissions)
                                - offense(flag.num_previous_submissions)
                        )
            except KeyError:
                print(
                    f"Flag submitted for invalid team/service: "
                    f"flag #{flag.flag.id} ({flag.flag.team_id}, {flag.flag.service_id})"
                )
                log(
                    "scoring",
                    "Flag submitted for invalid team/service",
                    f"flag #{flag.flag.id} ({flag.flag.team_id}, {flag.flag.service_id})",
                    level=LogMessage.WARNING,
                )

        # 4. Update points for not being attacked in previous and current round
        def defense(max_victims: int, num_victims: int, num_attackers: int, exploited: bool):
            if exploited or num_victims == 0: return 0
            value = self._jeopardy_scaling(max_victims - num_victims)
            return value * max_victims / num_attackers

        max_ticks = min(self.config.flags_rounds_valid, current_tick)
        min_tick = current_tick - max_ticks + 1
        for flag_tick in range(min_tick, current_tick + 1):
            for service in self.services:
                for flagstore_id in range(service.num_payloads):
                    flag_key = (flag_tick, service.id, flagstore_id)
                    prev_attacking_tick = prev_attacking[flag_key]
                    new_attacking_tick = new_attacking[flag_key]
                    num_prev_attacking_tick = sum(1 for team in self.team_ids if team in prev_attacking_tick)
                    num_new_attacking_tick = sum(1 for team in self.team_ids if team in prev_attacking_tick or team in new_attacking_tick) 
                    for attacker in set(prev_attacking_tick) | set(new_attacking_tick):
                        prev_victims = prev_attacking_tick.get(attacker, set())
                        new_victims = new_attacking_tick.get(attacker, set())
                        num_prev_victims = len(prev_victims)
                        num_new_victims = len(new_victims)
                        for team in self.team_ids:
                            if team == self.config.nop_team_id:
                                continue

                            prev_defense = 0
                            new_defense = 0
                            for related_tick in range(flag_tick, current_tick + 1):
                                status, getflags = checker_results[related_tick][team, service.id]
                                num_active_tick = len(num_active.get(related_tick, set()))
                                max_victims = max(num_active_tick - 1, 1)
                                if status not in {"SUCCESS", "RECOVERING"}:
                                    continue
                                if getflags is not None and getflags.get(f"{flag_tick}_{flagstore_id}") == "OK":
                                    new_defense_tick = defense(max_victims, num_prev_victims + num_new_victims, num_new_attacking_tick, (team in new_victims) or (team in prev_victims))
                                    new_defense += new_defense_tick / self.config.flags_rounds_valid
                                    if current_tick != related_tick:
                                        prev_defense_tick = defense(max_victims, num_prev_victims, num_prev_attacking_tick, team in prev_victims)
                                    else:
                                        prev_defense_tick = 0.0 # Not scored yet
                                    prev_defense += prev_defense_tick / self.config.flags_rounds_valid

                            teampts = new_tick_points[team, service.id]
                            if team == attacker:
                                teampts.off_points += new_defense - prev_defense
                            else:
                                teampts.def_points += new_defense - prev_defense

        # 5. Add the points from previous tick
        for (team_id, service_id), teampoints in new_tick_points.items():
            lr = last_tick_points[(team_id, service_id)]
            teampoints.off_points += lr.off_points
            teampoints.def_points += lr.def_points
            teampoints.sla_points = lr.sla_points + teampoints.sla_delta
            teampoints.flag_captured_count += lr.flag_captured_count
            teampoints.flag_stolen_count += lr.flag_stolen_count

        return new_tick_points

