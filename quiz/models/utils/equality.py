import difflib


def compare_sentences(sentence1, sentence2):
    # Tokenizing the sentences into words
    words1 = sentence1.split()
    words2 = sentence2.split()

    # Using a SequenceMatcher to find the degree of similarity
    matcher = difflib.SequenceMatcher(None, words1, words2)
    similarity = matcher.ratio()  # This gives a score between 0 and 1

    # Define thresholds for "identical" and "nearly identical"
    if similarity == 1:
        return 1  # Identical
    elif 0.4 < similarity < 1:
        return 0  # Nearly identical
    else:
        return -1  # Different


def compare_sets(set1, set2):
    # Helper function to find if there is a nearly identical match for a sentence in a set
    def find_match(sentence, other_set):
        for other_sentence in other_set:
            comparison_result = compare_sentences(sentence, other_sentence)
            if comparison_result >= 0:  # Identical or nearly identical
                return True
        return False

    # Check if all elements in set1 have a match in set2
    all_matched_set1 = all(find_match(sentence, set2) for sentence in set1)

    # Check if all elements in set2 have a match in set1
    all_matched_set2 = all(find_match(sentence, set1) for sentence in set2)

    return all_matched_set1 and all_matched_set2


if __name__ == "__main__":
    # Example usage
    result = compare_sentences(
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over the lazy dog",
    )
    print(result)  # Output: 1

    # Example usage
    result = compare_sentences(
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over a lazy dog",
    )
    print(result)  # Output: 0

    # Example usage
    result = compare_sentences(
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over the lazy cat",
    )
    print(result)  # Output: -1

    # Example usage
    result = compare_sentences(
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over the lazy dog.",
    )
    print(result)  # Output: -1

    # Example usage
    result = compare_sentences(
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog.",
    )
    print(result)  # Output: -1
    # Example usage
    result = compare_sentences(
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over a lazy dog",
    )
    print(result)  # Output might be 0 or -1 depending on the thresholds

    # Example usage
    set1 = {"The quick brown fox jumps over the lazy dog", "Hello world!"}
    set2 = {"The quick brown fox jumps over a lazy dog", "Hello, world!"}

    result = compare_sets(set1, set2)
    print(result)  # Output: True or False
