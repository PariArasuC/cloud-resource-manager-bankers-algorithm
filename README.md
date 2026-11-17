# Cloud Server Resource Manager – Banker's Resource Request Algorithm

An Operating Systems mini project that simulates a cloud server allocating
CPU, RAM and Storage to virtual machines (VMs) using the **Banker's Algorithm**
to avoid deadlock.

## Features
- Safety algorithm (finds a safe sequence)
- Resource-request algorithm (grants a request only if the system stays safe)
- Release resources
- Menu-driven console interface

## How it works
1. Check request <= Need
2. Check request <= Available
3. Pretend to allocate the resources
4. Run the safety algorithm – keep the allocation if safe, otherwise roll back

## Run
```
python banker.py
```
Requires Python 3.8+ (no external libraries).

## Sample test cases
| Request | Result |
|---|---|
| VM1 asks `1 0 2` | Granted (safe) |
| VM4 asks `3 3 0` | Denied (not enough resources) |
| VM0 asks `0 2 0` | Denied (unsafe state) |

## Author
Pari Arasu C – [GitHub](https://github.com/PariArasuC)
