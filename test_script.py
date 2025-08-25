import os
import subprocess
import sys
import pytest

# Path to the script under test
SCRIPT = os.path.join(os.path.dirname(__file__), "edit_file_names.py")  # rename if needed

# ---- Helpers ----
def run_cmd(args, cwd=None):
    """Run the script with given args and return stdout/stderr."""
    result = subprocess.run(
        [sys.executable, SCRIPT] + args,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def create_file(path, content="data"):
    path.write_text(content)
    return str(path)


# ---- CLI Tests ----
def test_trim_mode_dry_run(tmp_path):
    file1 = create_file(tmp_path / "abcdef.txt")
    file2 = create_file(tmp_path / "12345.txt")

    stdout, stderr, code = run_cmd([
        "-s", "2", "-e", "4",
        "-m", "pattern",
        "-i", str(tmp_path / "*.txt"),
        "--dry-run"
    ], cwd=tmp_path)

    assert code == 0
    assert "[DRY-RUN]" in stdout
    assert "abcdef.txt -> aef.txt" in stdout
    assert "12345.txt -> 15.txt" in stdout
    # Files should remain unchanged
    assert os.path.exists(file1)
    assert os.path.exists(file2)


def test_trim_mode_actual(tmp_path):
    file1 = create_file(tmp_path / "abcdef.txt")

    stdout, stderr, code = run_cmd([
        "-s", "2", "-e", "5",
        "-m", "pattern",
        "-i", str(tmp_path / "*.txt"),
    ], cwd=tmp_path)

    assert code == 0
    assert "Renamed: abcdef.txt -> af.txt" in stdout
    assert not os.path.exists(file1)
    assert os.path.exists(tmp_path / "af.txt")


def test_replace_mode_dry_run(tmp_path):
    file1 = create_file(tmp_path / "draft_report.docx")

    stdout, stderr, code = run_cmd([
        "-s", "draft", "-e", "final",
        "-m", "pattern",
        "-i", str(tmp_path / "*.docx"),
        "--dry-run"
    ], cwd=tmp_path)

    assert code == 0
    assert "[DRY-RUN]" in stdout
    assert "draft_report.docx -> final_report.docx" in stdout
    assert os.path.exists(file1)


def test_replace_mode_actual(tmp_path):
    file1 = create_file(tmp_path / "draft_report.docx")

    stdout, stderr, code = run_cmd([
        "-s", "draft", "-e", "final",
        "-m", "pattern",
        "-i", str(tmp_path / "*.docx"),
    ], cwd=tmp_path)

    assert code == 0
    assert "Renamed: draft_report.docx -> final_report.docx" in stdout
    assert not os.path.exists(file1)
    assert os.path.exists(tmp_path / "final_report.docx")


def test_invalid_mode_mix(tmp_path):
    file1 = create_file(tmp_path / "file1.txt")

    stdout, stderr, code = run_cmd([
        "-s", "3", "-e", "final",
        "-m", "pattern",
        "-i", str(tmp_path / "*.txt"),
    ], cwd=tmp_path)

    assert code != 0
    assert "ERROR" in stdout or "ERROR" in stderr


# ---- Unit Tests ----
import edit_file_names  # import functions directly

def test_trim_filename_dry_run(tmp_path):
    f = create_file(tmp_path / "abcdef.txt")
    edit_file_names.trim_filename(f, 2, 4, dry_run=True)
    # File should not be renamed
    print("inside")
    assert os.path.exists(f)


def test_trim_filename_actual(tmp_path):
    f = create_file(tmp_path / "abcdef.txt")
    edit_file_names.trim_filename(f, 2, 5, dry_run=False)
    assert not os.path.exists(f)
    assert os.path.exists(tmp_path / "af.txt")


def test_replace_phrase_filename_dry_run(tmp_path):
    f = create_file(tmp_path / "draft_notes.txt")
    edit_file_names.replace_phrase_filename(f, "draft", "final", dry_run=True)
    assert os.path.exists(f)


def test_replace_phrase_filename_actual(tmp_path):
    f = create_file(tmp_path / "draft_notes.txt")
    edit_file_names.replace_phrase_filename(f, "draft", "final", dry_run=False)
    assert not os.path.exists(f)
    assert os.path.exists(tmp_path / "final_notes.txt")

def test_replace_phrase_not_found(tmp_path):
    f = create_file(tmp_path / "report.txt")
    # Old phrase not present, should skip without renaming
    edit_file_names.replace_phrase_filename(f, "draft", "final", dry_run=False)
    assert os.path.exists(f)
    assert not os.path.exists(tmp_path / "final_notes.txt")

