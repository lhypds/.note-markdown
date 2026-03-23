import os
import unicodedata
import json
import argparse


def display_width(s):
    """Return display width of a string, counting CJK/wide characters as 2."""
    width = 0
    for ch in s:
        eaw = unicodedata.east_asian_width(ch)
        width += 2 if eaw in ("W", "F") else 1
    return width


def scan_mismatches(scan_dir):
    mismatches = []

    for filename in sorted(os.listdir(scan_dir)):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(scan_dir, filename)

        with open(filepath, "r", encoding="UTF8") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            stripped = line.rstrip("\n")

            is_underline = stripped != "" and (
                stripped.replace("-", "") == "" or stripped.replace("=", "") == ""
            )

            if not is_underline:
                continue

            underline_char = "-" if stripped.replace("-", "") == "" else "="

            if i == 0:
                mismatches.append(
                    {
                        "file": filename,
                        "line": i + 1,
                        "title": "(none)",
                        "under": stripped,
                        "title_len": 0,
                        "underline_char": underline_char,
                        "underline_len": display_width(stripped),
                        "issue": "underline on first line, no title above",
                    }
                )
                continue

            title = lines[i - 1].rstrip("\n")

            # Skip if title is empty
            if not title.strip():
                continue

            title_len = display_width(title)
            underline_len = display_width(stripped)

            if title_len != underline_len:
                mismatches.append(
                    {
                        "file": filename,
                        "line": i + 1,
                        "title": title,
                        "under": stripped,
                        "title_len": title_len,
                        "underline_char": underline_char,
                        "underline_len": underline_len,
                        "issue": f"length mismatch: title={title_len}, underline={underline_len}",
                    }
                )

    return mismatches


def write_report(mismatches, report_file):
    with open(report_file, "w", encoding="UTF8") as f:
        json.dump(mismatches, f, ensure_ascii=False, indent=2)
    print(f"Found {len(mismatches)} mismatch(es). Report written to: {report_file}")


def apply_fixes(fix_list_file, scan_dir):
    with open(fix_list_file, "r", encoding="UTF8") as f:
        mismatches = json.load(f)

    # Group fixes by file
    fixes_by_file = {}
    for m in mismatches:
        if m["title_len"] == 0:
            print(f"  Skipping {m['file']} line {m['line']}: {m['issue']}")
            continue
        fname = m["file"]
        if fname not in fixes_by_file:
            fixes_by_file[fname] = []
        fixes_by_file[fname].append(m)

    total_fixed = 0
    for filename, fixes in fixes_by_file.items():
        filepath = os.path.join(scan_dir, filename)
        with open(filepath, "r", encoding="UTF8") as f:
            lines = f.readlines()

        for fix in fixes:
            line_idx = fix["line"] - 1  # convert to 0-based index
            char = fix["underline_char"]
            new_underline = char * fix["title_len"]

            # Preserve original line ending
            original = lines[line_idx]
            if original.endswith("\r\n"):
                ending = "\r\n"
            elif original.endswith("\n"):
                ending = "\n"
            else:
                ending = ""

            lines[line_idx] = new_underline + ending
            total_fixed += 1
            print(
                f"  Fixed: {filename} line {fix['line']}: {original.rstrip()!r} -> {new_underline!r}"
            )

        with open(filepath, "w", encoding="UTF8") as f:
            f.writelines(lines)

    print(f"\nTotal fixed: {total_fixed}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(
        description="Check and fix underline length mismatches in note files."
    )
    default_fix_file = os.path.join(script_dir, "scan_result.json")
    parser.add_argument(
        "scan_dir",
        nargs="?",
        help="Target directory to scan.",
    )

    parser.add_argument(
        "--fix",
        nargs="?",
        const=default_fix_file,
        metavar="FIX_LIST_FILE",
        help="Apply fixes from a JSON fix list file (default: scan_result.json).",
    )
    args = parser.parse_args()

    scan_dir_input = args.scan_dir
    if not scan_dir_input:
        scan_dir_input = input("Enter scan directory path: ").strip()

    if not scan_dir_input:
        print("Error: no scan directory provided.")
        raise SystemExit(1)

    scan_dir = os.path.abspath(scan_dir_input)

    if not os.path.isdir(scan_dir):
        print(f"Error: '{scan_dir}' is not a valid directory.")
        raise SystemExit(1)

    if args.fix is not None:
        apply_fixes(args.fix, scan_dir)
    else:
        mismatches = scan_mismatches(scan_dir)
        write_report(mismatches, default_fix_file)


if __name__ == "__main__":
    main()
