import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMClient:
    """
    Universal LLM client that supports multiple providers:
    - OpenAI (GPT models)
    - Google Gemini (free tier available)
    - Groq (free, fast)
    - Anthropic Claude
    - Ollama (local, completely free)
    """
    
    def __init__(self, provider="openai", api_key=None, model=None, base_url=None):
        """
        Initialize the LLM client.
        
        Args:
            provider: LLM provider ("openai", "gemini", "groq", "anthropic", "ollama")
            api_key: API key for the provider (if needed)
            model: Model name (defaults to provider's recommended model)
            base_url: Base URL for API (mainly for Ollama)
        """
        self.provider = provider.lower()
        self.api_key = api_key
        self.base_url = base_url
        
        # Set default models for each provider
        default_models = {
            "openai": "gpt-4o-mini",
            "gemini": "gemini-2.0-flash",
            "groq": "llama-3.1-70b-versatile",
            "anthropic": "claude-3-5-sonnet-20241022",
            "ollama": "llama3.2"
        }
        
        self.model = model or default_models.get(self.provider, "gpt-4o-mini")
        
        # Initialize provider-specific client
        self._init_provider()
    
    def _init_provider(self):
        """Initialize the specific provider client."""
        if self.provider == "openai":
            from openai import OpenAI
            self.api_key = self.api_key or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OpenAI API key required. Set OPENAI_API_KEY or pass api_key parameter.")
            self.client = OpenAI(api_key=self.api_key)
            
        elif self.provider == "gemini":
            import google.generativeai as genai
            self.api_key = self.api_key or os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                raise ValueError("Gemini API key required. Set GEMINI_API_KEY or pass api_key parameter.")
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
            
        elif self.provider == "groq":
            from groq import Groq
            self.api_key = self.api_key or os.getenv("GROQ_API_KEY")
            if not self.api_key:
                raise ValueError("Groq API key required. Set GROQ_API_KEY or pass api_key parameter.")
            self.client = Groq(api_key=self.api_key)
            
        elif self.provider == "anthropic":
            from anthropic import Anthropic
            self.api_key = self.api_key or os.getenv("ANTHROPIC_API_KEY")
            if not self.api_key:
                raise ValueError("Anthropic API key required. Set ANTHROPIC_API_KEY or pass api_key parameter.")
            self.client = Anthropic(api_key=self.api_key)
            
        elif self.provider == "ollama":
            self.base_url = self.base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            self.client = None  # Ollama uses direct HTTP requests
            
        else:
            raise ValueError(f"Unknown provider: {self.provider}. Supported: openai, gemini, groq, anthropic, ollama")
    
    def answer_question(self, question_text, question_number=None):
        """
        Send a question to the LLM and get an answer.
        
        Args:
            question_text: The text of the question
            question_number: Optional question number for context
            
        Returns:
            The LLM's answer as a string
        """
        try:
            system_prompt = """Você responde questões do vestibular da UFRGS.
IMPORTANTE: Responda APENAS com a letra da alternativa correta (A, B, C, D ou E).
NÃO forneça explicações, justificativas ou texto adicional.
Responda somente: A, B, C, D ou E."""

            user_prompt = f"{question_text}"
            
            if self.provider == "openai":
                return self._answer_openai(system_prompt, user_prompt)
            elif self.provider == "gemini":
                return self._answer_gemini(system_prompt, user_prompt)
            elif self.provider == "groq":
                return self._answer_groq(system_prompt, user_prompt)
            elif self.provider == "anthropic":
                return self._answer_anthropic(system_prompt, user_prompt)
            elif self.provider == "ollama":
                return self._answer_ollama(system_prompt, user_prompt)
                
        except Exception as e:
            return f"Error getting answer: {str(e)}"
    
    def _answer_openai(self, system_prompt, user_prompt):
        """Get answer from OpenAI."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        answer = response.choices[0].message.content
        return answer.strip() if answer else "No answer provided"
    
    def _answer_gemini(self, system_prompt, user_prompt):
        """Get answer from Google Gemini."""
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        try:
            response = self.client.generate_content(full_prompt)
            return response.text.strip() if hasattr(response, 'text') and response.text else "No answer provided"
        except Exception as e:
            # Try alternative prompt format
            try:
                response = self.client.generate_content([full_prompt])
                return response.text.strip() if hasattr(response, 'text') and response.text else "No answer provided"
            except:
                return f"Error: {str(e)}"
    
    def _answer_groq(self, system_prompt, user_prompt):
        """Get answer from Groq."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        answer = response.choices[0].message.content
        return answer.strip() if answer else "No answer provided"
    
    def _answer_anthropic(self, system_prompt, user_prompt):
        """Get answer from Anthropic Claude."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        answer = response.content[0].text
        return answer.strip() if answer else "No answer provided"
    
    def _answer_ollama(self, system_prompt, user_prompt):
        """Get answer from Ollama (local)."""
        import requests
        
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": f"{system_prompt}\n\n{user_prompt}",
            "stream": False
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "No answer provided").strip()
    
    def answer_multiple_questions(self, questions):
        """
        Answer multiple questions and return a dictionary of results.
        
        Args:
            questions: List of question texts or dict with question numbers as keys
            
        Returns:
            Dictionary mapping question IDs to answers
        """
        answers = {}
        
        if isinstance(questions, list):
            for idx, question in enumerate(questions, 1):
                print(f"Processing question {idx}/{len(questions)}...")
                answer = self.answer_question(question, question_number=idx)
                answers[f"question_{idx}"] = {
                    "question": question,
                    "answer": answer
                }
        elif isinstance(questions, dict):
            total = len(questions)
            for idx, (q_id, question) in enumerate(questions.items(), 1):
                print(f"Processing question {idx}/{total}...")
                answer = self.answer_question(question, question_number=q_id)
                answers[q_id] = {
                    "question": question,
                    "answer": answer
                }
        
        return answers


# Provider information for users
PROVIDER_INFO = {
    "openai": {
        "name": "OpenAI",
        "models": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
        "free": False,
        "api_key_url": "https://platform.openai.com/api-keys",
        "notes": "Most reliable, moderate cost"
    },
    "gemini": {
        "name": "Google Gemini",
        "models": ["gemini-1.5-flash", "gemini-1.5-pro"],
        "free": True,
        "api_key_url": "https://makersuite.google.com/app/apikey",
        "notes": "FREE tier available! Fast and good quality"
    },
    "groq": {
        "name": "Groq",
        "models": ["llama-3.1-70b-versatile", "mixtral-8x7b-32768"],
        "free": True,
        "api_key_url": "https://console.groq.com/keys",
        "notes": "FREE! Very fast, good for testing"
    },
    "anthropic": {
        "name": "Anthropic Claude",
        "models": ["claude-3-5-sonnet-20241022", "claude-3-haiku-20240307"],
        "free": False,
        "api_key_url": "https://console.anthropic.com/",
        "notes": "High quality, moderate cost"
    },
    "ollama": {
        "name": "Ollama (Local)",
        "models": ["llama3.2", "llama3.1", "mistral", "gemma2"],
        "free": True,
        "api_key_url": "Not needed - runs locally",
        "notes": "100% FREE! Runs on your computer. Install from https://ollama.com"
    }
}
