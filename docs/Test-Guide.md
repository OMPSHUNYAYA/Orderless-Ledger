# ⭐ **ORL — Test Guide**

**Orderless Ledger (ORL) v2.0.0**

**Validated Canonical Evidence • Deterministic Structural Resolution • Reproducible Receipts • Bounded Closure**

**Developed within the Shunyaya Framework**

---

`same validated canonical fragment set + same ruleset + same declared boundary context -> same bounded resolution bundle`

This guide defines the recommended verification procedure for the ORL v2.0.0 Python reference kernel and browser Structural Laboratory.

The tests verify the declared reference behavior and committed conformance vectors.

They do not establish production safety, authorization, settlement, universal ledger correctness, or regulatory suitability.

---

## ⚡ **Start Here**

The current reference implementations are:

```text
demo/ORL_Reference_Kernel_v2_0_0.py
demo/ORL_Structural_Lab_v2_0_0.html
```

The recommended release-verification sequence is:

`Python reference run -> Python audit -> Browser reference story -> Browser laboratory flows -> Browser audit -> Cross-engine checks -> Artifact identity`

---

## 🐍 **1. Run the Python Reference Kernel**

From the repository root:

```text
python demo/ORL_Reference_Kernel_v2_0_0.py
```

Expected headline output:

```text
ORL v2.0.0
Validation       : ACCEPTED
Closure          : SEALED
State Summary    : R:2 I:1 A:2
Node Equality    : True
```

The exact reference identities should also be printed for:

- fragment set  
- ruleset  
- projection  
- sealed bundle  

The transaction results should be:

```text
ORL100   RESOLVED   COMPATIBLE_PAIR
ORL200   RESOLVED   COMPATIBLE_PAIR
ORL300   INCOMPLETE MISSING_DEBIT
ORL400   ABSTAIN    AMOUNT_MISMATCH
ORL500   ABSTAIN    MULTIPLE_CREDITS
```

Expected structural projection:

```text
UNIT
  Alice  -500
  Bob    +200
  Dina   +300
```

### **Pass Criteria**

`PASS` when:

- validation is `ACCEPTED`  
- closure is `SEALED` for the frozen reference boundary  
- state summary is `R:2 I:1 A:2`  
- node equality is `True`  
- the five transaction classifications match  
- the structural projection matches  

---

## ✅ **2. Run the Python Full Audit**

From the repository root:

```text
python demo/ORL_Reference_Kernel_v2_0_0.py --audit
```

Expected final result:

```text
TOTAL 272/272 PASS
```

Expected audit groups:

| Audit Group | Expected Result |
|---|---:|
| `VALIDATION` | `20/20 PASS` |
| `CANONICALIZATION` | `8/8 PASS` |
| `EXACT_AMOUNTS` | `5/5 PASS` |
| `RESOLUTION` | `18/18 PASS` |
| `DEDUPLICATION` | `3/3 PASS` |
| `REFERENCE_SCENARIO` | `10/10 PASS` |
| `PERMUTATION_INVARIANCE` | `120/120 PASS` |
| `SET_ALGEBRA` | `3/3 PASS` |
| `EVIDENCE_GROWTH` | `3/3 PASS` |
| `EVIDENCE_GROWTH_EXHAUSTIVE` | `65/65 PASS` |
| `CLOSURE` | `6/6 PASS` |
| `RECEIPTS` | `7/7 PASS` |
| `KNOWN_REGRESSIONS` | `4/4 PASS` |
| **Total** | **`272/272 PASS`** |

A failed check should be treated as a release-blocking implementation or environment issue until explained.

---

## 🌐 **3. Open the Browser Structural Laboratory**

Open locally:

```text
demo/ORL_Structural_Lab_v2_0_0.html
```

No server or internet connection is required after the file is available locally.

The page should open with:

- a thin ORL v2.0.0 header  
- the structural architecture summary  
- a sticky live status area  
- the Three-Node Reference Story  
- frozen cross-engine contract identities  
- Node Views  
- Current Transaction Receipts  
- Resolved-Only Structural Projection  
- Structural Laboratory controls  
- Latest Structural Effect feedback  
- Laboratory Evidence Log  
- Executable ORL Audit  

---

## 🎬 **4. Verify the Three-Node Reference Story**

### **Stage 1 — Local Views**

Click:

**Reset Story**

Confirm:

- the three nodes begin with different evidence subsets  
- local transaction snapshots may differ  
- closure is `OPEN`  
- the interface does not claim node equality while evidence differs  

Expected interpretation:

`different evidence -> equality not required`

---

### **Stage 2 — Same Evidence, Open Closure**

Click:

**Next Stage**

Confirm:

- every node receives the same deduplicated canonical evidence set  
- all nodes show the same fragment-set identity  
- all nodes produce the same open bundle  
- closure remains `OPEN` because no exact boundary has yet been applied  

Expected relation:

`same canonical evidence + same ruleset + same no-boundary context -> same open bundle`

---

### **Stage 3 — Declared Boundary Satisfied**

Click:

**Next Stage**

Confirm:

- the same canonical evidence set remains present  
- an explicit exact boundary is now satisfied  
- closure becomes `SEALED`  
- all nodes produce the same sealed bundle  

Expected relation:

`same canonical evidence + same ruleset + same satisfied boundary -> same sealed bundle`

The correct interpretation is:

`SEALED = declared exact boundary satisfied`

not:

`SEALED = proof that no undisclosed evidence exists anywhere`

---

### **Full Story Check**

Click:

**Reset Story**

Then click:

**Run Full Story**

Confirm the interface deterministically advances through all three stages.

---

## 📊 **5. Verify the Frozen Reference Scenario in the Browser**

At the shared reference state, confirm:

```text
R:2 I:1 A:2
```

Expected transaction results:

| Transaction | State | Reason |
|---|---|---|
| `ORL100` | `RESOLVED` | `COMPATIBLE_PAIR` |
| `ORL200` | `RESOLVED` | `COMPATIBLE_PAIR` |
| `ORL300` | `INCOMPLETE` | `MISSING_DEBIT` |
| `ORL400` | `ABSTAIN` | `AMOUNT_MISMATCH` |
| `ORL500` | `ABSTAIN` | `MULTIPLE_CREDITS` |

Expected projection:

```text
Alice = -500
Bob   = +200
Dina  = +300
```

Confirm that `ORL300`, `ORL400`, and `ORL500` do not contribute to the structural projection.

---

## 🧪 **6. Verify the Structural Laboratory Controls**

Start by clicking:

**Reset Laboratory**

The reference union should be restored with closure `OPEN`.

The Latest Structural Effect panel and Laboratory Evidence Log should explain the result of each action.

---

### **Test 6.1 — Shuffle Evidence**

Click:

**Shuffle Evidence**

Confirm:

- raw input order changes  
- canonical evidence identity remains unchanged  
- ruleset and closure context remain unchanged  
- bounded bundle identity remains unchanged  

Expected invariant:

`same canonical evidence + unchanged ruleset and closure context -> same bundle`

---

### **Test 6.2 — Add Exact Duplicate**

Click:

**Add Exact Duplicate**

Confirm:

- raw input count increases  
- canonical unique fragment count does not increase  
- canonical bundle identity remains unchanged  

Expected invariant:

`D(E union E) = D(E)`

---

### **Test 6.3 — Complete ORL300**

Click:

**Complete ORL300**

Confirm:

`ORL300 -> RESOLVED`

The expected state transition is:

`INCOMPLETE -> RESOLVED`

The current projection should gain the newly resolved ORL300 contribution.

Closure should remain or return `OPEN` unless the new exact set is separately declared as a boundary.

---

### **Test 6.4 — Conflict ORL100**

Reset the laboratory if necessary, then click:

**Conflict ORL100**

Confirm:

`ORL100 -> ABSTAIN`

Expected transition:

`RESOLVED -> ABSTAIN`

Confirm that ORL100's previous structural projection contribution is removed from the recomputed current projection.

This is a structural recomputation over current evidence.

It is not a claim that an executed financial transfer has been reversed.

---

### **Test 6.5 — Add Evidence After Conflict**

After ORL100 is already in `ABSTAIN`, click:

**Add Evidence After Conflict**

Confirm:

`ABSTAIN -> ABSTAIN`

under the current append-only valid-evidence ruleset.

---

### **Test 6.6 — Inject Malformed Fragment**

Reset the laboratory, then click:

**Inject Malformed Fragment**

Confirm:

- validation becomes `REFUSED`  
- the resolver does not silently ignore the unsupported fragment  
- no normal transaction-resolution bundle is produced for the refused batch  
- the interface explains the refusal state  

Expected relation:

`invalid fragment -> REFUSED`

---

### **Test 6.7 — Declare + Seal Current Set**

Reset the laboratory, then click:

**Declare + Seal Current Set**

Confirm:

- validation remains `ACCEPTED`  
- evidence identity remains unchanged  
- closure changes from `OPEN` to `SEALED`  
- the exact current canonical fragment set satisfies the newly declared boundary  

Expected relation:

`OPEN -> SEALED`

with:

`same evidence identity`

---

### **Test 6.8 — Reset Laboratory**

After performing several actions, click:

**Reset Laboratory**

Confirm:

- reference evidence is restored  
- malformed inputs are removed  
- the declared boundary is removed  
- closure returns to `OPEN`  
- controls return to their initial usable state  

---

## 🖱 **7. Verify Browser Interaction Quality**

For every clickable button, confirm:

- hover feedback is visible  
- pressing the button produces a tactile pressed-state depth change  
- keyboard focus remains visibly indicated  
- actions that are no longer meaningful are disabled when appropriate  
- the active working area is visually emphasized  
- the Latest Structural Effect panel updates after laboratory actions  
- the evidence log records the latest action and interpretation  

These checks verify the user-facing interaction layer, not the mathematical resolver alone.

---

## 🧾 **8. Verify Transaction Receipts**

At the reference shared state, confirm that a receipt is shown for each of:

- `ORL100`  
- `ORL200`  
- `ORL300`  
- `ORL400`  
- `ORL500`  

Each displayed receipt should include or bind:

- transaction identifier  
- state  
- reason  
- transaction evidence identity  
- receipt identity  

The automated audit additionally verifies:

- all five reference receipts reconstruct correctly  
- a tampered receipt is rejected  
- open and sealed receipt identities differ  

---

## 🔒 **9. Verify Bounded Closure**

The automated closure group checks six conditions.

Expected:

```text
CLOSURE 6/6 PASS
```

The checks establish that:

- absence of a declared boundary leaves closure `OPEN`  
- an exact declared boundary seals  
- the sealed reason is explicit  
- boundary identity is stable under supported permutation  
- a subset does not seal against a larger boundary  
- a superset does not seal against a smaller boundary  

The closure claim remains bounded to the declared exact evidence set.

---

## 🔀 **10. Verify Order Independence**

The committed audit tests all:

`5! = 120`

permutations of a frozen five-fragment conformance vector.

Expected result:

```text
PERMUTATION_INVARIANCE 120/120 PASS
```

The tested invariant is:

`R(P(E)) = R(E)`

for the same ruleset and unchanged declared boundary context.

When complete bounded bundle identities are compared, the ruleset and boundary context are held fixed.

This is conformance evidence for the declared vector and implementation profile.

It is not a universal proof that every ledger problem is order-independent.

---

## 🔁 **11. Verify Set Algebra**

Expected result:

```text
SET_ALGEBRA 3/3 PASS
```

The committed checks cover:

`D(A union B) = D(B union A)`

`D(E union E) = D(E)`

`D((A union B) union C) = D(A union (B union C))`

---

## 📈 **12. Verify Evidence-Growth Transitions**

Expected direct result:

```text
EVIDENCE_GROWTH 3/3 PASS
```

Expected exhaustive result:

```text
EVIDENCE_GROWTH_EXHAUSTIVE 65/65 PASS
```

The active append-only valid-evidence transition model is:

`INCOMPLETE -> INCOMPLETE | RESOLVED | ABSTAIN`

`RESOLVED -> RESOLVED | ABSTAIN`

`ABSTAIN -> ABSTAIN`

This is a tested property of the current ruleset and committed corpus.

---

## 💰 **13. Verify Exact Amount Handling**

Expected result:

```text
EXACT_AMOUNTS 5/5 PASS
```

The audit verifies:

- a 78-digit amount resolves exactly  
- the 78-digit debit projection is exact  
- the 78-digit credit projection is exact  
- a value above the JavaScript safe-integer boundary resolves exactly  
- its projection remains exact  

Supported amounts are not evaluated with binary floating-point arithmetic.

---

## 🛡 **14. Verify Known Regression Coverage**

Expected result:

```text
KNOWN_REGRESSIONS 4/4 PASS
```

The permanent regression checks confirm:

- unsupported side values cannot be silently ignored  
- multiple debits without a credit produce `ABSTAIN`  
- multiple credits without a debit produce `ABSTAIN`  
- separator-bearing account identifiers remain safe under canonical framing  

---

## 🎮 **15. Verify Browser Interactive-Flow Regression Coverage**

Expected result:

```text
INTERACTIVE_FLOWS 8/8 PASS
```

The group permanently checks:

- shuffle preserves the canonical bundle  
- exact duplicate preserves the canonical bundle  
- completing ORL300 resolves  
- conflicting ORL100 abstains  
- the conflict removes ORL100's previous projection contribution  
- additional valid evidence preserves existing abstention  
- malformed laboratory input is refused  
- declaring the current exact set seals without changing evidence identity  

---

## 🔄 **16. Verify Frozen Python/Browser Cross-Engine Agreement**

Expected result:

```text
CROSS_ENGINE_FROZEN 6/6 PASS
```

The browser checks the Python-frozen values for:

- ruleset ID  
- reference fragment-set ID  
- open bundle ID  
- boundary ID  
- sealed bundle ID  
- projection ID  

This is frozen cross-engine conformance for the committed reference contract.

It is not an independent third-party verifier claim.

---

## 🧑‍💻 **17. Run the Browser Full Audit from the Console**

Open Developer Tools and paste:

```text
await ORL_AUDIT.runAll()
```

Expected final result:

```text
ORL AUDIT TOTAL 286/286 PASS
```

The browser should also print a group summary table with every group marked:

`PASS`

---

## 🔎 **18. Inspect the Most Recent Browser Audit**

After a full audit, run:

```text
ORL_AUDIT.last()
```

To inspect the current reference scenario directly:

```text
ORLCore.referenceScenario(true)
```

The reference scenario should report:

```text
all_nodes_match_after_sharing: true
```

A trailing `undefined` displayed by the developer console after a command with no explicit returned value is not an ORL test failure.

---

## 🧪 **19. Recommended Complete Browser Verification Block**

Paste:

```text
console.clear();

const result = await ORL_AUDIT.runAll();

console.log("FINAL STATUS:", result.status);
console.log("TOTAL:", `${result.passed}/${result.total}`);

console.log("KNOWN REGRESSIONS");
console.table(result.groups.KNOWN_REGRESSIONS.checks);

console.log("INTERACTIVE FLOWS");
console.table(result.groups.INTERACTIVE_FLOWS.checks);

console.log("CROSS-ENGINE FROZEN");
console.table(result.groups.CROSS_ENGINE_FROZEN.checks);

console.log("REFERENCE SCENARIO");
console.log(ORLCore.referenceScenario(true));
```

Expected headline results:

```text
FINAL STATUS: PASS
TOTAL: 286/286
KNOWN_REGRESSIONS: 4/4 PASS
INTERACTIVE_FLOWS: 8/8 PASS
CROSS_ENGINE_FROZEN: 6/6 PASS
```

---

## 🔐 **20. Artifact Identity Check**

After final release files are frozen, use the repository verification material to compare committed files with their recorded SHA-256 values.

On Windows, the standard pattern is:

```text
certutil -hashfile "demo\ORL_Reference_Kernel_v2_0_0.py" SHA256
certutil -hashfile "demo\ORL_Structural_Lab_v2_0_0.html" SHA256
```

Compare the reported values with:

`verify/FREEZE_DEMO_SHA256.txt`

The meaning is:

`same bytes -> same SHA-256 hash`

A matching SHA-256 value confirms that the checked artifact reproduces the recorded release digest.

It does not by itself establish behavioral correctness.

`artifact digest agreement != behavioral proof`

---

## ✅ **21. Current Release Pass Criteria**

The ORL v2.0.0 reference implementation passes the documented release checks when:

- the Python reference kernel executes without exception  
- Python reports `Validation : ACCEPTED`  
- Python reports `Closure : SEALED` for the frozen reference boundary  
- Python reports `R:2 I:1 A:2`  
- Python reports `Node Equality : True`  
- the Python audit reports `272/272 PASS`  
- the browser reference story reaches the expected shared open and sealed states  
- the browser reference scenario matches the expected five transaction results  
- the browser laboratory controls produce the documented effects  
- the browser audit reports `286/286 PASS`  
- known regressions report `4/4 PASS`  
- interactive flows report `8/8 PASS`  
- frozen cross-engine identities report `6/6 PASS`  
- final release artifact hashes match the release hash record  

---

## ⚠️ **22. What These Tests Do Not Establish**

Passing the current ORL tests does not establish:

- universal ledger correctness  
- authorization  
- identity verification  
- signature verification  
- account ownership  
- available funds  
- fraud prevention  
- consensus  
- Byzantine fault tolerance  
- reliable broadcast  
- network finality  
- payment execution  
- account posting  
- settlement  
- immutable financial finality  
- regulatory compliance  
- production readiness  
- universal order independence  

The tests establish the observed behavior of the declared ORL v2.0.0 reference contract and committed vectors.

---

## 🧭 **23. One-Minute Demonstration**

1. Open `demo/ORL_Structural_Lab_v2_0_0.html`.  
2. Click **Run Full Story**.  
3. Observe different local node views becoming the same canonical evidence set.  
4. Observe `OPEN` closure before a boundary is applied.  
5. Observe `SEALED` closure after the exact declared boundary is satisfied.  
6. Reset the laboratory.  
7. Click **Complete ORL300** and observe `INCOMPLETE -> RESOLVED`.  
8. Reset the laboratory.  
9. Click **Conflict ORL100** and observe `RESOLVED -> ABSTAIN` with projection removal.  
10. Run `await ORL_AUDIT.runAll()` and confirm `286/286 PASS`.  

The correct interpretation is:

`same validated canonical fragment set + same ruleset + same declared boundary context -> same bounded resolution bundle`

with bounded closure kept separate from authorization, settlement, and universal finality.

---

## ⭐ **One-Line Summary**

The ORL v2.0.0 test procedure verifies strict supported-input refusal, canonical evidence identity, exact duplicate absorption, deterministic resolution, exact-value projection, reproducible receipts, bounded closure, order-invariance vectors, evidence-growth transitions, interactive browser behavior, and frozen Python/browser agreement while preserving a precise boundary around what the reference implementation does not claim.
