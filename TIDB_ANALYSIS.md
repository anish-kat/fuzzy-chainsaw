# TiDB System Design Analysis

## 🏗 High-Level Architecture
TiDB is a distributed SQL database that separates **Compute** from **Storage**. This allows both layers to scale independently.



### Core Components:
1. **TiDB Server (Stateless)**: The SQL layer. It handles client connections, parses SQL, and generates execution plans.
2. **PD (Placement Driver)**: The "Brain." It manages metadata, handles timestamps for distributed transactions (TSO), and balances data across nodes.
3. **TiKV (Storage)**: A distributed transactional Key-Value store. It uses the **Raft** consensus algorithm to ensure data consistency across replicas.

---

## 🛠 Key Distributed Concepts in TiDB
* **Raft Consensus**: Ensures that if one node fails, the data remains available and consistent.
* **MVCC (Multi-Version Concurrency Control)**: Allows for "snapshot isolation" so reads don't block writes.
* **Percolator Model**: The protocol used to handle 2-phase commits (2PC) across multiple machines.

---

## 📈 My Contribution Log
| Date | Issue | Component | Impact |
| :--- | :--- | :--- | :--- |
| 2026-01-23 | Setup & Architecture Deep Dive | All | Initialized environment and analyzed TiDB-X architecture. |
| [TBD] | [Your First Issue Link] | [Go/Rust] | [Description of the fix/feature] |

---

## 📝 Learning Journal
* **Challenge**: Understanding how TiDB translates SQL into Key-Value pairs.
* **Insight**: TiDB maps table rows to KV pairs using `TableID`, `RowID`, and `ColumnID` to ensure unique keys in the global TiKV space.
