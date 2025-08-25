import os
import argparse
import sys
import glob


def trim_filename(filepath, start, end, dry_run=False):
    """Trim characters from filename using numeric indices."""
    if not os.path.isfile(filepath):
        print(f"Skipping: {filepath} is not a valid file.")
        return
    file_name = os.path.basename(filepath)
    dir_name = os.path.dirname(filepath)

    try:
        new_file_name = file_name[:start - 1] + file_name[end:]
    except IndexError:
        print(f"Index error trimming file: {file_name}")
        return

    new_path = os.path.join(dir_name, new_file_name)

    if dry_run:
        print(f"[DRY-RUN] Would rename: {file_name} -> {new_file_name}")
    else:
        os.rename(filepath, new_path)
        print(f"Renamed: {file_name} -> {new_file_name}")


def replace_phrase_filename(filepath, old_phrase, new_phrase, dry_run=False):
    """Replace a phrase in the filename with another phrase."""
    if not os.path.isfile(filepath):
        print(f"Skipping: {filepath} is not a valid file.")
        return
    file_name = os.path.basename(filepath)
    dir_name = os.path.dirname(filepath)

    if old_phrase not in file_name:
        print(f"Skipping: '{old_phrase}' not found in {file_name}")
        return

    new_file_name = file_name.replace(old_phrase, new_phrase)
    new_path = os.path.join(dir_name, new_file_name)

    if dry_run:
        print(f"[DRY-RUN] Would rename: {file_name} -> {new_file_name}")
    else:
        os.rename(filepath, new_path)
        print(f"Renamed: {file_name} -> {new_file_name}")


def process_file_list(file_path, start, end, dry_run=False, phrase_mode=False):
    if not os.path.isfile(file_path):
        print(f"ERROR: File list not found: {file_path}")
        sys.exit(1)

    with open(file_path, 'r') as f:
        for line in f:
            filepath = line.strip()
            if phrase_mode:
                replace_phrase_filename(filepath, start, end, dry_run=dry_run)
            else:
                trim_filename(filepath, start, end, dry_run=dry_run)


def process_patterns(patterns, start, end, dry_run=False, phrase_mode=False):
    expanded_files = []
    for pattern in patterns:
        print("inside", pattern)
        matches = glob.glob(pattern, recursive=True)  # ✅ recursive search
        if not matches:
            print(f"Warning: No files matched pattern '{pattern}'")
        expanded_files.extend(matches)

    for file in expanded_files:
        if phrase_mode:
            replace_phrase_filename(file, start, end, dry_run=dry_run)
        else:
            trim_filename(file, start, end, dry_run=dry_run)


def main():
    parser = argparse.ArgumentParser(
        description="Rename files by trimming characters or replacing phrases in filenames."
    )

    parser.add_argument(
        "-s", "--start", required=True,
        help="Start index (1-based) of characters to remove OR phrase to replace."
    )
    parser.add_argument(
        "-e", "--end", required=True,
        help="End index (1-based, exclusive) of characters to remove OR replacement phrase."
    )
    parser.add_argument(
        "-m", "--mode", choices=["file", "pattern"], required=True,
        help="'file' to read list from a file, 'pattern' to pass file paths or wildcard patterns."
    )
    parser.add_argument(
        "-i", "--inputs", nargs="+", required=True,
        help="If mode is 'file', provide a single file list. If 'pattern', provide one or more file paths or patterns."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview changes without renaming files."
    )

    args = parser.parse_args()

    # Detect whether we are in phrase replacement mode
    phrase_mode = False

    # Try to interpret start/end as integers
    try:
        start_val = int(args.start)
        end_val = int(args.end)
        phrase_mode = False
    except ValueError:
        # Must both be strings
        if args.start.isdigit() or args.end.isdigit():
            print("ERROR: Both --start and --end must be integers (trim mode) or both must be strings (replace mode).")
            sys.exit(1)
        start_val = args.start
        end_val = args.end
        phrase_mode = True

    # Validate trim indices
    if not phrase_mode:
        if start_val < 1 or end_val < start_val:
            print("Invalid start/end indices. Ensure start >= 1 and end >= start.")
            sys.exit(1)

    # Run in correct mode
    if args.mode == "file":
        if len(args.inputs) != 1:
            print("ERROR: In 'file' mode, exactly one input file should be provided.")
            sys.exit(1)
        process_file_list(args.inputs[0], start_val, end_val, dry_run=args.dry_run, phrase_mode=phrase_mode)
    elif args.mode == "pattern":
        process_patterns(args.inputs, start_val, end_val, dry_run=args.dry_run, phrase_mode=phrase_mode)


if __name__ == "__main__":
    main()

