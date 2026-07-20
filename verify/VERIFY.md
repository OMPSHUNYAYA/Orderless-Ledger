# ✅ **ORL — Verification Guide**

## **Orderless Ledger v2.0.0**

### **Verify Behavior • Verify Cross-Engine Identity • Verify Artifact Identity • Review Claim Boundaries**

`validation -> canonical evidence -> deterministic resolution -> projection -> bounded closure evaluation -> receipts -> bundle`

---

## **1. Purpose**

This guide defines the recommended verification procedure for ORL v2.0.0.

The current reference implementation contains:

- a Python reference kernel
- a browser Structural Laboratory
- deterministic canonical identities
- transaction resolution receipts
- bounded closure
- built-in Python and browser audits
- frozen cross-engine reference identities
- SHA-256 artifact-identity checks

The verification layers are intentionally separate.

`behavioral audit != artifact hash`

`cross-engine identity != production safety`

`receipt verification != external source authenticity`

`SEALED != universal completeness`

A successful verification supports only the conclusions explicitly described in this guide.

---

## **2. Reference Files**

From the repository root, the current demo files are:

```text
demo/ORL_Reference_Kernel_v2_0_0.py
demo/ORL_Structural_Lab_v2_0_0.html
```

The artifact freeze file is:

```text
verify/FREEZE_DEMO_SHA256.txt
```

---

# **3. Run the Python Full Audit**

From the repository root:

```text
python demo/ORL_Reference_Kernel_v2_0_0.py --audit
```

Expected result:

```text
ORL AUDIT ORL-AUDIT-1-D01
VALIDATION                     20/20 PASS
CANONICALIZATION               8/8 PASS
EXACT_AMOUNTS                  5/5 PASS
RESOLUTION                     18/18 PASS
DEDUPLICATION                  3/3 PASS
REFERENCE_SCENARIO             10/10 PASS
PERMUTATION_INVARIANCE         120/120 PASS
SET_ALGEBRA                    3/3 PASS
EVIDENCE_GROWTH                3/3 PASS
EVIDENCE_GROWTH_EXHAUSTIVE     65/65 PASS
CLOSURE                        6/6 PASS
RECEIPTS                       7/7 PASS
KNOWN_REGRESSIONS              4/4 PASS
TOTAL 272/272 PASS
```

The Python audit passes only when every committed check in the current audit profile passes.

---

## **4. Run the Python Reference Scenario**

Run:

```text
python demo/ORL_Reference_Kernel_v2_0_0.py
```

Confirm:

```text
Validation       : ACCEPTED
Closure          : SEALED
State Summary    : R:2 I:1 A:2
Node Equality    : True
```

Confirm the final transaction states:

```text
ORL100 = RESOLVED   / COMPATIBLE_PAIR
ORL200 = RESOLVED   / COMPATIBLE_PAIR
ORL300 = INCOMPLETE / MISSING_DEBIT
ORL400 = ABSTAIN    / AMOUNT_MISMATCH
ORL500 = ABSTAIN    / MULTIPLE_CREDITS
```

Confirm the resolved-only structural projection:

```text
UNIT
  Alice = -500
  Bob   = +200
  Dina  = +300
```

Confirm that `ORL300`, `ORL400`, and `ORL500` do not contribute to the projection.

---

## **5. Confirm the Python Reference Identities**

The normal Python execution should reproduce:

```text
Fragment Set ID
7a37a07d4a83a0235199b2846da6a68d045d7dde458520fdf91c9504943b6a6f

Ruleset ID
389eb1062a4cf7668450c475fd84c7611c3ab6c7c402f9e34ac37698fea09909

Projection ID
9c714030a7a333a4018fc610a6e086e3b64a106a2cbc957b6b58a8253653c3ff

Sealed Bundle ID
857564e4e9f24a77ef1a9550e385d203c5e41e55b8fae624f37b82ee684c39f5
```

These are deterministic identities for the current frozen reference contract.

---

# **6. Run the Browser Full Audit**

Open:

```text
demo/ORL_Structural_Lab_v2_0_0.html
```

Open the browser developer console and run:

```text
await ORL_AUDIT.runAll()
```

Expected final result:

```text
ORL AUDIT TOTAL 286/286 PASS
```

Expected audit-group summary:

```text
VALIDATION                     20/20 PASS
CANONICALIZATION               8/8 PASS
EXACT_AMOUNTS                  5/5 PASS
RESOLUTION                     18/18 PASS
DEDUPLICATION                  3/3 PASS
REFERENCE_SCENARIO             10/10 PASS
PERMUTATION_INVARIANCE         120/120 PASS
SET_ALGEBRA                    3/3 PASS
EVIDENCE_GROWTH                3/3 PASS
EVIDENCE_GROWTH_EXHAUSTIVE     65/65 PASS
CLOSURE                        6/6 PASS
RECEIPTS                       7/7 PASS
KNOWN_REGRESSIONS              4/4 PASS
INTERACTIVE_FLOWS              8/8 PASS
CROSS_ENGINE_FROZEN            6/6 PASS
```

Useful inspection commands:

```text
ORL_AUDIT.last()
ORLCore.referenceScenario(true)
```

---

## **7. Verify the Frozen Cross-Engine Contract**

The browser audit must report:

```text
CROSS_ENGINE_FROZEN 6/6 PASS
```

The six frozen values are:

```text
Ruleset ID
389eb1062a4cf7668450c475fd84c7611c3ab6c7c402f9e34ac37698fea09909

Reference Fragment Set ID
7a37a07d4a83a0235199b2846da6a68d045d7dde458520fdf91c9504943b6a6f

Open Bundle ID
046d1de963dcb4b4ab05aeb4e7e81afaca56b9a8fceb6bb50f22d8c087c2d973

Boundary ID
ba855c228a92ea9414bc3b4ad354aba92f92e62c767b9f2535a0db3d2188806b

Sealed Bundle ID
857564e4e9f24a77ef1a9550e385d203c5e41e55b8fae624f37b82ee684c39f5

Projection ID
9c714030a7a333a4018fc610a6e086e3b64a106a2cbc957b6b58a8253653c3ff
```

The Python and browser implementations compute these values independently from the same declared canonical contract.

A `6/6 PASS` result establishes agreement for these committed frozen reference values.

It does not establish agreement for every conceivable implementation or unsupported input.

---

# **8. Verify the Reference Scenario in the Browser**

In the Structural Laboratory, use the three-node reference story.

### **Stage 1 — Local Views**

Confirm:

- the three nodes begin with different valid fragment subsets
- local evidence identities differ
- local outputs are not required to match

### **Stage 2 — Same Evidence, Open Closure**

Advance to the shared stage.

Confirm:

- every node holds the same canonical fragment set
- every node reproduces the same open bundle
- closure remains `OPEN`

### **Stage 3 — Declared Boundary Satisfied**

Advance to the final stage.

Confirm:

- the exact shared canonical fragment set matches the declared boundary
- closure becomes `SEALED`
- every node reproduces the same sealed bundle

Correct interpretation:

`same validated canonical fragment set + same ruleset + same declared boundary context -> same bounded resolution bundle`

The `SEALED` state is bounded to the declared evidence boundary.

It does not assert that no undisclosed evidence exists elsewhere.

---

# **9. Verify the Interactive Structural Flows**

The browser audit includes:

```text
INTERACTIVE_FLOWS 8/8 PASS
```

The committed interactive behaviors are:

### **Shuffle Evidence**

Expected:

`same canonical evidence + unchanged ruleset and closure context -> same bundle`

when only input order changes.

### **Add Exact Duplicate**

Expected:

`canonical bundle unchanged`

when an exact canonical duplicate is added.

### **Complete ORL300**

Expected:

`INCOMPLETE -> RESOLVED`

### **Conflict ORL100**

Expected:

`RESOLVED -> ABSTAIN`

### **Projection Retraction Under Conflict**

Expected:

the earlier ORL100 resolved contribution is absent from the new current structural projection.

### **Add Evidence After Conflict**

Expected under the current append-only model:

`ABSTAIN -> ABSTAIN`

### **Inject Malformed Fragment**

Expected:

`validation_state = REFUSED`

The unsupported fragment must not be silently ignored.

### **Declare Current Set as Boundary**

Expected:

`OPEN -> SEALED`

without changing the canonical evidence identity.

---

# **10. Verify Validation and Exact Amount Handling**

The current audits verify:

```text
VALIDATION 20/20 PASS
EXACT_AMOUNTS 5/5 PASS
```

The tested validation behavior includes refusal of:

- non-array batches
- non-object fragments
- missing required fields
- unknown fields
- unsupported schema values
- unsupported side values
- non-string amounts
- zero amounts
- negative amounts
- decimal amounts
- leading-zero amounts
- amounts longer than 78 digits
- empty transaction identifiers
- empty account identifiers
- edge whitespace
- control characters
- lowercase unit identifiers
- invalid unit separators

The exact-amount tests include:

- a 78-digit amount
- values above the JavaScript safe-integer range
- exact debit projection
- exact credit projection

---

# **11. Verify Permutation Invariance**

Both implementations report:

```text
PERMUTATION_INVARIANCE 120/120 PASS
```

The bounded invariant is:

`R(P(E)) = R(E)`

for the committed permutation corpus under the same ruleset and unchanged declared boundary context.

When complete bounded bundle identities are compared, the ruleset and boundary context are held fixed.

The committed checks operate under the current:

- fragment schema
- canonicalization profile
- duplicate policy
- resolver profile
- projection policy
- receipt construction
- boundary context

This is not a claim of universal order independence for every ledger operation.

---

# **12. Verify Set Algebra**

Both implementations report:

```text
SET_ALGEBRA 3/3 PASS
```

The tested identities are:

`D(A union B) = D(B union A)`

`D(E union E) = D(E)`

`D((A union B) union C) = D(A union (B union C))`

These properties apply to the declared canonical duplicate-absorption and bounded-union model.

---

# **13. Verify Evidence-Growth Constraints**

Both implementations report:

```text
EVIDENCE_GROWTH 3/3 PASS
EVIDENCE_GROWTH_EXHAUSTIVE 65/65 PASS
```

Under append-only valid evidence and the current ruleset, the tested state relation is:

`INCOMPLETE -> INCOMPLETE | RESOLVED | ABSTAIN`

`RESOLVED -> RESOLVED | ABSTAIN`

`ABSTAIN -> ABSTAIN`

These constraints do not describe:

- evidence deletion
- revocation
- supersession
- remediation
- ruleset migration

Those require separately defined semantics.

---

# **14. Verify Receipts**

Both implementations report:

```text
RECEIPTS 7/7 PASS
```

The current receipt checks confirm:

- each reference transaction receipt reconstructs correctly
- a tampered receipt is rejected
- open and sealed receipt identities differ

A valid ORL receipt demonstrates consistency with the current declared receipt construction.

It does not prove:

- external source authenticity
- authorization
- available funds
- fraud absence
- legal validity
- settlement
- global evidence completeness

---

# **15. Verify Artifact Identity**

Current ORL v2.0.0 demo SHA-256 values:

```text
ORL_Reference_Kernel_v2_0_0.py
c9fe03c56631d5751669c8635227f1e737e1c419add1bdc40138860210daf4c1

ORL_Structural_Lab_v2_0_0.html
1f8918e8214385f63288003c4842cf600e7e95e1fa8431afe237768b57f406e1
```

From the repository root on Windows:

```text
certutil -hashfile demo\ORL_Reference_Kernel_v2_0_0.py SHA256
certutil -hashfile demo\ORL_Structural_Lab_v2_0_0.html SHA256
```

Compare the reported values with:

```text
verify\FREEZE_DEMO_SHA256.txt
```

Both values must match exactly.

The deterministic relation is:

`same bytes -> same SHA-256 hash`

A matching SHA-256 value confirms that the checked artifact reproduces the recorded release digest.

It does not by itself establish behavioral correctness.

`artifact digest agreement != behavioral proof`

---

# **16. Current Verification Pass Criteria**

The current ORL v2.0.0 verification passes when all of the following are true:

- Python full audit reports `272/272 PASS`
- Python reference execution reports `Validation = ACCEPTED`
- Python reference execution reports `Closure = SEALED`
- Python reference execution reports `R:2 I:1 A:2`
- Python reference execution reports `Node Equality = True`
- reference transaction states and reason codes match the documented values
- resolved-only projection is `Alice = -500`, `Bob = +200`, `Dina = +300`
- browser full audit reports `286/286 PASS`
- browser `INTERACTIVE_FLOWS` reports `8/8 PASS`
- browser `CROSS_ENGINE_FROZEN` reports `6/6 PASS`
- both demo-file SHA-256 values match the committed freeze file

---

# **17. Permitted Verification Conclusion**

When all current pass criteria are satisfied, the following bounded conclusion is supported:

**The committed ORL v2.0.0 reference implementation passes its declared Python and browser audit suites, reproduces the committed frozen cross-engine reference identities, produces the documented reference scenario, and matches the recorded demo artifact identities.**

This conclusion is bounded to the committed implementation, declared profiles, supplied audits, and frozen reference material.

---

# **18. Do Not Interpret the Result As Proof Of**

- universal ledger correctness
- universal order independence
- universal evidence completeness
- immutable financial finality
- source authenticity
- identity verification
- cryptographic signatures
- authorization
- account ownership
- available-funds verification
- fraud prevention
- consensus
- Byzantine fault tolerance
- reliable broadcast
- network correctness
- payment execution
- account posting
- settlement
- regulatory compliance
- production financial authority
- suitability for safety-critical or high-risk deployment

---

# **19. Governing Reference Relation**

`same validated canonical fragment set + same ruleset + same declared boundary context -> same bounded resolution bundle`

The current implementation further separates:

`validation != resolution`

`resolution != closure`

`closure != authorization`

`projection != settlement`

`artifact digest agreement != behavioral proof`

---

## ⭐ **Verification Summary**

ORL v2.0.0 verification combines behavioral audits, frozen Python/browser identity agreement, reference-scenario checks, interactive-flow checks, receipt reconstruction, bounded-closure checks, and SHA-256 artifact identity while preserving explicit limits on what those results establish.
