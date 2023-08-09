import logging
import sys
from luci.settings import TOKEN, SETTINGS_MODULE, __version__
from core.commands import client
from core.training.text_gen import GenerativeModel, ddic, ddic_aux

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
         Logical Unit for
    Communicational Interactivity
        '''
    )
    log.info('Running LUCI version: %s\n', __version__)

    client.run(TOKEN)
