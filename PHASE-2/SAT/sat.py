def generate_sat_formula(num_guests, num_tables, seats_per_table, incompatible_pairs, required_pairs):
    formula = []

    # 1. Each guest must be seated at a table
    for guest in range(1, num_guests + 1):
        clause = []
        for table in range(1, num_tables + 1):
            clause.append(f"x_{guest}_{table}")
        formula.append(" OR ".join(clause))

    # 2. Each guest can sit at most at one table
    for guest in range(1, num_guests + 1):
        for table1 in range(1, num_tables + 1):
            for table2 in range(table1 + 1, num_tables + 1):
                formula.append(f"NOT x_{guest}_{table1} OR NOT x_{guest}_{table2}")

    # 3. Each table can have at most seats_per_table guests
    for table in range(1, num_tables + 1):
        for guest1 in range(1, num_guests + 1):
            for guest2 in range(guest1 + 1, num_guests + 1):
                formula.append(f"NOT x_{guest1}_{table} OR NOT x_{guest2}_{table}")

    # 4. Incompatible pairs cannot sit together
    for pair in incompatible_pairs:
        guest1, guest2 = pair
        for table in range(1, num_tables + 1):
            formula.append(f"NOT x_{guest1}_{table} OR NOT x_{guest2}_{table}")

    # 5. Required pairs must sit together
    for pair in required_pairs:
        guest1, guest2 = pair
        for table in range(1, num_tables + 1):
            formula.append(f"NOT x_{guest1}_{table} OR x_{guest2}_{table}")
            formula.append(f"NOT x_{guest2}_{table} OR x_{guest1}_{table}")

    return formula

num_guests = 100
num_tables = 10
seats_per_table = 10

incompatible_pairs = [
    (1, 5),
    (10, 20)
]

required_pairs = [
    (2, 3),
    (4, 7)
]


formula = generate_sat_formula(num_guests, num_tables, seats_per_table, incompatible_pairs, required_pairs)


with open("sat_formula.txt", "w") as file:
    for clause in formula:
        file.write(clause + "\n")

print("SAT Formula is saved in the file 'sat_formula.txt'.")