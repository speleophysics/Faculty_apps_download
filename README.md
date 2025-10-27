# Faculty Application PDF Tools

Tools for processing faculty job application PDFs from Workday.

## Overview

This repository contains a Python script to split bundled PDF files containing multiple job candidates into individual PDFs, organized by candidate name.

## Tool: PDF Splitter (`split_pdf_by_candidate.py`)

Split a bundled PDF containing all candidates into individual PDFs organized by candidate name.

**Features:**
- Extracts table of contents from PDF bookmarks/outlines
- Splits PDF by candidate sections
- Creates `Lastname_Firstname` folders for each candidate
- Saves individual PDFs automatically
- Comprehensive logging

## Prerequisites

- Python 3.7 or higher
- pypdf library

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd Faculty_apps_download
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

---

## Usage

### Quick Start

Run the script with a specific PDF file:
```bash
python split_pdf_by_candidate.py path/to/your/file.pdf
```

Or let it automatically find PDFs starting with "R007" in the current directory:
```bash
python split_pdf_by_candidate.py
```

The script will:
- Extract the table of contents to identify candidates
- Create a `candidates/` folder (or custom output directory)
- Create subfolders for each candidate named `Lastname_Firstname`
- Save individual PDFs in each candidate's folder

### Command Line Options

```bash
python split_pdf_by_candidate.py [PDF_FILE] [OPTIONS]
```

**Arguments:**
- `PDF_FILE` - (Optional) Path to the PDF file to process. If not specified, searches for files starting with "R007" in the current directory.

**Options:**
- `-o, --output DIR` - Output directory for candidate folders (default: `candidates`)
- `-a, --analyze` - Analyze PDF structure without splitting (useful for debugging)
- `-h, --help` - Show help message

**Examples:**
```bash
# Process a specific file
python split_pdf_by_candidate.py applications_2025.pdf

# Process with custom output directory
python split_pdf_by_candidate.py applications.pdf -o output_folder

# Analyze PDF structure without splitting
python split_pdf_by_candidate.py applications.pdf --analyze
```

### Output Structure
```
candidates/
├── Smith_John/
│   └── Smith_John.pdf
├── Doe_Jane/
│   └── Doe_Jane.pdf
└── Johnson_Mary/
    └── Johnson_Mary.pdf
```

### Troubleshooting

**No TOC found:**
If the script can't find the table of contents, use the analyze option:
```bash
python split_pdf_by_candidate.py your_file.pdf --analyze
```
This will show you the PDF structure to help debug.

**Name format issues:**
The script handles both "Lastname, Firstname" and "Firstname Lastname" formats automatically.

**Manual page ranges:**
If the TOC extraction doesn't work, you can modify the script to manually specify page ranges per candidate.

## Logging

The script creates a log file `pdf_splitter.log` with detailed information about:
- PDF loading and structure
- Table of contents extraction
- Candidate processing
- PDFs created
- Any errors encountered

## Files Ignored by Git

The following files/folders are excluded from version control (see `.gitignore`):
- `candidates/` - Output folder with split PDFs
- `*.log` - Log files
- `*.pdf` - PDF files
- `config.json` - Configuration files with credentials
- Python cache files

## Legal and Ethical Considerations

- Handle applicant data according to your organization's policies and relevant privacy laws
- This tool is for legitimate business use only
- Ensure compliance with data protection regulations (GDPR, etc.)

## License

Use at your own risk. Ensure compliance with your organization's policies and applicable laws.
