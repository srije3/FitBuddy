import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY)


def update_workout_plan(original_plan, feedback):

    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Original 7-day general wellness plan:

{original_plan}

User feedback:

{feedback}

Create an updated 7-day general wellness and physical-activity plan
based on the user's feedback.

Requirements:
- Keep the plan safe and age-appropriate.
- Include Day 1 through Day 7.
- Modify activities according to the feedback.
- Include warm-up and cool-down suggestions.
- Include rest and recovery when appropriate.
- Do not recommend extreme exercise.
- Do not recommend restrictive eating.
- Do not recommend rapid weight changes.
- Keep the plan simple and easy to understand.
"""

    models = [
        "gemini-3.5-flash",
        "gemini-3.1-flash-lite",
        "gemini-3.8-flash"
    ]

    for model in models:

        try:

            print(f"Trying update model: {model}")

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            if response.text:

                print(
                    f"Update success with model: {model}"
                )

                return response.text

        except Exception as e:

            print(
                f"Update error with {model}: {e}"
            )

            # Try the next model
            time.sleep(1)

    # Safe fallback so FastAPI does not return 500
    return """
Your feedback was received, but the AI service is temporarily
busy and could not generate the updated plan.

Please try submitting your feedback again in a few moments.
"""