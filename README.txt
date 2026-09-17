CS19L - Second Laboratory Exam
CPU Scheduling Algorithms + Banker's Algorithm
================================================

CONTENTS
--------
1. cpu_scheduling.py          - CPU scheduling simulator (FCFS, SJF,
                                 Round Robin, SRTF)
2. bankers_algorithm.py       - Banker's Algorithm deadlock-avoidance
                                 simulator
4. sample_cpu_scheduling.txt  - Corresponding console output
5. sample_output_bankers.txt  - Sample output for Banker's Algorithm
6. README.txt                 - This file

REQUIREMENTS
------------
Python 3.6 or newer (uses only the standard library, no extra
packages need to be installed).

HOW TO RUN
----------
1. CPU Scheduling Simulator

   Open a terminal in this folder and run:

       python cpu_scheduling.py

   You will be asked for:
     - Number of processes
     - Arrival time and Burst time for each process

   Then choose which algorithm to run from the menu:
     1 - FCFS (Non-Preemptive)
     2 - SJF  (Non-Preemptive)
     3 - Round Robin (Preemptive)  -> also asks for a Time Quantum
     4 - SRTF (Preemptive SJF)
     5 - Run ALL four algorithms one after another
     0 - Exit

   For each algorithm the program prints a text Gantt Chart, a table
   of Completion/Turnaround/Waiting time per process, and the
   Average Waiting Time and Average Turnaround Time.

   Example inputs and output are in sample_cpu_scheduling.txt.

2. Banker's Algorithm Simulator

   Run:

       python bankers_algorithm.py

   You will be asked for:
     - Number of processes
     - Number of resource types
     - Allocation matrix (one row per process)
     - Maximum matrix (one row per process)
     - Available resource vector

   The program then prints the computed Need matrix, states whether
   the system is in a Safe State or an Unsafe State, and (if safe)
   prints a Safe Sequence of processes. It will also optionally let
   you test whether a specific resource request from a process can
   be granted safely.

   sample_output_bankers.txt shows the expected output for the
   classic 5-process / 3-resource-type example (the same example
   used in the exam's sample output image):

       Allocation:                 Maximum:
       P0: 0 1 0                   P0: 7 5 3
       P1: 2 0 0                   P1: 3 2 2
       P2: 3 0 2                   P2: 9 0 2
       P3: 2 1 1                   P3: 2 2 2
       P4: 0 0 2                   P4: 4 3 3

       Available: 3 3 2

IMPLEMENTATION NOTES
---------------------
- FCFS orders processes strictly by arrival time (ties broken by
  process ID) and runs them to completion in that order.
- SJF (non-preemptive) always picks, among the processes that have
  already arrived, the one with the smallest burst time; it does not
  interrupt a process once it starts.
- Round Robin cycles through a ready queue, giving each process at
  most one time-quantum slice per turn; newly-arriving processes are
  appended to the back of the queue before a re-queued process.
- SRTF (preemptive SJF) re-evaluates every time unit and always runs
  whichever arrived, unfinished process currently has the smallest
  remaining burst time, preempting the running process if a shorter
  one arrives.
- Banker's Algorithm computes Need = Maximum - Allocation, then
  repeatedly looks for a process whose Need can be satisfied by the
  currently available resources (Work). If found, its resources are
  simulated as released back into Work and it is added to the Safe
  Sequence; this repeats until either all processes are sequenced
  (Safe State) or no further process can be satisfied (Unsafe State).


