"""
Banker's Algorithm Simulator
-----------------------------
Checks whether a system is in a SAFE state (i.e., deadlock can be
avoided) given the current Allocation matrix, Maximum matrix, and
Available resource vector.

Input (from console):
  - Number of processes
  - Number of resource types
  - Allocation matrix   (resources currently held by each process)
  - Maximum matrix      (maximum resources each process may need)
  - Available resources (resources currently free in the system)

Output:
  - Need matrix (Maximum - Allocation)
  - Whether the system is in a Safe State or an Unsafe State
  - A Safe Sequence of processes, if one exists
"""


def read_matrix(name, n_processes, n_resources):
    """Read an n_processes x n_resources matrix from the console."""
    matrix = []
    print(f"\nEnter the {name} matrix ({n_processes} rows x {n_resources} columns):")
    for i in range(n_processes):
        row = input(f"  P{i}: ").split()
        row = [int(x) for x in row]
        if len(row) != n_resources:
            # Basic validation so a mistyped row fails loudly instead
            # of silently corrupting later calculations.
            raise ValueError(
                f"Expected {n_resources} values for P{i}, got {len(row)}"
            )
        matrix.append(row)
    return matrix


def read_vector(name, n_resources):
    """Read a single vector of length n_resources from the console."""
    print(f"\nEnter the {name} vector ({n_resources} values):")
    row = input("  > ").split()
    row = [int(x) for x in row]
    if len(row) != n_resources:
        raise ValueError(f"Expected {n_resources} values, got {len(row)}")
    return row


def compute_need(allocation, maximum, n_processes, n_resources):
    need = []
    for i in range(n_processes):
        need.append([maximum[i][j] - allocation[i][j] for j in range(n_resources)])
    return need


def print_matrix(title, matrix):
    print(f"\n{title}:")
    for i, row in enumerate(matrix):
        print(f"P{i}: {row}")


def bankers_algorithm(n_processes, n_resources, allocation, maximum, available):
    """Runs the Banker's Algorithm SAFETY ALGORITHM:
    
          1. Work  = a working copy of Available (resources currently free).
          2. Finish[i] = False for every process (none have been proven
             safe to finish yet).
          3. Repeatedly look for some process i that is not yet finished
             whose Need can be fully covered by Work (Need[i] <= Work).
             - If found: pretend it runs to completion and gives back all
               of its Allocation, so Work += Allocation[i], mark
               Finish[i] = True, and append it to the Safe Sequence.
             - Keep scanning from the top until a full pass finds no more
               processes that qualify.
          4. If every process ends up Finished, the system is in a SAFE
             state and the order they finished in is a valid Safe
             Sequence. Otherwise, it's UNSAFE (deadlock may occur).
        """
    need = compute_need(allocation, maximum, n_processes, n_resources)
    print_matrix("Need Matrix", need)

    work = available[:]
    finish = [False] * n_processes
    safe_sequence = []

    # Keep looping and scanning for eligible processes until either
    # everyone is finished, or a full pass finds nobody new to add.
    while len(safe_sequence) < n_processes:
        found = False
        for i in range(n_processes):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(n_resources)):
                # Process i can get everything it might still need
                # from the currently available pool, so it can run to
                # completion. Simulate that by releasing everything it
                # currently holds back into the pool.
                for j in range(n_resources):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(f"P{i}")
                found = True
        if not found:
            # A full pass over every process found no one whose Need
            # fits in Work -- the remaining processes are stuck, so no
            # safe sequence exists.
            break

    if all(finish):
        print("\nSystem is in a Safe State.")
        print("Safe Sequence: " + " -> ".join(safe_sequence))
        return True, safe_sequence
    else:
        unfinished = [f"P{i}" for i in range(n_processes) if not finish[i]]
        print("\nSystem is in an Unsafe State (deadlock may occur).")
        print("Processes that could not be scheduled: " + ", ".join(unfinished))
        return False, safe_sequence


def request_resources(n_processes, n_resources, allocation, maximum, available):
    """Optional extension: test whether a resource request from a
    process can be granted safely (standard Banker's request check)."""
    pid = int(input("\nEnter process number requesting resources: "))
    request = input(f"Enter request vector for P{pid} ({n_resources} values): ").split()
    request = [int(x) for x in request]

    need = compute_need(allocation, maximum, n_processes, n_resources)

    # Rule 1: a process can never request more than it originally
    # declared as its maximum remaining need.
    if any(request[j] > need[pid][j] for j in range(n_resources)):
        print("Error: Process has exceeded its maximum claim.")
        return
    
    # Rule 2: the request can't exceed what's currently free.
    if any(request[j] > available[j] for j in range(n_resources)):
        print("Request cannot be granted: not enough resources currently available.")
        return

    # Tentatively grant the request: move the requested resources
    # from Available into this process's Allocation, then re-run the
    # safety algorithm to see if the resulting state is still safe.
    new_available = [available[j] - request[j] for j in range(n_resources)]
    new_allocation = [row[:] for row in allocation]
    new_allocation[pid] = [new_allocation[pid][j] + request[j] for j in range(n_resources)]

    print("\nChecking resulting state for safety...")
    safe, _ = bankers_algorithm(n_processes, n_resources, new_allocation, maximum, new_available)
    if safe:
        print(f"\nRequest can be granted immediately for P{pid}.")
    else:
        # Not actually applied to the real state -- the request would
        # have to wait until the system can grant it safely.
        print(f"\nRequest for P{pid} must wait (would leave system unsafe).")


def main():
    print("==============================================")
    print("           BANKER'S ALGORITHM SIMULATOR")
    print("==============================================")

    n_processes = int(input("Enter number of processes: "))
    n_resources = int(input("Enter number of resource types: "))

    allocation = read_matrix("Allocation", n_processes, n_resources)
    maximum = read_matrix("Maximum", n_processes, n_resources)
    available = read_vector("Available", n_resources)

    print_matrix("\nAllocation Matrix", allocation)
    print_matrix("Maximum Matrix", maximum)
    print(f"\nAvailable Resources: {available}")

    # Run the core safety check -- this prints the Need matrix and
    # the Safe/Unsafe verdict.
    bankers_algorithm(n_processes, n_resources, allocation, maximum, available)

    # Optional bonus feature: let the user simulate an incoming
    # resource request and see whether it could be safely granted.
    choice = input("\nWould you like to test a resource request? (y/n): ").strip().lower()
    if choice == "y":
        request_resources(n_processes, n_resources, allocation, maximum, available)

    print("\nDone.")


if __name__ == "__main__":
    main()
