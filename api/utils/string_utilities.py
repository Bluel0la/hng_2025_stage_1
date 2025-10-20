import hashlib


def word_count(sentence: str) -> int:
    """
    Returns the number of words in the given sentence.
    Words are separated by whitespace.
    """
    return len(sentence.split())


def sentence_length(sentence: str) -> int:
    """
    Returns the number of letters in a given sentence.
    """
    return len(sentence)


def is_palindrome(sentence: str) -> bool:
    """
    Returns either true or false after checking wether a
    sentence is a palindrome.
    """

    cleaned_sentence = "".join(char.lower() for char in sentence if char.isalnum())
    return cleaned_sentence == cleaned_sentence[::-1]


def sha256_hasher(sentence: str) -> str:
    """
    Returns the SHA-256 hash of the given sentence.
    """
    sha256_hash = hashlib.sha256()
    sha256_hash.update(sentence.encode("utf-8"))
    return sha256_hash.hexdigest()


def unique_characters(sentence: str) -> tuple[int, list[str]]:
    """
    Returns all the unique characters in a sentence along
    with the total number.
    """

    unique_chars = set(sentence)
    return len(unique_chars), list(sorted(unique_chars))


def character_frequency_mapper(sentence: str) -> dict:
    """
    Returns a dictionary mapping each character in the sentence to its frequency,
    sorted alphabetically by character.
    """
    freq = {}
    for char in sentence:
        freq[char] = freq.get(char, 0) + 1
    return dict(sorted(freq.items()))
