from db import Database
from config import get_banlist_ids
import logging

#db
db = Database()

#banlist
banlist: set[int] = set(get_banlist_ids())

#logger for users
file_handler = logging.FileHandler(filename='logs\log_users.txt', encoding='utf-8')

file_handler.setLevel(logging.INFO)

file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)

logger = logging.getLogger("users")
logger.addHandler(file_handler)

#logger for admins
file_handler_admin = logging.FileHandler(filename='logs\log_admins.txt', encoding='utf-8')

file_handler_admin.setLevel(logging.INFO)

file_format_admin = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler_admin.setFormatter(file_format)

logger_admin = logging.getLogger("admin")
logger_admin.addHandler(file_handler_admin)