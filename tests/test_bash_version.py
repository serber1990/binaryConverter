import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "bash" / "binaryConverter.sh"

pytestmark = pytest.mark.skipif(shutil.which("bash") is None, reason="bash not available")


@pytest.fixture
def run(tmp_path):
    # Fake clipboard tools so the tests never touch the real clipboard.
    clip = tmp_path / "clip.txt"
    fakebin = tmp_path / "bin"
    fakebin.mkdir()
    for tool in ("xclip", "xsel", "wl-copy", "pbcopy"):
        exe = fakebin / tool
        exe.write_text(f"#!/bin/sh\ncat > '{clip}'\n")
        exe.chmod(exe.stat().st_mode | stat.S_IEXEC)
    env = {**os.environ, "PATH": f"{fakebin}{os.pathsep}{os.environ['PATH']}"}

    def _run(*args, stdin=None):
        r = subprocess.run(["bash", str(SCRIPT), *args], input=stdin, env=env,
                           capture_output=True, text=True, timeout=20)
        copied = clip.read_text() if clip.exists() else None
        return r, copied
    return _run


@pytest.mark.parametrize("arg, dec, bin_, hex_, oct_", [
    ("255", "255", "1111 1111", "FF", "377"),
    ("010", "10", "1010", "A", "12"),          # decimal, not octal
    ("0b101", "5", "0101", "5", "5"),
    ("0xff", "255", "1111 1111", "FF", "377"),
    ("0o17", "15", "1111", "F", "17"),
    ("0", "0", "0000", "0", "0"),
])
def test_one_shot(run, arg, dec, bin_, hex_, oct_):
    r, _ = run(arg)
    assert r.returncode == 0, r.stdout
    for label, value in (("DEC", dec), ("BIN", bin_), ("HEX", hex_), ("OCT", oct_)):
        assert f"{label}  {value} " in r.stdout


def test_max_value_and_overflow(run):
    r, _ = run("9223372036854775807")
    assert r.returncode == 0 and "7FFFFFFFFFFFFFFF" in r.stdout
    for too_big in ("9223372036854775808", "0xFFFFFFFFFFFFFFFF"):
        r, _ = run(too_big)
        assert r.returncode == 2 and "Too large" in r.stdout


def test_invalid_input(run):
    r, _ = run("0b102")
    assert r.returncode == 1 and "Invalid input" in r.stdout


def test_clipboard_content(run):
    assert run("42")[1] == "101010"
    assert run("0b101010")[1] == "42"


def test_interactive(run):
    r, _ = run(stdin="42\nxyz\nq\n")
    assert r.returncode == 0
    assert "DEC  42" in r.stdout and "Invalid input: xyz" in r.stdout and "Bye." in r.stdout


def test_no_ansi_when_piped(run):
    r, _ = run("7")
    assert "\033[" not in r.stdout
