import random
import time
import zlib
import pickle
from tqdm import tqdm

# Function to read data from a binary file in the 0-255 range
def read_0_to_255_data(file_name):
    try:
        with open(file_name, 'rb') as file:
            data = file.read()
        return data
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return None

# Function to generate random Huffman trees (bit patterns)
def generate_random_huffman_trees(num_trees, min_bits, max_bits):
    huffman_trees = []
    for _ in range(num_trees):
        tree_length = random.randint(min_bits, max_bits)
        tree = bytes([random.randint(0, 255) for _ in range(tree_length)])
        huffman_trees.append(tree)
    return huffman_trees

# Function to compress data using zlib
def compress_data(data, huffman_trees):
    compressed_data = zlib.compress(data)

    for _ in tqdm(huffman_trees, desc="Compressing"):
        tree = huffman_trees.pop(0)
        while compressed_data:
            if compressed_data.startswith(tree):
                compressed_data = compressed_data[len(tree):]
            else:
                break
    return compressed_data

# Function to extract data using zlib
def extract_data(compressed_data, huffman_trees):
    extracted_data = zlib.decompress(compressed_data)

    for _ in tqdm(huffman_trees, desc="Extracting"):
        tree = huffman_trees.pop(0)
        while extracted_data:
            if extracted_data.startswith(tree):
                extracted_data = extracted_data[len(tree):]
            else:
                break
    return extracted_data

# Function to save Huffman trees to a binary file
def save_huffman_trees_to_binary(file_name, huffman_trees):
    with open(file_name, 'wb') as file:
        pickle.dump(huffman_trees, file)

# Function to load Huffman trees from a binary file
def load_huffman_trees_from_binary(file_name):
    try:
        with open(file_name, 'rb') as file:
            huffman_trees = pickle.load(file)
        return huffman_trees
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return None

# Function to save data to a binary file
def save_to_binary_file(file_name, data):
    with open(file_name, 'wb') as file:
        file.write(data)

# Main program
while True:
    option = input("Options:\n1. Compression and Save Huffman Trees\n2. Extract by Trees\n3. Exit\nSelect an option (1, 2, or 3): ")
    if option == "1":
        input_file_name = input("Enter the name of the input file: ")
        output_file_name = input("Enter the name of the compressed output file: ")

        try:
            with open(input_file_name, 'rb') as file:
                original_data = file.read()
                if original_data:
                    start_time = time.time()

                    # Generate random Huffman trees
                    huffman_trees = generate_random_huffman_trees(99, 8, 106)

                    # Compress data into Huffman trees
                    compressed_data = compress_data(original_data, huffman_trees)

                    # Save the compressed result
                    save_to_binary_file(output_file_name, compressed_data)

                    # Save the Huffman trees to a binary file
                    save_huffman_trees_to_binary("huffmantrees.bin", huffman_trees)

                    end_time = time.time()
                    time_taken = end_time - start_time

                    if read_0_to_255_data(output_file_name) == compressed_data:
                        print("Right compression!!!")
                    else:
                        print("Error during compression")

                    print(f"Data successfully compressed and saved to '{output_file_name}'.")
                    print(f"Huffman trees saved to 'huffmantrees.bin'.")
                    print(f"Time taken: {time_taken} seconds")
        except FileNotFoundError:
            print(f"File '{input_file_name}' not found.")

    elif option == "2":
        input_file_name = input("Enter the name of the compressed input file: ")
        output_file_name = input("Enter the name of the extracted output file: ")

        try:
            with open(input_file_name, 'rb') as file:
                compressed_data = file.read()
                if compressed_data:
                    # Load Huffman trees from a binary file
                    huffman_trees = load_huffman_trees_from_binary("huffmantrees.bin")

                    # Extract data using Huffman trees
                    extracted_data = extract_data(compressed_data, huffman_trees)

                    # Save the extracted binary data
                    save_to_binary_file(output_file_name, extracted_data)

                    print(f"Data successfully extracted and saved to '{output_file_name}'.")
        except FileNotFoundError:
            print(f"File '{input_file_name}' not found.")

    elif option == "3":
        break
    else:
        print("Invalid option. Please select 1 for Compression and Save Huffman Trees, 2 for Extract by Trees, or 3 to Exit.")

print("Program terminated.")