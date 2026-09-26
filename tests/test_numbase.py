import pytest

import numbase
from numbase import bin_grouped, convert, default_copy_format, parse_number


@pytest.fixture(autouse=True)
def fake_clipboard(monkeypatch):
    """Never touch the real clipboard during tests."""
    copied = []
    monkeypatch.setattr(numbase, "copy_to_clipboard", lambda text: copied.append(text) or True)
    return copied


@pytest.mark.parametrize("raw, expected", [
    ("255", (255, "DEC")),
    ("007", (7, "DEC")),
    ("0b11111111", (255, "BIN")),
    ("0B1010", (10, "BIN")),
    ("0xFF", (255, "HEX")),
    ("0xff", (255, "HEX")),
    ("0o377", (255, "OCT")),
    ("  42  ", (42, "DEC")),
    ("1_000", (1000, "DEC")),
    ("0", (0, "DEC")),
])
def test_parse_number(raw, expected):
    assert parse_number(raw) == expected


@pytest.mark.parametrize("raw", ["", "abc", "0b102", "0xZZ", "0o8", "-5", "1.5", "0x"])
def test_parse_number_rejects_invalid(raw):
    with pytest.raises(ValueError):
        parse_number(raw)


def test_bin_grouped_pads_to_nibbles():
    assert bin_grouped(0) == "0000"
    assert bin_grouped(5) == "0101"
    assert bin_grouped(255) == "1111 1111"
    assert bin_grouped(256) == "0001 0000 0000"


def test_convert_all_bases():
    assert convert(255) == {"dec": "255", "bin": "11111111", "hex": "FF", "oct": "377"}


def test_big_numbers_are_exact():
    n = 2 ** 100 + 1
    assert parse_number(hex(n))[0] == n
    assert convert(n)["dec"] == str(n)


def test_default_copy_format():
    assert default_copy_format("BIN") == "dec"
    for base in ("DEC", "HEX", "OCT"):
        assert default_copy_format(base) == "bin"


def test_copy_override_is_what_gets_copied(fake_clipboard, capsys):
    assert numbase.run_once("255", "hex") == 0
    assert fake_clipboard == ["FF"]
    assert "Copied (HEX): FF" in capsys.readouterr().out


def test_default_copy(fake_clipboard):
    numbase.run_once("0b1010")
    numbase.run_once("10")
    assert fake_clipboard == ["10", "1010"]


def test_no_copy(fake_clipboard):
    numbase.run_once("255", "hex", copy=False)
    assert fake_clipboard == []


def test_invalid_input_exit_code(capsys):
    assert numbase.run_once("zz") == 1
    assert "Cannot parse" in capsys.readouterr().err


def test_output_is_plain_when_piped(capsys, monkeypatch):
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    with pytest.raises(SystemExit) as exc:
        numbase.main(["0xFF", "--no-copy"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "\033[" not in out
    assert "│  HEX  FF" in out


def test_interactive_session(monkeypatch, capsys, fake_clipboard):
    answers = iter(["42", "nope", "q"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    numbase.run_interactive()
    out = capsys.readouterr().out
    assert "101010" in out and "Invalid input" in out and "Bye." in out
    assert fake_clipboard == ["101010"]
