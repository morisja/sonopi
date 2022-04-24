# init app
# hw manager
import structlog
from hw_manager import get_hardware_manager
from app_manager import get_app_manager

logger = structlog.get_logger()

logger.info("starting")
app = get_app_manager()

hw = get_hardware_manager()

logger.info("binding")
hw.bind_and_run(
    app.scroll_right,
    app.scroll_left,
    app.press_select,
    app.press_k1,
    app.press_k2,
    app.press_k3,
    app.press_k4,
    app.info,
)
