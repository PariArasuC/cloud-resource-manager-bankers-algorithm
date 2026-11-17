"""
Cloud Server Resource Manager
Banker's Resource Request Algorithm (Deadlock Avoidance)

Clients = virtual machines / tenants asking the cloud server for resources.
Resources = CPU cores, RAM (GB), Storage (GB).
A request is granted ONLY if the system stays in a safe state afterwards.
"""

RESOURCES = ["CPU", "RAM", "Storage"]


class CloudResourceManager:
    def __init__(self, available, maximum, allocation):
        self.available = available[:]          # free resources on the server
        self.maximum = maximum                 # max demand of each client
        self.allocation = allocation           # currently held by each client
        self.n = len(maximum)                  # number of clients
        self.m = len(available)                # number of resource types
        self.need = [[maximum[i][j] - allocation[i][j] for j in range(self.m)]
                     for i in range(self.n)]

    # ---------- Safety Algorithm ----------
    def is_safe(self):
        work = self.available[:]
        finish = [False] * self.n
        sequence = []

        while len(sequence) < self.n:
            found = False
            for i in range(self.n):
                if not finish[i] and all(self.need[i][j] <= work[j] for j in range(self.m)):
                    # Client i can finish and release everything it holds
                    for j in range(self.m):
                        work[j] += self.allocation[i][j]
                    finish[i] = True
                    sequence.append(i)
                    found = True
            if not found:
                return False, []
        return True, sequence

    # ---------- Resource Request Algorithm ----------
    def request_resources(self, pid, request):
        # Step 1: request must not exceed declared need
        if any(request[j] > self.need[pid][j] for j in range(self.m)):
            return False, "DENIED: request exceeds the client's maximum claim."

        # Step 2: request must not exceed what is available
        if any(request[j] > self.available[j] for j in range(self.m)):
            return False, "DENIED: not enough free resources (client must wait)."

        # Step 3: pretend to allocate
        for j in range(self.m):
            self.available[j] -= request[j]
            self.allocation[pid][j] += request[j]
            self.need[pid][j] -= request[j]

        safe, seq = self.is_safe()

        # Step 4: keep it if safe, otherwise roll back
        if safe:
            order = " -> ".join(f"VM{i}" for i in seq)
            return True, f"GRANTED: system stays safe. Safe sequence: {order}"

        for j in range(self.m):
            self.available[j] += request[j]
            self.allocation[pid][j] -= request[j]
            self.need[pid][j] += request[j]
        return False, "DENIED: granting this would lead to an UNSAFE state (possible deadlock)."

    # ---------- Release ----------
    def release_resources(self, pid, release):
        if any(release[j] > self.allocation[pid][j] for j in range(self.m)):
            return False, "ERROR: client cannot release more than it holds."
        for j in range(self.m):
            self.available[j] += release[j]
            self.allocation[pid][j] -= release[j]
            self.need[pid][j] += release[j]
        return True, "Resources released back to the server."

    # ---------- Display ----------
    def show_state(self):
        header = " ".join(f"{r:>7}" for r in RESOURCES)
        print("\n{:<6}| {:<24}| {:<24}| {}".format("Client", "Allocation", "Max", "Need"))
        print(f"{'':<6}| {header:<24}| {header:<24}| {header}")
        print("-" * 90)
        for i in range(self.n):
            a = " ".join(f"{x:>7}" for x in self.allocation[i])
            mx = " ".join(f"{x:>7}" for x in self.maximum[i])
            nd = " ".join(f"{x:>7}" for x in self.need[i])
            print(f"VM{i:<4}| {a:<24}| {mx:<24}| {nd}")
        free = ", ".join(f"{RESOURCES[j]}={self.available[j]}" for j in range(self.m))
        print(f"\nAvailable on server: {free}\n")


def read_vector(prompt):
    values = input(prompt).split()
    return [int(v) for v in values]


def main():
    # Sample data: 5 VMs, resources = [CPU, RAM, Storage]
    available = [3, 3, 2]
    maximum = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]

    manager = CloudResourceManager(available, maximum, allocation)

    print("=== Cloud Server Resource Manager (Banker's Algorithm) ===")
    manager.show_state()
    safe, seq = manager.is_safe()
    if safe:
        print("Initial state is SAFE. Safe sequence:", " -> ".join(f"VM{i}" for i in seq))
    else:
        print("Initial state is UNSAFE!")

    while True:
        print("\n1. Show state")
        print("2. Check safety")
        print("3. Request resources")
        print("4. Release resources")
        print("5. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            manager.show_state()
        elif choice == "2":
            safe, seq = manager.is_safe()
            print("SAFE:" if safe else "UNSAFE", " -> ".join(f"VM{i}" for i in seq))
        elif choice == "3":
            pid = int(input(f"Client number (0-{manager.n - 1}): "))
            req = read_vector(f"Request ({' '.join(RESOURCES)}), e.g. 1 0 2: ")
            ok, msg = manager.request_resources(pid, req)
            print(msg)
        elif choice == "4":
            pid = int(input(f"Client number (0-{manager.n - 1}): "))
            rel = read_vector(f"Release ({' '.join(RESOURCES)}), e.g. 0 1 0: ")
            ok, msg = manager.release_resources(pid, rel)
            print(msg)
        elif choice == "5":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
