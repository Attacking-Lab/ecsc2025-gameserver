import os
import sys
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from typing import Iterable

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from saarctf_commons.config import config, load_default_config

load_default_config()
NAMESPACE = config.CTFROUTE_NAMESPACE
TIMEZONE = timezone.utc


class GateNames(StrEnum):
    CLOSE_NETWORK = "close-network"
    BLOCK_INTER_TEAMS = "block-inter-teams"
    BLOCK_VULNBOX_ACCESS = "block-vulnbox-access"


def delete_gates(names: Iterable[str]):
    # for gate in Gate.list(namespace=NAMESPACE):
    #     if gate.name in names:
    #         Gate.delete(name=gate.name)
    pass


def close_network(start: datetime | None = None, until: datetime | None = None):
    # if not any(
    #     GateNames.BLOCK_INTER_TEAMS == gate.name
    #     for gate in Gate.list(namespace=NAMESPACE)
    # ):
    #     add_connection_gate(
    #         namespace=NAMESPACE,
    #         name=GateNames.CLOSE_NETWORK,
    #         conn_src="any-team",
    #         conn_dst="any-team",
    #         from_time=start,
    #         to_time=until,
    #     )
    #
    # delete_gates(
    #     names=(
    #         GateNames.BLOCK_INTER_TEAMS,
    #         GateNames.BLOCK_VULNBOX_ACCESS,
    #     )
    # )
    pass


def open_network():
    # delete_gates(
    #     names=(
    #         GateNames.BLOCK_INTER_TEAMS,
    #         GateNames.BLOCK_VULNBOX_ACCESS,
    #         GateNames.CLOSE_NETWORK,
    #     ),
    # )
    pass


def open_network_within_teams(
    start: datetime | None = None, duration: timedelta | None = None
):
    # if (from_time := start) and duration:
    #     to_time = from_time + duration
    # else:
    #     to_time = None
    #
    # if not any(
    #     GateNames.BLOCK_INTER_TEAMS == gate.name
    #     for gate in Gate.list(namespace=NAMESPACE)
    # ):
    #     add_connection_gate(
    #         namespace=NAMESPACE,
    #         name=GateNames.BLOCK_INTER_TEAMS,
    #         conn_src="any-team",
    #         conn_dst="other-team",
    #         from_time=from_time,
    #         to_time=to_time,
    #     )
    #
    # delete_gates(
    #     names=(
    #         GateNames.CLOSE_NETWORK,
    #         GateNames.BLOCK_VULNBOX_ACCESS,
    #     ),
    # )
    pass


def open_network_within_teams_no_vulnbox(
    start: timedelta | None = None, duration: timedelta | None = None
):
    # if (from_time := start) and duration:
    #     to_time = from_time + duration
    # else:
    #     to_time = None
    #
    # if not any(
    #     GateNames.BLOCK_INTER_TEAMS == gate.name
    #     for gate in Gate.list(namespace=NAMESPACE)
    # ):
    #     add_connection_gate(
    #         namespace=NAMESPACE,
    #         name=GateNames.BLOCK_INTER_TEAMS,
    #         conn_src="any-team",
    #         conn_dst="other-team",
    #         from_time=from_time,
    #         to_time=to_time,
    #     )
    #
    # if GateNames.BLOCK_VULNBOX_ACCESS not in {
    #     gate.name for gate in Gate.list(namespace=NAMESPACE)
    # }:
    #     add_connection_gate(
    #         namespace=NAMESPACE,
    #         name=GateNames.BLOCK_VULNBOX_ACCESS,
    #         conn_src="any-team",
    #         conn_dst="any-vulnbox",
    #     )
    #
    # delete_gates(
    #     names=(GateNames.CLOSE_NETWORK,),
    # )
    pass


def ban_team(
    team: str, start: datetime | None = None, duration: timedelta | None = None
):
    # if (from_time := start) and duration:
    #     to_time = from_time + duration
    # else:
    #     to_time = None
    #
    # # TODO: support for timed bans (ctfroute feature)
    # if f"ban-{team}" not in [gate.name for gate in Gate.list(namespace=NAMESPACE)]:
    #     add_connection_gate(
    #         namespace=NAMESPACE,
    #         name=f"ban-{team}",
    #         conn_src=f"team-{team}",
    #         conn_dst="other-team",
    #         from_time=from_time,
    #         to_time=to_time,
    #     )
    #
    pass


def remove_ban(team: str):
    # delete_gates(names=(f"ban-{team}",))
    pass
