"""
LUCI settings module.
"""
from decouple import config

__version__ = '0.1.2'

TOKEN = config('TOKEN', '')
API_URL = config('BOT_API', '')
LISA_URL = config('LISA_URL', '')
SETTINGS_MODULE = config('SETTINGS_MODULE', 'common')
SELF_ID = config('SELF_ID', '')
