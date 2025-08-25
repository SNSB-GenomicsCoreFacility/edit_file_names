# File Renamer Tool

A Python utility to **rename files** by either:  
- **Trimming characters** from filenames (using numeric indices).  
- **Replacing phrases** in filenames.  

Supports both **file lists** and **wildcard patterns** with an optional **dry-run** mode for previewing changes.

---

## Features

- ✂️ **Trim characters by index** – Remove characters based on start/end positions.  
- 🔄 **Replace phrases** – Replace one substring with another in filenames.  
- 📂 **Batch processing** – Works on multiple files via wildcard patterns or file lists.  
- 🛠 **Dry-run mode** – Preview changes without modifying files.  

---

## Installation

Clone this repository and ensure you have **Python 3.7+** installed.

```bash
git clone https://github.com/SNSB-GenomicsCoreFacility/edit_file_names.git
cd edit_file_names

```

## Usage

python edit_file_names.py [options]

## Arguments

- **`-s`, `--start`** *(required)*  
  - **Trim mode:** Start index (1-based).  
  - **Replace mode:** Phrase to replace.  

- **`-e`, `--end`** *(required)*  
  - **Trim mode:** End index (exclusive).  
  - **Replace mode:** Replacement phrase.  

- **`-m`, `--mode`** *(required)*  
  - Operation mode:  
    - `file` → input is a file list.  
    - `pattern` → input is file paths or wildcard patterns.  

- **`-i`, `--inputs`** *(required)*  
  - Input sources:  
    - In `file` mode → provide a single text file with one path per line.  
    - In `pattern` mode → provide one or more paths/patterns.  

- **`--dry-run`** *(optional)*  
  - Preview renaming operations without modifying any files.  

## Modes of Operation

### 1. Trim Mode (numeric indices)

Removes a range of characters from filenames using **1-based indexing**.

```bash
python file_renamer.py -s 2 -e 5 -m pattern -i "./files/*.txt"

#Original: myfile123.txt
#Command: -s 2 -e 5
#Result: m123.txt

```

### 2. Replace Mode (phrases)

Replaces one phrase with another in filenames.

```bash
python file_renamer.py -s "draft" -e "final" -m pattern -i "./docs/*.docx"

#Original: report_draft.docx
#Command: -s "draft" -e "final"
#Result: report_final.docx

```

### 3. File List Mode

Provide a text file (file_list.txt) containing paths (one per line):

```bash
/path/to/file1.txt
/path/to/file2.txt
```
Run the script:
```bash
python file_renamer.py -s 1 -e 3 -m file -i file_list.txt
```


