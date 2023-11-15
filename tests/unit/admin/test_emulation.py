from unittest import mock

import pytest
from wtforms import Form, ValidationError

from overhave import db
from overhave.admin.views import EmulationView


@pytest.mark.parametrize("test_mock_patch_user_directory", ["overhave.admin.views.emulation.current_user"],
                         indirect=True)
class TestEmulationView:
    """Unit tests for EmulationView."""

    @pytest.mark.parametrize("user_role", [db.Role.admin], indirect=True)
    def test_admin_can_delete(
        self, test_emulation_view: EmulationView, test_emulation_row: db.Emulation, current_user_mock: mock.MagicMock
    ) -> None:
        test_emulation_view.on_model_delete(test_emulation_row)

    @pytest.mark.parametrize("user_role", [db.Role.user], indirect=True)
    def test_not_created_user_cannot_delete(
        self, test_emulation_view: EmulationView, test_emulation_row: db.Emulation, current_user_mock: mock.MagicMock
    ) -> None:
        with pytest.raises(ValidationError):
            test_emulation_view.on_model_delete(test_emulation_row)

    @pytest.mark.parametrize("user_role", [db.Role.user], indirect=True)
    def test_user_is_creator_if_is_created_true(
        self, test_emulation_view: EmulationView, test_emulation_row: db.Emulation, current_user_mock: mock.MagicMock,
        form_mock: Form
    ) -> None:
        assert test_emulation_row.created_by != current_user_mock.login
        test_emulation_view.on_model_change(form_mock, test_emulation_row, True)
        assert test_emulation_row.created_by == current_user_mock.login

    @pytest.mark.parametrize("user_role", [db.Role.user], indirect=True)
    def test_user_is_not_creator_if_is_created_false(
        self, test_emulation_view: EmulationView, test_emulation_row: db.Emulation, current_user_mock: mock.MagicMock,
        form_mock: Form
    ) -> None:
        assert test_emulation_row.created_by != current_user_mock.login
        test_emulation_view.on_model_change(form_mock, test_emulation_row, False)
        assert test_emulation_row.created_by != current_user_mock.login

    @pytest.mark.parametrize("user_role", [db.Role.user], indirect=True)
    def test_creator_user_can_delete(
        self, test_emulation_view: EmulationView, test_emulation_row: db.Emulation, current_user_mock: mock.MagicMock,
        form_mock: Form
    ) -> None:
        test_emulation_view.on_model_change(form_mock, test_emulation_row, True)
        test_emulation_view.on_model_delete(test_emulation_row)

    @pytest.mark.parametrize("user_role", [db.Role.user], indirect=True)
    def test_additional_cmd_description_is_equal_emulation_desc_link(self, test_emulation_view: EmulationView,
                                                                     current_user_mock: mock.MagicMock,
                                                                     test_emulation_desc_link: str,
                                                                     test_mock_admin_factory_for_emulation_view: mock.MagicMock) -> None:
        assert test_emulation_view.additional_cmd_description == test_emulation_desc_link

    @pytest.mark.parametrize("user_role", [db.Role.user], indirect=True)
    def test_description_link_is_equal_emulation_desc_link(self, test_emulation_view: EmulationView,
                                                           current_user_mock: mock.MagicMock,
                                                           test_emulation_desc_link: str,
                                                           test_mock_admin_factory_for_emulation_view: mock.MagicMock) -> None:
        assert test_emulation_view.description_link == test_emulation_desc_link
