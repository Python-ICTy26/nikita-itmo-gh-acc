from caesar import decrypt_caesar, encrypt_caesar


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ord_A, ord_Z = ord("A"), ord("Z")
    ord_a, ord_z = ord("a"), ord("z")
    ciphertext = ""
    is_up = False
    for i in range(len(plaintext)):
        j = i % len(keyword)
        if plaintext[i].isupper():
            is_up = True
        start = ord("a")
        shift = ord(keyword[j].lower()) - start
        ciphertext += encrypt_caesar(plaintext[i], shift)
    # PUT YOUR CODE HERE
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    ord_A, ord_Z = ord("A"), ord("Z")
    ord_a, ord_z = ord("a"), ord("z")
    plaintext = ""
    is_up = False
    for i in range(len(ciphertext)):
        j = i % len(keyword)
        if ciphertext[i].isupper():
            is_up = True
        start = ord("a")
        shift = ord(keyword[j].lower()) - start
        plaintext += decrypt_caesar(ciphertext[i], shift)
    # PUT YOUR CODE HERE
    return plaintext
