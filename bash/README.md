# binaryConverter — Bash version

Dependency-free Bash implementation of the number base converter. It shows a number in
decimal, binary, hexadecimal and octal at once and copies the result to the clipboard.

## Usage

```bash
./binaryConverter.sh            # interactive prompt (q or Ctrl+D to quit)
./binaryConverter.sh 255        # one-shot
./binaryConverter.sh 0xFF
./binaryConverter.sh 0b1010
./binaryConverter.sh 0o17
```

Exit codes: `0` success, `1` invalid input, `2` number larger than 2^63-1.

## Clipboard

The binary value is copied (the decimal value when the input was binary) using the first available
tool: `wl-copy` (Wayland), `xclip`, `xsel` or `pbcopy`. Nothing happens if none is installed.

## Limits

Bash integers are signed 64-bit, so the maximum is `9223372036854775807` (`0x7FFFFFFFFFFFFFFF`).
For bigger numbers use the Python version: `pip install numbase-converter` and run `numbase`.

See the [main README](../README.md) for more details.
