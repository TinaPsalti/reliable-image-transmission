#Sender
import requests
import base64
import random
import lz78_compression
import cyclic_code
import utilities


def send_image(image_path, error_percent):
    with open(image_path, "rb") as file:
        img_bytes = file.read()

    img_sha = utilities.calculate_sha256(img_bytes)
    img_entropy = utilities.calculate_entropy(img_bytes)

    #Συμπίεση LZ78
    compressed = lz78_compression.compress_lz78(img_bytes)

    #Μετατροπή σε bits
    compressed_bits = utilities.bytes_to_bits(compressed)

    #Κυκλικός κώδικας
    gen = [1, 0, 1, 1]
    encoded_bits, bit_padding = cyclic_code.encode_bits(compressed_bits, gen)

    #Προσθήκη τυχαίων σφαλμάτων
    encoded_list = list(encoded_bits)
    errors = int(len(encoded_list) * (error_percent / 100))

    error_positions = random.sample(range(len(encoded_list)), errors)

    for pos in error_positions:
        if encoded_list[pos] == "0":
            encoded_list[pos] = "1"
        else:
            encoded_list[pos] = "0"

    corrupted_bits = "".join(encoded_list)

    #Μετατροπή bits σε bytes
    final_bytes, byte_padding = utilities.bits_to_bytes(corrupted_bits)

    encoded_img = base64.b64encode(final_bytes).decode("utf-8")

    data = {
        "encoded_image": encoded_img,
        "compression_algorithm": "lz78",
        "encoding": "cyclic",
        "parameters": gen,
        "errors": errors,
        "SHA256": img_sha,
        "entropy": img_entropy,
        "bit_padding": bit_padding,
        "byte_padding": byte_padding
    }

    try:
        response = requests.post("http://127.0.0.1:5000/process", json=data)
        print("Απάντηση δέκτη:")
        print(response.json())

    except Exception as e:
        print("Αποτυχία Σύνδεσης.")
        print(e)


if __name__ == "__main__":
    x = float(input("Δώσε το ποσοστό σφαλμάτων(%): "))
    send_image("input/papei.png", error_percent=x)