import logging
import sys
from luci.settings import TOKEN, SETTINGS_MODULE, __version__
from core.commands import client

logging.basicConfig(level='INFO')
log = logging.getLogger()

if __name__ == '__main__':
    log.info(
        '''
            ==========
            ╦  ╦ ╦╔═╗╦
            ║  ║ ║║  ║
            ╩═╝╚═╝╚═╝╩
            ==========
         Logical Unity for
    Communicational Interactivity
        '''
    )
    log.info('Running LUCI version: %s\n', __version__)

    client.run(TOKEN)
