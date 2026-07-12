import datetime

def calculate_countdown(task):
    deadline = task.creation_date + datetime.timedelta(days=7)
    now = datetime.datetime.now()
    if task.completed:
        return "Task is Done"
    if now > deadline:
        return "If you waited more than a week to get an idea done, abandon it"
    delta = deadline - now
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    if days == 0:
        minutes, _ = divmod(remainder, 60)
        if hours == 0:
            return f"{minutes} minutes" 
        else: 
            return f"{hours} hours, {minutes} minutes" 
    else:
        return f"{days} days, {hours} hours" 
