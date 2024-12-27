from pysat.formula import CNF


def generate_sat_formula(num_guests, num_tables, seats_per_table, incompatible_pairs, required_pairs):
    cnf = CNF()

    # 1. Each guest must be seated at a table
    for guest in range(1, num_guests + 1):
        clause = [(guest - 1) * num_tables + table for table in range(1, num_tables + 1)]
        cnf.append(clause)

    # 2. Each guest can sit at most at one table
    for guest in range(1, num_guests + 1):
        for table1 in range(1, num_tables + 1):
            for table2 in range(table1 + 1, num_tables + 1):
                cnf.append([-(guest - 1) * num_tables - table1, -(guest - 1) * num_tables - table2])

    # 3. Each table can have at most seats_per_table guests
    for table in range(1, num_tables + 1):
        for guest1 in range(1, num_guests + 1):
            for guest2 in range(guest1 + 1, num_guests + 1):
                cnf.append([-(guest1 - 1) * num_tables - table, -(guest2 - 1) * num_tables - table])

    # 4. Incompatible pairs cannot sit together
    for guest1, guest2 in incompatible_pairs:
        for table in range(1, num_tables + 1):
            cnf.append([-(guest1 - 1) * num_tables - table, -(guest2 - 1) * num_tables - table])

    # 5. Required pairs must sit together
    for guest1, guest2 in required_pairs:
        for table in range(1, num_tables + 1):
            cnf.append([-(guest1 - 1) * num_tables - table, (guest2 - 1) * num_tables + table])
            cnf.append([-(guest2 - 1) * num_tables - table, (guest1 - 1) * num_tables + table])

    return cnf

def save_formula_to_file(cnf, file_name, num_tables):
    with open(file_name, 'w') as f:
        for clause in cnf.clauses:
            formatted_clause = " OR ".join([f"x_{(abs(literal) - 1) // num_tables + 1}_{(abs(literal) - 1) % num_tables + 1}" if literal > 0 else f"-x_{(abs(literal) - 1) // num_tables + 1}_{(abs(literal) - 1) % num_tables + 1}" for literal in clause])
            f.write(formatted_clause + "\n")


num_guests = 100
num_tables = 10
seats_per_table = 10
incompatible_pairs = [(1, 5), (10, 20)]
required_pairs = [(2, 3), (4, 7)]


cnf = generate_sat_formula(num_guests, num_tables, seats_per_table, incompatible_pairs, required_pairs)
file_name = "sat_formula1.txt"
save_formula_to_file(cnf, file_name, num_tables)

print(f"SAT Formula is saved in the '{file_name}'.")
