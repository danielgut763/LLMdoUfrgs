"""
Utility functions for UFRGS Vestibular Test LLM Processor
"""

import json
import os
from datetime import datetime


def format_json_output(data, indent=2):
    """
    Format data as pretty-printed JSON.
    
    Args:
        data: Data to format
        indent: Number of spaces for indentation
        
    Returns:
        Formatted JSON string
    """
    return json.dumps(data, indent=indent, ensure_ascii=False)


def handle_error(error_message):
    """
    Print error message with formatting.
    
    Args:
        error_message: Error message to display
    """
    print(f"❌ Error: {error_message}")


def validate_pdf_file(file_path):
    """
    Validate that a PDF file exists and is readable.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not os.path.exists(file_path):
        return False, f"File does not exist: {file_path}"
    
    if not os.path.isfile(file_path):
        return False, f"Path is not a file: {file_path}"
    
    if not file_path.lower().endswith('.pdf'):
        return False, f"File is not a PDF: {file_path}"
    
    if os.path.getsize(file_path) == 0:
        return False, f"File is empty: {file_path}"
    
    return True, None


def ensure_output_directory(file_path):
    """
    Ensure that the directory for the output file exists.
    
    Args:
        file_path: Path to the output file
        
    Returns:
        True if directory exists or was created, False otherwise
    """
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        try:
            os.makedirs(directory, exist_ok=True)
            return True
        except Exception as e:
            handle_error(f"Could not create directory: {e}")
            return False
    return True


def generate_output_filename(input_pdf_path, suffix="_answers"):
    """
    Generate an output filename based on the input PDF name.
    
    Args:
        input_pdf_path: Path to input PDF
        suffix: Suffix to add before .json extension
        
    Returns:
        Output filename with .json extension
    """
    base_name = os.path.splitext(os.path.basename(input_pdf_path))[0]
    return f"{base_name}{suffix}.json"


def get_timestamp():
    """
    Get current timestamp as formatted string.
    
    Returns:
        Timestamp string in ISO format
    """
    return datetime.now().isoformat()


def count_tokens_estimate(text):
    """
    Estimate the number of tokens in text (rough approximation).
    OpenAI typically uses ~4 characters per token for English,
    ~2-3 for Portuguese.
    
    Args:
        text: Text to estimate tokens for
        
    Returns:
        Estimated token count
    """
    # Rough estimate: 3 characters per token for Portuguese
    return len(text) // 3


def format_progress(current, total, bar_length=50):
    """
    Create a progress bar string.
    
    Args:
        current: Current progress value
        total: Total value
        bar_length: Length of the progress bar in characters
        
    Returns:
        Formatted progress bar string
    """
    if total == 0:
        percent = 100
    else:
        percent = int((current / total) * 100)
    
    filled = int((bar_length * current) / total) if total > 0 else 0
    bar = '█' * filled + '░' * (bar_length - filled)
    
    return f"|{bar}| {percent}% ({current}/{total})"


def save_json(data, file_path):
    """
    Save data to a JSON file with error handling.
    
    Args:
        data: Data to save
        file_path: Path to save to
        
    Returns:
        True if successful, False otherwise
    """
    try:
        ensure_output_directory(file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        handle_error(f"Could not save JSON file: {e}")
        return False


def load_json(file_path):
    """
    Load data from a JSON file with error handling.
    
    Args:
        file_path: Path to load from
        
    Returns:
        Loaded data or None if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        handle_error(f"Could not load JSON file: {e}")
        return None
