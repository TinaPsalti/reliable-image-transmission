#Receiver
from flask import Flask, request, jsonify
import base64
import io
from PIL import Image
import lz78_compression
import cyclic_code
import utilities

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process():
    data = request.json

    encoded_img = data["encoded_image"]
    errors_sent = data["errors"]
    client_sha = data["SHA256"]
    client_entropy = data["entropy"]
    gen = data["parameters"]
    bit_padding = data["bit_padding"]
    byte_padding = data["byte_padding"]

    received_bytes = base64.b64decode(encoded_img)
    received_bits = utilities.bytes_to_bits(received_bytes)
    received_bits = utilities.remove_byte_padding(received_bits, byte_padding)

    #Αποκωδικοποίηση με κυκλικό κώδικα
    decoded_bits, corrected_errors = cyclic_code.decode_bits(
        received_bits,
        bit_padding,
        gen
    )

    #Μετατροπή bits σε compressed bytes
    compressed_bytes, _ = utilities.bits_to_bytes(decoded_bits)

    #Αποσυμπίεση LZ78
    try:
        img_bytes = lz78_compression.decompress_lz78(compressed_bytes)

        with open("output/received_image.png", "wb") as file:
            file.write(img_bytes)

    except Exception:
        return jsonify({
            "status": "error",
            "message": "Αποτυχής αποσυμπίεση."
        })

    #Έλεγχοι
    server_sha = utilities.calculate_sha256(img_bytes)
    sha_ok = client_sha == server_sha

    server_entropy = utilities.calculate_entropy(img_bytes)

    img_ok = False
    try:
        img = Image.open(io.BytesIO(img_bytes))
        img.verify()
        img_ok = True
    except:
        img_ok = False

    error_difference = abs(errors_sent - corrected_errors)

    print("\Λήφθηκε νέο μήνυμα")
    print("Σφάλματα που στάλθηκαν:", errors_sent)
    print("Σφάλματα που διορθώθηκαν", corrected_errors)
    print("Διαφορά σφαλμάτων:", error_difference)
    print("Έγκυρη εικόνα:", img_ok)
    print("Ίδιο SHA256:", sha_ok)
    print("Client entropy:", client_entropy)
    print("Server entropy:", server_entropy)

    return jsonify({
        "status": "success",
        "corrected_errors": corrected_errors,
        "error_difference": error_difference,
        "image_verified": img_ok,
        "sha256_match": sha_ok,
        "server_sha256": server_sha,
        "client_entropy": client_entropy,
        "server_entropy": server_entropy
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)