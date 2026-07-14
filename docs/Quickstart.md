# ⭐ **ORL — Quickstart**

**Orderless Ledger (ORL)**

**Deterministic Structural Reconciliation Reference Model**

**Order-Independent • Clock-Independent Resolution • Explicit Incompleteness • Demonstrated Conflict Abstention**

**Powered by the Shunyaya Framework**

---

## ⚡ **30-Second Start**

From the repository root, run:

```text
python demo/orl_demo_reference.py
```

Expected final summary:

```text
R:2 I:1 A:2
```

Equivalent Python output may appear as:

```text
{'ABSTAIN': 2, 'INCOMPLETE': 1, 'RESOLVED': 2}
```

Expected final balance projection:

```text
Alice = -500
Bob   = +200
Dina  = +300
```

Expected equality result:

```text
all_nodes_match_after_sharing = True
```

---

## 👀 **What to Observe**

For the supplied scenario:

- three nodes begin with different local fragment collections  
- the resolver does not read timestamps or wall-clock values  
- the resolver does not consult fragment arrival position when classifying the supported example transactions  
- exact duplicate entries are absorbed  
- matching supported debit and credit fragments can resolve  
- missing demonstrated structure remains `INCOMPLETE`  
- demonstrated amount mismatch or same-transaction multiplicity conflict produces `ABSTAIN`  
- only `RESOLVED` transactions affect the demonstrated balance projection  
- after every node receives the same merged fragment set, every node produces the same demonstrated resolver output  

The governing relation is:

`same deduplicated supported fragment set + same resolver rules -> same bounded resolution`

---

## ⚡ **Browser Demo**

Open:

```text
demo/orl_demo_v3.html
```

Then click:

**Run Full Demo**

The browser demonstration runs locally after download.

No internet connection, GPS signal, NTP service, synchronized clock, database, or server is required to execute the supplied reference demo.

### **Browser Controls**

- **Next Step** — advances one declared stage  
- **Run Full Demo** — runs the complete local-to-shared sequence  
- **Reset** — restores the initial local fragment views  
- **Jump to Sharing** — moves directly to the final `All Nodes Complete Bounded Sharing` stage  

The sharing sequence is a test mechanism.

It is not a consensus, reliable-broadcast, network-finality, or settlement protocol.

---

## 🧭 **Core Principle**

`bounded_resolution = resolve(supported_fragment_set, resolver_rules)`

For a supported fragment collection `E`, a supported permutation `P(E)`, and a fixed resolver version `v`:

`R_v(P(E)) = R_v(E)`

When two nodes hold the same deduplicated supported fragment set and use the same resolver rules:

`D(E_i) = D(E_j) -> R_v(E_i) = R_v(E_j)`

Where:

- `R_v` is the resolver under ruleset version `v`  
- `D(E)` is exact-duplicate absorption  
- `E_i` and `E_j` are the fragment collections held by two nodes  

This is a bounded claim about the declared model and supplied examples.

It is not a universal theorem about every ledger architecture.

---

## 🔍 **Structural Transaction Model**

The current demos represent a transaction as declared fragments associated with a transaction identifier.

Example:

`ORL100 = {debit(Alice,500), credit(Bob,500)}`

The resolver examines which supported fragments are present under that identifier.

It does not use which fragment arrived first as the classification authority.

### **Current Demonstrated Rules**

For the supplied examples:

`one debit + one credit + matching amount -> RESOLVED`

`missing counterpart -> INCOMPLETE`

`debit_credit_mismatch OR demonstrated_same_transaction_multiplicity_conflict -> ABSTAIN`

Other malformed, unsupported, or untested conflict forms remain outside the current conformance claim.

---

## ⚖️ **Resolution States**

### **RESOLVED**

For the supplied examples, `RESOLVED` means:

- one declared debit is present  
- one declared credit is present  
- the declared amounts match  

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

`INCOMPLETE` means that a required demonstrated counterpart is missing.

The resolver does not invent the missing fragment.

---

### **ABSTAIN**

For the conflict forms included in the supplied scenario, `ABSTAIN` means that the demonstrated declarations are incompatible and no demonstrated balance effect is applied.

Within the current examples:

`INCOMPLETE OR ABSTAIN -> no demonstrated balance effect`

---

## 🔍 **Declared Transactions**

### **ORL100**

```text
debit(Alice,500)
credit(Bob,500)
```

Final state:

`ORL100 -> RESOLVED`

---

### **ORL200**

```text
debit(Bob,300)
credit(Dina,300)
```

Final state:

`ORL200 -> RESOLVED`

---

### **ORL300**

Only one counterpart is present.

Final state:

`ORL300 -> INCOMPLETE`

---

### **ORL400**

The declared debit and credit amounts differ.

Final state:

`ORL400 -> ABSTAIN`

---

### **ORL500**

One debit and two incompatible credit declarations share the same transaction identifier.

Final state:

`ORL500 -> ABSTAIN`

`ORL500` is a same-transaction multiplicity-conflict example.

It is not a complete demonstration of general double-spend prevention.

---

## 📊 **Expected Final Result**

| Transaction | Expected State | Demonstrated Reason |
|---|---|---|
| `ORL100` | `RESOLVED` | Matching debit and credit |
| `ORL200` | `RESOLVED` | Matching debit and credit |
| `ORL300` | `INCOMPLETE` | Missing counterpart |
| `ORL400` | `ABSTAIN` | Debit-credit amount mismatch |
| `ORL500` | `ABSTAIN` | Same-transaction multiple-credit conflict |

Expected state summary:

```text
R:2 I:1 A:2
```

Expected balance projection:

```text
Alice = -500
Bob   = +200
Dina  = +300
```

---

## 🔁 **Repeatability Check**

Run the Python demo again:

```text
python demo/orl_demo_reference.py
```

For the unchanged supplied scenario, confirm the same:

- transaction states  
- balance projection  
- state counts  
- node-equality result  

Expected relation:

`same supplied input + same resolver -> same supplied output`

This is a repeatability check for the declared scenario.

It is not a universal conformance proof.

---

## 🔀 **Order-Independence Meaning**

In the current resolver, classification is based on the supported fragments present under each transaction identifier.

Fragment arrival position is not read as part of the transaction-state rule.

The intended invariant is:

`R_v(P(E)) = R_v(E)`

A stronger future release should add an automated permutation corpus that asserts this invariant across many declared vectors.

---

## 🔎 **Precise Meaning of No Time, No Order, and No Coordinator**

### **No Time as Classification Authority**

The resolver does not use:

- timestamps  
- synchronized clocks  
- wall-clock time  
- GPS time  
- NTP state  

Time may still remain useful outside the resolver for history, monitoring, reporting, or operations.

---

### **No Arrival Order as Classification Authority**

The resolver classifies the present supported fragment set rather than asking which fragment arrived first.

Operational systems may still use:

- logs  
- queues  
- sequence numbers  
- replay  
- ordered transport  

---

### **No Coordinator State as Classification Authority**

The resolver does not accept a coordinator's declared result as an input to transaction classification.

The supplied demonstrations still use scripted code to distribute fragments.

The repository does not implement coordinator-free networking or distributed consensus.

---

## 🚫 **What ORL Does Not Implement or Prove**

The current repository does not implement or prove:

- universal ledger correctness  
- immutable transaction finality  
- complete malformed-input validation  
- authorization  
- identity or account ownership  
- available-funds verification  
- cryptographic signatures  
- fraud prevention  
- consensus  
- Byzantine fault tolerance  
- reliable broadcast  
- payment execution  
- account posting  
- settlement  
- regulatory compliance  
- production readiness  
- general double-spend prevention  
- universal order independence  

ORL should be evaluated as a bounded structural-reconciliation reference model.

---

## ✅ **Appropriate Current Uses**

The repository may be used as:

- a deterministic reconciliation example  
- an order-invariance research prototype  
- a duplicate-absorption demonstration  
- a partial-state classification example  
- an audit-oriented evidence comparison model  
- an educational disconnected-node demonstration  
- a basis for later conformance work  

It should not be used directly as a production financial authority.

---

## ⚙️ **Minimum Requirements**

- Python 3.9 or later  
- Python standard library only  
- a modern browser for the HTML demo  
- no external Python packages  
- no server required  
- no internet connection required after download  

---

## 📁 **Repository Structure**

```text
ORDERLESS-LEDGER/

├── README.md
├── LICENSE
│
├── demo
│   ├── orl_demo_reference.py
│   └── orl_demo_v3.html
│
├── docs
│   ├── FAQ.md
│   ├── Quickstart.md
│   ├── Test-Guide.md
│   └── ORL-Structural-Overview.png
│
└── verify
    ├── FREEZE_DEMO_SHA256.txt
    └── VERIFY.txt
```

---

## 🧠 **Repository Roles**

- `demo/` — Python and browser reference demonstrations  
- `docs/` — usage, testing, boundaries, and conceptual explanation  
- `README.md` — repository overview and claim boundary  
- `verify/` — artifact-identity and reference-verification material  
- `LICENSE` — repository usage terms  

---

## 🔐 **Artifact Identity Check**

The repository records SHA-256 values in:

```text
verify/FREEZE_DEMO_SHA256.txt
```

Follow:

```text
verify/VERIFY.txt
```

On Windows, run:

```text
certutil -hashfile demo\orl_demo_reference.py SHA256
certutil -hashfile demo\orl_demo_v3.html SHA256
```

Then compare both values with the committed freeze file.

The meaning of this check is:

`same bytes -> same SHA-256 hash`

A successful hash comparison establishes artifact identity.

It does not by itself establish behavioral correctness, complete conformance, cross-engine equality, or production safety.

---

## ⚠️ **Current Validation Boundary**

The current demos assume well-formed example inputs.

They do not yet certify behavior for:

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

These conditions belong to the later resolver-hardening and conformance stage.

---

## 🧪 **Future Technical Direction**

A stronger technical revision should add:

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

Future target relation:

`same validated canonical structure + same ruleset version -> same independently verified output`

This stronger verification layer is not part of the current public demos.

---

## ⚡ **Suggested One-Minute Demo**

1. Open `demo/orl_demo_v3.html`.
2. Click **Reset**.
3. Observe the three different local fragment views.
4. Click **Run Full Demo**.
5. Observe fragments becoming jointly visible.
6. Confirm `ORL100` and `ORL200` resolve.
7. Confirm `ORL300` remains incomplete.
8. Confirm `ORL400` and `ORL500` abstain.
9. Confirm the final summary is `R:2 I:1 A:2`.
10. Confirm every node shows the same final demonstrated snapshot.

Correct interpretation:

`same deduplicated supported evidence + same resolver rules -> same bounded resolution`

---

## ⭐ **One-Line Summary**

ORL is a public deterministic reference model in which independent nodes can begin with different supported transaction fragments and, after receiving the same deduplicated fragment set, produce the same bounded resolver output without using timestamps, fragment arrival order, GPS, NTP, or coordinator state as the classification authority — while preserving explicit `INCOMPLETE` and demonstrated `ABSTAIN` outcomes and keeping authorization, consensus, settlement, and immutable finality outside the current implementation.
