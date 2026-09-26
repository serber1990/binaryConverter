# binaryConverter — Number Base Converter

[![CI](https://github.com/serber1990/binaryConverter/actions/workflows/ci.yml/badge.svg)](https://github.com/serber1990/binaryConverter/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/numbase-converter.svg)](https://badge.fury.io/py/numbase-converter)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/serber1990/binaryConverter?style=social)](https://github.com/serber1990/binaryConverter/stargazers)

Convert between **decimal**, **binary**, **hexadecimal** and **octal** — all at once, in one command.
Available as a pip-installable Python CLI (`numbase`) and as a dependency-free Bash script.

---

## ✨ Features

- 🔄 **All bases at once** — enter a number in any base, see DEC / BIN / HEX / OCT simultaneously
- 🔍 **Auto-detection** — prefix-based input: `255`, `0b1010`, `0xFF`, `0o17` (underscores allowed: `1_000`)
- ♾️ **Interactive or one-shot** — a prompt for quick sessions, or a single command for scripts
- 📋 **Clipboard support** — result copied automatically (`wl-copy`, `xclip`, `xsel` or `pbcopy`), or `--no-copy`
- 🔢 **Arbitrary precision** — the Python version handles numbers of any size
- 🔇 **Script-friendly** — plain output when piped or when `NO_COLOR` is set

---

## 📥 Installation

### Python (recommended)

```bash
pip install numbase-converter
```

### Bash (no dependencies)

```bash
git clone https://github.com/serber1990/binaryConverter.git
./binaryConverter/bash/binaryConverter.sh
```

---

## 🛠 Usage

### One-shot mode

```bash
numbase 255
numbase 0xFF
numbase 0b11001010
numbase 0o377
```

```
  ╭──────────────────╮
  │  DEC  255        │
  │  BIN  1111 1111  │
  │  HEX  FF         │
  │  OCT  377        │
  ╰──────────────────╯

  ✔  Copied (BIN): 11111111
```

### Interactive mode

```bash
numbase
```

Type numbers one after another; `q` (or Ctrl+D) quits.

### Clipboard

By default the most useful counterpart is copied: the **decimal** value for binary input, the **binary** value otherwise.

```bash
numbase 255 --copy hex     # copies FF
numbase 0xFF --copy dec    # copies 255
numbase 255 --no-copy      # leaves the clipboard alone
```

---

## 🎨 Input formats

| Format | Example | Description |
|--------|---------|-------------|
| Decimal | `255` | Plain number (leading zeros are fine) |
| Binary | `0b11111111` | Prefix `0b` or `0B` |
| Hexadecimal | `0xFF` | Prefix `0x` or `0X` |
| Octal | `0o377` | Prefix `0o` or `0O` |

The Bash version accepts the same formats, both as an argument (`binaryConverter.sh 0xFF`) and at the prompt.
It is limited to 63-bit values (max `9223372036854775807`); larger numbers are rejected with a clear error.

---

## 🗂 Repository structure

```
binaryConverter/
├── numbase.py                  Python CLI (pip-installable as numbase)
├── bash/
│   └── binaryConverter.sh      Bash version
├── python/
│   └── binaryConverter.py      Compatibility shim → numbase
└── tests/                      pytest suite (Python + Bash)
```

---

## 🧪 Development

```bash
pip install -e ".[dev]"
ruff check .
pytest
shellcheck bash/binaryConverter.sh
```

See [CHANGELOG.md](CHANGELOG.md) for release notes.

---

## 📝 License

MIT — see [LICENSE](LICENSE).

---

## 💬 Feedback

Open an issue or reach out via GitHub.

## 🌐 Connect

[![GitHub](https://img.shields.io/badge/GitHub-@serber1990-181717?style=flat-square&logo=github)](https://github.com/serber1990)
