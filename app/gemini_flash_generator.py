import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY)


def generate_nutrition_tip_with_flash(goal):

    prompt = f"""
You are FitBuddy, a general wellness assistant.

Give one short, age-appropriate nutrition and recovery tip
related to this fitness goal:

Goal: {goal}

Requirements:
- Focus on balanced meals, hydration, sleep, and recovery.
- Do not recommend restrictive diets.
- Do not recommend calorie counting.
- Do not recommend rapid weight changes.
- Keep the answer simple and practical.
- Give only one useful tip.
"""

    models = [
        "gemini-3.1-flash-lite",
        "gemini-3.5-flash",
        "gemini-3.8-flash"
    ]

    for model in models:

        try:
            print(f"Trying nutrition model: {model}")

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            if response.text:
                print(f"Nutrition success with model: {model}")
                return response.text

        except Exception as e:

            print(
                f"Nutrition error with {model}: {e}"
            )

            time.sleep(1)

    # Don't let the entire FastAPI request fail
    return (
        "For general wellness, focus on regular balanced meals, "
        "drink enough water, get adequate sleep, and allow time "
        "for recovery."
    )