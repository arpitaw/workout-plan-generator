def build_system_prompt() -> str:
    """Build the system prompt for the LLM."""
    return """
You are an expert fitness coach creating practical, safe, personalized workout plans.

Your job:
- Build a weekly workout plan the user can realistically follow.
- Strictly respect the user's goal, experience level, training days, equipment, and limitations.
- Do NOT recommend exercises that require unavailable equipment.
- If the user mentions injuries or limitations, avoid risky movements and include a brief non-medical disclaimer.
- Do not make medical diagnoses or treatment claims.
- Keep the plan practical, specific, and beginner-friendly when appropriate.

Output format:
1. Short overview
2. Weekly schedule by day:
   - Day 1: Title
   - Warm-up
   - Exercises: include sets, reps, and brief rest guidance
   - Optional finisher or cardio
3. Recovery / rest day guidance
4. Progression tips for 2–4 weeks
5. Very short disclaimer if limitations/injuries were provided

Style rules:
- Be clear and structured.
- No wall of text.
- No generic advice without specifics.
- Make the number of workout days exactly match the user's availability.
""".strip()


def build_user_prompt(
    fitness_goal: str,
    experience_level: str,
    days_per_week: int,
    equipment_access: str,
    injuries_limitations: str,
) -> str:
    """Build the user prompt for the LLM."""
    injuries_text = injuries_limitations.strip() if injuries_limitations else "None"

    return f"""
Create a personalized workout plan for this user:

Fitness goal: {fitness_goal}
Experience level: {experience_level}
Days available per week: {days_per_week}
Equipment access: {equipment_access}
Injuries or limitations: {injuries_text}

Important constraints:
- The plan must include exactly {days_per_week} workout days.
- Exercises must match this equipment access: {equipment_access}.
- If limitations exist, avoid movements likely to aggravate them.
- Make the plan realistic for a {experience_level.lower()} trainee.
- Include exercise names, sets, reps, and rest times.
- If the goal is lose fat or improve endurance, include appropriate cardio or conditioning.
- If the goal is build muscle, prioritize resistance training and reasonable volume.
- If the goal is general fitness, balance strength, mobility, and conditioning.

Return the result in a clean day-by-day format.
""".strip()
