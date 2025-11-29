import json
import os
from pdf_parser import extract_questions_from_pdf
from llm_client import LLMClient, PROVIDER_INFO


def process_test(pdf_path, output_json_path, provider="gemini", api_key=None, model=None):
    """
    Main pipeline to process a UFRGS vestibular test PDF and generate answers using LLM.
    
    Args:
        pdf_path: Path to the input PDF file
        output_json_path: Path to save the output JSON file with answers
        provider: LLM provider to use (default: gemini)
        api_key: API key for the provider (optional, can be set via environment variable)
        model: LLM model to use (optional, uses provider default)
        
    Returns:
        Dictionary with the results
    """
    print(f"Starting processing of: {pdf_path}")
    print(f"Using provider: {provider}")
    
    # Step 1: Extract questions from PDF
    print("Step 1: Extracting questions from PDF...")
    questions = extract_questions_from_pdf(pdf_path)
    
    if not questions:
        print("Error: No questions could be extracted from the PDF.")
        return None
    
    print(f"Successfully extracted {len(questions)} questions.")
    
    # Step 2: Initialize LLM client
    print(f"Step 2: Initializing {provider.upper()} client...")
    try:
        llm_client = LLMClient(provider=provider, api_key=api_key, model=model)
        print(f"Using model: {llm_client.model}")
    except ValueError as e:
        print(f"Error initializing LLM client: {e}")
        return None
    
    # Step 3: Get answers from LLM
    print("Step 3: Getting answers from LLM...")
    answers = llm_client.answer_multiple_questions(questions)
    
    # Step 4: Prepare output structure
    output = {
        "metadata": {
            "pdf_file": os.path.basename(pdf_path),
            "provider": provider,
            "model_used": llm_client.model,
            "total_questions": len(questions)
        },
        "answers": answers
    }
    
    # Step 5: Save to JSON file
    print(f"Step 4: Saving results to {output_json_path}...")
    try:
        with open(output_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(output, json_file, ensure_ascii=False, indent=2)
        print(f"Successfully saved answers to {output_json_path}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")
        return None
    
    return output


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Process a UFRGS vestibular test PDF and generate answers using LLM.'
    )
    parser.add_argument(
        'pdf_file',
        type=str,
        help='Path to the PDF file containing the test'
    )
    parser.add_argument(
        'output_json',
        type=str,
        help='Path to save the output JSON file with answers'
    )
    parser.add_argument(
        '--provider',
        type=str,
        default='gemini',
        choices=['openai', 'gemini', 'groq', 'anthropic', 'ollama'],
        help='LLM provider to use (default: gemini - FREE!)'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        default=None,
        help='API key for the provider (optional if set in environment variable)'
    )
    parser.add_argument(
        '--model',
        type=str,
        default=None,
        help='Specific model to use (optional, uses provider default)'
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not os.path.isfile(args.pdf_file):
        print(f"Error: File '{args.pdf_file}' does not exist.")
        exit(1)
    
    # Process the test
    result = process_test(
        pdf_path=args.pdf_file,
        output_json_path=args.output_json,
        provider=args.provider,
        api_key=args.api_key,
        model=args.model
    )
    
    if result:
        print("\n✓ Processing completed successfully!")
    else:
        print("\n✗ Processing failed.")
        exit(1)
