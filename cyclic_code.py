#Cyclic code

#g(x) = x^3 + x + 1 (1011)
polyonimo = [1, 0, 1, 1]

#Διαίρεση mod-2 ανάμεσα στο μήνυμα και στο πολυώνυμο 
def div_mod2(dividend, divisor):
    #Κρατάμε αντίγραφο των bits για να τα αλλάξουμε 
    bits = list(dividend)
    #Μήκος πολυωνύμου
    div_len = len(divisor)

    #περνάμε από κάθε θέση που μπορεί να γίνει διαίρεση
    for i in range(len(dividend) - div_len +1):
        #Αν το τρέχον bit είναι 1 τότε κάνουμε XOR με το divisor
        if bits[i] == 1:
            for j in range(div_len):
                bits[i+j] = bits[i+j] ^ divisor[j]

    #Επιστρέφουμε το υπόλοιπο της διαίρεσης 
    return bits[-(div_len - 1):]

#Κωδικοποίηση με κυκλικό κώδικα 
def encode_bits(inbits, gen = polyonimo):
    padding = 0

    #Πρόσθεση 0 ώστε να χωρίζονται σε 4αδες τα bits
    while len(inbits) % 4 != 0:
        inbits = inbits + "0"
        padding = padding + 1

    encoded_bits = ""
    parity_len = len(gen) - 1

    #Παίρνουμε 4 bits 
    for pos in range(0, len(inbits), 4):
        data_block = [int(bit) for bit in inbits[pos:pos + 4]]
        block_z = data_block + [0] * parity_len
        parbits = div_mod2(block_z, gen)
        encoded_block = data_block + parbits
        encoded_bits = encoded_bits + "".join(map(str, encoded_block))
    return encoded_bits, padding 

#Αποκωδικοποίηση και διόρθωση σφαλμάτων
def decode_bits(encoded_bits, padding, gen = polyonimo):
    decoded_bits = ""
    corrected_er = 0
    block_len = 4 + (len(gen) - 1)

    for pos in range(0, len(encoded_bits), block_len):
        block = [int(bit) for bit in encoded_bits[pos:pos + block_len]]

        if len(block) < block_len:
            break

        syndrome = div_mod2(block, gen)

        #Αν το syndrome δεν είναι 0 τότε υπάρχει λάθος
        if any(syndrome):
            corrected = False

            #Δοκιμάζω κάθε θέση μέχρι να βρω το bit που έχει λάθος
            for bit_pos in range(block_len):
                block[bit_pos] = block[bit_pos] ^ 1

                n_syndrome = div_mod2(block, gen)

                if not any(n_syndrome):
                    corrected = True
                    break
                block[bit_pos] = block[bit_pos]^1

            if corrected:
                corrected_er = corrected_er + 1

        #Κρατάω μόνο τα 4 bits
        decoded_bits = decoded_bits + "".join(map(str, block[:4]))

    if padding > 0 :
        decoded_bits = decoded_bits[:-padding]

    return decoded_bits, corrected_er