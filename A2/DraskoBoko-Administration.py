# This script was generated with the help of AI tool ChatGPT

import sys

def read_input(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f if line.strip()]

    n, cost_limit = map(int, lines[0].split())
    capitals = lines[1].split()
    cost = {}

    for i in range(n):
        entries = lines[2 + i].split()
        for j in range(n):
            if entries[j] != '-':
                c = int(entries[j])
                cost[(capitals[i], capitals[j])] = c
                cost[(capitals[j], capitals[i])] = c  # Matrix is symmetric

    return n, cost_limit, capitals, cost

def generate_partitions_bnb(capitals, cost_dict, partial_partition=[], partial_cost=0, cost_limit=float('inf')):
    if not capitals:
        yield partial_partition, partial_cost
        return

    first = capitals[0]
    for i in range(1, len(capitals)):
        second = capitals[i]
        cost = cost_dict[(first, second)]
        new_cost = partial_cost + cost
        if new_cost > cost_limit:
            continue  # Prune branch if partial cost exceeds limit
        rest = capitals[1:i] + capitals[i+1:]
        yield from generate_partitions_bnb(
            rest,
            cost_dict,
            partial_partition + [[first, second]],
            new_cost,
            cost_limit
        )

def partition_to_string(partition):
    sorted_pairs = [''.join(sorted(pair)) for pair in partition]
    sorted_pairs.sort()
    return ' '.join(sorted_pairs)

def main():
    optimize = False
    args = sys.argv[1:]

    if '-o' in args:
        optimize = True
        args.remove('-o')

    if not args:
        print("Usage: script.py [-o] inputfile")
        sys.exit(1)

    inputfile = args[0]
    n, cost_limit, capitals, cost_dict = read_input(inputfile)

    best_cost = cost_limit + 1
    seen = set()

    for partition, part_cost in generate_partitions_bnb(
        capitals,
        cost_dict,
        cost_limit=cost_limit if not optimize else best_cost
    ):
        if optimize:
            if part_cost < best_cost:
                best_cost = part_cost
        else:
            if part_cost <= cost_limit:
                p_string = partition_to_string(partition)
                if p_string not in seen:
                    seen.add(p_string)
                    print(p_string)

    if optimize:
        print(best_cost)

if __name__ == "__main__":
    main()
