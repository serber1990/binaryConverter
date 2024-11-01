# Binary Converter

Binary Converter is a Python command-line tool for converting decimal numbers to binary and binary numbers to decimal. The tool also uses the `colorize-term` library to enhance terminal output with colors.

---

## ✨ Features

- 🔢 **Convert Decimal to Binary**: Converts any decimal number into an 8-bit binary representation.
- 🔠 **Convert Binary to Decimal**: Converts binary numbers back into decimal format.
- 📋 **Clipboard Support**: Automatically copies results to the clipboard (requires `xclip` on Linux).
- 🌈 **Colorized Output**: Uses the `colorize-term` library for colorful terminal output.

---

## 📥 Installation

Clone the repository and install `colorize-term`:

```bash
git clone https://github.com/serber1990/binaryConverter.git
cd binaryConverter
pip install colorize-term
```

For clipboard functionality on Linux, make sure `xclip` is installed:

```bash
sudo apt-get install xclip
```

---

## 🛠 Usage

Run the script with:

```bash
python binary_converter.py
```

### Options

1. Convert decimal to binary
2. Convert binary to decimal
3. Quit

The script will prompt you to enter a decimal or binary number depending on your choice.

---

## 🎨 Examples

### Convert Decimal to Binary

```plaintext
Choose an option:
1. Convert decimal to binary
2. Convert binary to decimal
q. To Quit
> 1
Enter a decimal number: 45

Binary representation: 00101101
Binary result copied to clipboard.
```

### Convert Binary to Decimal

```plaintext
Choose an option:
1. Convert decimal to binary
2. Convert binary to decimal
q. To Quit
> 2
Enter a binary number: 101010

Decimal representation: 42
Decimal result copied to clipboard.
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💬 Feedback

If you have any questions, issues, or suggestions, please feel free to open an issue in the repository or contact me directly via GitHub.

---

## 🌐 Connect with Me

[![GitHub](https://img.shields.io/badge/GitHub-@serber1990-181717?style=flat-square&logo=github)](https://github.com/serber1990)

---

### 🚀 Easily convert between binary and decimal with Binary Converter!
