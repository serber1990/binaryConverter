#!/usr/bin/env python3
"""
numbase — Number Base Converter
Converts between decimal, binary, hexadecimal and octal.
Interactive REPL or one-shot CLI usage.
"""
import argparse
import os
import re
import subprocess
import sys
from typing import Dict, Optional, Tuple

from shellcolorize import Color

VERSION = "2.1.0"

# ── Clipboard ─────────────────────────────────────────────────────────────────

_CLIPBOARD_CMDS = (
    ['wl-copy'],
    ['xclip', '-selection', 'clipboard'],
    ['xsel', '--clipboard', '--input'],
    ['pbcopy'],
)


def copy_to_clipboard(text: str) -> bool:
    """Copy text using the first available clipboard tool. Returns True on success."""
    for cmd in _CLIPBOARD_CMDS:
        if cmd[0] == 'wl-copy' and not os.environ.get('WAYLAND_DISPLAY'):
            continue
        try:
            # xclip/xsel keep running in the background to serve the selection:
            # their stdout/stderr must not be pipes or we would wait for them forever.
            r = subprocess.run(cmd, input=text.encode(), timeout=5,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
        if r.returncode == 0:
            return True
    return False

# ── Parsing ───────────────────────────────────────────────────────────────────

_PREFIXED = {
    'BIN': (re.compile(r'0[bB]([01]+)'), 2),
    'HEX': (re.compile(r'0[xX]([0-9a-fA-F]+)'), 16),
    'OCT': (re.compile(r'0[oO]([0-7]+)'), 8),
    'DEC': (re.compile(r'(\d+)'), 10),
}


def parse_number(s: str) -> Tuple[int, str]:
    """
    Parse a non-negative integer, detecting the base from its prefix.
      0b / 0B  → binary
      0x / 0X  → hexadecimal
      0o / 0O  → octal
      digits   → decimal (leading zeros allowed)
    Returns (value, base_label). Raises ValueError on invalid input.
    """
    s = s.strip().replace('_', '')
    for label, (regex, base) in _PREFIXED.items():
        m = regex.fullmatch(s)
        if m:
            return int(m.group(1), base), label
    raise ValueError(f"Cannot parse '{s}'")

# ── Formatting ────────────────────────────────────────────────────────────────

def bin_grouped(n: int) -> str:
    """Binary string grouped in nibbles (4 bits) for readability."""
    raw = format(n, 'b')
    raw = raw.zfill(-(-len(raw) // 4) * 4)
    return ' '.join(raw[i:i + 4] for i in range(0, len(raw), 4))


def convert(value: int) -> Dict[str, str]:
    """Plain (copyable) representation of value in every base."""
    return {
        'dec': str(value),
        'bin': format(value, 'b'),
        'hex': format(value, 'X'),
        'oct': format(value, 'o'),
    }


def default_copy_format(from_base: str) -> str:
    """Copy the most useful counterpart: decimal for binary input, binary otherwise."""
    return 'dec' if from_base == 'BIN' else 'bin'

# ── Display ───────────────────────────────────────────────────────────────────

def _header() -> None:
    title = 'Number Base Converter'
    w = len(title) + 4
    print()
    print(f"  {Color.CYAN}╔{'═' * w}╗{Color.RESET}")
    print(f"  {Color.CYAN}║{Color.RESET}  {Color.BOLD}{Color.CYAN}{title}{Color.RESET}  {Color.CYAN}║{Color.RESET}")
    print(f"  {Color.CYAN}╚{'═' * w}╝{Color.RESET}")


def _hint() -> None:
    print(f"  {Color.DIM}Accepts:  255   0b1010   0xFF   0o17   ·   q to quit{Color.RESET}")


def print_result(value: int, copy_format: Optional[str]) -> None:
    """Print the conversion box and copy `copy_format` ('dec'|'bin'|'hex'|'oct') if given."""
    plain = convert(value)
    rows = [
        ('DEC', Color.YELLOW,  plain['dec']),
        ('BIN', Color.CYAN,    bin_grouped(value)),
        ('HEX', Color.GREEN,   plain['hex']),
        ('OCT', Color.MAGENTA, plain['oct']),
    ]
    val_w = max(len(r[2]) for r in rows)
    box_w = 5 + val_w + 4

    print()
    print(f"  {Color.CYAN}╭{'─' * box_w}╮{Color.RESET}")
    for label, color, val in rows:
        print(f"  {Color.CYAN}│{Color.RESET}  "
              f"{Color.BOLD}{Color.GREEN}{label}{Color.RESET}  "
              f"{color}{val:<{val_w}}{Color.RESET}  "
              f"{Color.CYAN}│{Color.RESET}")
    print(f"  {Color.CYAN}╰{'─' * box_w}╯{Color.RESET}")

    if copy_format:
        copy_val = plain[copy_format]
        if copy_to_clipboard(copy_val):
            print(f"\n  {Color.DIM}✔  Copied ({copy_format.upper()}): {copy_val}{Color.RESET}")
    print()

# ── Modes ─────────────────────────────────────────────────────────────────────

def run_interactive(copy: bool = True) -> None:
    _header()
    print()
    try:
        while True:
            _hint()
            try:
                raw = input(f"  {Color.GREEN}>{Color.RESET} ").strip()
            except EOFError:
                print()
                break
            if not raw:
                continue
            if raw.lower() in ('q', 'quit', 'exit'):
                break
            try:
                value, base = parse_number(raw)
            except ValueError:
                print(f"\n  {Color.RED}✖  Invalid input.{Color.RESET}\n")
                continue
            print_result(value, default_copy_format(base) if copy else None)
    except KeyboardInterrupt:
        print()
    print(f"\n  {Color.DIM}Bye.{Color.RESET}\n")


def run_once(raw: str, copy_format: Optional[str] = None, copy: bool = True) -> int:
    try:
        value, base = parse_number(raw)
    except ValueError:
        print(f"\n  {Color.RED}✖  Cannot parse '{raw}'{Color.RESET}\n", file=sys.stderr)
        return 1
    if copy:
        copy_format = copy_format or default_copy_format(base)
    else:
        copy_format = None
    print_result(value, copy_format)
    return 0

# ── CLI ───────────────────────────────────────────────────────────────────────

def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        prog='numbase',
        description='Convert between decimal, binary, hex and octal.',
    )
    parser.add_argument('number', nargs='?', default=None,
                        help='Number to convert (decimal, 0b binary, 0x hex, 0o octal). '
                             'Omit to start interactive mode.')
    parser.add_argument('--copy', choices=['dec', 'bin', 'hex', 'oct'], metavar='BASE',
                        help='Format to copy to the clipboard: dec, bin, hex or oct')
    parser.add_argument('--no-copy', action='store_true',
                        help='Do not touch the clipboard')
    parser.add_argument('-v', '--version', action='version', version=f'numbase {VERSION}')
    args = parser.parse_args(argv)

    Color.auto()

    if args.number is None:
        run_interactive(copy=not args.no_copy)
    else:
        sys.exit(run_once(args.number, args.copy, copy=not args.no_copy))


if __name__ == '__main__':
    main()
