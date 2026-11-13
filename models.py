from datetime import datetime

DESTINATIONS = ["Delhi", "Jaipur"]
TIME_SLOTS = ["Morning", "Afternoon", "Evening", "Night"]


class RideRequest:
    def __init__(self, name, destination, time_slot, year):
        self.name = name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year
        self.submitted_at = datetime.now()

    def __str__(self):
        return f"{self.name} (Year {self.year}) -> {self.destination}, {self.time_slot}"