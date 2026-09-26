#!/usr/bin/env bash
# binaryConverter — number base converter (DEC ↔ BIN ↔ HEX ↔ OCT)
#
# Usage:
#   binaryConverter.sh            interactive mode
#   binaryConverter.sh NUMBER     one-shot mode (255, 0b1010, 0xFF, 0o17)

set -uo pipefail

if [[ -t 1 && -z "${NO_COLOR:-}" ]]; then
    C_CYAN=$'\033[0;36m'
    C_GREEN=$'\033[0;32m'
    C_YELLOW=$'\033[1;33m'
    C_MAGENTA=$'\033[0;35m'
    C_RED=$'\033[0;31m'
    C_BOLD=$'\033[1m'
    C_DIM=$'\033[2m'
    C_RESET=$'\033[0m'
else
    C_CYAN='' C_GREEN='' C_YELLOW='' C_MAGENTA='' C_RED='' C_BOLD='' C_DIM='' C_RESET=''
fi

# ── Clipboard ─────────────────────────────────────────────────────────────────

# xclip/xsel stay in the background to serve the selection: their output must go
# to /dev/null or they keep pipes open and block command substitutions.
copy_to_clipboard() {
    local text="$1"
    if [[ -n "${WAYLAND_DISPLAY:-}" ]] && command -v wl-copy &>/dev/null; then
        printf '%s' "$text" | wl-copy >/dev/null 2>&1 && return 0
    fi
    if command -v xclip &>/dev/null; then
        printf '%s' "$text" | xclip -selection clipboard >/dev/null 2>&1 && return 0
    fi
    if command -v xsel &>/dev/null; then
        printf '%s' "$text" | xsel --clipboard --input >/dev/null 2>&1 && return 0
    fi
    if command -v pbcopy &>/dev/null; then
        printf '%s' "$text" | pbcopy >/dev/null 2>&1 && return 0
    fi
    return 1
}

# ── Conversions ───────────────────────────────────────────────────────────────

to_bin() {
    local n=$1 result=""
    (( n == 0 )) && { echo 0; return; }
    while (( n > 0 )); do
        result="$(( n % 2 ))${result}"
        n=$(( n / 2 ))
    done
    echo "$result"
}

# Group a binary string in nibbles of 4: 11111111 → "1111 1111"
bin_display() {
    local raw="$1" out="" i
    local pad=$(( (4 - ${#raw} % 4) % 4 ))
    while (( pad-- > 0 )); do raw="0${raw}"; done
    for (( i = 0; i < ${#raw}; i += 4 )); do
        out+="${out:+ }${raw:i:4}"
    done
    echo "$out"
}

strip_leading_zeros() {
    local d="$1"
    while [[ ${#d} -gt 1 && ${d:0:1} == 0 ]]; do d="${d:1}"; done
    echo "$d"
}

# Parse a number with optional 0b/0x/0o prefix.
# Sets VALUE and BASE. Returns 1 on invalid input, 2 if it does not fit in 63 bits.
parse_number() {
    local s="${1//[[:space:]]/}" digits back
    case "$s" in
        0[bB]*) BASE=BIN; digits="${s:2}"; [[ "$digits" =~ ^[01]+$ ]]         || return 1 ;;
        0[xX]*) BASE=HEX; digits="${s:2}"; [[ "$digits" =~ ^[0-9a-fA-F]+$ ]]  || return 1 ;;
        0[oO]*) BASE=OCT; digits="${s:2}"; [[ "$digits" =~ ^[0-7]+$ ]]        || return 1 ;;
        *)      BASE=DEC; digits="$s";     [[ "$digits" =~ ^[0-9]+$ ]]        || return 1 ;;
    esac
    digits="$(strip_leading_zeros "$digits")"
    (( ${#digits} <= 64 )) || return 2

    # Explicit base prefixes avoid Bash reading "010" as octal.
    case "$BASE" in
        BIN) VALUE=$(( 2#$digits ));  back="$(to_bin "$VALUE")" ;;
        HEX) VALUE=$(( 16#$digits )); back="$(printf '%X' "$VALUE")"; digits="${digits^^}" ;;
        OCT) VALUE=$(( 8#$digits ));  back="$(printf '%o' "$VALUE")" ;;
        DEC) VALUE=$(( 10#$digits )); back="$VALUE" ;;
    esac
    # Bash integers are signed 64-bit: a value that does not round-trip overflowed.
    (( VALUE >= 0 )) && [[ "$back" == "$digits" ]] || return 2
}

# ── Output ────────────────────────────────────────────────────────────────────

box_row() {
    local label="$1" color="$2" value="$3" width="$4"
    printf '  %s│%s  %s%s%s%s  %s%-*s%s  %s│%s\n' \
        "$C_CYAN" "$C_RESET" "$C_BOLD" "$C_GREEN" "$label" "$C_RESET" \
        "$color" "$width" "$value" "$C_RESET" "$C_CYAN" "$C_RESET"
}

show_result() {
    local value="$1" base="$2"
    local bin_raw bin_d hex oct width line copy_val
    bin_raw="$(to_bin "$value")"
    bin_d="$(bin_display "$bin_raw")"
    hex="$(printf '%X' "$value")"
    oct="$(printf '%o' "$value")"

    width=${#value}
    for v in "$bin_d" "$hex" "$oct"; do (( ${#v} > width )) && width=${#v}; done
    printf -v line '%*s' $(( width + 9 )) ''
    line="${line// /─}"

    echo ""
    printf '  %s╭%s╮%s\n' "$C_CYAN" "$line" "$C_RESET"
    box_row DEC "$C_YELLOW"  "$value" "$width"
    box_row BIN "$C_CYAN"    "$bin_d" "$width"
    box_row HEX "$C_GREEN"   "$hex"   "$width"
    box_row OCT "$C_MAGENTA" "$oct"   "$width"
    printf '  %s╰%s╯%s\n' "$C_CYAN" "$line" "$C_RESET"

    # Copy the most useful counterpart: decimal for binary input, binary otherwise.
    if [[ "$base" == BIN ]]; then copy_val="$value"; else copy_val="$bin_raw"; fi
    if copy_to_clipboard "$copy_val"; then
        printf '\n  %s✔  Copied: %s%s\n' "$C_DIM" "$copy_val" "$C_RESET"
    fi
    echo ""
}

convert() {
    local rc=0
    parse_number "$1" || rc=$?
    case $rc in
        0) show_result "$VALUE" "$BASE" ;;
        1) printf '\n  %s✖  Invalid input: %s%s\n\n' "$C_RED" "$1" "$C_RESET" ;;
        2) printf '\n  %s✖  Too large for the Bash version (max 2^63-1). Use the Python version: numbase%s\n\n' "$C_RED" "$C_RESET" ;;
    esac
    return $rc
}

usage() {
    cat <<EOF
Usage: $(basename "$0") [NUMBER]

Convert a number between decimal, binary, hexadecimal and octal.
Without NUMBER an interactive prompt is started.

Accepted input:  255   0b1010   0xFF   0o17
EOF
}

# ── Main ──────────────────────────────────────────────────────────────────────

if (( $# > 0 )); then
    case "$1" in
        -h|--help) usage; exit 0 ;;
    esac
    convert "$1"
    exit $?
fi

echo ""
printf '  %s╔══════════════════════════╗%s\n' "$C_CYAN" "$C_RESET"
printf '  %s║%s  %s%sNumber Base Converter%s   %s║%s\n' "$C_CYAN" "$C_RESET" "$C_BOLD" "$C_CYAN" "$C_RESET" "$C_CYAN" "$C_RESET"
printf '  %s╚══════════════════════════╝%s\n' "$C_CYAN" "$C_RESET"
echo ""

trap 'printf "\n  %sBye.%s\n\n" "$C_DIM" "$C_RESET"; exit 0' INT

while true; do
    printf '  %sAccepts:  255   0b1010   0xFF   0o17   ·   q to quit%s\n' "$C_DIM" "$C_RESET"
    if ! read -rp "  ${C_GREEN}>${C_RESET} " input; then
        echo ""
        break
    fi
    [[ -z "${input// /}" ]] && continue
    if [[ "$input" == [qQ] ]]; then
        printf '\n  %sBye.%s\n\n' "$C_DIM" "$C_RESET"
        break
    fi
    convert "$input"
done
