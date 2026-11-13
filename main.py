import heapq
import itertools
import json

from models import RideRequest, Cab, DESTINATIONS, TIME_SLOTS

CABS_FILE = "cabs.json"

queues = {}                    # one waiting queue per trip
for d in DESTINATIONS:
    for t in TIME_SLOTS:
        queues[(d, t)] = []

counter = itertools.count()    # gives 0, 1, 2, ... one number per request
cabs = []      # this is loaded from cabs.json during startup


def ask_choice(prompt, options):
    while True:
        answer = input(prompt).strip().title()
        if answer in options:
            return answer
        print(f"Sorry, that's not valid. Choose from: {', '.join(options)}")


def ask_year():
    while True:
        answer = input("Year (1-5): ").strip()
        if answer.isdigit() and 1 <= int(answer) <= 5:
            return int(answer)
        print("Sorry, year must be a number from 1 to 5.")

def find_open_cab(destination, time_slot):
    for cab in cabs:
        if (not cab.departed and cab.destination == destination
                and cab.time_slot == time_slot):
            return cab
    return None

def add_request():
    name = input("Name: ").strip()
    if name == "":
        print("Name can't be empty.")
        return
    destination = ask_choice("Destination (Delhi/Jaipur): ", DESTINATIONS)
    time_slot = ask_choice("Time (Morning/Afternoon/Evening/Night): ", TIME_SLOTS)
    year = ask_year()
    request = RideRequest(name, destination, time_slot, year)
    entry = (-year, next(counter), request)
    heapq.heappush(queues[(destination, time_slot)], entry)
    print("Request added. You're on the waiting list.")
    if find_open_cab(destination, time_slot) is None:
        print("Note: there is no open cab for this trip right now. "
              "You will stay on the waiting list.")


def show_all():
    print("\n--- Waiting students ---")
    nobody = True
    for heap in queues.values():
        for entry in sorted(heap):
            print(entry[2])
            nobody = False
    if nobody:
        print("Nobody is waiting.")

    print("\n--- Cabs ---")
    if not cabs:
        print("No cabs loaded.")
    for cab in cabs:
        print(cab)
        for request in cab.passengers:
            print("   ", request)

def load_cabs():
    try:
        with open(CABS_FILE) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Could not find {CABS_FILE}. Starting with no cabs.")
        return
    except json.JSONDecodeError:
        print(f"{CABS_FILE} is not valid JSON. Starting with no cabs.")
        return

    for item in data:
        if (item["destination"] not in DESTINATIONS
                or item["time_slot"] not in TIME_SLOTS
                or not 1 <= item["seats"] <= 4):
            print(f"Skipping invalid cab: {item}")
            continue
        cabs.append(Cab(item["driver"], item["seats"],
                        item["destination"], item["time_slot"]))
    print(f"Loaded {len(cabs)} cabs.")

def find_matches():
    print("\n--- Matches (preview only, nobody is seated yet) ---")
    taken = {}          # students already claimed by earlier cabs of the same trip
    found_open = False

    for cab in cabs:
        if cab.departed:
            continue
        found_open = True
        trip = (cab.destination, cab.time_slot)
        start = taken.get(trip, 0)
        ordered = sorted(queues[trip])
        chosen = ordered[start:start + cab.free_seats()]
        taken[trip] = start + len(chosen)

        print(cab)
        if not chosen:
            print("    (nobody waiting for this cab)")
        for entry in chosen:
            print("   ", entry[2])

    if not found_open:
        print("No open cabs.")

def dispatch_cab():
    destination = ask_choice("Destination (Delhi/Jaipur): ", DESTINATIONS)
    time_slot = ask_choice("Time (Morning/Afternoon/Evening/Night): ", TIME_SLOTS)
    heap = queues[(destination, time_slot)]
    cab = find_open_cab(destination, time_slot)

    if cab is None:
        print("No open cab for this trip. Nothing changed.")
        return
    if not heap:
        print("Nobody is waiting for this trip. Nothing changed.")
        return

    while heap and cab.free_seats() > 0:
        entry = heapq.heappop(heap)
        cab.passengers.append(entry[2])
    cab.departed = True

    print(f"{cab.driver}'s cab has left with "
          f"{len(cab.passengers)}/{cab.seats} seats filled:")
    for request in cab.passengers:
        print("   ", request)
    if heap:
        print(f"{len(heap)} student(s) are still waiting for this trip.")

def main():
    load_cabs()
    while True:
        print("\n===== Cab Pool =====")
        print("1. Add ride request")
        print("2. Show waiting students and cabs")
        print("3. Find matches")
        print("4. Dispatch cab")
        print("5. Quit")
        choice = input("Choose: ").strip()

        if choice == "1":
            add_request()
        elif choice == "2":
            show_all()
        elif choice == "3":
            find_matches()
        elif choice == "4":
            dispatch_cab()
        elif choice == "5":
            print("Bye")
            break
        else:
            print("Please type a number from 1 to 5.")

if __name__ == "__main__":
    main()