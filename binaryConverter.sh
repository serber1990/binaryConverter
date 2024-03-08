#!/bin/bash

# Color codes for easy visualization
GREEN="\033[1;32m"
BLUE="\033[1;34m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
RESET="\033[0m"

# Function to convert decimal to binary
convert_to_binary() {
    decimal=$1
    binary=""  # Initialize an empty string to store binary digits
    
    # Convert decimal to binary
    while [ $decimal -gt 0 ]; do
        remainder=$((decimal % 2))  # Get the remainder when dividing by 2
        binary="${remainder}${binary}"  # Prepend the remainder to the binary string
        decimal=$((decimal / 2))  # Update the decimal by integer division by 2
    done
    
    # Ensure the binary representation is 8 bits long
    while [ ${#binary} -lt 8 ]; do
        binary="0${binary}"  # Prepend '0's to make it 8 bits long
    done
    
    # Print the binary representation in blue color
    echo -e "\n${BLUE}Binary representation: ${RESET}$binary"
    
    # Copy the binary result to clipboard
    echo -n "$binary" | xclip -selection clipboard
    echo -e "\n${GREEN}Binary result copied to clipboard.${RESET}"
}

# Function to convert binary to decimal
convert_from_binary() {
    binary=$1
    decimal=0
    
    # Iterate over each bit of the binary number
    for ((i=${#binary}-1; i>=0; i--)); do
        bit="${binary:$i:1}"  # Get each bit from right to left
        
        # If the bit is 1, add the corresponding power of 2 to the decimal value
        if [ "$bit" == "1" ]; then
            decimal=$((decimal + 2 ** (${#binary} - i - 1)))
        fi
    done
    
    # Print the decimal representation in yellow color
    echo -e "\n${YELLOW}Decimal representation: $decimal${RESET}"
    
    # Copy the decimal result to clipboard
    echo -n "$decimal" | xclip -selection clipboard
    echo -e "\n${GREEN}Decimal result copied to clipboard.${RESET}"
}

# Main loop to provide options to the user
while true; do
    echo -e "\n${BLUE}Choose an option:${RESET}"
    echo -e "1. Convert ${YELLOW}decimal${RESET} to binary"
    echo -e "2. Convert ${BLUE}binary${RESET} to decimal"
    echo -e "q. To ${RED}Quit${RESET}"
    read -p "> " option

    # Perform actions based on user input
    if [ "$option" == "1" ]; then
        echo -e "${RESET}Enter a ${YELLOW}decimal${RESET} number:"
        read decimal_input
        
        # Validate the input as a decimal number
        if ! [[ "$decimal_input" =~ ^[0-9]+$ ]]; then
            echo -e "\n${RED}Invalid input. Please enter a valid decimal number.${RESET}"
        else
            convert_to_binary $decimal_input  # Convert the decimal to binary
            break  # Exit the loop
        fi
    elif [ "$option" == "2" ]; then
        echo -e "${RESET}Enter a ${BLUE}binary${RESET} number:"
        read binary_input
        
        # Validate the input as a binary number
        if ! [[ "$binary_input" =~ ^[01]+$ ]]; then
            echo -e "\n${RED}Invalid input. Please enter a valid binary number.${RESET}"
        else
            convert_from_binary $binary_input  # Convert the binary to decimal
            break  # Exit the loop
        fi
    elif [ "$option" == "q" ]; then
        echo -e "\n${GREEN}Exiting.${RESET}"
        break  # Exit the loop
    else
        echo -e "\n${RED}Invalid option.${RESET}"
    fi
done
