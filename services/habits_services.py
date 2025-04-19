def create_text_with_count_days(habit_text: str, days: int) -> str:
    text = (f"Привычка '{habit_text}' создана\n"
            f"Я буду напоминать про неё ")
    if days == 1:
        text += "раз в день"
    elif days in (2, 3, 4,):
        text += f"раз в {days} дня"
    else:
        text += f"раз в {days} дней"
    return text
