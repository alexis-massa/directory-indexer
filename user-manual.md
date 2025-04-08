# Directory Indexer - User Manual

- [Directory Indexer - User Manual](#directory-indexer---user-manual)
  - [Overview](#overview)
  - [Features](#features)
  - [How to Use](#how-to-use)
  - [Output Formats](#output-formats)
    - [Excel](#excel)
      - [`Index` Sheet](#index-sheet)
      - [`Infos` Sheet](#infos-sheet)
  - [License](#license)

## Overview
**Directory Indexer** is a cross-platform tool for indexing the contents of a directory into an Excel file, including nested subfolders.

## Features
- Recursively index all files and folders
- Customizable file extension filter (not functional in 0.1)
- Output saved in Excel format (more formats to be implemented)
- Includes metadata (settings, file/folder count, timestamp)
- Clean UI with directory pickers

---

## How to Use

1. **Launch the App**

2. **Input Fields**
- **Input Directory**: Folder to index (defaults to current directory)
- **File Extensions**: Comma-separated list (e.g., `txt, xls`) or leave empty for all
- **Output Directory**: Destination for the Excel file (defaults to current directory)

3. **Run Indexing**
- Click **"Index Directory"**
- On success, a file is created in the output directory.
- On error, a notification appears. If the problem is not from the inputs, please open an issue.
- Execution logs are available in the `directory_indexer.log` file, next to the executable.

---

## Output Formats

### Excel 

#### `Index` Sheet
| Name        | Path                        | Sub-folder Level | Type   |
|-------------|-----------------------------|------------------|--------|
| `file.txt`  | `/path/to/file.txt`         | 1                | File   |
| `subfolder` | `/path/to/subfolder`        | 1                | Folder |

- Files are listed before folders at each level
- Subfolders are nested with incremented depth

#### `Infos` Sheet
| Setting Name     | Value                      |
|------------------|----------------------------|
| Input Directory  | `/path/to/input`           |
| Output Directory | `/path/to/output`          |
| Extensions       | `txt, xls`                 |
| Timestamp        | `2025-04-02 13:45:00`      |
| Files Count      | `123`                      |
| Folders Count    | `45`                       |
| Total Entries    | `168`                      |

---

## License

This tool is released under the MIT License — free to use, modify, and distribute with proper attribution.
