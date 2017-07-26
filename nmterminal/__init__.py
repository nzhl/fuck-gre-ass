from .client import Client
from .logger import get_logger

logger = get_logger(__name__)

def go():
    try:
        client = Client()
        client.loop()
    except KeyboardInterrupt:
        logger.debug("\n" + "-" * 40 + "\nProgram Exit\n" + "-" * 40)
    finally:
        client.ui.deinit()
        client.moodle.save_cookies()
