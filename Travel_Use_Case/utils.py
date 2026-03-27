from dateutil import parser
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re


def parse_date(date_str):
    if not date_str:
        return None

    original_str = date_str
    date_str = date_str.lower().strip()

    # Use current date (March 26, 2026 as per context)
    today = datetime(2026, 3, 26).date()

    # EXACT MATCHES for relative dates (most important - do these first)
    # Using both exact match and substring match for flexibility
    if date_str == "next weekend" or "next weekend" in date_str:
        days_until_saturday = (5 - today.weekday()) % 7
        if days_until_saturday == 0:
            days_until_saturday = 7
        next_saturday = today + timedelta(days=days_until_saturday)
        return datetime.combine(next_saturday, datetime.min.time())

    if date_str == "this weekend" or "this weekend" in date_str:
        days_until_saturday = (5 - today.weekday()) % 7
        if days_until_saturday == 0:
            this_saturday = today
        else:
            this_saturday = today + timedelta(days=days_until_saturday)
        return datetime.combine(this_saturday, datetime.min.time())

    if "tomorrow" in date_str:
        return datetime.combine(today + timedelta(days=1), datetime.min.time())

    if "today" in date_str:
        return datetime.combine(today, datetime.min.time())

    # In X days/weeks/months
    in_match = re.search(r'in\s+(\d+)\s+(days?|weeks?|months?)', date_str)
    if in_match:
        num = int(in_match.group(1))
        unit = in_match.group(2).rstrip('s')
        if unit == "day":
            return datetime.combine(today + timedelta(days=num), datetime.min.time())
        elif unit == "week":
            return datetime.combine(today + timedelta(weeks=num), datetime.min.time())
        elif unit == "month":
            return datetime.combine(today + relativedelta(months=num), datetime.min.time())

    # Next [day name]
    next_match = re.search(r'next\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday|weekend)', date_str)
    if next_match:
        day_name = next_match.group(1)
        if day_name == "weekend":
            days_until_saturday = (5 - today.weekday()) % 7
            if days_until_saturday == 0:
                days_until_saturday = 7
            next_saturday = today + timedelta(days=days_until_saturday)
            return datetime.combine(next_saturday, datetime.min.time())
        
        day_map = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }
        target_weekday = day_map[day_name]
        days_ahead = (target_weekday - today.weekday()) % 7
        if days_ahead <= 0:
            days_ahead += 7
        target_date = today + timedelta(days=days_ahead)
        return datetime.combine(target_date, datetime.min.time())

    # This [day name]
    this_match = re.search(r'this\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday|weekend)', date_str)
    if this_match:
        day_name = this_match.group(1)
        if day_name == "weekend":
            days_until_saturday = (5 - today.weekday()) % 7
            if days_until_saturday == 0:
                this_saturday = today
            else:
                this_saturday = today + timedelta(days=days_until_saturday)
            return datetime.combine(this_saturday, datetime.min.time())
        
        day_map = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }
        target_weekday = day_map[day_name]
        days_ahead = (target_weekday - today.weekday()) % 7
        if days_ahead < 0:
            days_ahead += 7
        elif days_ahead == 0:
            # If it's the same day, use today
            pass
        target_date = today + timedelta(days=days_ahead)
        return datetime.combine(target_date, datetime.min.time())

    # Standard date patterns - use default year as current year
    try:
        parsed = parser.parse(date_str, default=datetime(today.year, 1, 1), fuzzy=False)
        # If parsed date is in the past, assume next year
        if parsed.date() < today:
            parsed = parsed.replace(year=today.year + 1)
        return parsed
    except:
        pass

    # Last resort: fuzzy parsing with safety checks
    try:
        parsed = parser.parse(date_str, fuzzy=True, default=datetime(today.year, 1, 1))
        
        # CRITICAL SAFETY CHECK: If parsed date is suspiciously old (more than 1 year ago), assume it's a month/day pattern for current/next year
        if parsed.date() < datetime(today.year - 1, 1, 1).date():
            # Try parsing without year and use current year
            year_less = date_str
            # Remove any 4-digit year patterns
            year_less = re.sub(r'\b(19|20)\d{2}\b', '', year_less).strip()
            try:
                parsed_no_year = parser.parse(year_less, default=datetime(today.year, 1, 1), fuzzy=True)
                if parsed_no_year.date() < today:
                    parsed_no_year = parsed_no_year.replace(year=today.year + 1)
                return parsed_no_year
            except:
                pass
        
        # If still in past, assume next year
        if parsed.date() < today:
            parsed = parsed.replace(year=today.year + 1)
        
        return parsed
    except:
        return None


def calculate_duration(start, end):
    if start and end:
        return (end.date() - start.date()).days + 1  # Include both start and end days
    return None