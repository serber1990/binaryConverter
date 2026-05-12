#!/usr/bin/env python3
"""
numbase — Number Base Converter
Converts between decimal, binary, hexadecimal and octal.
Interactive REPL or one-shot CLI usage.
"""
import argparse
import re
import signal
import sys
from shellcolorize import Color

VERSION = "2.0.0"

# ── Clipboard ─────────────────────────────────────────────────────────────────

def _copy(text: str) -> bool:
    import subprocess
    for cmd in (['xclip', '-selection', 'clipboard'],
                ['xsel', '--clipboard', '--input'],
                ['pbcopy']):
        try:
            r = subprocess.run(cmd, input=text.encode(), capture_output=True)
            if r.returncode == 0:
                return True
        except FileNotFoundError:
            continue
    return False

# ── Parsing ───────────────────────────────────────────────────────────────────

def parse_number(s: str) -> tuple:
    """
    Parse an integer from a string, detecting base from prefix.
      0b / 0B  → binary
      0x / 0X  → hexadecimal
      0o / 0O  → octal
      digits   → decimal
    Returns (value: int, base_label: str).
    Raises ValueError on invalid input.
    """
    s = s.strip()
    if re.fullmatch(r'0[bB][01]+', s):
        return int(s, 2), 'BIN'
    if re.fullmatch(r'0[xX][0-9a-fA-F]+', s):
        return int(s, 16), 'HEX'
    if re.fullmatch(r'0[oO][0-7]+', s):
        return int(s, 8), 'OCT'
    if re.fullmatch(r'\d+', s):
        return int(s, 10), 'DEC'
    raise ValueError(f"Cannot parse '{s}'")

# ── Formatting ────────────────────────────────────────────────────────────────

def _bin_display(n: int) -> str:
    """Binary string grouped in nibbles (4 bits) for readability."""
    raw = bin(n)[2:]
    pad = (4 - len(raw) % 4) % 4
    raw = '0' * pad + raw
    return ' '.join(raw[i:i+4] for i in range(0, len(raw), 4))

def _bin_raw(n: int) -> str:
    return bin(n)[2:]

# ── Display primitives ────────────────────────────────────────────────────────

def _header() -> None:
    title = 'Number Base Converter'
    w = len(title) + 6
    print()
    print(f"  {Color.CYAN}╔{'═' * w}╗{Color.RESET}")
    print(f"  {Color.CYAN}║{Color.RESET}  {Color.BOLD}{Color.CYAN}{title}{Color.RESET}  {Color.CYAN}║{Color.RESET}")
    print(f"  {Color.CYAN}╚{'═' * w}╝{Color.RESET}")

def _print_result(value: int, from_base: str) -> None:
    dec   = str(value)
    bin_d = _bin_display(value)
    bin_r = _bin_raw(value)
    hex_  = hex(value)[2:].upper()
    oct_  = oct(value)[2:]

    rows = [
        ('DEC', Color.YELLOW,  dec),
        ('BIN', Color.CYAN,    bin_d),
        ('HEX', Color.GREEN,   hex_),
        ('OCT', Color.MAGENTA, oct_),
    ]

    # Determine clipboard value: complement of input base, always BIN if DEC input
    copy_map = {'DEC': bin_r, 'BIN': dec, 'HEX': bin_r, 'OCT': bin_r}
    copy_val = copy_map[from_base]

    val_w = max(len(r[2]) for r in rows)
    box_w = 5 + val_w + 2

    print()
    print(f"  {Color.CYAN}╭{'─' * box_w}╮{Color.RESET}")
    for label, color, val in rows:
        padding = ' ' * (val_w - len(val))
        print(f"  {Color.CYAN}│{Color.RESET}  "
              f"{Color.BOLD}{Color.GREEN}{label}{Color.RESET}  "
              f"{color}{val}{Color.RESET}{padding}  "
              f"{Color.CYAN}│{Color.RESET}")
    print(f"  {Color.CYAN}╰{'─' * box_w}╯{Color.RESET}")

    if _copy(copy_val):
        print(f"\n  {Color.DIM}✔  Copied: {copy_val}{Color.RESET}")
    print()

def _hint() -> None:
    print(f"  {Color.DIM}Accepts:  255   0b1010   0xFF   0o17   ·   q to quit{Color.RESET}")

# ── Modes ─────────────────────────────────────────────────────────────────────

def run_interactive() -> None:
    signal.signal(signal.SIGINT, lambda *_: (print(f"\n  {Color.DIM}Bye.{Color.RESET}\n"), sys.exit(0)))
    _header()
    print()

    while True:
        _hint()
        try:
            raw = input(f"  {Color.GREEN}>{Color.RESET} ").strip()
        except EOFError:
            break

        if not raw:
            continue
        if raw.lower() == 'q':
            print(f"\n  {Color.DIM}Bye.{Color.RESET}\n")
            break

        try:
            value, base = parse_number(raw)
        except ValueError:
            print(f"\n  {Color.RED}✖  Invalid input.{Color.RESET}\n")
            continue

        _print_result(value, base)


def run_once(raw: str, copy_override: str = None) -> None:
    try:
        value, base = parse_number(raw)
    except ValueError:
        print(f"\n  {Color.RED}✖  Cannot parse '{raw}'{Color.RESET}\n")
        sys.exit(1)

    if copy_override:
        override_map = {
            'dec': str(value),
            'bin': _bin_raw(value),
            'hex': hex(value)[2:].upper(),
            'oct': oct(value)[2:],
        }
        copy_val = override_map.get(copy_override.lower())
        if copy_val:
            _copy(copy_val)

    _print_result(value, base)

# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        prog='numbase',
        description='Convert between decimal, binary, hex and octal.',
    )
    parser.add_argument('number', nargs='?', default=None,
                        help='Number to convert (decimal, 0b binary, 0x hex, 0o octal). '
                             'Omit to start interactive mode.')
    parser.add_argument('--copy', choices=['dec', 'bin', 'hex', 'oct'], metavar='BASE',
                        help='Format to copy to clipboard: dec, bin, hex or oct')
    parser.add_argument('-v', '--version', action='version', version=f'numbase {VERSION}')
    args = parser.parse_args()

    if args.number is None:
        run_interactive()
    else:
        run_once(args.number, args.copy)


if __name__ == '__main__':
    main()
