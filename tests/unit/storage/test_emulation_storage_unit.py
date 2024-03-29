from typing import Callable, List, Tuple
from unittest import mock

import pytest

from overhave.storage import EmulationStorage


class TestEmulationStorage:
    """
    Unit tests for :class:`EmulationStorage`.

    functions with logic over redis or database.
    """

    TARGET_USER_ID = 1
    OTHER_USER_ID = 2

    @pytest.mark.parametrize(
        ("allocated_port_user_pairs", "used_ports", "expected_result"),
        [
            ([], [], False),
            ([(8080, TARGET_USER_ID), (8081, OTHER_USER_ID)], [8080], True),
            ([(8080, TARGET_USER_ID), (8081, OTHER_USER_ID)], [8081], False),
            ([(8080, TARGET_USER_ID), (8081, TARGET_USER_ID), (8082, TARGET_USER_ID)], [], False),
            ([(8080, TARGET_USER_ID), (8081, TARGET_USER_ID), (8082, TARGET_USER_ID)], [8082], True),
        ],
        ids=[
            "empty_suite",
            "used_by_target_user",
            "used_by_other_user",
            "nothing_is_used",
            "one_from_many_is_used",
        ],
    )
    def test_has_running_emulation_with_user(
        self,
        allocated_port_user_pairs: List[Tuple[int, int]],
        used_ports: List[int],
        expected_result: bool,
    ) -> None:
        # No database or redis is used, as necessary database layer functions in
        # storage should are mocked
        emulation_storage = EmulationStorage(mock.MagicMock(), mock.MagicMock())
        emulation_storage.get_allocated_port_user_pairs = lambda **_: allocated_port_user_pairs  # type: ignore
        emulation_storage._is_port_in_use = get_dummy_used_ports_method(used_ports)  # type: ignore

        result = emulation_storage.has_running_emulation_with_user(self.TARGET_USER_ID)

        assert result == expected_result


# +---------+
# | Helpers |
# +---------+


def get_dummy_used_ports_method(used_ports: List[int]) -> Callable[[int], bool]:
    ports = used_ports.copy()

    def dummy_method(port: int) -> bool:
        return port in ports

    return dummy_method
