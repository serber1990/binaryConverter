#!/usr/bin/env python3

import sys
from colorize_term import Color
from pwn import log, context

# Set context for pwntools (optional)
context.log_level = 'info'  # Sets default log level

# Function to convert decimal to binary
def convert_to_binary(decimal):
    binary = bin(decimal)[2:].zfill(8)  # Convert to binary and pad to 8 bits
    log.info(f"{Color.BLUE}Binary representation: {Color.RESET}{binary}")
    try:
        # Copy to clipboard if xclip is available
        import subprocess
        subprocess.run("echo -n '{}' | xclip -selection clipboard".format(binary), shell=True)
        log.success(f"{Color.GREEN}Binary result copied to clipboard.{Color.RESET}")
    except Exception as e:
        log.failure(f"{Color.RED}Failed to copy to clipboard: {e}{Color.RESET}")

# Function to convert binary to decimal
def convert_from_binary(binary):
    decimal = int(binary, 2)  # Convert binary string to decimal
    log.info(f"{Color.YELLOW}Decimal representation: {Color.RESET}{decimal}")
    try:
        # Copy to clipboard if xclip is available
        import subprocess
        subprocess.run("echo -n '{}' | xclip -selection clipboard".format(decimal), shell=True)
        log.success(f"{Color.GREEN}Decimal result copied to clipboard.{Color.RESET}")
    except Exception as e:
        log.failure(f"{Color.RED}Failed to copy to clipboard: {e}{Color.RESET}")

# Main loop to provide options to the user
def main():
    banner_text = f"{Color.GREEN}Welcome to Binary Converter!{Color.RESET}"
    log.info(banner_text.center(50, '-'))
    
    while True:
        print(f"\n{Color.CYAN}Choose an option:{Color.RESET}")
        print(f"{Color.MAGENTA}1. Convert {Color.YELLOW}decimal{Color.MAGENTA} to binary{Color.RESET}")
        print(f"{Color.MAGENTA}2. Convert {Color.BLUE}binary{Color.MAGENTA} to decimal{Color.RESET}")
        print(f"{Color.MAGENTA}q. To {Color.RED}Quit{Color.RESET}")
        
        option = input(f"{Color.GREEN}> {Color.RESET}")

        if option == "1":
            decimal_input = input(f"Enter a {Color.YELLOW}decimal{Color.RESET} number: ")
            if not decimal_input.isdigit():
                log.failure(f"{Color.RED}Invalid input. Please enter a valid decimal number.{Color.RESET}")
            else:
                convert_to_binary(int(decimal_input))
                break
        elif option == "2":
            binary_input = input(f"Enter a {Color.BLUE}binary{Color.RESET} number: ")
            if not all(bit in "01" for bit in binary_input):
                log.failure(f"{Color.RED}Invalid input. Please enter a valid binary number.{Color.RESET}")
            else:
                convert_from_binary(binary_input)
                break
        elif option.lower() == "q":
            log.info(f"{Color.GREEN}Exiting...{Color.RESET}")
            break
        else:
            log.failure(f"{Color.RED}Invalid option.{Color.RESET}")

if __name__ == "__main__":
    main()
