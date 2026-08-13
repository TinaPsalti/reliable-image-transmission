# Reliable Image Transmission

This application is a Python client-server system that demonstrates reliable image transmission over a simulated noisy channel. Data compression, error-correcting codes, and cryptographic integrity verification were used in the development of this project.

This project combines LZ78 compression, cyclic error detection and correction as well as SHA-256 verification to reconstruct transmitted images even when errors are introduced during transmission.

Developed as an individual second-year project for the University of Piraeus.

## Features
- Custom implementation of LZ78 compression and decompression
- Cyclic encoding for transmission error detection and correction 
- Configurable simulation of random transmission errors
- Client-server communication using HTTP and Flask
- Base64 encoding for transferring binary data through JSON
- SHA-256 hashing for end-to-end integrity verification 
- Entropy calculation and comparison before and after transmission
- Automatic image reconstruction 
- Reporting of detected and corrected transmission errors

## Architecture

The transmission process follows this pipeline:

```
Original Image
    |
    V
SHA-256 Hash + Entropy Calculation 
    |
    V
LZ78 Compression
    |
    V
Cyclic Encoding
    |
    V
Simulated Transmission Errors
    |
    V
Base64 Encoding
    |
    V
HTTP POST / Flask REST API
    |
    V
Cyclic Error Detection & Correction
    |
    V
LZ78 Decompression 
    |
    V
Image Reconstruction
    |
    V
SHA-256 + Entropy Verification
```

The system is divided into sender and receiver.

### Sender

sender.py

The sender:

- Reads the source image
- Calculates its SHA-256 hash
- Calculates the entropy of the original data
- Compresses the image using LZ78
- Encodes the compressed data using the cyclic coding algorithm 
- Introduces a configurable percentage of simulated transmission errors
- Encodes the resulting data using Base64
- Sends the payload to the receiver through an HTTP request

### Receiver

receiver.py

The receiver runs a Flask server that:

- Receives the encoded data 
- Detects and corrects transmission errors
- Reconstructs the compressed data
- Performs LZ78 decompression
- Recreates the original image
- Calculates the SHA-256 hash and entropy of the reconstructed data
- Compares the reconstructed file against the original integrity information
- Reports whether the image was successfully recovered

## Project Structure

```text
reliable-image-transmission/
|
|-- sender.py
|-- receiver.py
|-- lz78_compression.py
|-- cyclic_code.py
|-- utilities.py
|-- requirements.txt
|-- README.md
|-- .gitignore
|
|-- input/
|   `-- papei.png
|
|-- output/
|   `-- .gitkeep
|
`-- docs/
    `-- university-report.pdf
```

### Main Files

sender.py
Handles the image preprocessing, the compression and the encoding, as well as the simulated errors and the transmission.

receiver.py
Provides the Flask endpoint and performs the error correction, decompression and the reconstruction of the image.

lz78_compression.py
Contains the custom LZ78 compression and decompression implementation.

cyclic_code.py
Implements cyclic encoding as well as error detection and correction.

utilities.py
Contains supporting functions such as SHA-256 hashing and entropy calculation.

## Technologies

- Python
- Flask
- Requests
- Pillow
- REST APIs
- JSON
- Base64
- SHA-256
- LZ78 compression
- Cyclic error-correcting codes
- Information entropy

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/TinaPsalti/reliable-image-transmission.git 
cd reliable-image-transmission
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass 
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```
python -m pip install -r requirements.txt
```
## Running the Project

The receiver must be running before starting the sender.

### Terminal 1 - Start the receiver

```bash
python receiver.py
```

The Flask server will run locally

### Terminal 2 - Start the sender

```bash
python sender.py
```

The program asks for the percentage of transmission errors to simulate:

Δώσε το ποσοστό σφαλμάτων(%):

For example:

0.01

The sender then processes the image and sends it to the receiver.

## Example Result

A transmission test was performed with a simulated error rate of 0.01%.

The receiver reported:

```text
Corrected errors: 543
Error difference: 0

Image verified: True
SHA-256 match: True

Client entropy: 7.974252999859821
Server entropy: 7.974252999859821

Status: success
```

Despite 543 transmission errors being corrected, the reconstructed image produced the same SHA-256 hash and entropy value as the original image.

This confirms that the complete pipeline successfully: 

1. compressed the original data,
2. transmitted encoded data through a simulated noisy channel,
3. corrected transmission errors,
4. decompressed the resulting data,
5. reconstructed the original image, and 
6. verified its integrity.

## Error-Correction Limitations

The simulated channel introduces errors randomly across the encoded bitstream.

At high enough error rates, multiple errors may occur within the same protected codeword. The current coding scheme cannot guarantee recovery when its correction capability is exceeded.

For example: 

0.01% simulated errors -> successful recovery
0.05% simulated errors -> decompression may fail

This behaviour demonstrates the relationship between channel error rate and the correction capability of an error-control coding scheme.

Future versions could investigate stronger codes or modify the simulation to control the number of errors introduced per codeword.

## Integrity Verification

SHA-256 is calculated before transmission and again after reconstruction.

A successful transmission requires:

Original SHA-256 == Reconstructed SHA-256

The project also compares information entropy between the original image data and the reconstructed image data as an additional verification metric.

## What I learned

Through this project I gained practical experience with:

- implementing a compression algorithm rather than relying on an external compression library;
- applying error-control coding to binary data;
- working with binary representations and bit-level operations;
- designing sender-receiver communication;
- building a REST endpoint with Flask;
- transmitting structured data using JSON and Base64;
- using cryptographic hashes for integrity checking; 
- analysing the behaviour of a communication system under transmission errors;
- integrating several independent algorithms into a complete working system.

## Academic Context

This project was developed as an individual university assignment at the University of Piraeus in the area of Information Theory and Coding.

The original academic report is available:
docs/university-report.pdf

## Author 

Stamatia Erato Psalti 

BSc Informatics
University of Piraeus

GitHub: [TinaPsalti](https://github.com/TinaPsalti)