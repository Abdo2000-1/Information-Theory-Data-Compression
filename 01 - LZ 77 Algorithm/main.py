import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def show_file(filename, title):
    file_path = BASE_DIR / filename

    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)

    if not file_path.exists():
        print(f"File not found: {filename}")
    else:
        content = file_path.read_text(encoding="utf-8")

        if content:
            print(content)
        else:
            print("The file is empty.")

    print("=" * 50)
    input("Press Enter to return to the menu...")


def run_script(script_name):
    script_path = BASE_DIR / script_name

    if not script_path.exists():
        print(f"Error: {script_name} was not found.")
        input("Press Enter to continue...")
        return

    try:
        subprocess.run(
            [sys.executable, str(script_path)],
            cwd=BASE_DIR,
            check=True
        )
    except subprocess.CalledProcessError:
        print(f"Error while running {script_name}.")

    input("\nPress Enter to return to the menu...")


def verify_files():
    original_file = BASE_DIR / "file1.txt"
    decompressed_file = BASE_DIR / "decompressed.txt"

    if not original_file.exists() or not decompressed_file.exists():
        print("Please run Compression and Decompression first.")
        return

    original = original_file.read_bytes()
    decompressed = decompressed_file.read_bytes()

    if original == decompressed:
        print("\nSUCCESS: Original and decompressed texts match!")
    else:
        print("\nERROR: The texts do not match!")


def main():
    while True:
        print("\n")
        print("=" * 50)
        print("          LZ77 DATA COMPRESSION SYSTEM")
        print("=" * 50)
        print("1. View Original Text (file1.txt)")
        print("2. Compress Text")
        print("3. View Compressed Tags (file2.txt)")
        print("4. Decompress Text")
        print("5. View Decompressed Text")
        print("6. Verify Decompression")
        print("7. Exit")
        print("=" * 50)

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            show_file("file1.txt", "ORIGINAL TEXT - file1.txt")

        elif choice == "2":
            print("\nStarting Compression...")
            run_script("compressor.py")

        elif choice == "3":
            show_file("file2.txt", "COMPRESSED TAGS - file2.txt")

        elif choice == "4":
            print("\nStarting Decompression...")
            run_script("decompressor.py")

        elif choice == "5":
            show_file(
                "decompressed.txt",
                "DECOMPRESSED TEXT - decompressed.txt"
            )

        elif choice == "6":
            verify_files()
            input("\nPress Enter to return to the menu...")

        elif choice == "7":
            print("\nThank you for using LZ77 Compression System!")
            break

        else:
            print("\nInvalid choice. Please select a number from 1 to 7.")


if __name__ == "__main__":
    main()