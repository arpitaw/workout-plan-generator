from typing import Optional
from groq import Groq
import config


def generate_workout_plan(
    fitness_goal: str,
    experience_level: str,
    days_per_week: int,
    equipment_access: str,
    injuries_limitations: Optional[str] = None,
) -> str:
    """
    Generate a personalized weekly workout plan using the Groq API.

    Args:
        fitness_goal: User's primary fitness goal.
        experience_level: User's training experience level.
        days_per_week: Number of days available for training per week.
        equipment_access: Equipment the user has access to.
        injuries_limitations: Optional injuries or movement limitations.

    Returns:
        A formatted workout plan as a string.

    Raises:
        RuntimeError: If API call fails or response is malformed.
    """
    from src.prompt_builder import build_system_prompt, build_user_prompt

    if not config.GROQ_API_KEY:
        raise RuntimeError("Missing GROQ_API_KEY. Please set it in your .env file.")

    try:
        client = Groq(api_key=config.GROQ_API_KEY)

        system_prompt = build_system_prompt()
        user_prompt = build_user_prompt(
            fitness_goal=fitness_goal,
            experience_level=experience_level,
            days_per_week=days_per_week,
            equipment_access=equipment_access,
            injuries_limitations=injuries_limitations or "",
        )

        response = client.chat.completions.create(
            model=config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=config.LLM_TEMPERATURE,
            max_tokens=config.LLM_MAX_TOKENS,
        )

        content = response.choices[0].message.content if response.choices else None

        if not content or not content.strip():
            raise RuntimeError("The model returned an empty response.")

        return content.strip()

    except Exception as e:
        raise RuntimeError(f"Failed to generate workout plan: {str(e)}") from e
