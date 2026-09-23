import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY)


def generate_workout_gemini(age, weight, goal, intensity):

    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Create a safe, beginner-friendly 7-day general wellness
and physical-activity plan.

User information:
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

Requirements:
- Provide Day 1 through Day 7.
- Include simple exercises or physical activities.
- Include warm-up and cool-down suggestions.
- Include rest or recovery when appropriate.
- Keep activities age-appropriate and safe.
- Do not prescribe extreme exercise.
- Do not recommend restrictive eating.
- Do not recommend rapid weight changes.
- Keep the response easy to read.
"""

    models = [
        "gemini-3.8-flash",
        "gemini-3.5-flash",
        "gemini-3.1-flash-lite"
    ]

    for model in models:

        for attempt in range(2):

            try:
                print(f"Trying Gemini model: {model}")

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if response.text:
                    print(f"Success with model: {model}")
                    return response.text

            except Exception as e:

                print(
                    f"Gemini error with {model}, "
                    f"attempt {attempt + 1}: {e}"
                )

                time.sleep(2)

    # If every model fails, return a readable message
    # instead of crashing the FastAPI page.
    return """
Unable to generate the AI workout plan right now.

The Gemini service is temporarily unavailable.
Please try again in a few moments.
"""