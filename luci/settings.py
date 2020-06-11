"""
LUCI settings module.
"""
from decouple import config

__version__ = '0.0.0'

TOKEN = config('TOKEN', '')
API_URL = config('BOT_API', '')
LISA_URL = config('LISA', '')
SETTINGS_MODULE = config('SETTINGS_MODULE', 'common')
