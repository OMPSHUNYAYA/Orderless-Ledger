# ⭐ **ORL — Quickstart**

**Orderless Ledger (ORL) v2.0.0**

**Validated Canonical Evidence • Deterministic Structural Resolution • Resolution Receipts • Bounded Closure**

**Developed within the Shunyaya Framework**

---

## ⚡ **30-Second Start**

From the repository root, run the Python reference kernel:

```text
python demo/ORL_Reference_Kernel_v2_0_0.py
```

Expected headline output:

```text
Validation       : ACCEPTED
Closure          : SEALED
State Summary    : R:2 I:1 A:2
Node Equality    : True
```

Expected resolved-only structural projection:

```text
UNIT
  Alice = -500
  Bob   = +200
  Dina  = +300
```

Then run the full Python audit:

```text
python demo/ORL_Reference_Kernel_v2_0_0.py --audit
```

Expected final result:

```text
TOTAL 272/272 PASS
```

---

## 🌐 **Open the Browser Structural Laboratory**

Open:

```text
demo/ORL_Structural_Lab_v2_0_0.html
```

The browser application runs locally after download.

No server, database, external package, GPS input, NTP input, synchronized clock, or internet connection is required to execute the supplied reference implementation.

The browser application contains:

- a three-node reference story
- deterministic transaction receipts
- a resolved-only structural projection
- canonical evidence identities
- bounded `OPEN` / `SEALED` closure
- interactive structural experiments
- an embedded executable audit

---

## 🧭 **Core Relation**

The current ORL v2.0.0 contract is:

`same validated canonical fragment set + same ruleset + same declared boundary context -> same bounded resolution bundle`

The processing path is:

`raw fragments -> validate -> canonicalize -> deduplicate -> resolve -> project -> evaluate declared closure boundary -> receipt -> bundle`

Validation, resolution, and closure remain separate.

---

## 🧱 **Three Separate State Lanes**

### **1. Validation**

A batch is either:

`ACCEPTED`

or:

`REFUSED`

Malformed or unsupported fragments do not silently enter the resolver.

The current strict batch policy is:

`any invalid fragment -> REFUSE_WHOLE_BATCH`

---

### **2. Resolution**

Accepted transaction structure is classified as:

- `RESOLVED`
- `INCOMPLETE`
- `ABSTAIN`

Examples:

`one debit + one credit + same amount + same unit + different accounts -> RESOLVED`

`missing debit OR missing credit -> INCOMPLETE`

`multiplicity conflict OR self-transfer OR amount mismatch OR unit mismatch -> ABSTAIN`

Only `RESOLVED` transactions contribute to the structural projection.

---

### **3. Closure**

Closure is separately classified as:

- `OPEN`
- `SEALED`

`SEALED` means that the current canonical fragment ID set exactly matches a declared evidence boundary under the current ruleset.

It does not mean that no evidence exists outside that declared boundary.

---

## 🧩 **Reference Fragment Schema**

Each supported fragment contains exactly:

```text
schema
tx
side
account
amount_minor
unit
```

The current schema profile is:

```text
ORL-FRAGMENT-2-D01
```

The supported sides are:

```text
debit
credit
```

`amount_minor` is a positive decimal integer string from 1 to 78 digits.

Examples:

```text
"1"
"500"
"9007199254740993"
```

Floating-point amounts are not used by the resolver.

Exact amounts are processed with arbitrary-precision integers in Python and `BigInt` in the browser.

---

## 🔍 **Reference Scenario**

The supplied scenario contains five transactions.

| Transaction | Final State | Reason |
|---|---|---|
| `ORL100` | `RESOLVED` | `COMPATIBLE_PAIR` |
| `ORL200` | `RESOLVED` | `COMPATIBLE_PAIR` |
| `ORL300` | `INCOMPLETE` | `MISSING_DEBIT` |
| `ORL400` | `ABSTAIN` | `AMOUNT_MISMATCH` |
| `ORL500` | `ABSTAIN` | `MULTIPLE_CREDITS` |

Expected summary:

```text
R:2 I:1 A:2
```

Expected projection:

```text
Alice = -500
Bob   = +200
Dina  = +300
```

`ORL300`, `ORL400`, and `ORL500` do not contribute to the projection.

---

## 🔁 **Three-Node Reference Story**

The browser begins with three nodes holding different valid fragment subsets.

### **Stage 1 — Local Views**

Different evidence may produce different local bounded snapshots.

### **Stage 2 — Same Evidence, Open Closure**

After every node receives the same canonical fragment set with no declared boundary:

`same fragment_set_id + same ruleset_id + same no-boundary context -> same open bundle`

### **Stage 3 — Same Evidence, Declared Boundary Satisfied**

When that exact canonical fragment set also matches the declared boundary:

`closure_state = SEALED`

All nodes then reproduce the same sealed bundle under the same declared boundary.

The sharing sequence is a demonstration mechanism.

It is not a consensus, reliable-broadcast, authorization, settlement, or network-finality protocol.

---

## 🧪 **Structural Laboratory**

The browser laboratory exposes eight principal experiments.

### **Shuffle Evidence**

Changes input order while preserving the canonical evidence set.

Expected:

`same canonical evidence + unchanged ruleset and closure context -> same bundle`

### **Add Exact Duplicate**

Adds an exact duplicate fragment.

Expected:

`D(E union E) = D(E)`

The raw input count changes.

The canonical unique set does not.

### **Complete ORL300**

Adds the missing compatible debit.

Expected transition:

`INCOMPLETE -> RESOLVED`

### **Conflict ORL100**

Adds a second distinct credit declaration.

Expected transition:

`RESOLVED -> ABSTAIN`

The earlier ORL100 projection contribution is removed from the current structural projection.

### **Add Evidence After Conflict**

Adds another distinct valid declaration after conflict.

Under the current append-only evidence model:

`ABSTAIN -> ABSTAIN`

### **Inject Malformed Fragment**

Adds an unsupported side.

Expected:

`validation_state = REFUSED`

The resolver does not silently ignore the fragment.

### **Declare + Seal Current Set**

Declares the current valid canonical fragment ID set as the evidence boundary.

Expected:

`OPEN -> SEALED`

The evidence identity itself does not change.

### **Reset Laboratory**

Restores the reference union with no declared boundary.

Expected:

`closure_state = OPEN`

---

## ✅ **Run the Browser Audit**

Open the browser developer console and run:

```text
await ORL_AUDIT.runAll()
```

Expected final result:

```text
ORL AUDIT TOTAL 286/286 PASS
```

The current browser audit groups are:

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

Useful console commands:

```text
await ORL_AUDIT.runAll()
ORL_AUDIT.last()
ORLCore.referenceScenario(true)
```

---

## 🐍 **Python Audit**

Run:

```text
python demo/ORL_Reference_Kernel_v2_0_0.py --audit
```

Expected final result:

```text
TOTAL 272/272 PASS
```

Current Python audit groups:

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
```

---

## 🔀 **Order Independence**

For a validated fragment collection `E`, a permutation `P(E)`, and the same ruleset:

`R(P(E)) = R(E)`

The current Python and browser audits each execute:

```text
PERMUTATION_INVARIANCE 120/120 PASS
```

The order-independent property is bounded to the declared ORL v2.0.0 schema, canonicalization rules, and resolver profile.

It is not a universal theorem about all ledger systems or all operations.

---

## 🧮 **Set Algebra**

The current canonical duplicate-absorption and union model tests:

`D(A union B) = D(B union A)`

`D(E union E) = D(E)`

`D((A union B) union C) = D(A union (B union C))`

The current result in both implementations is:

```text
SET_ALGEBRA 3/3 PASS
```

---

## 📈 **Evidence-Growth Model**

Under append-only valid evidence and the current resolver profile, the tested state transitions are:

`INCOMPLETE -> INCOMPLETE | RESOLVED | ABSTAIN`

`RESOLVED -> RESOLVED | ABSTAIN`

`ABSTAIN -> ABSTAIN`

The exhaustive current test result is:

```text
EVIDENCE_GROWTH_EXHAUSTIVE 65/65 PASS
```

These transition constraints apply only to the declared append-only evidence model and current ruleset.

Removal, revocation, supersession, remediation, or ruleset migration are separate concerns.

---

## 🧾 **Resolution Receipts**

Every transaction identifier in an accepted batch that reaches structural classification receives a deterministic receipt containing its:

- transaction identifier
- transaction evidence identity
- ruleset identity
- resolution state
- reason code
- resolved fields where applicable
- closure state
- closure reason
- declared boundary identity where applicable
- receipt identity

The current audits verify:

```text
RECEIPTS 7/7 PASS
```

This includes receipt reconstruction, tamper rejection, and distinct open/sealed receipt identities.

A receipt proves consistency with the declared receipt construction.

It does not prove authorization, authenticity of external sources, available funds, legal validity, settlement, or global completeness.

---

## 🔐 **Frozen Cross-Engine Contract**

The Python kernel and browser implementation independently reproduce the current frozen identities.

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

Expected browser result:

```text
CROSS_ENGINE_FROZEN 6/6 PASS
```

---

## 🔐 **Artifact Identity**

Current v2.0.0 demo file SHA-256 values:

```text
ORL_Reference_Kernel_v2_0_0.py
c9fe03c56631d5751669c8635227f1e737e1c419add1bdc40138860210daf4c1

ORL_Structural_Lab_v2_0_0.html
1f8918e8214385f63288003c4842cf600e7e95e1fa8431afe237768b57f406e1
```

On Windows:

```text
certutil -hashfile demo\ORL_Reference_Kernel_v2_0_0.py SHA256
certutil -hashfile demo\ORL_Structural_Lab_v2_0_0.html SHA256
```

Compare the reported values with:

```text
verify\FREEZE_DEMO_SHA256.txt
```

A matching SHA-256 value establishes byte identity for the checked artifact.

`artifact identity != behavioral proof`

Run the audits as well.

---

## ⚙️ **Minimum Requirements**

Python reference kernel:

- Python 3.9 or later
- Python standard library only

Browser Structural Laboratory:

- a modern browser with `BigInt` support

No external Python package or server is required for the supplied reference implementation.

---

## 📁 **Repository Structure**

```text
ORDERLESS-LEDGER/

├── README.md
├── LICENSE
│
├── demo/
│   ├── ORL_Reference_Kernel_v2_0_0.py
│   └── ORL_Structural_Lab_v2_0_0.html
│
├── docs/
│   ├── FAQ.md
│   ├── Quickstart.md
│   ├── ORL_Core_Architecture.md
│   ├── Test-Guide.md
│   └── ORL-Structural-Overview.png
│
└── verify/
    ├── FREEZE_DEMO_SHA256.txt
    └── VERIFY.md
```

---

## ⚖️ **What ORL v2.0.0 Does Not Establish**

The current reference implementation does not establish or provide:

- universal ledger correctness
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
- network dissemination
- payment execution
- account posting
- settlement
- immutable financial finality
- regulatory compliance
- production financial authority
- universal order independence

ORL v2.0.0 should be evaluated as a bounded deterministic structural-reconciliation reference implementation.

---

## ⭐ **One-Line Summary**

ORL v2.0.0 validates and canonicalizes supported transaction fragments, absorbs exact duplicates, classifies accepted structure deterministically, produces reproducible receipts and structural projections, and can separately verify exact bounded closure — while keeping authorization, consensus, settlement, and production financial authority outside the implementation.
