from colorama import Fore, Style


def pretty_print(text="", color=Fore.WHITE):
    print(color + text + Style.RESET_ALL)


def pretty_input(text="", color=Fore.CYAN):
    return input(color + text + Style.RESET_ALL)