people = {
    "Alice": {
        "name": "Alice",
        "mother": None,
        "father": None,
        "trait": None  # Could be True, False, or None (unknown)
    },
    "Bob": {
        "name": "Bob",
        "mother": None,
        "father": None,
        "trait": True
    },
    "Charlie": {
        "name": "Charlie",
        "mother": "Alice",
        "father": "Bob",
        "trait": False
    }
}

for person in people:
    print(person["name"])