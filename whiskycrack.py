import argparse
import itertools
import string

def generate_wordlist(entry_length, words, output_file, include_numbers, include_caps, include_special):
    characters = string.ascii_lowercase
    if include_caps:
        characters += string.ascii_uppercase
    if include_numbers:
        characters += string.digits
    if include_special:
        characters += string.punctuation

    with open(output_file, 'w') as file:
        if words:
            for word in words:
                file.write(word + '\n')
            if len(words) > 1:
                for combination in itertools.permutations(words, len(words)):
                    combined_word = ''.join(combination)
                    file.write(combined_word + '\n')
        else:
            for combination in itertools.product(characters, repeat=entry_length):
                word = ''.join(combination)
                file.write(word + '\n')

def main():
    parser = argparse.ArgumentParser(description='Generate a wordlist.')
    parser.add_argument('-l', type=int, help='Length of each entry')
    parser.add_argument('-w', nargs='+', help='Individual words to add')
    parser.add_argument('-f', type=str, help='Output file')
    parser.add_argument('-n', action='store_true', help='Include numbers')
    parser.add_argument('-c', action='store_true', help='Include capital letters')
    parser.add_argument('-s', action='store_true', help='Include special characters')

    args = parser.parse_args()

    if args.f is None:
        print("Error: Output file not specified. Please use the -f option to specify the output file.")
        return

    entry_length = args.l
    words = args.w if args.w else []
    output_file = args.f
    include_numbers = args.n
    include_caps = args.c
    include_special = args.s

    generate_wordlist(entry_length, words, output_file, include_numbers, include_caps, include_special)

if __name__ == '__main__':
    main()
