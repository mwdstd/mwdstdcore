class Date:
    def __init__(self, day: int, month: int, year: int):
        self.Year = 0
        self.Month = 0
        self.Day = 0
        self.DecimalYear = 0.
        self.update(day, month, year)

    def update(self, day: int, month: int, year: int):
        self.Year = year
        self.Month = month
        self.Day = day

        temp = 0
        if month == 0:
            self.DecimalYear = float(self.Year)
            return

        if (self.Year % 4 == 0 and self.Year % 100 != 0) or self.Year % 400 == 0:
            extra_day = 1
        else:
            extra_day = 0
        month_days = [0, 31, 28 + extra_day, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if self.Month <= 0 or self.Month > 12:
            raise Exception("Error: The Month entered is invalid, valid months are 1 to 12")
        if self.Day <= 0 or self.Day > month_days[self.Month]:
            raise Exception("Error: The day entered is invalid")

        i = 1
        while i <= self.Month:
            temp += month_days[i - 1]
            i += 1
        temp += self.Day
        self.DecimalYear = float(self.Year + (temp - 1) / (365.0 + extra_day))

