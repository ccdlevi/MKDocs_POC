#!/usr/bin/env python3
"""
Word to Markdown Converter

This script converts Microsoft Word documents to Markdown files for use with MkDocs.
It handles images, tables, and formatting to create clean Markdown output.

Requirements:
- python-docx
- mammoth
- Pillow
- pathlib
- yaml

Usage:
python word_to_markdown.py --input /path/to/word/docs --output /path/to/markdown/docs
"""

import os
import argparse
import re
import shutil
import mammoth
import yaml
from pathlib import Path
from docx import Document
from PIL import Image
from datetime import datetime

def extract_metadata(docx_path):
    """Extract metadata from Word document properties."""
    doc = Document(docx_path)
    core_properties = doc.core_properties
    
    metadata = {
        "title": core_properties.title or os.path.basename(docx_path).replace('.docx', ''),
        "author": core_properties.author or "Unknown",
        "date": core_properties.modified.strftime("%Y-%m-%d") if core_properties.modified else datetime.now().strftime("%Y-%m-%d"),
        "summary": core_properties.comments or ""
    }
    
    return metadata

def clean_markdown(markdown):
    """Clean up the Markdown content."""
    # Fix headers (ensure space after #)
    markdown = re.sub(r'(^|\n)#+([^\s#])', r'\1## \2', markdown)
    
    # Fix lists (ensure space after bullet)
    markdown = re.sub(r'(^|\n)[*-]([^\s])', r'\1* \2', markdown)
    
    # Fix tables
    # (Add more cleanup as needed)
    
    return markdown

def extract_images(docx_path, markdown, output_dir):
    """Extract images from Word document and update links in Markdown."""
    image_dir = os.path.join(output_dir, "images")
    os.makedirs(image_dir, exist_ok=True)
    
    # This is a simplified version - actual implementation would need
    # to extract images from the Word document and update references
    
    # For demonstration purposes, we'll assume mammoth handles the basics
    # and we just need to adjust paths
    markdown = re.sub(r'!\[(.*?)\]\(word\/(.*?)\)', r'![\1](images/\2)', markdown)
    
    return markdown

def process_document(docx_path, output_dir):
    """Process a single Word document."""
    filename = os.path.basename(docx_path).replace('.docx', '.md')
    output_path = os.path.join(output_dir, filename)
    
    # Extract metadata
    metadata = extract_metadata(docx_path)
    
    # Convert document to markdown
    with open(docx_path, 'rb') as docx_file:
        result = mammoth.convert_to_markdown(docx_file)
        markdown = result.value
        
    # Clean up the markdown
    markdown = clean_markdown(markdown)
    
    # Extract and process images
    markdown = extract_images(docx_path, markdown, output_dir)
    
    # Create front matter
    front_matter = "---\n" + yaml.dump(metadata) + "---\n\n"
    
    # Write the output file
    with open(output_path, 'w', encoding='utf-8') as md_file:
        md_file.write(front_matter + markdown)
    
    print(f"Converted: {docx_path} -> {output_path}")
    
    # Report any warnings
    for warning in result.warnings:
        print(f"Warning: {warning}")

def main():
    parser = argparse.ArgumentParser(description='Convert Word documents to Markdown for MkDocs')
    parser.add_argument('--input', required=True, help='Input directory containing Word documents')
    parser.add_argument('--output', required=True, help='Output directory for Markdown files')
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    # Process all Word documents in the input directory
    for file in os.listdir(args.input):
        if file.endswith('.docx') and not file.startswith('~$'):  # Skip temporary Word files
            docx_path = os.path.join(args.input, file)
            process_document(docx_path, args.output)

if __name__ == "__main__":
    main()
