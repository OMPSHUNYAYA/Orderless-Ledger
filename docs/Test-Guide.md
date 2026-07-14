# ⭐ **ORL — Test Guide**

**Orderless Ledger (ORL)**

**Deterministic Structural Reconciliation Reference Model**

**Order-Independent • Clock-Independent Resolution • Explicit Incompleteness • Demonstrated Conflict Abstention**

**Powered by the Shunyaya Framework**

---

## ⚡ **Start Here — Run the Browser Demo**

Open:

```text
demo/orl_demo_v3.html
```

Then click:

**Run Full Demo**

The browser demo runs locally after download.

No internet connection, GPS signal, NTP service, synchronized clock, or server is required to execute the reference demonstration.

---

## 🐍 **Run the Python Reference Demo**

From the repository root, run:

```text
python demo/orl_demo_reference.py
```

The Python program prints:

- each node's initial local view  
- transaction classifications before sharing  
- the bounded-sharing phase  
- transaction classifications after sharing  
- the final balance projection  
- the final state summary  
- the node-equality check  

The expected final state summary for the supplied scenario is:

```text
R:2 I:1 A:2
```

Equivalent Python output may appear as:

```text
{'ABSTAIN': 2, 'INCOMPLETE': 1, 'RESOLVED': 2}
```

---

## 👀 **What the Demonstrations Show**

The supplied Python and browser demonstrations exhibit the following behavior for the declared examples:

- three nodes begin with different local fragment collections  
- the resolver does not read timestamps or wall-clock values  
- the resolver does not consult fragment arrival position when classifying the supported example transactions  
- exact duplicate entries are absorbed  
- missing demonstrated structure remains `INCOMPLETE`  
- demonstrated amount mismatch or same-transaction multiplicity conflict produces `ABSTAIN`  
- only `RESOLVED` transactions affect the demonstrated balance projection  
- after each node receives the same merged fragment set, every node produces the same demonstrated resolver output  

The governing relation is:

`same deduplicated supported fragment set + same resolver rules -> same bounded resolution`

---

## 🧭 **What the Demonstrations Do Not Show**

The current demonstrations do not implement or prove:

- universal ledger correctness  
- immutable transaction finality  
- complete malformed-input validation  
- authorization  
- account ownership  
- available-funds verification  
- cryptographic signatures  
- fraud detection  
- consensus  
- Byzantine fault tolerance  
- reliable broadcast  
- payment execution  
- account posting  
- settlement  
- regulatory compliance  
- production readiness  
- general double-spend prevention  

The demos are bounded structural-reconciliation examples.

---

## 🎮 **Browser Controls**

### **Next Step**

Moves the demonstration forward by one declared stage.

Use it to observe:

- the current node view  
- the current sharing stage  
- changes in transaction visibility  
- changes in the demonstrated state summary  

---

### **Run Full Demo**

Runs the declared demonstration sequence automatically.

Use it for:

- a quick overview  
- presentations  
- observing the complete local-to-shared transition  

---

### **Reset**

Returns the browser demonstration to its initial local views.

After reset:

- each node again holds its original local fragments  
- the nodes do not yet possess the same evidence set  
- the local resolver snapshots may differ  

---

### **Jump to Sharing**

Moves directly to the final `All Nodes Complete Bounded Sharing` stage.

This is a display and test control.

It does not represent a network, consensus, or reliable-broadcast protocol.

---

## 🔬 **Demonstration Stages**

### **1. Local Views**

Each node begins with a different subset of the declared fragments.

At this stage:

- nodes have different evidence  
- local transaction states may differ  
- some transactions are missing counterparts  
- some conflicts are not yet jointly visible  
- node outputs are not expected to match  

This is not a failure of convergence.

The nodes do not yet hold the same evidence set.

---

### **2. Bounded Sharing**

The demonstration distributes the declared fragment union to the nodes.

The sharing process:

- makes additional fragments visible  
- preserves exact duplicate absorption  
- does not use timestamps as classification authority  
- does not use fragment arrival position as classification authority  
- does not ask a coordinator to decide the transaction state  

The sharing code is part of the test harness.

It is not a distributed-network protocol.

---

### **3. Shared Resolver Snapshot**

After every node receives the same demonstrated fragment collection:

- matching supported debit and credit fragments resolve  
- the demonstrated missing counterpart remains `INCOMPLETE`  
- the demonstrated conflicts produce `ABSTAIN`  
- every node produces the same transaction-state map  
- every node produces the same demonstrated balance projection  

The relevant condition is:

`D(E_i) = D(E_j) -> R_v(E_i) = R_v(E_j)`

Where:

- `D(E)` is exact-duplicate absorption  
- `R_v` is the current resolver under ruleset version `v`  
- `E_i` and `E_j` are the fragment collections held by two nodes  

---

## ⚖️ **Current Transaction States**

### **RESOLVED**

For the supplied examples, `RESOLVED` means:

- one declared debit is present  
- one declared credit is present  
- the declared amounts match  

Demonstrated relation:

`one debit + one credit + matching amount -> RESOLVED`

Only `RESOLVED` transactions affect the demonstrated balance projection.

`RESOLVED` does not mean:

- authorized  
- funded  
- settled  
- immutable  
- legally final  
- globally complete  

---

### **INCOMPLETE**

For the supplied examples, `INCOMPLETE` means that a required demonstrated counterpart is missing.

Demonstrated relation:

`missing counterpart -> INCOMPLETE`

The resolver does not invent the missing fragment.

---

### **ABSTAIN**

For the conflict forms included in the current demonstrations:

`debit_credit_mismatch OR demonstrated_same_transaction_multiplicity_conflict -> ABSTAIN`

`ABSTAIN` means that the resolver does not apply a demonstrated balance effect for that transaction.

Other malformed, unsupported, or untested conflict forms remain outside the current conformance claim.

---

## 🔍 **Declared Transactions**

### **ORL100**

Initial distribution:

- debit fragment appears at one node  
- matching credit fragment appears at another node  

After sharing:

`ORL100 -> RESOLVED`

Purpose:

- demonstrates a matching pair becoming jointly visible  
- demonstrates same-evidence resolution after different starting views  

---

### **ORL200**

Initial distribution:

- debit and credit fragments begin at different nodes  

After sharing:

`ORL200 -> RESOLVED`

Purpose:

- demonstrates a second matching transaction with a different starting distribution  

---

### **ORL300**

Initial distribution:

- only one counterpart is present in the supplied evidence  

After sharing:

`ORL300 -> INCOMPLETE`

Purpose:

- demonstrates that missing structure is not guessed into completion  

---

### **ORL400**

Declared structure:

- debit amount and credit amount differ  

After sharing:

`ORL400 -> ABSTAIN`

Purpose:

- demonstrates explicit abstention for an amount mismatch  

---

### **ORL500**

Declared structure:

- one debit declaration  
- two incompatible credit declarations under the same transaction identifier  

After sharing:

`ORL500 -> ABSTAIN`

Purpose:

- demonstrates explicit abstention for the supplied same-transaction multiplicity conflict  

`ORL500` is not a complete demonstration of general double-spend prevention.

---

## 📊 **Expected Final Result**

The supplied scenario should end with:

```text
R:2 I:1 A:2
```

Meaning:

- 2 `RESOLVED`  
- 1 `INCOMPLETE`  
- 2 `ABSTAIN`  

Expected transaction classifications:

| Transaction | Expected State | Demonstrated Reason |
|---|---|---|
| `ORL100` | `RESOLVED` | Matching debit and credit |
| `ORL200` | `RESOLVED` | Matching debit and credit |
| `ORL300` | `INCOMPLETE` | Missing counterpart |
| `ORL400` | `ABSTAIN` | Debit-credit amount mismatch |
| `ORL500` | `ABSTAIN` | Same-transaction multiple-credit conflict |

---

## 💰 **Expected Demonstrated Balance Projection**

The two resolved transactions are:

```text
ORL100 = debit(Alice,500) + credit(Bob,500)
ORL200 = debit(Bob,300) + credit(Dina,300)
```

Expected balance projection:

```text
Alice = -500
Bob   = +200
Dina  = +300
```

Transactions `ORL300`, `ORL400`, and `ORL500` must not affect the demonstrated balance projection.

Expected invariant:

`INCOMPLETE OR ABSTAIN -> no demonstrated balance effect`

---

## 🔁 **Repeatability Check**

Run the same supplied demonstration multiple times.

For an unchanged demo file and unchanged runtime behavior, observe:

- the same final transaction classifications  
- the same final balance projection  
- the same final state summary  
- the same equality result after sharing  

Expected result:

`same supplied input + same resolver -> same supplied output`

This is a repeatability check for the declared scenario.

It is not a universal conformance proof.

---

## 🔀 **Order-Independence Check**

The current resolver logic groups fragments by transaction identifier and does not consult their arrival position when classifying the supported example transactions.

The intended invariant is:

`R_v(P(E)) = R_v(E)`

Where `P(E)` is a permutation of the same supported fragment collection.

The current repository demonstrates this design property through the supplied resolver structure and examples.

A stronger release should add an automated permutation corpus that asserts this invariant across many declared vectors.

---

## 📋 **Manual Browser Test Procedure**

### **Test 1 — Initial State**

1. Open `demo/orl_demo_v3.html`.
2. Click **Reset**.
3. Confirm that the nodes show different local fragment views.
4. Confirm that the node outputs are not yet required to match.
5. Confirm that the stage display describes local visibility.

Expected result:

`PASS` if the nodes begin differently, the active stage is `Local Views Only`, and the node outputs are not yet shown as aligned. General explanatory text may still describe the later shared stage.

---

### **Test 2 — Step Progression**

1. Click **Next Step**.
2. Observe the active stage.
3. Continue clicking **Next Step**.
4. Confirm that fragments become visible according to the declared demonstration sequence.
5. Confirm that transaction states update as the visible evidence changes.

Expected result:

`PASS` if the stage progression is deterministic and the display updates consistently.

---

### **Test 3 — Full Run**

1. Click **Reset**.
2. Click **Run Full Demo**.
3. Wait for the declared sequence to complete.
4. Confirm the final state summary is `R:2 I:1 A:2`.
5. Confirm every node displays the same final demonstrated snapshot.

Expected result:

`PASS` if all nodes match after receiving the same merged fragment set.

---

### **Test 4 — Incomplete State**

1. Locate `ORL300`.
2. Confirm that its missing counterpart never appears.
3. Confirm that its final state is `INCOMPLETE`.
4. Confirm that it does not affect the demonstrated balance projection.

Expected result:

`PASS` if `ORL300` remains unresolved without a balance effect.

---

### **Test 5 — Amount Mismatch**

1. Locate `ORL400`.
2. Confirm that the debit and credit amounts differ.
3. Confirm that its final state is `ABSTAIN`.
4. Confirm that it does not affect the demonstrated balance projection.

Expected result:

`PASS` if the amount mismatch remains explicit and non-posting.

---

### **Test 6 — Multiplicity Conflict**

1. Locate `ORL500`.
2. Confirm that one debit and two incompatible credits are present.
3. Confirm that its final state is `ABSTAIN`.
4. Confirm that it does not affect the demonstrated balance projection.

Expected result:

`PASS` if the supplied multiplicity conflict remains explicit and non-posting.

---

### **Test 7 — Reset Repeatability**

1. Complete a full run.
2. Click **Reset**.
3. Run the demonstration again.
4. Compare the final state summary and balance projection.

Expected result:

`PASS` if the same supplied scenario produces the same final output.

---

## 🐍 **Manual Python Test Procedure**

### **Test 1 — Program Execution**

Run:

```text
python demo/orl_demo_reference.py
```

Expected result:

- the program completes without an exception for the supplied scenario  
- the initial node snapshots are printed  
- the sharing phase is printed  
- the final shared snapshot is printed  

---

### **Test 2 — Final Equality**

Locate:

```text
all_nodes_match_after_sharing = True
```

Expected result:

`PASS` if the value is `True`.

This confirms equality after every node receives the same merged fragment set.

---

### **Test 3 — Final State Summary**

Locate the printed state summary.

Expected result:

```text
ABSTAIN = 2
INCOMPLETE = 1
RESOLVED = 2
```

The dictionary key order may depend on the print representation, but the counts must match.

---

### **Test 4 — Final Balances**

Confirm:

```text
Alice = -500
Bob   = +200
Dina  = +300
```

Expected result:

`PASS` if no other transaction contributes to the balance projection.

---

## 🔐 **Artifact Identity Check**

The repository includes:

```text
verify/FREEZE_DEMO_SHA256.txt
```

Use the instructions in:

```text
verify/VERIFY.txt
```

to compare the committed demo files with the recorded SHA-256 values.

The meaning of this check is:

`same bytes -> same hash`

A successful hash comparison establishes artifact identity.

It does not by itself establish:

- behavioral correctness  
- complete conformance  
- cross-engine equality  
- production safety  
- universal order independence  

---

## ✅ **Current Pass Criteria**

The current supplied demonstration passes its documented scenario when:

- the browser demo opens locally  
- the Python demo executes successfully  
- the final state summary is `R:2 I:1 A:2`  
- `ORL100` and `ORL200` are `RESOLVED`  
- `ORL300` is `INCOMPLETE`  
- `ORL400` and `ORL500` are `ABSTAIN`  
- only resolved transactions affect the demonstrated balances  
- all nodes match after receiving the same merged fragment set  
- repeated runs of the unchanged supplied scenario produce the same output  

---

## ⚠️ **Current Non-Conformance Boundary**

The present test guide does not certify behavior for:

- malformed transaction identifiers  
- unsupported side values  
- non-integer amounts  
- negative or zero amounts  
- oversized amounts  
- self-transfers  
- adversarial delimiter content  
- cross-language numeric limits  
- every possible conflict shape  
- every possible fragment permutation  
- undisclosed external evidence  

These conditions require later resolver hardening and expanded conformance tests.

---

## 🧪 **Planned Stronger Verification Direction**

A future technical revision should add:

- a formal supported-input schema  
- explicit invalid-input refusal  
- assertion-based expected outputs  
- a deterministic permutation corpus  
- malformed-input vectors  
- adversarial conflict vectors  
- canonical serialization  
- exact cross-language amount representation  
- Python and browser conformance tests  
- versioned resolver receipts  
- independent reconstruction  

The future target relation is:

`same validated canonical structure + same ruleset version -> same independently verified output`

This stronger verification layer is not part of the current public demos.

---

## ⚡ **Suggested One-Minute Demonstration**

1. Open `demo/orl_demo_v3.html`.
2. Click **Reset**.
3. Observe the three different local views.
4. Click **Run Full Demo**.
5. Observe fragments becoming jointly visible.
6. Confirm `ORL100` and `ORL200` resolve.
7. Confirm `ORL300` remains incomplete.
8. Confirm `ORL400` and `ORL500` abstain.
9. Confirm the final summary is `R:2 I:1 A:2`.
10. Confirm every node shows the same final demonstrated snapshot.

The correct interpretation is:

`same deduplicated supported evidence + same resolver rules -> same bounded resolution`

---

## ⭐ **One-Line Summary**

The ORL reference demos show that independent nodes can begin with different supported transaction fragments and, after receiving the same deduplicated fragment set, produce the same bounded resolver output without using timestamps, fragment arrival order, GPS, NTP, or coordinator state as the classification authority — while preserving explicit `INCOMPLETE` and demonstrated `ABSTAIN` outcomes.
