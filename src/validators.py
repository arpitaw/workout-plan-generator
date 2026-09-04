from typing import Optional


def validate_inputs(
    fitness_goal: str,
    experience_level: str,
    days_per_week: int,
    equipment_access: str,
) -> tuple[bool, Optional[str]]:
    """
    Validate user inputs.

    Returns:
        (is_valid, error_message)
    """
    if not fitness_goal:
        return False, "Please select a fitness goal."
    if not experience_level:
        return False, "Please select your experience level."
    if days_per_week < 1 or days_per_week > 7:
        return False, "Days available per week must be between 1 and 7."
    if not equipment_access:
        return False, "Please select your equipment access."
    return True, None
