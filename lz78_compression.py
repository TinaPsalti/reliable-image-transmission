import json

#Συμπίεση LZ78
def compress_lz78(data):
    dictionary = {}
    current = b""
    compressed = []
    next_in = 1

    for byte in data:
        n_current = current + bytes([byte])
        
        if n_current in dictionary:
            current = n_current

        else:
            if current in dictionary:
                index = dictionary[current]
            else:
                index = 0

            compressed.append([index,byte])

            dictionary[n_current] = next_in
            next_in = next_in + 1

            current = b""

    if current != b"":
        if current in dictionary:
            index = dictionary[current]
        else:
            index = 0

        compressed.append([index,None])

    #Αποθήκευση λίστας σε JSON strings για να γίνει εύκολα bytes
    compressed_json = json.dumps(compressed)
    return compressed_json.encode("utf-8")

#Αποσυμπίεση LZ78
def decompress_lz78(compressed_data):
    dictionary = {}
    res = bytearray()
    next_in = 1
    compressed_json = compressed_data.decode("utf-8")
    compressed = json.loads(compressed_json)

    for pair in compressed:
        index = pair[0]
        byte = pair[1]

        if index == 0:
            seq = b""
        else:
            seq = dictionary[index]

        if byte is not None:
            seq = seq+ bytes([byte])

        res.extend(seq)

        dictionary[next_in] = seq
        next_in = next_in +1

    return bytes(res)