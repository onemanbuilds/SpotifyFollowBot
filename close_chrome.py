from os import system,name
from sys import stdout

def SetTitle(title:str):
    if name == 'posix':
        stdout.write(f"\x1b]2;{title}\x07")
    elif name in ('ce', 'nt', 'dos'):
        system(f'title {title}')
    else:
        stdout.write(f"\x1b]2;{title}\x07")

def clear():
    if name == 'posix':
        system('clear')
    elif name in ('ce', 'nt', 'dos'):
        system('cls')
    else:
        print("\n") * 120

SetTitle('[One Man Builds Chrome Killer]')
clear()
system('color 2 & taskkill /F /IM chrome.exe /T')
print('')
print('PRESS ANY KEY TO EXIT...')
system('pause > nul')