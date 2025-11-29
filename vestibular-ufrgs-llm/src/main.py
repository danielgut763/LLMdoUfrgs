#!/usr/bin/env python3
"""
UFRGS Vestibular Test LLM Processor
Main entry point for the application.
"""

import os
import sys
from pipeline import process_test
from llm_client import PROVIDER_INFO


def print_provider_info():
    """Print information about available LLM providers."""
    print("\n" + "="*70)
    print("Available LLM Providers:")
    print("="*70)
    
    for idx, (key, info) in enumerate(PROVIDER_INFO.items(), 1):
        free_badge = "🆓 FREE!" if info["free"] else "💰 Paid"
        print(f"\n{idx}. {info['name']} {free_badge}")
        print(f"   Models: {', '.join(info['models'][:2])}")
        print(f"   {info['notes']}")
        if info["api_key_url"] != "Not needed - runs locally":
            print(f"   Get API key: {info['api_key_url']}")
    
    print("="*70)


def main():
    """
    Main function to run the UFRGS vestibular test processor.
    """
    print("=" * 70)
    print("🎓 UFRGS Vestibular Test LLM Processor")
    print("=" * 70)
    print()
    
    # Show provider information
    print_provider_info()
    
    # Get provider selection
    print("\nSelect LLM Provider:")
    print("  1. Gemini (Google) - 🆓 FREE and RECOMMENDED!")
    print("  2. Groq - 🆓 FREE and very fast")
    print("  3. Ollama - 🆓 FREE (runs locally on your computer)")
    print("  4. OpenAI - 💰 Paid but very reliable")
    print("  5. Anthropic Claude - 💰 Paid, high quality")
    
    provider_map = {
        "1": "gemini",
        "2": "groq",
        "3": "ollama",
        "4": "openai",
        "5": "anthropic"
    }
    
    provider_choice = input("\nEnter choice (1-5) or press Enter for Gemini: ").strip()
    provider = provider_map.get(provider_choice, "gemini")
    
    print(f"\n✓ Selected: {PROVIDER_INFO[provider]['name']}")
    
    # Get API key if needed
    api_key = None
    if provider != "ollama":
        env_key_name = f"{provider.upper()}_API_KEY"
        api_key = os.getenv(env_key_name)
        
        if not api_key:
            print(f"\n⚠️  No {env_key_name} found in environment.")
            api_key = input(f"Enter your {PROVIDER_INFO[provider]['name']} API key (or press Enter to skip): ").strip()
            
            if not api_key:
                print(f"\n❌ {PROVIDER_INFO[provider]['name']} requires an API key.")
                print(f"Get one here: {PROVIDER_INFO[provider]['api_key_url']}")
                sys.exit(1)
        else:
            print(f"✓ Using {env_key_name} from environment")
    else:
        print("✓ Ollama doesn't require an API key (runs locally)")
        print("⚠️  Make sure Ollama is installed and running!")
        print("   Download from: https://ollama.com")
    
    # Get input PDF file path
    print("\n" + "-"*70)
    pdf_path = input("Enter the path to the PDF file: ").strip()
    
    # Remove quotes if user dragged file
    pdf_path = pdf_path.strip('"').strip("'")
    
    # Validate file exists
    if not os.path.isfile(pdf_path):
        print(f"❌ Error: The file '{pdf_path}' does not exist.")
        sys.exit(1)
    
    # Get output JSON file path
    output_path = input("Enter output path (or press Enter for default): ").strip()
    
    # If no output path provided, create a default one
    if not output_path:
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = f"{base_name}_answers_{provider}.json"
        print(f"✓ Using default: {output_path}")
    
    # Model selection (optional)
    available_models = PROVIDER_INFO[provider]["models"]
    if len(available_models) > 1:
        print(f"\nAvailable models for {PROVIDER_INFO[provider]['name']}:")
        for idx, model in enumerate(available_models, 1):
            print(f"  {idx}. {model}")
        
        model_choice = input("Select model (or press Enter for default): ").strip()
        if model_choice.isdigit() and 1 <= int(model_choice) <= len(available_models):
            model = available_models[int(model_choice) - 1]
        else:
            model = None
    else:
        model = None
    
    print()
    print("-" * 70)
    print("Configuration:")
    print(f"  Provider: {PROVIDER_INFO[provider]['name']}")
    print(f"  Input PDF: {pdf_path}")
    print(f"  Output JSON: {output_path}")
    if model:
        print(f"  Model: {model}")
    print("-" * 70)
    print()
    
    # Confirm before proceeding
    confirm = input("Proceed with processing? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Processing cancelled.")
        sys.exit(0)
    
    print()
    
    # Process the test
    result = process_test(
        pdf_path=pdf_path,
        output_json_path=output_path,
        provider=provider,
        api_key=api_key if api_key else None,
        model=model
    )
    
    if result:
        print()
        print("=" * 70)
        print("✅ SUCCESS!")
        print("=" * 70)
        print(f"Results saved to: {output_path}")
        print(f"Provider used: {PROVIDER_INFO[provider]['name']}")
        print(f"Total questions processed: {result['metadata']['total_questions']}")
        print()
    else:
        print()
        print("=" * 70)
        print("❌ FAILED!")
        print("=" * 70)
        print("Processing encountered errors. Please check the output above.")
        print()
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
