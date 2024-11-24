# Parameters
weeks = 5
groups = 8
group_size = 4
golfers = groups * group_size
max_depth = 160  # Maximum depth for DLS, weeks*groups*group_size


played_pairs = set()


def main():
    schedule = [[[0 for _ in range(group_size)] for _ in range(groups)] for _ in range(weeks)]

    if dls(0, 0, 0, schedule, 0):
        print("\nSolution found:")
        print_solution(schedule)
        validate_solution(schedule)
    else:
        print("No solution found.")


def dls(week, group, slot, schedule, depth):
    # Base Case
    if week == weeks:
        return True

    if depth == max_depth:
        print(f"Reached max depth ({max_depth}). Backtracking...")
        return False

    if slot == group_size:
        return dls(week, group + 1, 0, schedule, depth)

    if group == groups:
        return dls(week + 1, 0, 0, schedule, depth + 1)

    for golfer in range(1, golfers + 1):
        print(f"Trying golfer {golfer} in Week {week + 1}, Group {group + 1}, Slot {slot + 1}")
        print(f"Current played pairs: {played_pairs}")

        if is_valid(golfer, week, group, slot, schedule):
            schedule[week][group][slot] = golfer
            print(f"Placed golfer {golfer} in Week {week + 1}, Group {group + 1}, Slot {slot + 1}")

            if dls(week, group, slot + 1, schedule, depth):
                return True

            print(f"Backtracking from golfer {golfer} in Week {week + 1}, Group {group + 1}, Slot {slot + 1}")
            schedule[week][group][slot] = 0
            remove_played_pairs(golfer, week, group, schedule)


    return False


def is_valid(golfer, week, group, slot, schedule):
    for g in range(groups):
        for s in range(group_size):
            if schedule[week][g][s] == golfer:
                return False

    for s in range(slot):
        other_golfer = schedule[week][group][s]
        pair = generate_pair(golfer, other_golfer)
        if pair in played_pairs:
            return False


    for s in range(slot):
        other_golfer = schedule[week][group][s]
        pair = generate_pair(golfer, other_golfer)
        played_pairs.add(pair)

    return True


def generate_pair(golfer1, golfer2):
    return f"{min(golfer1, golfer2)}-{max(golfer1, golfer2)}"


def remove_played_pairs(golfer, week, group, schedule):
    for s in range(group_size):
        if schedule[week][group][s] != 0:
            pair = generate_pair(golfer, schedule[week][group][s])
            played_pairs.discard(pair)

def print_solution(schedule):
    for w in range(weeks):
        print(f"Week {w + 1}:")
        for g in range(groups):
            print(f"  Group {g + 1}: {' '.join(map(str, schedule[w][g]))}")


def validate_solution(schedule):
    duplicate_pairs = set()
    player_week_assignments = {week: set() for week in range(weeks)}

    for week in range(weeks):
        for group in schedule[week]:
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    player1 = group[i]
                    player2 = group[j]
                    pair = generate_pair(player1, player2)
                    if pair in duplicate_pairs:
                        print(f"Invalid: Pair {pair} played together more than once.")
                        return
                    duplicate_pairs.add(pair)

            for player in group:
                if player in player_week_assignments[week]:
                    print(f"Invalid: Player {player} assigned to multiple groups in Week {week + 1}.")
                    return
                player_week_assignments[week].add(player)

    print("Solution is valid: No duplicate pairs or player conflicts.")


if __name__ == "__main__":
    main()
