import argparse
import itertools
import string
import time

def calculate_wordlist_size(entry_length, characters):
    return len(characters) ** entry_length

def estimate_wordlist_size(entry_length, characters):
    bytes_per_character = 1.4
    total_combinations = calculate_wordlist_size(entry_length, characters)
    return total_combinations * entry_length * bytes_per_character

def generate_wordlist(entry_length, words, output_file, include_numbers, include_caps, include_special, incremental_alphabet, append_mode=False, default=False):
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

    if not characters:
        print("Error: Please specify at least one character type or use -d for lowercase letters.")
        return

    mode = 'a' if append_mode else 'w'

    with open(output_file, mode) as file:
        if words:
            for word in words:
                file.write(word + '\n')
            if len(words) > 1:
                for combination in itertools.permutations(words, len(words)):
                    combined_word = ''.join(combination)
                    file.write(combined_word + '\n')
        else:
            wordlist_size = estimate_wordlist_size(entry_length, characters)
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
                file.write(word + '\n')

            elapsed_time = time.time() - start_time
            remaining_time = max(0, estimated_time_seconds - elapsed_time)
            print("Elapsed time:", elapsed_time, "seconds | Estimated remaining time:", remaining_time, "seconds")

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

    args = parser.parse_args()

    if args.f is None:
        print("Error: Output file not specified. Please use the -f option to specify the output file.")
        return

    if args.w is not None and args.l is not None:
        print("Warning: -w option used. Length specified by -l will be ignored.")

    if args.w is not None:
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

    generate_wordlist(entry_length, words, output_file, include_numbers, include_caps, include_special, incremental_alphabet, append_mode,
                      default)

if __name__ == '__main__':
    main()
