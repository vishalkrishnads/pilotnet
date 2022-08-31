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

def clear(print_banner=True):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    if print_banner:
        banner()