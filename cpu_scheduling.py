"""
CPU Scheduling Algorithm Simulator
-----------------------------------
Simulates the following scheduling algorithms:
  1. First Come First Serve (FCFS)            - Non-preemptive
  2. Shortest Job First (SJF)                 - Non-preemptive
  3. Round Robin (RR)                         - Preemptive
  4. Shortest Remaining Time First (SRTF)     - Preemptive SJF

For each algorithm the program prints:
  - A text Gantt Chart showing the execution order of the processes
  - Average Waiting Time
  - Average Turnaround Time

Input is taken from the console (number of processes, arrival time,
burst time, and time quantum where needed).
"""

import copy


# ---------------------------------------------------------------------
# Helper: read process data from the user
# ---------------------------------------------------------------------
def read_processes():
    n = int(input("Enter number of processes: "))
    processes = []
    for i in range(n):
        print(f"\n--- Process P{i} ---")
        at = int(input(f"  Arrival time of P{i}: "))
        bt = int(input(f"  Burst time of P{i}: "))
        processes.append({
            "pid": f"P{i}",
            "arrival": at,
            "burst": bt,
        })
    return processes


# ---------------------------------------------------------------------
# Helper: print a simple text Gantt chart from a timeline of
# (pid, start_time, end_time) tuples
# ---------------------------------------------------------------------
def print_gantt_chart(timeline):
    print("\nGantt Chart:")
    top = "|"
    bottom = ""
    for pid, start, end in timeline:
        width = max(len(pid) + 2, len(str(end)) + 1)
        top += f" {pid} ".center(width, " ") + "|"
    print(top)

    # print the time markers under each block
    line = f"{timeline[0][1]}"
    for pid, start, end in timeline:
        width = max(len(pid) + 2, len(str(end)) + 1)
        line += " " * (width - len(str(end))) + str(end)
    print(line)


# ---------------------------------------------------------------------
# Helper: print the final per-process results table + averages
# ---------------------------------------------------------------------
def print_results(processes):
    print("\n{:<6}{:<10}{:<8}{:<12}{:<14}{:<10}".format(
        "PID", "Arrival", "Burst", "Completion", "Turnaround", "Waiting"))
    total_wt = 0
    total_tat = 0
    for p in sorted(processes, key=lambda x: x["pid"]):
        total_wt += p["waiting"]
        total_tat += p["turnaround"]
        print("{:<6}{:<10}{:<8}{:<12}{:<14}{:<10}".format(
            p["pid"], p["arrival"], p["burst"],
            p["completion"], p["turnaround"], p["waiting"]))

    n = len(processes)
    avg_wt = total_wt / n
    avg_tat = total_tat / n
    print(f"\nAverage Waiting Time    : {avg_wt:.2f}")
    print(f"Average Turnaround Time : {avg_tat:.2f}")
    return avg_wt, avg_tat


# ---------------------------------------------------------------------
# 1. First Come First Serve (Non-Preemptive)
# ---------------------------------------------------------------------
def fcfs(process_list):
    processes = copy.deepcopy(process_list)
    processes.sort(key=lambda p: (p["arrival"], p["pid"]))

    time = 0
    timeline = []
    for p in processes:
        start = max(time, p["arrival"])
        end = start + p["burst"]
        timeline.append((p["pid"], start, end))
        p["completion"] = end
        p["turnaround"] = end - p["arrival"]
        p["waiting"] = p["turnaround"] - p["burst"]
        time = end

    print("\n================ FCFS (Non-Preemptive) ================")
    print_gantt_chart(timeline)
    print_results(processes)


# ---------------------------------------------------------------------
# 2. Shortest Job First (Non-Preemptive)
# ---------------------------------------------------------------------
def sjf_non_preemptive(process_list):
    processes = copy.deepcopy(process_list)
    n = len(processes)
    completed = 0
    time = 0
    timeline = []
    done = [False] * n

    while completed < n:
        # find the ready process with smallest burst time
        idx = -1
        best_burst = None
        for i, p in enumerate(processes):
            if not done[i] and p["arrival"] <= time:
                if best_burst is None or p["burst"] < best_burst or \
                        (p["burst"] == best_burst and p["arrival"] < processes[idx]["arrival"]):
                    best_burst = p["burst"]
                    idx = i

        if idx == -1:
            # no process has arrived yet, jump time forward
            time = min(p["arrival"] for i, p in enumerate(processes) if not done[i])
            continue

        p = processes[idx]
        start = time
        end = start + p["burst"]
        timeline.append((p["pid"], start, end))
        p["completion"] = end
        p["turnaround"] = end - p["arrival"]
        p["waiting"] = p["turnaround"] - p["burst"]
        time = end
        done[idx] = True
        completed += 1

    print("\n============ SJF (Non-Preemptive) ============")
    print_gantt_chart(timeline)
    print_results(processes)


# ---------------------------------------------------------------------
# 3. Round Robin (Preemptive)
# ---------------------------------------------------------------------
def round_robin(process_list, quantum):
    processes = copy.deepcopy(process_list)
    n = len(processes)
    remaining = {p["pid"]: p["burst"] for p in processes}
    arrival = {p["pid"]: p["arrival"] for p in processes}
    completion = {}

    processes_sorted = sorted(processes, key=lambda p: p["arrival"])
    queue = []
    timeline = []
    time = 0
    i = 0  # pointer into processes_sorted for arrivals not yet queued
    in_queue = set()

    # start clock at first arrival
    time = processes_sorted[0]["arrival"]

    while i < n and processes_sorted[i]["arrival"] <= time:
        queue.append(processes_sorted[i]["pid"])
        in_queue.add(processes_sorted[i]["pid"])
        i += 1

    while queue:
        pid = queue.pop(0)
        in_queue.discard(pid)
        run_time = min(quantum, remaining[pid])
        start = time
        end = start + run_time
        timeline.append((pid, start, end))
        remaining[pid] -= run_time
        time = end

        # add any processes that arrived during this run
        while i < n and processes_sorted[i]["arrival"] <= time:
            queue.append(processes_sorted[i]["pid"])
            in_queue.add(processes_sorted[i]["pid"])
            i += 1

        if remaining[pid] > 0:
            queue.append(pid)
        else:
            completion[pid] = time

        if not queue and i < n:
            # CPU idle until next arrival
            time = processes_sorted[i]["arrival"]
            while i < n and processes_sorted[i]["arrival"] <= time:
                queue.append(processes_sorted[i]["pid"])
                in_queue.add(processes_sorted[i]["pid"])
                i += 1

    for p in processes:
        p["completion"] = completion[p["pid"]]
        p["turnaround"] = p["completion"] - p["arrival"]
        p["waiting"] = p["turnaround"] - p["burst"]

    print(f"\n============ Round Robin (Quantum = {quantum}) ============")
    print_gantt_chart(timeline)
    print_results(processes)


# ---------------------------------------------------------------------
# 4. Shortest Remaining Time First (Preemptive SJF)
# ---------------------------------------------------------------------
def srtf(process_list):
    processes = copy.deepcopy(process_list)
    n = len(processes)
    remaining = {p["pid"]: p["burst"] for p in processes}
    arrival = {p["pid"]: p["arrival"] for p in processes}
    completed = 0
    time = min(p["arrival"] for p in processes)
    timeline = []
    last_pid = None
    seg_start = time
    completion = {}

    max_time_guard = sum(p["burst"] for p in processes) + max(p["arrival"] for p in processes) + 1

    while completed < n and time <= max_time_guard:
        # candidates that have arrived and are not finished
        candidates = [pid for pid in remaining if arrival[pid] <= time and remaining[pid] > 0]
        if not candidates:
            time += 1
            if last_pid is not None:
                timeline.append((last_pid, seg_start, time - 1))
                last_pid = None
            continue

        current = min(candidates, key=lambda pid: (remaining[pid], arrival[pid]))

        if current != last_pid:
            if last_pid is not None:
                timeline.append((last_pid, seg_start, time))
            seg_start = time
            last_pid = current

        remaining[current] -= 1
        time += 1

        if remaining[current] == 0:
            completion[current] = time
            timeline.append((last_pid, seg_start, time))
            last_pid = None
            completed += 1

    for p in processes:
        p["completion"] = completion[p["pid"]]
        p["turnaround"] = p["completion"] - p["arrival"]
        p["waiting"] = p["turnaround"] - p["burst"]

    print("\n============ SRTF (Preemptive SJF) ============")
    print_gantt_chart(timeline)
    print_results(processes)


# ---------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------
def main():
    print("==============================================")
    print("        CPU SCHEDULING ALGORITHM SIMULATOR")
    print("==============================================")
    processes = read_processes()

    while True:
        print("\nChoose a scheduling algorithm:")
        print("  1. FCFS (Non-Preemptive)")
        print("  2. SJF  (Non-Preemptive)")
        print("  3. Round Robin (Preemptive)")
        print("  4. SRTF (Preemptive SJF)")
        print("  5. Run ALL of the above")
        print("  0. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            fcfs(processes)
        elif choice == "2":
            sjf_non_preemptive(processes)
        elif choice == "3":
            q = int(input("Enter time quantum: "))
            round_robin(processes, q)
        elif choice == "4":
            srtf(processes)
        elif choice == "5":
            fcfs(processes)
            sjf_non_preemptive(processes)
            q = int(input("\nEnter time quantum for Round Robin: "))
            round_robin(processes, q)
            srtf(processes)
        elif choice == "0":
            print("Exiting program.")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
