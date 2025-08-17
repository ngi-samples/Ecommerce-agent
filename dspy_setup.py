# dspy_setup.py
import dspy
import os
from dotenv import load_dotenv

# Module-level guard: prevent re-import side effects
if not hasattr(dspy, "_configured_by_dspy_setup"):
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("❌ GEMINI_API_KEY not found in .env file. Please check your .env.")

    try:
        # Initialize the LLM
        print("🧠 Initializing Gemini AI model...")
        lm = dspy.LM("gemini/gemini-1.5-flash", api_key=api_key)  # ✅ Correct model name
        dspy.settings.configure(lm=lm)

        # Mark DSPy as configured to prevent re-configuration
        dspy._configured_by_dspy_setup = True
        print("✅ Gemini configured successfully via dspy_setup.py")

    except Exception as e:
        print(f"❌ Failed to configure DSPy: {str(e)}")
        raise