import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    ord_A, ord_Z = ord("A"), ord("Z")
    ord_a, ord_z = ord("a"), ord("z")
    for c in plaintext:
        if ord_a <= ord(c) <= ord_z:
            ciphertext += chr(ord_a + (ord(c) - ord_a + shift) % 26)
        elif ord_A <= ord(c) <= ord_Z:
            ciphertext += chr(ord_A + (ord(c) - ord_A + shift) % 26)
        else:
            ciphertext += c
    # PUT YOUR CODE HERE
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    ord_A, ord_Z = ord("A"), ord("Z")
    ord_a, ord_z = ord("a"), ord("z")
    plaintext = ""
    for c in ciphertext:
        if ord_a <= ord(c) <= ord_z:
            plaintext += chr(ord_a + (ord(c) - ord_a - shift) % 26)
        elif ord_A <= ord(c) <= ord_Z:
            plaintext += chr(ord_A + (ord(c) - ord_A - shift) % 26)
        else:
            plaintext += c
    # PUT YOUR CODE HERE
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
