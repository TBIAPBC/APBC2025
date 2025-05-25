# This script was generated with the help of AI tool ChatGPT

import sys
import re

def clean_text(text, ignore_case):
    if ignore_case:
        text = text.lower()
    # Replace punctuation and special characters with spaces
    text = re.sub(r"[^a-zA-Z0-9]", ' ', text)
    return text

def count_words(text):
    word_counts = {}
    words = text.split()
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    return word_counts

def print_word_list(word_counts):
    # Sort first by frequency descending, then alphabetically
    sorted_words = sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))
    for word, freq in sorted_words:
        print(f"{word}\t{freq}")

def main():
    args = sys.argv[1:]
    ignore_case = False
    list_words = False

    # Extract options and filename
    filename = None
    for arg in args:
        if arg == '-I':
            ignore_case = True
        elif arg == '-l':
            list_words = True
        else:
            filename = arg

    if not filename:
        print("Usage: WordCount.py [-I] [-l] <filename>")
        sys.exit(1)

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
    except IOError:
        print(f"Error: Cannot open file {filename}")
        sys.exit(1)

    cleaned_text = clean_text(text, ignore_case)
    word_counts = count_words(cleaned_text)

    total_words = sum(word_counts.values())
    different_words = len(word_counts)

    print(f"{different_words} / {total_words}")

    if list_words:
        print_word_list(word_counts)

if __name__ == '__main__':
    main()

