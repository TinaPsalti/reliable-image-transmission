#Utilities
import hashlib
import math


def calculate_sha256(data):
    return hashlib.sha256(data).hexdigest()


def calculate_entropy(data):
    if not data:
        return 0

    freq = {}

    for byte in data:
        if byte in freq:
            freq[byte] = freq[byte] + 1
        else:
            freq[byte] = 1

    entropy = 0
    total = len(data)

    for count in freq.values():
        p = count / total
        entropy = entropy - p * math.log2(p)

    return entropy


def bytes_to_bits(data):
    bits = ""

    for byte in data:
        bits = bits + format(byte, "08b")

    return bits


def bits_to_bytes(bits):
    padding = 0

    #Θέλουμε 8άδες, άρα προσθέτουμε ο αν περισσέυουν bits
    while len(bits) % 8 != 0:
        bits = bits + "0"
        padding = padding + 1

    if bits == "":
        return b"", padding

    #Μετατροπή σε bytes
    data = int(bits, 2).to_bytes(len(bits) // 8, byteorder="big")

    return data, padding


def remove_byte_padding(bits, padding):
    if padding > 0:
        bits = bits[:-padding]

    return bits