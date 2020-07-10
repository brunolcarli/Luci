import sys
from luci.settings import __version__
from core.training.train import train_bot, no_free_lunch


def help_message():
    """Shows help message"""
    sys.stdout.write('Luci command manager options: \n\n')
    for key, value in interface.items():
        sys.stdout.write(f'\t{key}\n')
        sys.stdout.write(f'\t\t{value["help"]}\n\n')


interface = {
    'train': {
        'runner': train_bot,
        'help': 'Train bot machine learn model.'
    },
    'no_free_lunch': {
        'runner': no_free_lunch,
        'help': 'Test models scores.'
    },
    'help': {
        'runner': help_message,
        'help': 'Shows this message.'
    }
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
