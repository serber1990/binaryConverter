# Binary Converter (Bash Version)

This is a Bash script to convert between decimal and binary numbers. The script includes colored terminal output to improve readability and makes use of the `xclip` tool to copy results to the clipboard.

---

## ✨ Features

- 🔢 **Convert Decimal to Binary**: Converts any decimal number into an 8-bit binary representation.
- 🔠 **Convert Binary to Decimal**: Converts binary numbers back into decimal format.
- 📋 **Clipboard Support**: Automatically copies results to the clipboard (requires `xclip` on Linux).
- 🌈 **Colorized Output**: Colored output in the terminal for easy readability.

---

## 📥 Installation

### Prerequisites

This script uses `xclip` for clipboard functionality on Linux. Install it with:
```bash
sudo apt-get install xclip
```

### Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/serber1990/binaryConverter.git
cd binaryConverter/bash
```

---

## 🛠 Usage

Make the script executable and run it:

```bash
chmod +x binary_converter.sh
./binary_converter.sh
```

### Options

The script provides a menu with the following options:

1. Convert decimal to binary
2. Convert binary to decimal
3. Quit

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

### 🚀 Easily convert between binary and decimal with Binary Converter (Bash Version)!
