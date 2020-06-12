from sys import stdout
from luci.settings import TOKEN, SETTINGS_MODULE, __version__
from core.keep_alive import keep_alive
from core.commands import client

banner = r'''
===========
╦  ╦ ╦╔═╗╦
║  ║ ║║  ║
╩═╝╚═╝╚═╝╩
===========
'''

if __name__ == "__main__":
    stdout.write(banner)
    stdout.write(f'Running LUCI version: {__version__}\n')
    stdout.write(f'Settings module: {SETTINGS_MODULE}\n')

    if SETTINGS_MODULE == 'production':
        keep_alive()

    client.run(TOKEN)