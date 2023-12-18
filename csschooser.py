from bs4 import BeautifulSoup
import os
import re
import requests
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.theme import Theme
import sys
import validators

# Fetch the file or URL as prettyprinted HTML
# Selector editor
# Highlight matching elements
# Tune the selector
# Return selector as output

regex_count = 3


def get_soup(name):
    """Get a BeuatifulSoup object of a file or URL.

    :param str name: A filename or URL to open and convert.
    :raises FileNotFoundError: Thrown if both the filename does not exist and the URL is not a valid URL.
    :return BeautifulSoup: A BeautifulSoup instance representing the contents of the file or URL.
    """
    is_url = validators.url(name)

    try:
        if is_url:
            r = re.sub(
                r"\<(script|style)[\s\S]*?\<\/\1\>",
                "",
                requests.get(name)
                .text.replace("\r\n", "\n")
                .replace("\n\r", "\n")
                .strip(),
            )
            s = BeautifulSoup(r, "html.parser")
        else:
            with open(name, "r") as f:
                s = BeautifulSoup(f.read().strip(), "html.parser")
    except:
        raise FileNotFoundError

    return s


def clear(lines=1, out=True):
    """Clear the screen and set the cursor back `lines` lines if lines is greater than 0, else run the operating
    system's clear screen command

    :param int lines: Number of lines to clear, defaults to 1
    :param bool out: Whether to write to the terminal as well as return the string, defaults to True
    :return str: A string that would clear the screen if printed to the console
    """
    if lines < 1:
        _ = os.system("cls") if os.name == "nt" else os.system("clear")
        return ""

    up = "\033[1A"
    erase = "\x1b[2K"
    s = ""

    for _ in range(lines):
        if out:
            print(up, end=erase)

        s += up + erase

    return s


def get_regex(s):
    """Get a Regular Expression to match the DOM element in a prettified string
    with proper indentation.

    :param str s: An outer HTML value including the contents of the element; e.g. <b>Important</b>
    :return str: A pattern string that can be used to match the element as a Regular Expression
    """
    global regex_count
    s = str(s)
    r = re.findall(r"(<[^\>\<]*?>)", s)
    if r:
        open, close = re.escape(r[0]), re.escape(r[len(r) - 1])
    else:
        s = re.escape(s)
        open = s
        close = s
    if open != close:
        s = r"(\s*){}[\s\S]*?\{}{}".format(open, regex_count, close)
        regex_count += 1
    return s


def paginate(console, pretty):
    """Open a string with the operating system's pager using a specified console.

    :param rich.console.Console console: A `rich` library console to print the output
    :param str pretty: The text to open with pagination
    """
    with console.pager(styles=True):
        console.print(pretty)


def interactive_select(soup):
    """Interactively select a CSS selector from a BeautifulSoup DOM object.

    :param BeautifulSoup soup: The BeautifulSoup object to choose from
    :return str: The last CSS selector you entered before exiting
    """
    global regex_count

    first = True
    full = ""
    finalize = ""
    sel = "null"
    theme = Theme({"selector.elements": "blue", "code": "none", "reverse": "none"})

    print()

    while first or full:
        console = Console(highlighter=ClassHighlighter(soup, sel=sel), theme=theme)
        old_log = "" if first else pretty
        pretty = soup.prettify()

        if len(pretty.split("\n")) > os.get_terminal_size()[1]:
            paginate(console, pretty)
            clear(-1)
        elif not first:
            clear(len(old_log.split("\n")) + 2)

        console.print(pretty)

        first = False
        finalize = " [Leave empty to exit]"
        old = full
        full = input(f"\nSelector ({full}){finalize}: ")
        sel = full
        regex_count = 3

    clear(-1)
    return old


def main():
    while True:
        try:
            name = input("Filename or URL: ")
            soup = get_soup(name)

            old = interactive_select(soup)
            break
        except:
            sys.exit("Invalid filename or URL!")

    print()
    print(f"You chose: {old}")


class ClassHighlighter(RegexHighlighter):
    """Apply style based on a Regular Expression.

    :param class RegexHighlighter: A class to be used with the `rich` highlighting library.
    """

    base_style = "selector."

    def __init__(self, soup, sel="null"):
        s = soup.select(sel)
        regex = "(" + "|".join([get_regex(x) for x in s]) + ")"

        self.highlights = [r"(?P<elements>" + regex + ")"]


if __name__ == "__main__":
    main()
