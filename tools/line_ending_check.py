import argparse
import os


def contains_only_lf(file_path):
    """Check if a given file contains LF line endings without any CRLF."""
    with open(file_path, "rb") as f:
        content = f.read()
    return b"\n" in content and b"\r\n" not in content


def contains_crlf(file_path):
    """Check if a given file contains CRLF line endings."""
    with open(file_path, "rb") as f:
        content = f.read()
    return b"\r\n" in content


def main():
    parser = argparse.ArgumentParser(
        description="Check .txt files in a target folder for LF and CRLF line endings."
    )
    parser.add_argument(
        "folder_path",
        nargs="?",
        help="Target folder path to scan.",
    )
    args = parser.parse_args()

    folder_input = args.folder_path
    if not folder_input:
        folder_input = input("Enter target folder path: ").strip()

    if not folder_input:
        print("Error: no folder path provided.")
        raise SystemExit(1)

    folder_path = os.path.abspath(folder_input)

    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        raise SystemExit(1)

    lf_count = 0
    crlf_count = 0
    total_txt_count = 0

    # Walk through folder and sub-folders
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith(".txt"):
                total_txt_count += 1
                file_path = os.path.join(dirpath, filename)
                if contains_only_lf(file_path):
                    print(f"LF only: {file_path}")
                    lf_count += 1
                elif contains_crlf(file_path):
                    print(f"CRLF: {file_path}")
                    crlf_count += 1

    print(f"\nTotal .txt files with only LF line endings: {lf_count}")
    print(f"Total .txt files with CRLF line endings: {crlf_count}")
    print(f"Total .txt files: {total_txt_count}")


if __name__ == "__main__":
    main()
