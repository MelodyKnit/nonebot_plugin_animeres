import pytest
import nonebot
from nonebug import NONEBOT_INIT_KWARGS


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "asyncio: mark test as async")
    config.stash[NONEBOT_INIT_KWARGS] = {
        "driver": "~none",
        "command_start": {"", "/"},
    }


@pytest.fixture(scope="session", autouse=True)
def load_bot(nonebug_init: None) -> None:
    try:
        from nonebot.adapters.onebot.v11 import Adapter

        driver = nonebot.get_driver()
        driver.register_adapter(Adapter)
    except ImportError:
        pass  # OneBot 适配器是 optional 依赖
    nonebot.require("nonebot_plugin_animeres")
