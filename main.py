import sys
from luci.settings import TOKEN, SETTINGS_MODULE, __version__
from core.keep_alive import keep_alive
from core.commands import client
from core.training.train import train_bot, no_free_lunch

banner = r'''
===========
╦  ╦ ╦╔═╗╦
║  ║ ║║  ║
╩═╝╚═╝╚═╝╩
===========
'''

def initialize_bot():
    sys.stdout.write(banner)
    sys.stdout.write(f'Running LUCI version: {__version__}\n')
    sys.stdout.write(f'Settings module: {SETTINGS_MODULE}\n')

    if SETTINGS_MODULE == 'production':
        keep_alive()

    client.run(TOKEN)


interface = {
    'run': {
        'runner': initialize_bot,
        'help': 'Starts bot execution.'
    },
    'train': {
        'runner': train_bot,
        'help': 'Train bot machine learn model.'
    },
    'no_free_lunch': {
        'runner': no_free_lunch,
        'help': 'Test models scores.'
    },
}

if not len(sys.argv) > 1:
    sys.stdout.write(
        'Nenhum parâmetro foi fornecido!\nUtilize o parâmetro -h para ajuda'
    )
else:
    command = sys.argv[1]

    if command not in interface.keys():
        sys.stdout.write('Comando não reconhecido!')
    start = interface[command].get('runner')
    start()
