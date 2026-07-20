# ⭐ **ORL — Orderless Ledger**

**Validated Canonical Evidence • Deterministic Structural Resolution • Reproducible Receipts • Bounded Closure**

![ORL](https://img.shields.io/badge/ORL-Orderless%20Ledger-black)
![Version](https://img.shields.io/badge/Version-2.0.0-blue)
![Python Audit](https://img.shields.io/badge/Python%20Audit-272%2F272%20PASS-green)
![Browser Audit](https://img.shields.io/badge/Browser%20Audit-286%2F286%20PASS-green)
![Cross Engine](https://img.shields.io/badge/Frozen%20Cross--Engine-6%2F6%20PASS-green)
![Deterministic](https://img.shields.io/badge/Resolution-Deterministic-purple)
![Arrival Order](https://img.shields.io/badge/Arrival%20Order-Not%20Authoritative-lightgrey)
![Clock Metadata](https://img.shields.io/badge/Clock%20Metadata-Not%20Used-lightgrey)
![Reference Model](https://img.shields.io/badge/Implementation-Public%20Reference-orange)

[![ORL Verification](https://github.com/OMPSHUNYAYA/Orderless-Ledger/actions/workflows/verify.yml/badge.svg)](https://github.com/OMPSHUNYAYA/Orderless-Ledger/actions/workflows/verify.yml)

**No timestamp authority • No fragment-arrival-order authority • No coordinator-state authority**

**No GPS • No NTP • No Internet Required to Run the Reference Implementations**

---

`same validated canonical fragment set + same ruleset + same declared boundary context -> same bounded resolution bundle`

ORL v2.0.0 is a bounded structural-reconciliation reference implementation developed within the Shunyaya Framework.

It separates five questions that are often collapsed into one:

`is the input valid?`

`what canonical evidence is present?`

`what does that evidence resolve to?`

`what projection follows from the resolved subset?`

`has the current evidence set satisfied an explicitly declared boundary?`

---

## ⚡ **The Central Idea**

Many operational systems use timestamps, ordered logs, queues, coordinators, consensus, or replay histories for important reasons.

ORL asks a narrower question:

> Can a bounded set of transaction declarations be validated, identified, classified, and reproduced deterministically without using fragment arrival order or clock metadata as the authority over the classification result?

Within the implemented ORL v2.0.0 profiles, the reference implementations demonstrate that:

- malformed or unsupported fragments can be refused before resolution  
- valid fragments can be canonicalized into deterministic identities  
- exact canonical duplicates can be absorbed without creating multiplicity conflicts  
- supported fragment permutations can produce the same bounded resolution bundle  
- incomplete structure can remain explicitly `INCOMPLETE`  
- conflicting structure can produce explicit `ABSTAIN` outcomes  
- only `RESOLVED` transactions contribute to the structural projection  
- every transaction result can receive a deterministic receipt  
- a separately declared exact evidence boundary can produce `SEALED` closure  
- Python and browser implementations can reproduce the same frozen reference identities  

The implementation does not claim that order, time, coordination, authorization, consensus, or settlement can be removed from every real system.

The narrower architectural statement is:

`operational sequence != structural resolution authority`

---

## 🧭 **Architecture at a Glance**

The ORL v2.0.0 processing path is:

`raw fragments -> validate -> canonicalize -> deduplicate -> resolve -> project -> evaluate declared closure boundary -> receipt -> bundle`

The three principal state lanes remain separate:

`validation_state = ACCEPTED | REFUSED`

`resolution_state = RESOLVED | INCOMPLETE | ABSTAIN`

`closure_state = OPEN | SEALED`

This separation is intentional.

`validation != resolution`

`resolution != closure`

`closure != authorization`

`projection != settlement`

---

## ⚖️ **What ORL Is / Is Not**

### **ORL IS**

- a bounded structural ledger-reconciliation reference model  
- a strict supported-fragment validation model  
- a deterministic canonical identity model for supported evidence  
- an order-invariance implementation for the declared resolver profile  
- an exact duplicate-absorption model  
- an explicit model of incomplete and conflicting transaction structure  
- a deterministic transaction-receipt implementation  
- a bounded evidence-closure demonstration  
- a Python/browser cross-engine conformance reference for frozen vectors  
- an executable research foundation for later ORL-domain projects  

### **ORL IS NOT**

- a banking, accounting, payment, custody, or settlement platform  
- a blockchain replacement claim  
- a consensus or Byzantine-fault-tolerance protocol  
- a reliable-broadcast or network-dissemination protocol  
- an identity, authentication, signature, or authorization system  
- an available-funds or account-ownership verifier  
- a fraud-prevention system  
- a proof of universal order independence  
- an implementation of universal or immutable financial finality  
- a production-readiness claim  
- a performance-superiority claim  

ORL classifies declared supported structure.

It does not establish that a structurally resolved transaction is legitimate, authorized, funded, settled, legally valid, or safe for real-world execution.

---

## 🧩 **Supported Fragment Contract**

The v2.0.0 fragment schema is:

`ORL-FRAGMENT-2-D01`

Each supported fragment contains exactly these fields:

| Field | Meaning |
|---|---|
| `schema` | Required schema profile identifier |
| `tx` | Transaction grouping identifier; distinct real-world transfers require distinct identifiers |
| `side` | `debit` or `credit` |
| `account` | Declared account identifier |
| `amount_minor` | Exact positive decimal integer string |
| `unit` | Declared uppercase unit identifier |

### **Validation Rules**

The current profile requires:

- all six required fields  
- no unknown fields  
- string values for every supported field  
- `schema = ORL-FRAGMENT-2-D01`  
- `side = debit | credit`  
- `amount_minor` containing 1 to 78 decimal digits  
- a positive amount with no sign, decimal point, or leading zero  
- an uppercase ASCII unit identifier of 1 to 32 characters under the declared pattern  
- no empty transaction, account, or unit field  
- no leading or trailing whitespace in transaction, account, or unit fields  
- no forbidden control characters  
- bounded UTF-8 lengths for transaction and account identifiers  

Text is normalized using Unicode NFC before canonical identity is computed.

The batch policy is strict:

`any invalid fragment -> REFUSE_WHOLE_BATCH`

A refused batch does not enter the transaction resolver.

This prevents malformed or unsupported structure from being silently ignored or misclassified as legitimate incompleteness.

---

## 🔐 **Canonical Evidence Identity**

ORL v2.0.0 uses explicit length-framed UTF-8 canonical records rather than delimiter-based string concatenation.

Canonicalization is versioned through:

`ORL-CANON-1-D01`

The current implementation derives deterministic SHA-256 content identities for:

- individual canonical fragments  
- deduplicated fragment sets  
- per-transaction evidence sets  
- structural projections  
- transaction receipts  
- declared evidence boundaries  
- complete resolution bundles  

Conceptually:

`fragment_id = SHA256(canonical_fragment)`

`fragment_set_id = SHA256(canonical_order(unique(fragment_ids)))`

`transaction_evidence_id = SHA256(transaction_id + canonical_transaction_fragment_ids)`

`receipt_id = SHA256(canonical_receipt)`

`bundle_id = SHA256(canonical_resolution_bundle)`

The actual implementation uses explicit canonical framing rather than ambiguous raw concatenation.

These hashes provide deterministic content identity within the declared profiles.

They do not by themselves provide cryptographic signatures, source authenticity, ownership, or authorization.

---

## 🔁 **Exact Duplicate Absorption**

**Exact duplicates are identified from canonical fragment identity.**

The implemented policy is:

`ABSORB_EXACT_CANONICAL_DUPLICATES`

Therefore an exact duplicate does not create a false multiplicity conflict.

Exact duplicate absorption assumes that repeated canonically identical fragments under the same `tx` describe the same declaration. ORL does not infer that canonically identical fragments were intended to represent separate real-world movements.

Therefore:

`same canonical declaration repeated under the same tx -> exact duplicate`

`distinct real-world transfer -> distinct tx identifier`

A future schema that needs to preserve multiple otherwise identical declarations within one transaction would require an additional distinguishing field.

The bounded-union implementation is tested for these structural identities:

`D(A union B) = D(B union A)`

`D(E union E) = D(E)`

`D((A union B) union C) = D(A union (B union C))`

These are implementation invariants for the declared canonical-fragment model.

---

## 🧭 **Deterministic Resolution Model**

The active resolver profile is:

`ORL-RESOLUTION-2-D01`

After validation and exact canonical deduplication, fragments are grouped by transaction identifier.

The current conflict precedence is explicit:

`MULTIPLE_DEBITS_AND_CREDITS`

`-> MULTIPLE_DEBITS`

`-> MULTIPLE_CREDITS`

`-> MISSING_DEBIT`

`-> MISSING_CREDIT`

`-> SELF_TRANSFER_UNSUPPORTED`

`-> AMOUNT_MISMATCH`

`-> UNIT_MISMATCH`

`-> COMPATIBLE_PAIR`

### **Resolution Outcomes**

| Structural Condition | State | Reason Code |
|---|---|---|
| One compatible debit and one compatible credit | `RESOLVED` | `COMPATIBLE_PAIR` |
| Debit missing | `INCOMPLETE` | `MISSING_DEBIT` |
| Credit missing | `INCOMPLETE` | `MISSING_CREDIT` |
| Multiple distinct debits | `ABSTAIN` | `MULTIPLE_DEBITS` |
| Multiple distinct credits | `ABSTAIN` | `MULTIPLE_CREDITS` |
| Multiple distinct debits and credits | `ABSTAIN` | `MULTIPLE_DEBITS_AND_CREDITS` |
| Same account on both sides | `ABSTAIN` | `SELF_TRANSFER_UNSUPPORTED` |
| Debit and credit amounts differ | `ABSTAIN` | `AMOUNT_MISMATCH` |
| Debit and credit units differ | `ABSTAIN` | `UNIT_MISMATCH` |

The current model does not guess missing structure and does not silently select among incompatible alternatives.

---

## 💰 **Exact Amount Model**

ORL does not use binary floating-point arithmetic for supported amounts.

The canonical amount representation is:

`amount_minor = positive decimal integer string`

The current profile supports 1 to 78 digits.

The Python implementation evaluates exact values with arbitrary-precision integers.

The browser implementation evaluates projection arithmetic with `BigInt`.

The committed audits include values above the JavaScript safe-integer boundary and a 78-digit amount vector.

This means supported reference calculations are not dependent on binary floating-point rounding.

The field name `amount_minor` does not imply a specific currency.

Its meaning is determined by the accompanying declared `unit` and by any domain-specific profile built above ORL.

---

## 📊 **Resolved-Only Structural Projection**

Only transactions classified as `RESOLVED` contribute to the current structural projection.

`RESOLVED -> projection contribution`

`INCOMPLETE OR ABSTAIN -> no projection contribution`

The projection is a deterministic view over the currently admitted canonical evidence set.

It is not settlement, posting, authorization, or immutable ledger finality.

If additional valid evidence changes a transaction from:

`RESOLVED -> ABSTAIN`

its previous contribution is removed from the newly computed structural projection.

This is a recomputed bounded projection over the current evidence set, not a claim that an executed financial transfer has been reversed.

---

## 🧾 **Deterministic Resolution Receipts**

Every transaction identifier that reaches structural classification receives a deterministic receipt under:

`ORL-RECEIPT-1-D01`

A receipt binds the current result to fields including:

- schema profile  
- ruleset profile  
- ruleset identity  
- transaction identifier  
- transaction evidence identity  
- resolution state  
- reason code  
- resolved endpoints and amount when applicable  
- closure state  
- closure reason  
- boundary identity when applicable  

The receipt identity is reconstructed from the canonical receipt content.

The audit verifies:

- all five reference transaction receipts  
- rejection of a tampered receipt  
- distinct receipt identities between open and sealed closure states  

A valid receipt demonstrates deterministic agreement with the declared receipt construction.

It does not establish external authenticity, authorization, or legal validity.

---

## 🔒 **Bounded Structural Closure**

Resolution and closure are separate.

A transaction may be structurally resolved while the evidence set remains open:

`RESOLVED + OPEN`

ORL v2.0.0 implements a declared boundary profile:

`ORL-BOUNDARY-1-D01`

A boundary commits to the exact canonical fragment-ID set expected under the current schema and ruleset.

Closure becomes:

`SEALED`

only when:

`current canonical fragment IDs = declared expected fragment IDs`

Otherwise closure remains:

`OPEN`

The implemented distinction is:

`SEALED = declared exact boundary satisfied`

not:

`SEALED = proof that no undisclosed evidence exists anywhere`

The audit verifies that:

- absence of a declared boundary remains `OPEN`  
- the exact declared boundary becomes `SEALED`  
- boundary identity is stable under supported permutation  
- a subset does not seal against a larger boundary  
- a superset does not seal against a smaller boundary  

This provides bounded closure without claiming universal completeness or immutable external finality.

---

## 📈 **Evidence-Growth State Model**

Under the current append-only valid-evidence model and fixed resolver profile, the implemented state-transition discipline is:

`INCOMPLETE -> INCOMPLETE | RESOLVED | ABSTAIN`

`RESOLVED -> RESOLVED | ABSTAIN`

`ABSTAIN -> ABSTAIN`

The important distinction is:

`currently RESOLVED != permanently final`

Additional valid evidence may reveal conflict.

Within the declared append-only profile, once incompatible alternatives have produced `ABSTAIN`, adding further valid fragments cannot remove the already present conflict.

The committed Python and browser audits include:

- direct transition checks  
- 65 exhaustive subset-to-superset checks over the frozen evidence-growth corpus  

This is a tested property of the declared ORL resolver profile and audit corpus, not a universal theorem about every possible ledger design.

---

## 🔀 **Order Independence — Precise Meaning**

For a validated supported fragment collection `E`, a permutation `P(E)`, and the same fixed ruleset:

`R(P(E)) = R(E)`

for an unchanged declared boundary context.

When complete bounded bundle identities are compared, the ruleset and boundary context are held fixed.

The committed audit exhaustively checks all:

`5! = 120`

permutations of a frozen five-fragment conformance vector.

All 120 permutations produce the same bounded resolution bundle identity.

This establishes the tested invariant for that declared vector and implementation profile.

It is not a proof that every ledger problem is order-independent.

Operational systems may still use:

- ordered transport  
- logs  
- queues  
- sequence numbers  
- replay histories  
- timestamps  

ORL's narrower claim is that fragment arrival position is not an input to the current structural classification rules.

---

## 🌐 **Three-Node Same-Evidence Demonstration**

The reference story begins with three different local evidence views.

At that stage:

- each node may see different transaction structure  
- each node may produce a different local snapshot  
- equality is not required because the evidence sets differ  

The demonstration then gives every node the same deduplicated canonical fragment set.

With the same ruleset and no declared boundary:

`same canonical evidence + same ruleset + same no-boundary context -> same open bundle`

The demonstration can then declare the exact current set as a boundary:

`same canonical evidence + same ruleset + same satisfied boundary -> same sealed bundle`

The sharing mechanism is a demonstration harness.

It is not consensus, reliable broadcast, leader election, Byzantine agreement, network finality, or settlement execution.

---

## 📊 **Reference Scenario**

The frozen reference scenario produces:

`R:2 I:1 A:2`

| Transaction | State | Reason |
|---|---|---|
| `ORL100` | `RESOLVED` | `COMPATIBLE_PAIR` |
| `ORL200` | `RESOLVED` | `COMPATIBLE_PAIR` |
| `ORL300` | `INCOMPLETE` | `MISSING_DEBIT` |
| `ORL400` | `ABSTAIN` | `AMOUNT_MISMATCH` |
| `ORL500` | `ABSTAIN` | `MULTIPLE_CREDITS` |

The resolved-only structural projection is:

```text
UNIT
  Alice  -500
  Bob    +200
  Dina   +300
```

`ORL300`, `ORL400`, and `ORL500` do not contribute to that projection.

---

## 🧪 **Structural Laboratory**

The browser implementation includes an interactive Structural Laboratory for observing both invariants and legitimate state changes.

### **Shuffle Evidence**

Changes input order while preserving the bounded result when the canonical evidence, ruleset, and closure context remain unchanged.

`same canonical evidence + unchanged ruleset and closure context -> same bundle`

### **Add Exact Duplicate**

Increases raw input count while preserving the canonical unique evidence set.

`exact duplicate -> absorbed`

### **Complete ORL300**

Adds the missing counterpart and demonstrates:

`INCOMPLETE -> RESOLVED`

when compatible structure becomes complete.

### **Conflict ORL100**

Adds an incompatible declaration and demonstrates:

`RESOLVED -> ABSTAIN`

The earlier ORL100 projection contribution disappears from the recomputed current projection.

### **Add Evidence After Conflict**

Demonstrates the append-only profile behavior:

`ABSTAIN -> ABSTAIN`

### **Inject Malformed Fragment**

Demonstrates strict validation:

`invalid fragment -> REFUSED`

The resolver does not silently ignore the unsupported structure.

### **Declare + Seal Current Set**

Constructs an exact boundary from the current valid canonical fragment set and demonstrates:

`OPEN -> SEALED`

without changing the underlying evidence identity.

The browser audit permanently covers all eight current interactive flow invariants.

---

## 🔄 **Python and Browser Cross-Engine Contract**

ORL v2.0.0 provides two reference implementations:

- Python reference kernel  
- standalone browser Structural Laboratory  

Both use the same declared:

- fragment schema  
- canonical framing  
- Unicode normalization rule  
- exact amount domain  
- duplicate policy  
- conflict precedence  
- ruleset manifest  
- projection construction  
- receipt construction  
- boundary construction  
- bundle construction  

The browser audit includes six frozen equality checks against Python-produced reference identities.

Current frozen cross-engine checks:

`6/6 PASS`

This demonstrates equality for the committed frozen reference identities.

It is not presented as an independently implemented third-party verification system.

---

## 🧬 **Current Profiles**

| Purpose | Profile |
|---|---|
| Architecture version | `2.0.0` |
| Fragment schema | `ORL-FRAGMENT-2-D01` |
| Resolution rules | `ORL-RESOLUTION-2-D01` |
| Canonicalization | `ORL-CANON-1-D01` |
| Fragment-set identity | `ORL-FRAGMENT-SET-1-D01` |
| Transaction evidence | `ORL-TX-EVIDENCE-1-D01` |
| Resolution receipt | `ORL-RECEIPT-1-D01` |
| Structural projection | `ORL-PROJECTION-1-D01` |
| Resolution bundle | `ORL-BUNDLE-1-D01` |
| Declared boundary | `ORL-BOUNDARY-1-D01` |
| Validation refusal | `ORL-REFUSAL-1-D01` |
| Audit profile | `ORL-AUDIT-1-D01` |

Profiles make the implementation contract explicit and allow later ORL-family systems to define their own domain rules without silently changing the ORL core semantics.

---

## 🔑 **Frozen Reference Identities**

For the current v2.0.0 frozen reference contract:

### **Ruleset ID**

`389eb1062a4cf7668450c475fd84c7611c3ab6c7c402f9e34ac37698fea09909`

### **Reference Fragment Set ID**

`7a37a07d4a83a0235199b2846da6a68d045d7dde458520fdf91c9504943b6a6f`

### **Open Bundle ID**

`046d1de963dcb4b4ab05aeb4e7e81afaca56b9a8fceb6bb50f22d8c087c2d973`

### **Reference Boundary ID**

`ba855c228a92ea9414bc3b4ad354aba92f92e62c767b9f2535a0db3d2188806b`

### **Sealed Bundle ID**

`857564e4e9f24a77ef1a9550e385d203c5e41e55b8fae624f37b82ee684c39f5`

### **Projection ID**

`9c714030a7a333a4018fc610a6e086e3b64a106a2cbc957b6b58a8253653c3ff`

These values identify the frozen reference contract and scenario outputs under the current implementation profiles.

---

## 🚀 **Quick Start**

### **Run the Python Reference Kernel**

From the repository root:

```text
python demo/ORL_Reference_Kernel_v2_0_0.py
```

Expected headline result:

```text
ORL v2.0.0
Validation       : ACCEPTED
Closure          : SEALED
State Summary    : R:2 I:1 A:2
Node Equality    : True
```

### **Run the Python Audit**

```text
python demo/ORL_Reference_Kernel_v2_0_0.py --audit
```

Expected result:

`TOTAL 272/272 PASS`

### **Open the Browser Structural Laboratory**

Open locally:

```text
demo/ORL_Structural_Lab_v2_0_0.html
```

The browser implementation requires no server or internet connection after download.

### **Run the Browser Audit from the Console**

```text
await ORL_AUDIT.runAll()
```

Expected result:

`ORL AUDIT TOTAL 286/286 PASS`

Additional inspection commands:

```text
ORL_AUDIT.last()
ORLCore.referenceScenario(true)
```

---

## ✅ **Current Audit Coverage**

### **Python Reference Kernel**

| Audit Group | Result |
|---|---:|
| Validation | `20/20 PASS` |
| Canonicalization | `8/8 PASS` |
| Exact amounts | `5/5 PASS` |
| Resolution | `18/18 PASS` |
| Deduplication | `3/3 PASS` |
| Reference scenario | `10/10 PASS` |
| Permutation invariance | `120/120 PASS` |
| Set algebra | `3/3 PASS` |
| Evidence growth | `3/3 PASS` |
| Evidence growth exhaustive | `65/65 PASS` |
| Closure | `6/6 PASS` |
| Receipts | `7/7 PASS` |
| Known regressions | `4/4 PASS` |
| **Total** | **`272/272 PASS`** |

### **Browser Structural Laboratory**

The browser repeats the same core behavioral groups and additionally checks its interactive flows and frozen Python/browser identity agreement.

| Additional Browser Group | Result |
|---|---:|
| Interactive flows | `8/8 PASS` |
| Frozen cross-engine identities | `6/6 PASS` |
| **Browser Total** | **`286/286 PASS`** |

Passing these committed audits establishes that the tested implementation behavior matches the declared test expectations.

It does not establish universal ledger correctness, production safety, authorization, consensus, settlement, or regulatory suitability.

---

## 🛡 **Known Regression Coverage**

Permanent regression checks currently include:

- unsupported side values cannot be silently ignored  
- multiple debits without a credit produce `ABSTAIN` rather than false incompleteness  
- multiple credits without a debit produce `ABSTAIN` rather than false incompleteness  
- separator-bearing account identifiers remain structurally safe under canonical framing  

Browser interactive-flow regression coverage additionally checks:

- shuffle preserves the canonical bundle  
- an exact duplicate preserves the canonical bundle  
- completing ORL300 produces `RESOLVED`  
- conflicting ORL100 produces `ABSTAIN`  
- the conflict removes ORL100's previous projection contribution  
- additional valid evidence preserves existing abstention  
- malformed laboratory input is refused  
- declaring the current exact set seals closure without changing evidence identity  

---

## 🔍 **Verification Model**

ORL separates several forms of evidence.

### **1. Behavioral Audit**

The Python and browser audit suites execute deterministic assertions over the declared profiles and frozen vectors.

`implementation + test vectors -> observed pass/fail evidence`

### **2. Frozen Cross-Engine Equality**

The browser independently evaluates the declared JavaScript implementation and compares six frozen identities with the Python reference outputs.

`same declared contract -> same frozen identities`

### **3. Artifact Identity**

The repository verification material can bind released files to SHA-256 values.

`same bytes -> same SHA-256 hash`

Artifact identity does not by itself prove behavioral correctness.

`artifact identity != behavioral proof`

### **4. Independent Reconstruction**

A separately implemented independent verifier is not claimed by the current ORL v2.0.0 core release unless such a verifier is explicitly included and documented in the repository.

---

## 🔎 **No Time / No Order / No Coordinator — Precise Meaning**

### **No Time as Resolution Authority**

The current resolver does not use:

- timestamps  
- synchronized clocks  
- wall-clock time  
- GPS time  
- NTP state  

Time may still be useful or necessary outside the resolver for transport, monitoring, auditing, history, operations, or legal records.

### **No Arrival Order as Resolution Authority**

The resolver classifies the validated canonical fragment set currently supplied to it.

It does not ask which fragment arrived first.

Operational systems may still use ordered transport, queues, logs, and replay.

### **No Coordinator State as Resolution Authority**

The resolver does not accept a coordinator's declared transaction result as an input to classification.

The multi-node demonstration still uses scripted code to distribute the reference evidence.

That script is a demonstration mechanism, not a coordinator-free networking protocol.

### **No Continuous Internet Requirement for the Reference Implementations**

The supplied Python and browser implementations run locally after download.

A real distributed deployment would still require appropriate mechanisms for transport, storage, authentication, recovery, evidence exchange, and operational control.

---

## 🧠 **Why the Separation Matters**

A sequence-authoritative question is:

**Which declaration arrived first?**

The ORL structural question is:

**What validated canonical declarations are present under the current ruleset?**

A closure question is different again:

**Does this exact evidence set satisfy a declared boundary?**

An authorization question is different again:

**Is anyone permitted to act on the result?**

Keeping these questions separate makes the authority boundary explicit:

`collection != validation != resolution != closure != authorization != execution`

ORL v2.0.0 implements the structural path through bounded resolution and declared closure.

It deliberately stops before authorization and execution.

---

## 🌱 **ORL as a Core for Domain-Specific Systems**

ORL v2.0.0 is designed as a small structural foundation rather than a universal domain model.

Related ORL-family projects such as ORL-Money, ORL-Chat, and ORL-AI can define their own:

- supported schemas  
- semantic units  
- conflict rules  
- authority boundaries  
- closure conditions  
- domain-specific receipts  
- deployment constraints  

A domain project may reuse structural disciplines from ORL without inheriting claims that the ORL core does not make.

`shared structural discipline != shared domain authority`

This keeps the reusable mechanism separate from the correctness requirements of each application domain.

---

## 🧭 **Relationship to the Shunyaya Framework**

ORL applies a recurring Shunyaya structural discipline:

- validate before resolution  
- give evidence deterministic identity  
- preserve incompleteness instead of guessing  
- abstain when declared structure conflicts  
- make result reasons explicit  
- separate resolution from closure  
- separate structural outcomes from downstream authority  
- make important implementation claims executable and testable  

ORL remains a bounded reference implementation of these ideas rather than a claim that one structural method replaces every operational architecture.

---

## 🧪 **Appropriate Uses**

The current repository is appropriate for:

- deterministic structural-reconciliation research  
- canonical evidence-identity experiments  
- order-invariance testing  
- exact duplicate-absorption experiments  
- explicit incomplete/conflict classification  
- receipt-identity experiments  
- bounded closure research  
- disconnected or delayed-evidence demonstrations  
- cross-language deterministic implementation studies  
- education and prototyping  

Potential domain integrations require their own validated semantics and controls.

The current ORL core should not be treated directly as a production financial authority.

---

## 🚫 **Outside the Current Implementation Boundary**

ORL v2.0.0 does not implement or prove:

- source authenticity  
- cryptographic signatures  
- user or account identity  
- authorization  
- available funds  
- account ownership  
- fraud detection or prevention  
- general double-spend prevention  
- consensus  
- Byzantine fault tolerance  
- reliable broadcast  
- leader election  
- network dissemination correctness  
- payment execution  
- account posting  
- settlement  
- custody  
- regulatory compliance  
- universal evidence completeness  
- immutable external finality  
- universal order independence  
- production readiness  

These boundaries are part of the design, not omissions to be concealed by the resolver state names.

---

## 🔗 **Quick Links**

### 📘 **Documentation**

- [Quickstart](docs/Quickstart.md)
- [Architecture](docs/ORL_Core_Architecture.md)
- [FAQ](docs/FAQ.md)
- [Test Guide](docs/Test-Guide.md)
- [Structural Overview](docs/ORL-Structural-Overview.png)

### ⚡ **Reference Implementations**

- [Python Reference Kernel](demo/ORL_Reference_Kernel_v2_0_0.py)
- [Browser Structural Laboratory](demo/ORL_Structural_Lab_v2_0_0.html)

### 🔍 **Verification**

- [Verification Instructions](verify/VERIFY.md)
- [Frozen Demo Hashes](verify/FREEZE_DEMO_SHA256.txt)

### 📂 **Repository Structure**

- `demo/` — executable Python and browser reference implementations  
- `docs/` — conceptual, usage, and test documentation  
- `verify/` — verification instructions and released artifact identities  

---

## 📜 **License**

See [LICENSE](LICENSE) for the repository's current licensing terms.

The repository does not claim recognition as a formal technical standard.

---

## 🔗 **Related Shunyaya Projects**

- [Shunyaya Symbolic Mathematics Master Docs](https://github.com/OMPSHUNYAYA/Shunyaya-Symbolic-Mathematics-Master-Docs)
- [STOCRS](https://github.com/OMPSHUNYAYA/STOCRS)
- [SSUM-Time](https://github.com/OMPSHUNYAYA/SSUM-Time)

---

## 🌍 **Long-Horizon Research Direction**

The broader research question is not:

**Can order be removed from every system?**

It is:

**Which decisions genuinely require sequence as authority, and which bounded decisions can instead be reconstructed from validated canonical structure?**

Where a domain can define appropriate evidence, validation, conflict rules, closure conditions, and authority boundaries, structural resolution may allow some decisions to be reproduced independently of fragment arrival chronology.

Operational sequence, time, communication, authorization, and coordination may still remain essential elsewhere in the same system.

---

## ⭐ **One-Line Summary**

ORL v2.0.0 is a public bounded structural-reconciliation reference implementation in which supported fragments are strictly validated, canonically identified, deduplicated, deterministically classified into `RESOLVED`, `INCOMPLETE`, or `ABSTAIN`, projected only when resolved, bound to reproducible receipts, and optionally marked `SEALED` when the exact current canonical evidence set satisfies a declared boundary — while keeping authorization, consensus, settlement, immutable external finality, and production financial authority outside the implementation boundary.
