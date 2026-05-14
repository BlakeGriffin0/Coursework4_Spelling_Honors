
#PROG 1003H – Spring 2026
#HW-6H – Spelling+
#Solution by Blake Griffin 


import os
import string



# defining functions to later be called in the program


def load_wordlist(filename):
    """Load wordlist into a set for fast lookup"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            words = {line.strip().lower() for line in file if line.strip()}
        
        if not words:
            raise ValueError("Wordlist loaded but is empty.")
        
        return words

    except Exception as e:
        print(f"FATAL ERROR: Could not load wordlist '{filename}' -> {e}")
        return set()


def get_text_files():
    """Return list of valid .txt files (exclude output files)"""
    return [
        f for f in os.listdir()
        if f.endswith(".txt") and not f.startswith(("Enable wordlist")) and not f.startswith(("misspelled", "palindromes"))
    ]


def display_menu(files):
    """Display file selection menu"""
    print("Pick a file from this list by its index number.")
    for i, file in enumerate(files, start=1):
        print(f"{i} - {file}")


def get_user_choice(files):
    """Get validated user menu selection"""
    while True:
        try:
            choice = int(input("Pick a file by its index number: "))
            if 1 <= choice <= len(files):
                return files[choice - 1]
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid integer.")


def clean_word(word):
    """Remove leading/trailing punctuation and lowercase"""
 
    return word.strip(string.punctuation).lower()


def is_palindrome(word):
    """Check if word is a palindrome (ignore single letters)"""
    return len(word) > 1 and word == word[::-1]



# Levenshtein Distance Honors Poriton


def levenshtein_distance(s1, s2):
    """Compute Levenshtein distance between two words"""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    previous_row = list(range(len(s2) + 1))

    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def find_closest_word(word, wordlist):
    """Find closest match using Levenshtein distance"""
    min_distance = float('inf')
    closest_word = ""

    for candidate in wordlist:
        dist = levenshtein_distance(word, candidate)

        if dist < min_distance:
            min_distance = dist
            closest_word = candidate

        if min_distance == 0:
            break

    return closest_word


# process the selected file, returning word count, palindromes, and misspelled words with suggestions


def process_file(filename, wordlist):
    palindromes = set()
    misspelled = {}
    word_count = 0

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                words = line.split()

                for word in words:
                   
                    cleaned = clean_word(word)

                    if not cleaned:
                        continue

                    
                    if not cleaned.isalpha():
                        continue

                    word_count += 1

                    # Palindrome check
                    if is_palindrome(cleaned):
                        palindromes.add(cleaned)

                    # Misspelling check
                    if cleaned not in wordlist:
                        if cleaned not in misspelled:
                            suggestion = find_closest_word(cleaned, wordlist)
                            misspelled[cleaned] = suggestion

        return word_count, palindromes, misspelled

    except Exception as e:
        print(f"Error processing file '{filename}': {e}")
        return 0, set(), {}



# Save Output Files


def save_results(filename, palindromes, misspelled):
    base = os.path.splitext(filename)[0]

    misspelled_file = f"misspelled words in {base}.txt"
    palindrome_file = f"palindromes in {base}.txt"

    # Save misspelled words
    with open(misspelled_file, 'w', encoding='utf-8') as f:
        for word, suggestion in sorted(misspelled.items()):
            f.write(f"{word} did you mean {suggestion}\n")

    # Save palindromes
    with open(palindrome_file, 'w', encoding='utf-8') as f:
        for word in sorted(palindromes):
            f.write(word + "\n")



# Main Program


def main():
    print("HW-6H – Spelling+")
    print("Solution by Blake Griffin\n")

    #  "Enable wordlist.txt" variable
    wordlist_file = "Enable wordlist.txt"
    wordlist = load_wordlist(wordlist_file)

    if not wordlist:
        print("Program cannot continue without a valid wordlist.")
        return

    print(f"There are {len(wordlist)} words in {wordlist_file}")

    while True:
        files = get_text_files()

        if not files:
            print("No valid text files found.")
            break

        display_menu(files)
        selected_file = get_user_choice(files)

        word_count, palindromes, misspelled = process_file(selected_file, wordlist)

        print(f"\nResults for '{selected_file}':")
        print(f"Word Count = {word_count}")
        print(f"Palindromes count = {len(palindromes)}")
        print(f"Misspelled Words count = {len(misspelled)}")

        save_results(selected_file, palindromes, misspelled)

        while True:
            again = input("\nAnalyze another file? (Y/N): ").strip().lower()
            if again in ['y', 'n']:
                break
            print("Invalid input. Enter Y or N.")

        if again == 'n':
            break

    print("\nHW-6H Complete")



# Run Main Program


if __name__ == "__main__":
    main()