import pytest

from csschooser.csschooser import clear, get_soup, interactive_select, get_regex

# Disable console output
def paginate(c, p):
    pass

class Console():
    def print(self, s):
        pass

def test_get_regex():
    assert get_regex('') == ''
    assert get_regex(None) == 'None'
    assert get_regex('<p>Hi!</p>') == r"(\s*)<p>[\s\S]*?\{}</p>".format(3)
    assert get_regex('<p>Hi! Two</p>') == r"(\s*)<p>[\s\S]*?\{}</p>".format(4)
    assert get_regex('<meta />') == '<meta />'


def test_get_soup():
    soup = str(get_soup("test.html"))
    assert soup == '<html><body><p class="hi">Hi!!</p><p>Hello</p><div class="hi">Hello there!<p id="hi"><a href="#hi">Hi!</a></p></div></body></html>'
    
    with pytest.raises(FileNotFoundError):
        soup = str(get_soup("fake.html"))

def test_interactive_select(monkeypatch):
    global regex_count
    soup = get_soup("test.html")
    
    inputs = iter(['p', '', '#hi', ''])
    monkeypatch.setattr('builtins.input', lambda _="": next(inputs))
    monkeypatch.setattr('os.get_terminal_size', lambda _="": (10, 10))
    selection = interactive_select(soup)
    assert selection == "p"

    selection = interactive_select(soup)
    assert selection == "#hi"
    
def test_clear(monkeypatch):
    monkeypatch.setattr('os.system', lambda _="": 0)
    assert clear(-1) == False
    assert clear(10) == "\033[1A\x1b[2K" * 10