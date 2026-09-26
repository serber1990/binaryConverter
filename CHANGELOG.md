# Changelog

## 2.1.0

### Fixed
- `--copy BASE` was ignored: the default value was copied right after, overwriting it.
- The clipboard copy could hang forever (xclip/xsel keep running in the background holding the output pipe).
- Bash version: the BIN row was corrupted (`255` showed `00000000111111111111 1111`).
- Bash version: decimal input with leading zeros was read as octal (`010` → 8, `09` → error).
- Bash version: values above 2^63-1 silently overflowed; they are now rejected with a clear message.
- Bash version: the result box had no right border.

### Added
- `--no-copy` flag to leave the clipboard untouched.
- Wayland support (`wl-copy`).
- Plain output when piped or when `NO_COLOR` is set.
- Underscore separators in input (`1_000`, `0xFF_FF`).
- Bash version: auto-detected prefixes (`0b`, `0x`, `0o`) and one-shot mode (`binaryConverter.sh 0xFF`).
- Test suite (Python and Bash) and GitHub Actions CI with ShellCheck.

### Changed
- License file is now MIT, matching the package metadata.
- Requires Python 3.9+.

## 2.0.0

- Multi-base converter, continuous loop, pip-installable.
