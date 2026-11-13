# Cab Pool Matcher

This is an app in Python that helps students share cabs to Delhi or Jaipur at the end of the semester. Students submit ride requests, the requests wait in a queue for their trip, and when a cab is dispatched it gives priority to senior students first.

## How to run

Only Python 3 is required. No outside packages are used.

python3 main.py
```

## This is the Menu which appears on screen. The codes 1-5 do their respective tasks

1. **Add ride request**: name, destination, time slot and year. The request joins the waiting queue for that trip.
2. **Show waiting students and cabs**: everyone still waiting, and every cab with its seats (like `3/4`), status and passengers.
3. **Find matches**: a preview of who would get a seat in each open cab. Nothing changes.
4. **Dispatch cab**: pick a destination and time slot. The first open cab for that trip is filled with the most senior waiting students and leaves.
5. **Quit**

Wrong input (an invalid city, a time slot that doesn't exist, or a Year other than (1-5))
shows a friendly message and asks again instead of crashing.

## The cab file 

Cabs are loaded from `cabs.json` when the app starts. It is a list of cabs with required details:

```json
[
  {"driver": "Ramesh", "seats": 4, "destination": "Delhi", "time_slot": "Morning"},
  {"driver": "Mahesh", "seats": 2, "destination": "Jaipur", "time_slot": "Night"}
]
```

- `destination`: `Delhi` or `Jaipur`
- `time_slot`: `Morning`, `Afternoon`, `Evening` or `Night`
- `seats`: 1 to 4

Cabs are always checked in the order they appear in this file, so the app
gives the same result every time. A cab with invalid values is skipped with a
message. If the file is missing or broken, the app starts with no cabs.

## Working of the app

- `models.py` has the two classes, `RideRequest` and `Cab`.
- `main.py` has the menu, the queues and the logic for matching.
- There is one priority queue (a heap, using `heapq`) for every destination
  and time slot pair, for example `("Delhi", "Morning")`.
- Each heap entry is `(-year, order, request)`. `heapq` is a min-heap, so the
  negative year puts 5th years at the front. `order` is a counter that goes up
  by one with every request.

## Some specifications

**1. Half-empty cab.** A cab can leave with fewer students than seats. Dispatch
takes as many waiting students as there are (up to the free seats) and the cab
leaves, for example at `2/3`. The only case where it refuses is when nobody at
all is waiting for that trip, because an empty cab leaving helps no one.

**2. No cabs left.** Requests are still accepted and stay in the queue for
their trip. The student sees a note that there is no open cab for that trip
right now. Dispatch for that trip says "No open cab for this trip" and changes
nothing. Students are only removed from a queue when they are seated in a cab.

**3. Same year.** The heap entry is `(-year, order, request)`. If two students
have the same year, Python compares the `order` number next, so whoever asked
first comes out first. Since `order` is never the same twice, Python never has
to compare two `RideRequest` objects, which would crash.

**4. Lots of students (n waiting requests).**

| To add one request | O(log n) | One `heappush` into the trip's heap. log will have base 2 since heap is like a tree so for 1000 waiting it will take 10 steps maximum |
| Add all 1,000 | O(n log n) | n pushes, each O(log n). all 1000 just require 1 push 1000 times so 1000*10=10,000 (absolute upper limit) |
| Dispatch one cab | O(k log n), k ≤ 4 | Up to 4 `heappop` calls, each O(log n). Since k is at most 4, this will be at max 40|
| Find an open cab | O(c), c = number of cabs | A simple loop over the cab list in file order. This will be 5 regardless of the no. of students waiting |

Finding a cab could be made faster by grouping cabs by trip in a dictionary,
but there are only a few cabs, so a loop is simple and fast enough.

The Find Matches preview sorts a copy of each queue, which is O(n log n). That
is fine for a preview and keeps the real queue untouched.

## Design choices

- **Preview with two cabs on the same trip:** the first cab in the file gets
  the most senior students and the next cab gets the students after them. This
  matches what would happen if the cabs were dispatched one after the other.
- **Dispatch picks the cab by trip:** the user picks a destination and time
  slot, and the first open cab for that trip (in file order) leaves.