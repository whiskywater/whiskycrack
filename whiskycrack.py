import argparse
import itertools
import string
import time

def calculate_wordlist_size(entry_length, characters):
    return len(characters) ** entry_length

def estimate_wordlist_size(entry_length, characters, smart=False, smartplus=False):
    bytes_per_character = 1.4
    total_characters = len(characters)

    if smart or smartplus:
        if smartplus:
            total_combinations = ((total_characters ** entry_length) / 1.35)
        else:
            total_combinations = ((total_characters ** entry_length) / 1.3)
    else:
        total_combinations = total_characters ** entry_length

    return total_combinations * entry_length * bytes_per_character

def is_valid_ssn(ssn):
    if ssn[0] * 3 == ssn or ssn in ['123456789', '987654320', '000000000', '111111111', '222222222', '333333333',
                                    '444444444', '555555555', '666666666', '777777777', '888888888', '999999999']:
        return False
    return True

def is_smart(entry):
    for char in entry:
        if entry.count(char) >= 4:
            return False

    for i in range(len(entry) - 3):
        sequence = entry[i:i+4]
        if sequence[0] == sequence[1] and sequence[2] == sequence[3]:
            return False

    return True

def is_smartplus(entry):
    for char in entry:
        if entry.count(char) >= 4:
            return False

    for i in range(len(entry) - 3):
        sequence = entry[i:i+4]
        if sequence[0] == sequence[1] and sequence[2] == sequence[3]:
            return False

    awkward_combinations = ['fx', 'xf', 'zk', 'kz']
    for combo in awkward_combinations:
        if combo in entry:
            return False

    return True

def generate_wordlist(entry_length, words, output_file, include_numbers, include_caps, include_special, incremental_alphabet, append_mode=False, default=False, date_range=None, social=False, smart=False, smartplus=False):
    characters = ''

    if default:
        characters = string.ascii_lowercase

    if include_caps:
        characters += string.ascii_uppercase
    if include_numbers:
        characters += string.digits
    if include_special:
        characters += string.punctuation

    if incremental_alphabet:
        characters += ''.join(sorted(set(incremental_alphabet)))

    mode = 'a' if append_mode else 'w'

    with open(output_file, mode) as file:
        if words:
            for word in words:
                file.write(word + '\n')
            if len(words) > 1:
                for combination in itertools.permutations(words, len(words)):
                    combined_word = ''.join(combination)
                    if (smart and is_smart(combined_word)) or (smartplus and is_smartplus(combined_word)):
                        file.write(combined_word + '\n')
        else:
            if date_range:
                start_year = int(date_range)
                end_year = start_year + 99 if start_year < 100 else start_year + 999
                for year in range(start_year, end_year + 1):
                    for month in range(1, 13):
                        for day in range(1, 32):
                            file.write(f"{month:02}/{day:02}/{year}\n")
            elif social:
                excluded_ssns = ['000000000', '111111111', '222222222', '333333333', '444444444', '555555555',
                                 '666666666', '777777777', '888888888', '999999999']
                for combination in itertools.product(string.digits, repeat=9):
                    ssn = ''.join(combination)
                    if ssn[:3] != ssn[3:6] and ssn[3:5] != ssn[5:8] and ssn[0] * 9 != ssn:
                        formatted_ssn = f"{ssn[:3]}-{ssn[3:5]}-{ssn[5:]}"
                        file.write(formatted_ssn + '\n')
            elif characters:
                wordlist_size = estimate_wordlist_size(entry_length, characters, smart, smartplus)
                print("Estimated wordlist size (sizes may vary):", wordlist_size, "bytes")

                bytes_per_second = 1000000  # Adjust this value based on your system's processing speed
                estimated_time_seconds = wordlist_size / bytes_per_second
                print("Estimated time to generate wordlist:", estimated_time_seconds, "seconds")

                if wordlist_size > 1000000:
                    print("Warning: The estimated wordlist size is", wordlist_size, "bytes. Are you sure you want to continue?")
                    confirmation = input("Enter 'y' to continue and 'n' to cancel: ")
                    if confirmation.lower() != 'y':
                        print("Wordlist generation aborted.")
                        return

                start_time = time.time()
                for combination in itertools.product(characters, repeat=entry_length):
                    word = ''.join(combination)
                    if (smart and not is_smart(word)) or (smartplus and not is_smartplus(word)):
                        continue
                    file.write(word + '\n')

                elapsed_time = time.time() - start_time
                remaining_time = max(0, estimated_time_seconds - elapsed_time)
                print("Elapsed time:", elapsed_time, "seconds | Estimated remaining time:", remaining_time, "seconds")
            else:
                print("Error: Please specify at least one character type or use -d for lowercase letters.")
                return

def main():
    parser = argparse.ArgumentParser(description='Generate a wordlist.')
    parser.add_argument('-l', type=int, help='Length of each entry')
    parser.add_argument('-w', nargs='+', help='Individual words to add')
    parser.add_argument('-f', type=str, help='Output file')
    parser.add_argument('-n', action='store_true', help='Include numbers')
    parser.add_argument('-c', action='store_true', help='Include capital letters')
    parser.add_argument('-s', action='store_true', help='Include special characters')
    parser.add_argument('-r', type=str, help='Incremental alphabet characters')
    parser.add_argument('-a', action='store_true', help='Append to existing wordlist')
    parser.add_argument('-d', action='store_true', help='Use default (lowercase letters)')
    parser.add_argument('--date', type=str, help='Generate dates in the format MONTH/DAY/YEAR')
    parser.add_argument('--social', action='store_true', help='Generate SSN format "000-00-0000"')
    parser.add_argument('--smart', action='store_true', help='Exclude entries with repeating characters 4 or more times')
    parser.add_argument('--smartplus', action='store_true', help='Exclude entries with repeating characters 4 or more times and awkward letter combinations')

    args = parser.parse_args()

    if args.f is None:
        print("Error: Output file not specified. Please use the -f option to specify the output file.")
        return

    if args.date and not args.l and not args.social:
        entry_length = 10  # Set default entry length for dates
    elif args.social and not args.l and not args.date:
        entry_length = 9  # Set default entry length for SSN
    elif args.w is not None:
        entry_length = len(args.w[0])
    else:
        if args.l is None:
            print("Error: No length specified. Please use the -l option to specify the length.")
            return
        entry_length = args.l

    words = args.w if args.w else []
    output_file = args.f
    include_numbers = args.n
    include_caps = args.c
    include_special = args.s
    incremental_alphabet = args.r
    append_mode = args.a
    default = args.d
    date_range = args.date
    social = args.social
    smart = args.smart
    smartplus = args.smartplus

    generate_wordlist(entry_length, words, output_file, include_numbers, include_caps, include_special, incremental_alphabet, append_mode, default, date_range, social, smart, smartplus)

if __name__ == '__main__':
    main()
