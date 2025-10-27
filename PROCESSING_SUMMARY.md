# PDF Splitter Summary

## Purpose
This script splits a bundled PDF containing multiple job candidates into individual PDFs, organized by candidate name.

## Output Structure
Individual PDFs are created in folders with format: `Lastname_Firstname/`

### Example Output Directory Structure
```
candidates/
├── Lastname_Firstname/
│   └── Lastname_Firstname.pdf
├── Smith_John/
│   └── Smith_John.pdf
├── Doe_Jane/
│   └── Doe_Jane.pdf
... (one folder per candidate)
```

## Process
1. Extracts table of contents from PDF bookmarks
2. Identifies candidate sections with page ranges
3. Creates individual folders for each candidate
4. Splits and saves PDFs with proper naming: `Lastname_Firstname.pdf`

## Log File
See `pdf_splitter.log` for detailed processing information.

## Script
`split_pdf_by_candidate.py` - Automatically processes any PDF starting with "R007"
