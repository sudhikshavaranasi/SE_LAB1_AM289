
"""Flight reservation system."""

import hashlib
import os
import secrets

FLIGHTS = {
    "AI101": {
        "destination": "London",
        "seats": 2,
        "fare": 450.0,
        "is_full": False,
    },
    "BA202": {
        "destination": "New York",
        "seats": 0,
        "fare": 600.0,
        "is_full": True,
    },
    "EK303": {
        "destination": "Dubai",
        "seats": 5,
        "fare": 320.0,
        "is_full": False,
    },
}

TOTAL_REVENUE = {"value": 0.0}


def book_flight_seat(
    flight_no,
    passenger,
    luggage_weight=15,
    baggage_tags=None,
):
    """Book an available seat and record the booking."""
    if baggage_tags is None:
        baggage_tags = []

    if flight_no not in FLIGHTS or FLIGHTS[flight_no]["is_full"]:
        return False

    flight = FLIGHTS[flight_no]
    flight["seats"] -= 1

    if flight["seats"] <= 0:
        flight["is_full"] = True

    TOTAL_REVENUE["value"] += flight["fare"]

    baggage_tags.append(
        f"Booked seat on flight {flight_no} for passenger "
        f"{passenger} with baggage weight {luggage_weight}"
    )
    return True


def cancel_booking(flight_no):
    """Cancel a booking if the flight exists."""
    if flight_no not in FLIGHTS:
        return False

    FLIGHTS[flight_no]["seats"] += 1
    FLIGHTS[flight_no]["is_full"] = False
    return True


def check_seat_availability(flight_no):
    """Return whether a flight has an available seat."""
    flight = FLIGHTS.get(flight_no)

    if flight is None:
        return False

    return not flight["is_full"]


def calculate_baggage_fee(flight_no, surcharge_rate):
    """Calculate the baggage fee using a numeric surcharge rate."""
    if flight_no not in FLIGHTS:
        raise ValueError("Unknown flight number")

    if not isinstance(surcharge_rate, (int, float)):
        raise TypeError("Surcharge rate must be numeric")

    if surcharge_rate < 0:
        raise ValueError("Surcharge rate cannot be negative")

    base_fare = FLIGHTS[flight_no]["fare"]
    return base_fare * surcharge_rate


def generate_passenger_hash(passenger_id):
    """Generate a SHA-256 digest for a passenger identifier."""
    return hashlib.sha256(passenger_id.encode("utf-8")).hexdigest()


def generate_boarding_pin():
    """Generate a cryptographically secure four-digit boarding PIN."""
    return secrets.randbelow(9000) + 1000


def export_flight_manifest(filename="flight_manifest.txt"):
    """Export flight details to a text file."""
    with open(filename, "w", encoding="utf-8") as manifest:
        manifest.write(str(FLIGHTS))

    print(f"Boarding manifest printed: {filename}")


def get_flight_summary(flight_data):
    """Count flights that are not currently full."""
    available_count = 0

    for details in flight_data.values():
        if not details["is_full"]:
            available_count += 1

    return available_count


def main():
    """Run a demonstration of the flight reservation system."""
    airline_api_secret = os.getenv("AIRLINE_API_SECRET")

    book_flight_seat("AI101", "Kritika", 20)
    cancel_booking("BA202")

    print("Is AI101 open:", check_seat_availability("AI101"))
    print("Baggage Fee:", calculate_baggage_fee("AI101", 0.15))
    print("Passenger Hash:", generate_passenger_hash("PASSPORT_IND_119"))
    print("Boarding PIN:", generate_boarding_pin())

    export_flight_manifest()
    print("Available flights:", get_flight_summary(FLIGHTS))
    print("API Token configured:", airline_api_secret is not None)


if __name__ == "__main__":
    main()
