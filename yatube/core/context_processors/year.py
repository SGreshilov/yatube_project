from datetime import datetime


def year(request):
    """Текущий год"""

    y = datetime.now().year
    return {
        'year': y,
    }