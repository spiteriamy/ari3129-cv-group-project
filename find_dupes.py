import os
import hashlib

def calculate_md5(file_path):
    """Calculate MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def find_duplicates(folder_path):
    """Find and print duplicate images in the given folder."""
    hashes = {}
    duplicates = {}

    print(f"Scanning '{folder_path}' for duplicates...")
    
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return

    # List all files in the directory
    for filename in os.listdir(folder_path):
        # Check if it's an image file
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp', '.heic')):
            continue
            
        file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(file_path):
            try:
                file_hash = calculate_md5(file_path)
                
                if file_hash in hashes:
                    if file_hash not in duplicates:
                        duplicates[file_hash] = [hashes[file_hash]]
                    duplicates[file_hash].append(filename)
                else:
                    hashes[file_hash] = filename
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    if not duplicates:
        print("No duplicates found.")
    else:
        print(f"\nFound {len(duplicates)} sets of duplicates:")
        for file_hash, files in duplicates.items():
            print(f"Duplicate set (Hash: {file_hash}):")
            for file in files:
                print(f" - {file}")
            print("-" * 30)

if __name__ == "__main__":
    # Set the folder to scan (defaulting to 'obscure_in' based on your project structure)
    folder_to_scan = 'obscure_in' 
    find_duplicates(folder_to_scan)
