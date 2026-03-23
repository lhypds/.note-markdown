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
    folder_path = "../"

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
