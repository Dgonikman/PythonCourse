from colorama import Fore, Style


def pretty_print(text="", color=Fore.WHITE):
    """
    :param text: String
    :param color: AnsiFore
    """
    print(color + text + Style.RESET_ALL)


def pretty_input(text="", color=Fore.CYAN):
    """
    :param text: String
    :param color: AnsiFore
    """
    return input(color + text + Style.RESET_ALL)


def pretty_print_win(text):
    pretty_print(text, Fore.LIGHTGREEN_EX)


def pretty_print_lose(text):
    pretty_print(text, Fore.LIGHTRED_EX)


def pretty_print_info(text):
    pretty_print(text, Fore.CYAN)


def pretty_print_error(text):
    pretty_print(text, Fore.RED)
