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

- **Status:** In Progress / PR Opened
- **Technical Challenge:** TiDB's vector-based execution engine requires functions to handle "Chunks" of data rather than row-by-row.
- **Files Modified:** - `pkg/expression/builtin_math.go` (Logic)
  - `pkg/expression/builtin_math_test.go` (Unit Tests)
### Phase 2: Code Exploration
- Identified bottleneck: MySQL 9.6 client compatibility (Resolved via Go-native client).
- Researching: Vectorized expression evaluation in /pkg/expression.
## ✅ Milestone: System Connection
- Resolved MySQL 9.6 incompatibility by pinning mysql@8.0 client.
- Successfully connected to local TiDB server on port 4000.
- Verified cluster status using 'SHOW TABLE REGIONS'.
### Phase 3: Technical Analysis
- Component: pkg/expression
- Goal: Implement vectorized execution for a Math/Statistical function.
- Method: Identifying missing 'vecEval' methods in Sig structs.
## 🚀 Feature Implementation: Vectorized SQRT
- **Target:** builtinSqrtSig in pkg/expression/builtin_math.go
- **Improvement:** Implemented vecEvalReal to enable batch processing of square root calculations.
- **Key Learning:** Learned how TiDB uses Chunk and Column structures to minimize memory allocation during query execution.
### Phase 4: Testing & Debugging
- **Issue:** Encountered 'undefined' errors when running tests on single files.
- **Solution:** Shifted to package-level testing to resolve internal dependencies.
- **Command:** `go test -v ./pkg/expression -run TestSqrt`
### Phase 5: Adapting to Modern API
- **Discovery:** TiDB moved vectorized logic to `builtin_math_vec.go` to separate execution paths.
- **Refactor:** Updated code to match the latest `chunk.Column` API (Float64s vs Reals).
- **Debug:** Resolved method redeclaration by modifying the existing vec-file instead of the scalar-file.
