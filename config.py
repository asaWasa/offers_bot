import os
from dotenv import load_dotenv


load_dotenv()

MAIN_CHANNEL_ID = os.getenv("MAIN_CHANNEL_ID", default=None)
ADMIN_CHANNEL_ID = os.getenv("ADMIN_CHANNEL_ID", default=None)
API_KEY = os.getenv("API_KEY", default="0000")
DB_PATH = os.getenv("DB_PATH", default=None)
DB_LOGIN = os.getenv("DB_LOGIN", default=None)
DB_PASSWORD = os.getenv("DB_PASSWORD", default=None)
LOGGING = bool(int(os.getenv("LOGGING", default=0)))
ADMINS = list(os.getenv("ADMIN_LIST", default=[]))
