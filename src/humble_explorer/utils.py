"""This module contains utility functions for HumBLE Explorer."""
from random import shuffle

__author__ = "Koen Vervloesem"
__copyright__ = "Koen Vervloesem"
__license__ = "MIT"

permutation_table = list(range(256))
shuffle(permutation_table)


def hash8(message: str) -> int:
    """Compute an 8-bit hash from the message with Pearson hashing."""
    # Source: https://en.wikipedia.org/wiki/Pearson_hashing
    hash_value = len(message) % 256
    for i in message:
        hash_value = permutation_table[hash_value ^ ord(i)]
    return hash_value
