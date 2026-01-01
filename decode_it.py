import os
import glob

def decrypt_byte(byte):
    return (byte - 0x6F) & 0xFF

def main():
    # Find all .it files in the directory
    files = glob.glob("*.it")
    
    if not files:
        print("No .it files found.")
        return

    print(f"Found {len(files)} .it files to process.")

    for input_filename in files:
        try:
            with open(input_filename, 'rb') as f_in:
                # Read header to check if it needs decryption
                header = f_in.read(4)
                f_in.seek(0)
                data = bytearray(f_in.read())

            # Check for standard IMPM header
            if header == b'IMPM':
                print(f"Skipping {input_filename}: Already a valid IT file.")
                continue
            
            # Check if it decrypts to IMPM
            decrypted_header = bytearray(decrypt_byte(b) for b in header)
            if decrypted_header == b'IMPM':
                # Determine output filename
                if input_filename.startswith("_"):
                    output_filename = input_filename[1:]
                else:
                    output_filename = "decrypted_" + input_filename
                
                print(f"Processing encrypted file {input_filename} -> {output_filename}...")
                
                # Decrypt full data
                decrypted_data = bytearray(decrypt_byte(b) for b in data)
                
                with open(output_filename, 'wb') as f_out:
                    f_out.write(decrypted_data)
                    
                print(f"Successfully decrypted {output_filename}")
            else:
                print(f"Skipping {input_filename}: Unknown format or different encryption.")
            
        except Exception as e:
            print(f"Error processing {input_filename}: {e}")

if __name__ == "__main__":
    main()
