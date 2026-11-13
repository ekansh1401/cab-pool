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
class Cab:
    def __init__(self, driver, seats, destination, time_slot):
        self.driver = driver
        self.seats = seats
        self.destination = destination
        self.time_slot = time_slot
        self.passengers = []
        self.departed = False

    def free_seats(self):
        return self.seats - len(self.passengers)

    def __str__(self):
        status = "Left" if self.departed else "Open"
        return (f"{self.driver} | {self.destination}, {self.time_slot} | "
                f"{len(self.passengers)}/{self.seats} seats | {status}")