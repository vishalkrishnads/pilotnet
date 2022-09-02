# Two simple functions banner() & clear() pretty self explanatory

from termcolor import colored
import os

def banner():
    banner = '''
███████████   ███  ████            █████    ██████   █████           █████   
░░███░░░░░███ ░░░  ░░███           ░░███    ░░██████ ░░███           ░░███    
 ░███    ░███ ████  ░███   ██████  ███████   ░███░███ ░███   ██████  ███████  
 ░██████████ ░░███  ░███  ███░░███░░░███░    ░███░░███░███  ███░░███░░░███░   
 ░███░░░░░░   ░███  ░███ ░███ ░███  ░███     ░███ ░░██████ ░███████   ░███    
 ░███         ░███  ░███ ░███ ░███  ░███ ███ ░███  ░░█████ ░███░░░    ░███ ███
 █████        █████ █████░░██████   ░░█████  █████  ░░█████░░██████   ░░█████ 
░░░░░        ░░░░░ ░░░░░  ░░░░░░     ░░░░░  ░░░░░    ░░░░░  ░░░░░░     ░░░░░
                    https://arxiv.org/pdf/1704.07911.pdf
    '''

    print(colored(banner, 'green'))

def clear(print_banner: 'Whether to print the banner. Defaults to True' = True):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    if print_banner:
        banner()

def message(text: 'The message text you wanna print', mode='success'):
    color = {
        'success': 'green',
        'warn': 'yellow',
        'error': 'red'
    }
    print(f'{colored("*", color[mode])} {text}')

def warn(text: 'Warning message'):
    message(text, mode='warn')

def error(text: 'Error message'):
    message(text, mode='error')