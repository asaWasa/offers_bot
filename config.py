import os
from dotenv import load_dotenv


load_dotenv()

MAIN_CHANNEL_ID = os.getenv("MAIN_CHANNEL_ID", default=None)
ADMIN_CHANNEL_ID = os.getenv("ADMIN_CHANNEL_ID", default=None)

API_KEY = os.getenv("API_KEY", default="0000")

DB_REDIS_URL = os.getenv("DB_REDIS_URL", default=None)
DB_REDIS_PORT = os.getenv("DB_REDIS_PORT", default=None)


LOGGING = bool(int(os.getenv("LOGGING", default=0)))
LOGGING_LVL = int(os.getenv("LOGGING_LVL", default=20))
ADMINS = list(os.getenv("ADMIN_LIST", default=[]))

SLEEP_FOR_FORWARD_TASK_SEC = int(os.getenv("SLEEP_FOR_FORWARD_TASK_SEC", default=5))
