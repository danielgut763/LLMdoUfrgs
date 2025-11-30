import pdfplumber
import re


def extract_questions_from_pdf(pdf_path):
    """
    Extract questions from a UFRGS vestibular test PDF.
    Handles 2-day tests with duplicate question numbering.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary mapping question IDs to question text with metadata
    """
    questions = {}
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages_data = []
            
            # Extract text and images from all pages
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text() or ""
                images = page.images
                
                pages_data.append({
                    'page_num': page_num,
                    'text': text,
                    'has_images': len(images) > 0,
                    'image_count': len(images)
                })
            
            # Parse questions with page context
            questions = parse_questions_with_pages(pages_data)
            
    except Exception as e:
        print(f"Error extracting questions from PDF: {e}")
        return {}
    
    return questions


def parse_questions_with_pages(pages_data):
    """
    Parse questions from pages data with image context.
    Detects day transitions based on markers like "1º DIA" and "2º DIA".
    
    Args:
        pages_data: List of dicts with page_num, text, has_images, image_count
        
    Returns:
        Dictionary mapping question IDs to question data
    """
    questions = {}
    current_day = 1
    question_sequence = []  # Track (page, question_num, text)
    
    # First pass: collect all questions with page info
    for page_data in pages_data:
        text = page_data['text']
        page_num = page_data['page_num']
        
        # Check for day markers
        if re.search(r'2.?\s*[DºªOo]\s*DIA', text, re.IGNORECASE):
            current_day = 2
            print(f"DEBUG: Found Day 2 marker on page {page_num}")
        elif re.search(r'1.?\s*[DºªOo]\s*DIA', text, re.IGNORECASE) and current_day == 2:
            # Ignore, already on day 2
            pass
        
        # Extract questions from this page
        pattern = r'(\d{2,3})\.\s+(.*?)(?=\d{2,3}\.|$)'
        matches = re.findall(pattern, text, re.DOTALL)
        
        for match in matches:
            question_num = int(match[0])
            
            # Only valid question numbers
            if question_num < 1 or question_num > 150:
                continue
                
            question_text = clean_question_text(match[1].strip())
            
            if question_text and len(question_text) > 15:
                question_sequence.append({
                    'page': page_num,
                    'number': question_num,
                    'text': question_text,
                    'day': current_day,
                    'has_images': page_data['has_images'],
                    'image_count': page_data['image_count']
                })
    
    # Second pass: assign unique IDs
    for item in question_sequence:
        question_id = f"day{item['day']}_q{item['number']:03d}"
        
        # Include metadata about images
        question_data = {
            'text': item['text'],
            'page': item['page'],
            'has_images': item['has_images'],
            'image_count': item['image_count']
        }
        
        questions[question_id] = question_data
    
    # Summary
    day1_count = sum(1 for q in question_sequence if q['day'] == 1)
    day2_count = sum(1 for q in question_sequence if q['day'] == 2)
    
    print(f"DEBUG: Found {len(questions)} total questions")
    print(f"DEBUG: Day 1: {day1_count} questions")
    print(f"DEBUG: Day 2: {day2_count} questions")
    
    return questions


def parse_questions(text):
    """
    Parse questions from extracted text.
    UFRGS vestibular is a 2-day test, so questions repeat (Day 1: 1-90, Day 2: 1-45).
    Detects day transitions and labels questions accordingly.
    
    Args:
        text: Full text extracted from PDF
        
    Returns:
        Dictionary mapping question IDs to question text
    """
    questions = {}
    
    # Pattern to match question numbers
    pattern = r'(\d{2,3})\.\s+(.*?)(?=\d{2,3}\.|$)'
    matches = re.findall(pattern, text, re.DOTALL)
    
    current_day = 1
    last_question_num = 0
    day1_max = 0
    
    for match in matches:
        question_num = int(match[0])
        
        # Only accept question numbers between 1 and 150
        if question_num < 1 or question_num > 150:
            continue
            
        question_text = match[1].strip()
        question_text = clean_question_text(question_text)
        
        # Skip if too short
        if not question_text or len(question_text) < 15:
            continue
        
        # Detect day transition: if question number drops significantly, we're on day 2
        if question_num < last_question_num - 10:  # Big drop means new day
            current_day = 2
            print(f"DEBUG: Detected Day 2 starting at question {question_num}")
        
        # Track max question for day 1
        if current_day == 1:
            day1_max = max(day1_max, question_num)
        
        # Create unique question ID with day
        question_id = f"day{current_day}_q{question_num:03d}"
        questions[question_id] = question_text
        last_question_num = question_num
    
    print(f"DEBUG: Found {len(questions)} questions")
    print(f"DEBUG: Day 1 questions: 1-{day1_max}")
    print(f"DEBUG: Day 2 detected: {current_day == 2}")
    
    return questions


def clean_question_text(text):
    """
    Clean up question text by removing excessive whitespace and formatting.
    
    Args:
        text: Raw question text
        
    Returns:
        Cleaned question text
    """
    # Replace multiple spaces/newlines with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove page numbers and common footer/header text
    text = re.sub(r'Página\s+\d+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'UFRGS\s+\d{4}', '', text)
    
    return text.strip()


def parse_questions_alternative(text):
    """
    Alternative parsing method for different PDF formats.
    
    Args:
        text: Full text extracted from PDF
        
    Returns:
        Dictionary mapping question numbers to question text
    """
    questions = {}
    
    # Split by double newlines which often separate questions
    sections = text.split('\n\n')
    
    question_count = 0
    for section in sections:
        section = section.strip()
        
        # Check if section looks like a question (contains letters and punctuation)
        if len(section) > 20 and '?' in section:
            question_count += 1
            questions[f"question_{question_count:02d}"] = clean_question_text(section)
    
    return questions


def extract_questions_with_context(pdf_path):
    """
    Extract questions with additional context like tables and images metadata.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary with questions and additional context
    """
    questions_with_context = {}
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract text
                text = page.extract_text()
                
                # Extract tables if any
                tables = page.extract_tables()
                
                # Extract images metadata
                images = page.images
                
                context = {
                    "text": text,
                    "has_tables": len(tables) > 0,
                    "table_count": len(tables),
                    "has_images": len(images) > 0,
                    "image_count": len(images),
                    "page_number": page_num
                }
                
                questions_with_context[f"page_{page_num}"] = context
                
    except Exception as e:
        print(f"Error extracting questions with context: {e}")
    
    return questions_with_context
