# Complete Setup Guide - UFRGS Vestibular Test LLM Processor

## 📚 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Choosing Your LLM Provider](#choosing-your-llm-provider)
4. [Step-by-Step Setup for Each Provider](#step-by-step-setup-for-each-provider)
5. [Running the Program](#running-the-program)
6. [Switching Between Providers](#switching-between-providers)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required
- **Python 3.8 or higher** ([Download here](https://www.python.org/downloads/))
- **Internet connection** (for online providers)
- **A PDF file** with UFRGS vestibular test questions

### Recommended
- Basic command line knowledge
- Text editor to edit .env file

---

## Installation

### Step 1: Navigate to Project Directory
```bash
cd vestibular-ufrgs-llm
```

### Step 2: Install All Dependencies
```bash
pip install -r requirements.txt
```

This will install support for ALL LLM providers at once!

---

## Choosing Your LLM Provider

### 🆓 FREE OPTIONS (Recommended!)

#### 1. **Google Gemini** ⭐ BEST FOR BEGINNERS
- **Cost**: FREE (generous free tier)
- **Speed**: Fast
- **Quality**: Excellent
- **Setup Time**: 2 minutes
- **Best For**: Most users, Portuguese language, good reasoning
- **Get API Key**: https://makersuite.google.com/app/apikey

#### 2. **Groq** ⭐ FASTEST
- **Cost**: FREE (very generous limits)
- **Speed**: VERY FAST (fastest inference)
- **Quality**: Good
- **Setup Time**: 2 minutes
- **Best For**: Quick testing, batch processing
- **Get API Key**: https://console.groq.com/keys

#### 3. **Ollama** ⭐ 100% FREE & PRIVATE
- **Cost**: Completely FREE forever
- **Speed**: Depends on your computer
- **Quality**: Good to Excellent (depending on model)
- **Setup Time**: 10 minutes (includes download)
- **Best For**: Privacy, no internet required after setup, unlimited usage
- **Download**: https://ollama.com

### 💰 PAID OPTIONS

#### 4. **OpenAI**
- **Cost**: Pay per use (~$0.01-0.10 per test depending on model)
- **Speed**: Fast
- **Quality**: Excellent
- **Best For**: When you need the most reliable results
- **Get API Key**: https://platform.openai.com/api-keys

#### 5. **Anthropic Claude**
- **Cost**: Pay per use (~$0.05-0.15 per test)
- **Speed**: Fast
- **Quality**: Excellent
- **Best For**: Complex reasoning, detailed explanations
- **Get API Key**: https://console.anthropic.com/

---

## Step-by-Step Setup for Each Provider

### 🆓 Option 1: Google Gemini (RECOMMENDED)

#### Step 1: Get Your API Key
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with "AI...")

#### Step 2: Set Up Your Environment
```bash
# Option A: Create .env file
cp .env.example .env

# Option B: Edit .env file and add:
# GEMINI_API_KEY=your_actual_api_key_here
```

#### Step 3: Test It
```bash
python src/main.py
```
Select option "1" for Gemini when prompted.

---

### 🆓 Option 2: Groq (SUPER FAST)

#### Step 1: Get Your API Key
1. Go to https://console.groq.com/keys
2. Sign up for a free account
3. Click "Create API Key"
4. Copy the key

#### Step 2: Set Up Your Environment
Edit your `.env` file and add:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

#### Step 3: Test It
```bash
python src/main.py
```
Select option "2" for Groq when prompted.

---

### 🆓 Option 3: Ollama (100% FREE, LOCAL)

#### Step 1: Install Ollama
**On macOS**:
```bash
# Download and install from https://ollama.com
# Or use Homebrew:
brew install ollama
```

**On Linux**:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**On Windows**:
Download the installer from https://ollama.com/download

#### Step 2: Start Ollama Server
```bash
ollama serve
```
Leave this terminal running!

#### Step 3: Download a Model
Open a NEW terminal and run:
```bash
# Recommended: Llama 3.2 (fast, good quality)
ollama pull llama3.2

# Alternative options:
# ollama pull llama3.1    (more powerful)
# ollama pull mistral     (very good for Portuguese)
# ollama pull gemma2      (Google's model)
```

#### Step 4: Test It
```bash
python src/main.py
```
Select option "3" for Ollama when prompted.

**No API key needed!** ✨

---

### 💰 Option 4: OpenAI

#### Step 1: Get Your API Key
1. Go to https://platform.openai.com/api-keys
2. Create an account and add payment method
3. Click "Create new secret key"
4. Copy the key (starts with "sk-")

#### Step 2: Set Up Your Environment
Edit your `.env` file and add:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

#### Step 3: Test It
```bash
python src/main.py
```
Select option "4" for OpenAI when prompted.

---

### 💰 Option 5: Anthropic Claude

#### Step 1: Get Your API Key
1. Go to https://console.anthropic.com/
2. Create an account and add payment method
3. Generate an API key
4. Copy the key

#### Step 2: Set Up Your Environment
Edit your `.env` file and add:
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

#### Step 3: Test It
```bash
python src/main.py
```
Select option "5" for Anthropic when prompted.

---

## Running the Program

### Method 1: Interactive Mode (Easiest)

```bash
python src/main.py
```

The program will guide you through:
1. Selecting your LLM provider
2. Entering your PDF file path
3. Choosing where to save results
4. Selecting a model (optional)

### Method 2: Command Line

```bash
# Basic usage (uses Gemini by default)
python src/pipeline.py test.pdf output.json

# Specify provider
python src/pipeline.py test.pdf output.json --provider groq

# Specify provider and model
python src/pipeline.py test.pdf output.json --provider gemini --model gemini-1.5-pro

# With API key (if not in .env)
python src/pipeline.py test.pdf output.json --provider gemini --api-key YOUR_KEY
```

---

## Switching Between Providers

You can easily switch between providers without changing your setup!

### Option A: Using Interactive Mode
```bash
python src/main.py
```
Just select a different provider when prompted.

### Option B: Using Command Line
```bash
# Try with Gemini
python src/pipeline.py test.pdf answers_gemini.json --provider gemini

# Try with Groq
python src/pipeline.py test.pdf answers_groq.json --provider groq

# Try with Ollama
python src/pipeline.py test answers_ollama.json --provider ollama

# Compare results!
```

### Option C: Set Up Multiple API Keys
Edit your `.env` file with ALL your API keys:
```bash
GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key
```

Then switch providers anytime without re-entering keys!

---

## Troubleshooting

### "Module not found" Error
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

### "API key required" Error
```bash
# Solution: Check your .env file has the correct key
cat .env  # View your .env file

# Or enter API key when prompted
```

### "No questions extracted" Error
**Possible causes**:
- PDF contains only images (not text)
- PDF is corrupted
- Questions aren't numbered properly

**Solutions**:
- Try a different PDF
- Make sure PDF has selectable text
- Check if questions are numbered (01., 02., etc.)

### Ollama Connection Error
```bash
# Solution: Make sure Ollama is running
ollama serve

# In another terminal, test connection:
ollama list
```

### Slow Processing
**For Ollama**:
- Use a smaller model: `ollama pull llama3.2`
- Close other applications

**For Online Providers**:
- Check your internet connection
- Try a different provider (Groq is fastest)

---

## Comparison Table

| Provider | Cost | Speed | Quality | Setup | API Key Needed |
|----------|------|-------|---------|-------|---------------|
| **Gemini** | 🆓 FREE | ⚡⚡⚡ Fast | ⭐⭐⭐⭐⭐ Excellent | 2 min | Yes |
| **Groq** | 🆓 FREE | ⚡⚡⚡⚡⚡ Fastest | ⭐⭐⭐⭐ Good | 2 min | Yes |
| **Ollama** | 🆓 FREE | ⚡⚡ Moderate | ⭐⭐⭐⭐ Good | 10 min | No |
| **OpenAI** | 💰 $$ | ⚡⚡⚡ Fast | ⭐⭐⭐⭐⭐ Excellent | 5 min | Yes |
| **Claude** | 💰 $$$ | ⚡⚡⚡ Fast | ⭐⭐⭐⭐⭐ Excellent | 5 min  | Yes |

---

## Recommendations

### For Beginners
👉 Start with **Gemini** - It's free, fast, and excellent quality!

### For Maximum Speed
👉 Use **Groq** - FREE and incredibly fast

### For Privacy / No Internet
👉 Use **Ollama** - Runs completely on your computer

### For Best Results
👉 Use **OpenAI GPT-4o** or **Claude** - But they cost money

### For Testing Multiple Providers
👉 Set up all FREE providers (Gemini + Groq + Ollama) and compare!

---

## Next Steps

1. ✅ Choose your provider from the FREE options
2. ✅ Get your API key (2 minutes)
3. ✅ Run the program: `python src/main.py`
4. ✅ Process your first test!
5. ✅ Try other providers and compare results

**Happy testing!** 🎓📚
