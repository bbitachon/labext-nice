import pytest
from nicegui.testing import User
from labext_nice.gui_elements.labext import main

pytest_plugins = ["nicegui.testing.user_plugin"]


@pytest.fixture
def user(user: User) -> User:
    from click.testing import CliRunner
    from unittest.mock import patch

    with patch("labext_nice.gui_elements.labext.ui.run"):
        CliRunner().invoke(main, [])
    return user
