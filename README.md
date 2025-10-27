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

1. Download the bundled PDF from Workday containing all candidates
2. Place the PDF in this directory (filename should start with "R007")
3. Run the script:
```bash
python split_pdf_by_candidate.py
```

The script will:
- Automatically find PDF files starting with "R007"
- Extract the table of contents to identify candidates
- Create a `candidates/` folder
- Create subfolders for each candidate named `Lastname_Firstname`
- Save individual PDFs in each candidate's folder

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
If the script can't find the table of contents, uncomment the analysis line in the script:
```python
splitter.analyze_pdf_structure()
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

## Using the Workday Downloader (Advanced)
## Using the Workday Downloader (Advanced)

This tool requires customization for your specific Workday instance.

### Setup

1. Create your configuration file:
```bash
cp config.json.example config.json
```

2. Edit `config.json` with your Workday credentials and settings:

### Configuration Options

- **workday_url**: Your Workday login URL
- **applicants_url**: (Optional) Direct URL to applicants page if known
- **username**: Your Workday username
- **password**: Your Workday password
- **download_directory**: Where to save downloaded PDFs (default: ./downloads)
- **headless**: Run browser in headless mode (true/false)
- **chrome_binary**: (Optional) Path to Chrome binary if not in default location

## Usage

Run the script:
```bash
python workday_pdf_downloader.py
```

The script will:
1. Log into Workday
2. Navigate to the applicants/candidates page
3. Get a list of applicants
4. Visit each applicant's page
5. Download all available PDFs
6. Save PDFs in organized folders by applicant name

## Important Notes

### Security
- **Never commit `config.json` to version control** - it contains your credentials
- Add `config.json` to your `.gitignore` file
- Consider using environment variables for sensitive data in production

### Customization
The script may need customization based on your specific Workday instance:

1. **Login selectors** (lines 95-120): Workday login pages vary by organization
2. **Applicant page navigation** (lines 134-158): Adjust search and navigation logic
3. **PDF link detection** (lines 187-192): Modify XPath selectors to match your page structure

### Workday Page Structure
Different Workday implementations have different page structures. You may need to:
- Inspect your Workday pages to find correct element IDs and classes
- Update XPath selectors in the code
- Add wait times if pages load slowly

## Troubleshooting

### Login Issues
- Check that your credentials are correct in `config.json`
- Verify the login page element IDs match your Workday instance
- Try running with `headless: false` to see what's happening

### Download Issues
- Ensure Chrome has permission to download files
- Check that the download directory exists and is writable
- Verify PDF links are being detected correctly (check logs)

### Element Not Found Errors
- Workday pages vary by organization
- Use browser developer tools (F12) to inspect elements
- Update XPath selectors in the code to match your instance

## Logging

The script creates a log file `workday_downloader.log` with detailed information about:
- Login process
- Page navigation
- PDFs found and downloaded
- Any errors encountered

## Legal and Ethical Considerations

- Ensure you have permission to automate downloads from your Workday instance
- Respect rate limits and add appropriate delays
- Handle applicant data according to your organization's policies and relevant privacy laws
- This tool is for legitimate business use only

## License

Use at your own risk. Ensure compliance with your organization's policies and applicable laws.

## Support

For issues specific to your Workday instance, you'll need to:
1. Inspect your Workday pages using browser developer tools
2. Update the selectors in the code accordingly
3. Test with `headless: false` to debug issues

## Roadmap

Potential improvements:
- Multi-factor authentication support
- Parallel downloads
- Resume from previous session
- Filter applicants by job posting or date
- Export metadata to CSV
