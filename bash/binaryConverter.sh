#!/usr/bin/env bash
# binaryConverter — interactive base converter (DEC ↔ BIN ↔ HEX ↔ OCT)

C_CYAN="\033[0;36m"
C_GREEN="\033[0;32m"
C_YELLOW="\033[1;33m"
C_MAGENTA="\033[0;35m"
C_RED="\033[0;31m"
C_BOLD="\033[1m"
C_DIM="\033[2m"
C_RESET="\033[0m"

# ── Clipboard ─────────────────────────────────────────────────────────────────

copy_to_clipboard() {
    local text="$1"
    if command -v xclip &>/dev/null; then
        echo -n "$text" | xclip -selection clipboard && return 0
    elif command -v xsel &>/dev/null; then
        echo -n "$text" | xsel --clipboard --input && return 0
    elif command -v pbcopy &>/dev/null; then
        echo -n "$text" | pbcopy && return 0
    fi
    return 1
}

# ── Conversions ───────────────────────────────────────────────────────────────

dec_to_bin() {
    local n=$1
    [[ $n -eq 0 ]] && echo "0" && return
    local result=""
    while [[ $n -gt 0 ]]; do
        result="$((n % 2))${result}"
        n=$((n / 2))
    done
    echo "$result"
}

bin_to_dec() {
    echo "$((2#$1))"
}

dec_to_hex() {
    printf '%X' "$1"
}

hex_to_dec() {
    echo "$((16#$1))"
}

dec_to_oct() {
    printf '%o' "$1"
}

oct_to_dec() {
    echo "$((8#$1))"
}

# Group binary string in nibbles of 4
bin_display() {
    local raw="$1"
    local pad=$(( (4 - ${#raw} % 4) % 4 ))
    printf '%0*d%s' "$((${#raw} + pad))" 0 "${raw:0}" 2>/dev/null || echo "$raw"
    # simpler approach:
    raw=$(printf '%*s' "$((${#raw} + pad))" "$raw" | tr ' ' '0')
    local out=""
    for ((i=0; i<${#raw}; i+=4)); do
        [[ -n "$out" ]] && out+=" "
        out+="${raw:$i:4}"
    done
    echo "$out"
}

show_result() {
    local dec="$1"
    local bin_r; bin_r=$(dec_to_bin "$dec")
    local bin_d; bin_d=$(bin_display "$bin_r")
    local hex; hex=$(dec_to_hex "$dec")
    local oct; oct=$(dec_to_oct "$dec")

    echo ""
    echo -e "  ${C_CYAN}╭────────────────────────╮${C_RESET}"
    echo -e "  ${C_CYAN}│${C_RESET}  ${C_BOLD}${C_GREEN}DEC${C_RESET}  ${C_YELLOW}${dec}${C_RESET}"
    echo -e "  ${C_CYAN}│${C_RESET}  ${C_BOLD}${C_GREEN}BIN${C_RESET}  ${C_CYAN}${bin_d}${C_RESET}"
    echo -e "  ${C_CYAN}│${C_RESET}  ${C_BOLD}${C_GREEN}HEX${C_RESET}  ${C_GREEN}${hex}${C_RESET}"
    echo -e "  ${C_CYAN}│${C_RESET}  ${C_BOLD}${C_GREEN}OCT${C_RESET}  ${C_MAGENTA}${oct}${C_RESET}"
    echo -e "  ${C_CYAN}╰────────────────────────╯${C_RESET}"

    if copy_to_clipboard "$bin_r"; then
        echo -e "\n  ${C_DIM}✔  Copied: ${bin_r}${C_RESET}"
    fi
    echo ""
}

# ── Header ────────────────────────────────────────────────────────────────────

echo ""
echo -e "  ${C_CYAN}╔══════════════════════════╗${C_RESET}"
echo -e "  ${C_CYAN}║${C_RESET}  ${C_BOLD}${C_CYAN}Number Base Converter${C_RESET}  ${C_CYAN}║${C_RESET}"
echo -e "  ${C_CYAN}╚══════════════════════════╝${C_RESET}"
echo ""

# ── Main loop ─────────────────────────────────────────────────────────────────

trap 'echo -e "\n  ${C_DIM}Bye.${C_RESET}\n"; exit 0' INT

while true; do
    echo -e "  ${C_DIM}Choose input format:${C_RESET}"
    echo -e "    ${C_GREEN}1${C_RESET}  Decimal   → all bases"
    echo -e "    ${C_GREEN}2${C_RESET}  Binary    → all bases"
    echo -e "    ${C_GREEN}3${C_RESET}  Hex       → all bases"
    echo -e "    ${C_GREEN}4${C_RESET}  Octal     → all bases"
    echo -e "    ${C_GREEN}q${C_RESET}  Quit"
    echo ""
    read -rp "  $(echo -e "${C_GREEN}>${C_RESET}") " option

    case "$option" in
        1)
            read -rp "  $(echo -e "${C_YELLOW}Decimal number: ${C_RESET}")" input
            if ! [[ "$input" =~ ^[0-9]+$ ]]; then
                echo -e "\n  ${C_RED}✖  Not a valid decimal number.${C_RESET}\n"
                continue
            fi
            show_result "$input"
            ;;
        2)
            read -rp "  $(echo -e "${C_CYAN}Binary number: ${C_RESET}")" input
            if ! [[ "$input" =~ ^[01]+$ ]]; then
                echo -e "\n  ${C_RED}✖  Not a valid binary number.${C_RESET}\n"
                continue
            fi
            show_result "$(bin_to_dec "$input")"
            ;;
        3)
            read -rp "  $(echo -e "${C_GREEN}Hex number (without 0x): ${C_RESET}")" input
            if ! [[ "$input" =~ ^[0-9a-fA-F]+$ ]]; then
                echo -e "\n  ${C_RED}✖  Not a valid hexadecimal number.${C_RESET}\n"
                continue
            fi
            show_result "$(hex_to_dec "$input")"
            ;;
        4)
            read -rp "  $(echo -e "${C_MAGENTA}Octal number: ${C_RESET}")" input
            if ! [[ "$input" =~ ^[0-7]+$ ]]; then
                echo -e "\n  ${C_RED}✖  Not a valid octal number.${C_RESET}\n"
                continue
            fi
            show_result "$(oct_to_dec "$input")"
            ;;
        q|Q)
            echo -e "\n  ${C_DIM}Bye.${C_RESET}\n"
            exit 0
            ;;
        *)
            echo -e "\n  ${C_RED}✖  Invalid option.${C_RESET}\n"
            ;;
    esac
done
