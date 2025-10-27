#!/usr/bin/env python3
"""
PDF Splitter for Candidate Applications
Splits a bundled PDF containing multiple candidates into separate PDFs
organized by candidate name (Lastname_Firstname format)
"""

import os
import re
import logging
from pathlib import Path
from pypdf import PdfReader, PdfWriter

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_splitter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CandidatePDFSplitter:
    """Split a bundled candidate PDF into individual PDFs per candidate"""
    
    def __init__(self, input_pdf_path, output_base_dir='candidates'):
        """
        Initialize the splitter
        
        Args:
            input_pdf_path: Path to the input PDF file
            output_base_dir: Base directory for output folders
        """
        self.input_pdf_path = Path(input_pdf_path)
        self.output_base_dir = Path(output_base_dir)
        self.output_base_dir.mkdir(parents=True, exist_ok=True)
        self.reader = None
        
    def load_pdf(self):
        """Load the PDF file"""
        try:
            logger.info(f"Loading PDF: {self.input_pdf_path}")
            self.reader = PdfReader(str(self.input_pdf_path))
            logger.info(f"PDF loaded successfully. "
                       f"Total pages: {len(self.reader.pages)}")
            return True
        except Exception as e:
            logger.error(f"Error loading PDF: {e}")
            return False
    
    def extract_toc_from_outlines(self):
        """
        Extract table of contents from PDF outlines/bookmarks
        
        Returns:
            List of tuples: [(candidate_name, page_number), ...]
        """
        toc_entries = []
        
        try:
            if not self.reader.outline:
                logger.warning("No outlines/bookmarks found in PDF")
                return toc_entries
            
            def process_outline_item(item, level=0):
                """Recursively process outline items"""
                if isinstance(item, list):
                    for subitem in item:
                        process_outline_item(subitem, level + 1)
                else:
                    # item is a Destination object
                    try:
                        title = item.title if hasattr(item, 'title') \
                            else str(item)
                        
                        # Get page number - try different methods
                        page_obj = None
                        if hasattr(item, 'page'):
                            page_indirect = item.page
                            # Resolve indirect reference
                            page_obj = page_indirect.get_object() if \
                                hasattr(page_indirect, 'get_object') else \
                                page_indirect
                        elif '/Page' in item:
                            page_indirect = item['/Page']
                            page_obj = page_indirect.get_object() if \
                                hasattr(page_indirect, 'get_object') else \
                                page_indirect
                        
                        if page_obj:
                            page_num = self.reader.pages.index(page_obj)
                            toc_entries.append((title, page_num))
                            logger.debug(f"Found TOC entry: {title} -> "
                                       f"Page {page_num}")
                    except Exception as e:
                        logger.warning(f"Error processing outline item: "
                                     f"{e}")
            
            # Process all outline items
            for item in self.reader.outline:
                process_outline_item(item)
            
            logger.info(f"Extracted {len(toc_entries)} entries from TOC")
            
        except Exception as e:
            logger.error(f"Error extracting TOC from outlines: {e}")
            import traceback
            logger.error(traceback.format_exc())
        
        return toc_entries
    
    def extract_toc_from_text(self):
        """
        Extract table of contents by searching for TOC patterns in first pages
        
        Returns:
            List of tuples: [(candidate_name, page_number), ...]
        """
        toc_entries = []
        
        try:
            # Search first 5 pages for TOC
            max_pages_to_search = min(5, len(self.reader.pages))
            
            for page_idx in range(max_pages_to_search):
                page = self.reader.pages[page_idx]
                text = page.extract_text()
                
                # Look for patterns like:
                # "Name, Firstname ... 10" or "Lastname, Firstname 10"
                # Common TOC patterns with dots or spaces followed by page num
                pattern = r'([A-Z][a-zA-Z\-]+,\s+[A-Z][a-zA-Z\-]+)[\s.]+(\d+)'
                
                matches = re.findall(pattern, text)
                for name, page_num in matches:
                    toc_entries.append((name.strip(), int(page_num) - 1))
                    logger.debug(f"Found TOC entry: {name} -> Page {page_num}")
            
            logger.info(f"Extracted {len(toc_entries)} entries from text")
            
        except Exception as e:
            logger.error(f"Error extracting TOC from text: {e}")
        
        return toc_entries
    
    def parse_candidate_name(self, name_str):
        """
        Parse candidate name and convert to Lastname_Firstname format
        
        Args:
            name_str: Name string (e.g., "Smith, John" or "John Smith")
            
        Returns:
            Formatted name string "Lastname_Firstname"
        """
        # Clean up the name
        name_str = name_str.strip()
        
        # Handle "Lastname, Firstname" format
        if ',' in name_str:
            parts = name_str.split(',')
            lastname = parts[0].strip()
            firstname = parts[1].strip().split()[0]  # Take first name only
        else:
            # Handle "Firstname Lastname" format
            parts = name_str.split()
            if len(parts) >= 2:
                firstname = parts[0]
                lastname = parts[-1]
            else:
                # Single name - use as is
                return self.sanitize_filename(name_str)
        
        formatted = f"{lastname}_{firstname}"
        return self.sanitize_filename(formatted)
    
    def sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename.strip()
    
    def split_pdf(self):
        """Main method to split the PDF by candidates"""
        if not self.reader:
            if not self.load_pdf():
                return
        
        # Try to extract TOC from outlines first
        toc_entries = self.extract_toc_from_outlines()
        
        # If no outlines, try extracting from text
        if not toc_entries:
            logger.info("No outlines found, trying text extraction...")
            toc_entries = self.extract_toc_from_text()
        
        if not toc_entries:
            logger.error("Could not extract table of contents. "
                        "Manual parsing may be required.")
            return
        
        # Sort TOC entries by page number
        toc_entries.sort(key=lambda x: x[1])
        
        logger.info(f"Processing {len(toc_entries)} candidates...")
        
        # Process each candidate
        for i, (candidate_name, start_page) in enumerate(toc_entries):
            try:
                # Determine end page
                if i + 1 < len(toc_entries):
                    end_page = toc_entries[i + 1][1] - 1
                else:
                    # Last candidate goes to end of document
                    end_page = len(self.reader.pages) - 1
                
                # Parse and format name
                formatted_name = self.parse_candidate_name(candidate_name)
                
                logger.info(f"Processing {formatted_name}: "
                           f"pages {start_page + 1}-{end_page + 1}")
                
                # Create candidate folder
                candidate_folder = self.output_base_dir / formatted_name
                candidate_folder.mkdir(parents=True, exist_ok=True)
                
                # Create PDF for this candidate
                writer = PdfWriter()
                
                for page_num in range(start_page, end_page + 1):
                    if page_num < len(self.reader.pages):
                        writer.add_page(self.reader.pages[page_num])
                
                # Save the PDF
                output_path = candidate_folder / f"{formatted_name}.pdf"
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                
                logger.info(f"Created: {output_path}")
                
            except Exception as e:
                logger.error(f"Error processing {candidate_name}: {e}")
                continue
        
        logger.info("PDF splitting completed!")
    
    def analyze_pdf_structure(self):
        """
        Analyze PDF structure to help with manual TOC extraction if needed
        """
        if not self.reader:
            if not self.load_pdf():
                return
        
        logger.info("=== PDF Analysis ===")
        logger.info(f"Total pages: {len(self.reader.pages)}")
        logger.info(f"Has outlines: {bool(self.reader.outline)}")
        
        # Show first page text
        logger.info("\n=== First Page Text (first 1000 chars) ===")
        first_page_text = self.reader.pages[0].extract_text()
        logger.info(first_page_text[:1000])
        
        # Show second page text (might be TOC)
        if len(self.reader.pages) > 1:
            logger.info("\n=== Second Page Text (first 1000 chars) ===")
            second_page_text = self.reader.pages[1].extract_text()
            logger.info(second_page_text[:1000])


def main():
    """Main entry point"""
    import sys
    import glob
    import argparse
    
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Split a bundled PDF containing multiple candidates into '
                    'individual PDFs organized by candidate name.'
    )
    parser.add_argument(
        'pdf_file',
        nargs='?',
        help='Path to the PDF file to process. If not specified, looks for '
             'files starting with "R007".'
    )
    parser.add_argument(
        '-o', '--output',
        default='candidates',
        help='Output directory for candidate folders (default: candidates)'
    )
    parser.add_argument(
        '-a', '--analyze',
        action='store_true',
        help='Analyze PDF structure without splitting'
    )
    
    args = parser.parse_args()
    
    # Determine input PDF file
    if args.pdf_file:
        if not os.path.exists(args.pdf_file):
            logger.error(f"PDF file not found: {args.pdf_file}")
            sys.exit(1)
        input_pdf = args.pdf_file
    else:
        # Find PDF files starting with R007
        pdf_files = glob.glob('R007*.pdf')
        
        if not pdf_files:
            logger.error("No PDF files starting with 'R007' found in current "
                        "directory. Please specify a PDF file.")
            sys.exit(1)
        
        if len(pdf_files) > 1:
            logger.warning(f"Found {len(pdf_files)} PDF files. "
                          f"Using the first: {pdf_files[0]}")
        
        input_pdf = pdf_files[0]
    
    logger.info(f"Processing: {input_pdf}")
    
    # Create splitter instance
    splitter = CandidatePDFSplitter(input_pdf, args.output)
    
    # Analyze or split
    if args.analyze:
        splitter.analyze_pdf_structure()
    else:
        splitter.split_pdf()


if __name__ == "__main__":
    main()
