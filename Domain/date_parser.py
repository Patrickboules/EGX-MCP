from datetime import datetime

class DateParser:
    def stringfyDates(self, date:datetime):
        return date.strftime("%Y-%m-%d")