import hashlib
import os
import json

FILE_TO_MONITOR = "fileintegritychecker.txt"
BASELINE_FILE = "hashes.json"

def compute_hash(file_path):
    """compute SHA-256 hash of the file."""
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None

def generate_baseline():
    """"generate and save initial hash for the monitored file."""
    file_hash = compute_hash(FILE_TO_MONITOR)
    if file_hash is None:
        print(f"Error: {FILE_TO_MONITOR} not found!")
        return
    

    with open(BASELINE_FILE, "w") as f:
        json.dump({FILE_TO_MONITOR: file_hash}, f, indent=4)

    print(f"Baseline hashes stored in {BASELINE_FILE}")
              
        
def check_integrity():
    """"compare the current file hash with the stored baseline."""
    print("running integrity check...")

    try:
        with open(BASELINE_FILE, "r") as f:
            baseline_hashes = json.load(f)
    except FileNotFoundError:
        print("Baseline file not found. Run the script to generate one.")
        return

    old_hash = baseline_hashes.get(FILE_TO_MONITOR)
    new_hash = compute_hash(FILE_TO_MONITOR)

    print(f"Old Hash: {old_hash}")
    print(f"New Hash: {new_hash}")


    if new_hash is None:
        print(f"[DELETED] {FILE_TO_MONITOR} is missing!")
    elif old_hash is None:
        print(f"[NEW FILE] {FILE_TO_MONITOR} was created!")
    elif new_hash != old_hash:
        print(f"[MODIFIED] {FILE_TO_MONITOR} is changed!")

        baseline_hashes[FILE_TO_MONITOR] = new_hash
        with open(BASELINE_FILE, "w") as f:
            json.dump(baseline_hashes, f, indent=4)
            print("updated baseline with new hash.")

            

    else:
        print(f"No changes detected in {FILE_TO_MONITOR}. File is intact.")
    
    print("\nIntegrity check completed.")


print("choose an option:\n1. Generate Baseline\n2. Check Integrity")
choice = input("Enter 1 or 2: ")

if choice == "1":
    generate_baseline()
elif choice == "2":
    check_integrity()
else:
    print("Invalid choice! please run the script again.")