# csschooser

## Video Demo:   <URL HERE>

## Description:

An interactive CLI tool for choosing CSS selectors for a web page. Designed for use as a library with BeautifulSoup and Scrapy.

This project uses the [`BeautifulSoup`](https://pypi.org/project/beautifulsoup4/) and [`rich`](https://rich.readthedocs.io/en/stable/index.html) libraries to create an interactive element-selecting experience. It can be run as program or used as a library.

Created as a final project for the CS50P course.

## Prerequisites

This project was made using Python `3.10.12` and pip `22.0.2`. See `requirements.txt` for module information.

## Installation

### Using Git:

```bash
git clone https://github.com/Makaze/csschooser.git
cd csschooser
pip install -r requirements.txt
```

## Usage

### On the Command Line:

```bash
$ python3 csschooser.py
```

### As A Library:

Example using the `BeautifulSoup` library to print the text from all matching elements:

```py
import csschooser

soup = csschooser.get_soup("http://github.com/Makaze/csschooser") # Example URLexit

selector = csschooser.interactive_select(soup)

for tag in soup.select(selector):
    print(tag.get_text().strip())
```

## API / Documentation

#### `get_soup(name)`:

> Takes in a string `name` and returns a [`BeautifulSoup`](https://pypi.org/project/beautifulsoup4/) instance based on the contents of the file or URL named `name`. Raises a `FileNotFoundError` if `name` is neither a valid URL nor a valid file name.

#### `get_regex(s)`:

> Takes in a string `s` and returns a Regular Expression pattern as a string for matching the outermost element in `s`. Returns `s` unchanged if it contains no elements.

#### `interactive_select(soup)`:

> Takes in `soup` as a [`BeautifulSoup`](https://pypi.org/project/beautifulsoup4/) instance and prompts the user to enter a CSS selector. Matching elements are highlighted in an auto-scrolling output window. Clears the terminal screen and returns the last chosen selector when the user follows the prompt to exit.

#### `clear(lines)`:

> Takes in an int `lines`. If `lines` is ``>= 1``, moves the cursor up and to the end of the line `lines` times and returns the resulting backtrack sequence as a string. Otherwise calls the system's clear terminal command, clearing the terminal screen, then returns False.


#### `paginate(console, pretty)`:

> Takes in `console` as a [`rich.Console`](https://rich.readthedocs.io/en/stable/console.html) instance and `pretty` as a string, then passes pretty to the console and sends the rich string to the system's pager utility (`less` for Linux systems).
