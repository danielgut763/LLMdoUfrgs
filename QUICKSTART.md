# Quick Start Guide

Get started with the UFRGS Vestibular Test LLM Processor in 3 simple steps!

## Prerequisites

- Python 3.8 or higher installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation

### Option 1: Automated Setup (Recommended)

```bash
# Navigate to the project directory
cd vestibular-ufrgs-llm

# Run the setup script
python setup.py
```

This will:
- Check your Python version
- Install all required packages
- Create a .env file for your API key

### Option 2: Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Copy the environment file
cp .env.example .env

# Edit .env and add your API key
# OPENAI_API_KEY=your_key_here
```

## Usage

### Method 1: Interactive Mode (Easiest)

```bash
python src/main.py
```

Just follow the prompts! You'll be asked for:
1. Path to your PDF file
2. Where to save the results (optional)
3. Which AI model to use

### Method 2: Command Line

```bash
python src/pipeline.py path/to/test.pdf output.json
```

## Example

```bash
# Place your PDF in the project directory
# Run the program
python src/main.py

# When prompted:
# 1. Enter: vestibular_2024.pdf
# 2. Press Enter (for default output name)
# 3. Select model: 1 (for gpt-4o-mini)
# 4. Confirm: y

# Your results will be saved to: vestibular_2024_answers.json
```

## Output Format

The program creates a JSON file with this structure:

```json
{
  "metadata": {
    "pdf_file": "vestibular_2024.pdf",
    "model_used": "gpt-4o-mini",
    "total_questions": 90
  },
  "answers": {
    "question_01": {
      "question": "What is the capital of Brazil?",
      "answer": "The capital of Brazil is Brasília..."
    }
  }
}
```

## Model Selection Guide

| Model | Best For | Cost | Speed |
|-------|----------|------|-------|
| gpt-4o-mini | Most questions (recommended) | $ | Fast |
| gpt-4o | Complex reasoning | $$$ | Medium |
| gpt-3.5-turbo | Quick tests | $ | Very Fast |

## Troubleshooting

### "ModuleNotFoundError: No module named 'pdfplumber'"
**Solution:** Run `pip install -r requirements.txt`

### "OpenAI API key is required"
**Solution:** 
1. Get your key from https://platform.openai.com/api-keys
2. Add it to your .env file: `OPENAI_API_KEY=sk-...`

### "No questions could be extracted"
**Solution:** 
- Ensure your PDF contains text (not just images)
- Check that questions are numbered (01., 02., etc.)

## Tips

1. **Start with a small test**: Try with a PDF that has only a few questions first
2. **Use gpt-4o-mini**: It's fast, cheap, and accurate enough for most cases
3. **Check your results**: Always review the AI's answers for accuracy
4. **Save your API key**: Store it in the .env file to avoid re-entering it

## Need Help?

- Read the full [README.md](README.md) for detailed documentation
- Check the [GitHub Issues](../../issues) for common problems
- The program shows detailed error messages if something goes wrong

## Next Steps

After getting your first results:
1. Review the JSON output file
2. Compare AI answers with correct answers
3. Try different models to see which works best
4. Process multiple test PDFs

Happy testing! 🎓
