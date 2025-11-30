# UFRGS Vestibular Test LLM Processor

A Python application that processes UFRGS (Universidade Federal do Rio Grande do Sul) vestibular test PDFs and uses Large Language Models (LLMs) to generate answers for each question. The results are saved in a structured JSON format.

## Features

- 📄 **PDF Parsing**: Extracts questions from UFRGS vestibular test PDFs
- 🤖 **LLM Integration**: Uses OpenAI models to answer questions intelligently
- 💾 **JSON Output**: Saves answers in a structured JSON format
- 🎯 **Multiple Models**: Support for various OpenAI models (GPT-4o, GPT-4o-mini, GPT-3.5-turbo)
- 🌐 **Portuguese Support**: Optimized for Portuguese language questions
- 📊 **Metadata Tracking**: Includes test metadata in the output

## Requirements

- Python 3.8+
- OpenAI API key

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd LLMdoUfrgs/vestibular-ufrgs-llm
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_actual_api_key_here
```

## Usage

### Method 1: Interactive Mode (Recommended for beginners)

Run the main script and follow the interactive prompts:

```bash
python src/main.py
```

You'll be asked to provide:
- Path to the PDF file
- Output JSON file path (optional - will auto-generate if not provided)
- OpenAI API key (if not set in .env)
- Model selection (gpt-4o-mini, gpt-4o, or gpt-3.5-turbo)

### Method 2: Command Line

Run the pipeline script directly with command-line arguments:

```bash
python src/pipeline.py path/to/test.pdf path/to/output.json
```

**With options**:
```bash
python src/pipeline.py test.pdf answers.json --model gpt-4o --api-key YOUR_KEY
```

**Command-line arguments**:
- `pdf_file`: Path to the PDF file (required)
- `output_json`: Path to save the output JSON (required)
- `--api-key`: OpenAI API key (optional if set in .env)
- `--model`: Model to use (default: gpt-4o-mini)

## Output Format

The application generates a JSON file with the following structure:

```json
{
  "metadata": {
    "pdf_file": "vestibular_2024.pdf",
    "model_used": "gpt-4o-mini",
    "total_questions": 90
  },
  "answers": {
    "question_01": {
      "question": "Question text here...",
      "answer": "Answer provided by the LLM..."
    },
    "question_02": {
      "question": "Another question...",
      "answer": "Another answer..."
    }
  }
}
```

## Models Available

| Model | Speed | Cost | Quality | Recommended For |
|-------|-------|------|---------|----------------|
| **gpt-4o-mini** | Fast | Low | Good | General use (default) |
| **gpt-4o** | Medium | Medium | Excellent | Complex questions |
| **gpt-3.5-turbo** | Very Fast | Very Low | Acceptable | Quick testing |

## Project Structure

```
vestibular-ufrgs-llm/
├── src/
│   ├── __init__.py
│   ├── main.py           # Interactive entry point
│   ├── pipeline.py       # Main processing pipeline
│   ├── pdf_parser.py     # PDF extraction logic
│   ├── llm_client.py     # LLM integration
│   └── utils.py          # Utility functions
├── tests/
│   └── test_pipeline.py  # Unit tests
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitattributes
└── README.md            # This file
```

## How It Works

1. **PDF Extraction**: The application uses `pdfplumber` to extract text from the PDF file
2. **Question Parsing**: Uses regex patterns to identify and separate individual questions
3. **LLM Processing**: Each question is sent to the OpenAI API with a specialized system prompt
4. **Answer Collection**: Responses are collected and structured
5. **JSON Export**: Results are saved in a formatted JSON file with metadata

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
```

### API Key

Get your OpenAI API key from: https://platform.openai.com/api-keys

## Tips for Best Results

1. **PDF Quality**: Ensure the PDF has clear, extractable text (not scanned images)
2. **Model Selection**: 
   - Use `gpt-4o-mini` for most cases (good balance of cost and quality)
   - Use `gpt-4o` for complex reasoning questions
   - Use `gpt-3.5-turbo` for quick tests or simple questions
3. **Question Format**: The parser works best with numbered questions (01., 02., etc.)
4. **Review Answers**: Always review the LLM's answers for accuracy

## Troubleshooting

### "No questions could be extracted from the PDF"
- Check that the PDF contains text (not just images)
- Verify the question numbering format matches UFRGS standards
- Try opening the PDF manually to ensure it's not corrupted

### "Error initializing LLM client"
- Verify your OpenAI API key is correctly set
- Check your internet connection
- Ensure you have API credits available

### Import errors (pdfplumber not found)
- Run `pip install -r requirements.txt` again
- Verify you're using the correct Python environment

## Cost Estimation

Approximate costs per question (as of 2024):
- **gpt-4o-mini**: ~$0.0001 per question
- **gpt-4o**: ~$0.001 per question  
- **gpt-3.5-turbo**: ~$0.00005 per question

For a typical 90-question test:
- gpt-4o-mini: ~$0.009 (less than 1 cent)
- gpt-4o: ~$0.09 (9 cents)
- gpt-3.5-turbo: ~$0.0045 (less than 1 cent)

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

[Add your license information here]

## Disclaimer

This tool is designed to assist with analyzing vestibular tests. The accuracy of the answers depends on the LLM model used and the quality of the questions. Always verify important information independently.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the maintainers

---

**Note**: This application requires an active OpenAI API key and internet connection to function.
