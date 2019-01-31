from datetime import datetime


class DateTimeFunctions:

    time_in_string = ""
    am_or_pm = ""
    current_time_greet = "Good "

    @classmethod
    def get_current_time_str(cls):
        time = datetime.now().time()
        hour = time.hour
        minute = time.minute
        second = time.second
        if hour > 12:
            cls.am_or_pm = "PM"
        else:
            cls.am_or_pm = "AM"
        cls.time_in_string = str(int(hour) % 12) + ":" + str(minute) + ":" + str(second) + cls.am_or_pm
        return cls.time_in_string

    @classmethod
    def get_current_time_greet(cls):
        time = datetime.now().time()
        if time.hour < 12:
            cls.current_time_greet += "Morning"
        elif 12 <= time.hour < 17:
            cls.current_time_greet += "Afternoon"
        elif 17 <= time.hour < 21:
            cls.current_time_greet += "Evening"
        elif 21 <= time.hour < 23:
            cls.current_time_greet = "Hello"
        return cls.current_time_greet


dtf = DateTimeFunctions()
print(dtf.get_current_time_str())
