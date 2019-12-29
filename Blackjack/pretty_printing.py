"""
Utility class for pretty printing.
"""
from colorama import Fore, Style


def pretty_print(text="", color=Fore.WHITE):
    """
    :type text: String
    :type color: AnsiFore
    """
    print(color + text + Style.RESET_ALL)


def pretty_input(text="", color=Fore.CYAN):
    """
    :type text: String
    :type color: AnsiFore
    """
    return input(color + text + Style.RESET_ALL)


def pretty_print_win(text):
    """
    Print win
    """
    pretty_print(text, Fore.LIGHTGREEN_EX)


def pretty_print_lose(text):
    """
    Print lose
    """
    pretty_print(text, Fore.LIGHTRED_EX)


def pretty_print_info(text):
    """
    Print info
    """
    pretty_print(text, Fore.CYAN)


def pretty_print_error(text):
    """
    Print error
    """
    pretty_print(text, Fore.RED)
