import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME", "EduGenie")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    # The documentation names Gemini 1.5 Pro. Keep the model configurable;
    # this default is a current lightweight choice for new API keys.
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    USE_LOCAL_EXPLAINER = os.getenv("USE_LOCAL_EXPLAINER", "false").lower() == "true"
    LOCAL_EXPLAINER_MODEL = os.getenv(
        "LOCAL_EXPLAINER_MODEL", "MBZUAI/LaMini-Flan-T5-783M"
    )
    MAX_INPUT_CHARS = int(os.getenv("MAX_INPUT_CHARS", "20000"))
    REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "60"))

@lru_cache
def get_settings() -> Settings:
    return Settings()
