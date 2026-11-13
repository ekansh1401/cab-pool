from models import RideRequest, DESTINATIONS, TIME_SLOTS

waiting = []   # students waiting for a cab
cabs = []      # filled from a file in the next step


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


def add_request():
    name = input("Name: ").strip()
    if name == "":
        print("Name can't be empty.")
        return
    destination = ask_choice("Destination (Delhi/Jaipur): ", DESTINATIONS)
    time_slot = ask_choice("Time (Morning/Afternoon/Evening/Night): ", TIME_SLOTS)
    year = ask_year()
    waiting.append(RideRequest(name, destination, time_slot, year))
    print("Request added. You're on the waiting list.")


def show_all():
    print("\n--- Waiting students ---")
    if not waiting:
        print("Nobody is waiting.")
    for request in waiting:
        print(request)

    print("\n--- Cabs ---")
    if not cabs:
        print("No cabs loaded.")
    for cab in cabs:
        print(cab)


def main():
    while True:
        print("\n===== Cab Pool =====")
        print("1. Add ride request")
        print("2. Show waiting students and cabs")
        print("3. Quit")
        choice = input("Choose: ").strip()

        if choice == "1":
            add_request()
        elif choice == "2":
            show_all()
        elif choice == "3":
            print("Bye!")
            break
        else:
            print("Please type 1, 2 or 3.")


if __name__ == "__main__":
    main()