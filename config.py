import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "openai/gpt-oss-120b"
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 1200

FITNESS_GOALS = ["Build muscle", "Lose fat", "General fitness", "Improve endurance"]
EXPERIENCE_LEVELS = ["Beginner", "Intermediate", "Advanced"]
EQUIPMENT_OPTIONS = ["No equipment", "Home dumbbells", "Full gym"]
