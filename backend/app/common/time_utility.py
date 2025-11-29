from datetime import datetime
import pytz

def current_time_in_GMT():
    # Return timezone-naive UTC datetime for compatibility with TIMESTAMP WITHOUT TIME ZONE
    return datetime.utcnow()