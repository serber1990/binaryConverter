# binaryConverter — Number Base Converter

[![PyPI version](https://badge.fury.io/py/numbase-converter.svg)](https://badge.fury.io/py/numbase-converter)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/serber1990/binaryConverter?style=social)](https://github.com/serber1990/binaryConverter/stargazers)

Convert between **decimal**, **binary**, **hexadecimal** and **octal** — all at once, in one command. Available as both a Python CLI tool and a Bash script.

---

## ✨ Features

- 🔄 **All bases at once** — enter a number in any base, see DEC / BIN / HEX / OCT simultaneously
- 🔍 **Auto-detection** — prefix-based input: `255`, `0b1010`, `0xFF`, `0o17`
- ♾️ **Continuous loop** — convert multiple numbers without restarting
- 📋 **Clipboard support** — result copied automatically (`xclip`, `xsel` or `pbcopy`)
- 🖥️ **Two versions** — Python (`numbase`) and Bash (`binaryConverter.sh`)

---

## 📥 Installation

### Python (recommended)

```bash
pip install numbase-converter
```

### Bash

```bash
git clone https://github.com/serber1990/binaryConverter.git
chmod +x binaryConverter/bash/binaryConverter.sh
./binaryConverter/bash/binaryConverter.sh
```

---

## 🛠 Usage

### Interactive mode

```bash
numbase
```

```
  ╔══════════════════════════╗
  ║  Number Base Converter   ║
  ╚══════════════════════════╝

  Accepts:  255   0b1010   0xFF   0o17   ·   q to quit

  > 255

  ╭──────────────────────╮
  │  DEC  255            │
  │  BIN  1111 1111      │
  │  HEX  FF             │
  │  OCT  377            │
  ╰──────────────────────╯
  ✔  Copied: 11111111
```

### One-shot mode

```bash
numbase 255
numbase 0xFF
numbase 0b11001010
numbase 0o377
```

### Copy a specific format

```bash
numbase 255 --copy hex     # copies FF to clipboard
numbase 0xFF --copy dec    # copies 255 to clipboard
```

---

## 🎨 Input formats

| Format | Example | Description |
|--------|---------|-------------|
| Decimal | `255` | Plain number |
| Binary | `0b11111111` | Prefix `0b` or `0B` |
| Hexadecimal | `0xFF` | Prefix `0x` or `0X` |
| Octal | `0o377` | Prefix `0o` or `0O` |

---

## 🗂 Repository structure

```
binaryConverter/
├── numbase.py          Python CLI (pip-installable as numbase)
├── bash/
│   └── binaryConverter.sh   Bash version
└── python/
    └── binaryConverter.py   Compatibility shim → numbase
```

---

## 📝 License

MIT — see [LICENSE](LICENSE).

---

## 💬 Feedback

Open an issue or reach out via GitHub.

## 🌐 Connect

[![GitHub](https://img.shields.io/badge/GitHub-@serber1990-181717?style=flat-square&logo=github)](https://github.com/serber1990)
