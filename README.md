# ⭐ **ORL — Orderless Ledger**

**Deterministic • Order-Independent • Clock-Independent Resolution • Explicit Incompleteness • Demonstrated Conflict Abstention • Public Reference Implementation**

[![ORL Demo Verification](https://github.com/OMPSHUNYAYA/Orderless-Ledger/actions/workflows/verify.yml/badge.svg)](https://github.com/OMPSHUNYAYA/Orderless-Ledger/actions/workflows/verify.yml)

![ORL](https://img.shields.io/badge/ORL-Orderless%20Ledger-black)
![Deterministic](https://img.shields.io/badge/Resolution-Deterministic-green)
![Structure-Based](https://img.shields.io/badge/Resolution-Structure%20Based-purple)
![No-Time](https://img.shields.io/badge/Clock%20Metadata-Not%20Used-lightgrey)
![No-Order](https://img.shields.io/badge/Arrival%20Order-Not%20Authoritative-lightgrey)
![Conflict-Handling](https://img.shields.io/badge/Demonstrated%20Conflicts-Explicit%20Abstention-orange)
![Reference-Model](https://img.shields.io/badge/Implementation-Public%20Reference-blue)

**No timestamp authority • No arrival-order authority • No coordinator-state authority**

**No GPS • No NTP • No Internet Required to Run the Reference Demos**

---

**Same deduplicated supported fragment set + same resolver rules -> same bounded resolution**

**Using structural concepts developed within the Shunyaya Framework**

---

## 🧾 **One-Line Story**

From **SSUM-Time** — temporal continuity explored through structure  
to **STOCRS** — deterministic computation explored through complete structure  
to **ORL** — bounded ledger reconciliation explored through complete and compatible declarations:

ORL is a deterministic reference model in which independent nodes may begin with different fragments and produce the same resolver output after they possess the same supported fragment set.

---

## ⚡ **The Central Idea**

Many ledger systems use sequence, timestamps, logs, coordination, or consensus as part of their operational design.

ORL asks a narrower question:

> Can a bounded transaction structure be classified deterministically without using fragment arrival order or clock metadata as the authority over the result?

Within the declared reference model, the answer is yes.

ORL demonstrates that:

- incomplete fragments can remain visible without being guessed into completion  
- exact duplicates can be absorbed  
- supported fragment permutations can produce the same resolver output  
- conflicting declarations can produce an explicit abstention state  
- independently held fragments can be shared later  
- nodes with the same supported fragment set can reach the same bounded resolution snapshot  

The current result is not a claim that all ledgers can eliminate sequence, consensus, authorization, settlement, or operational coordination.

It is a focused demonstration that:

**arrival order does not have to govern every bounded reconciliation result**

---

## 🧭 **Visual Overview**

![ORL Structural Overview](docs/ORL-Structural-Overview.png)

The diagram presents the reference flow:

`local fragments -> bounded sharing -> structural classification -> identical resolver output`

The current demonstrations classify declared transaction fragments. They do not execute settlement, establish authorization, or provide immutable financial finality.

---

## ⚖️ **What ORL Is / Is Not**

### **ORL IS**

- a bounded structural ledger-reconciliation model  
- a deterministic resolver for the supported fragment schema  
- an order-invariance demonstration for supported fragment permutations  
- a multi-node same-evidence convergence demonstration  
- an explicit model of incomplete and conflicting transaction structure  
- a public reference implementation for structural resolution research  
- a domain application of broader Shunyaya structural principles  

### **ORL IS NOT**

- a full banking, accounting, payment, or settlement platform  
- a blockchain replacement claim  
- a consensus or Byzantine-fault-tolerance protocol  
- a network dissemination protocol  
- an authorization, identity, signature, custody, or fraud-control system  
- a proof that all ledger correctness is independent of order  
- an implementation of immutable transaction finality  
- a performance-superiority claim  
- a claim that real-world ordering, communication, or coordination disappears  

**The current architectural shift is bounded and precise:**

**transaction-fragment arrival order is separated from structural classification**

---

## 🧭 **Core Principle**

`bounded_resolution = resolve(supported_fragment_set, resolver_rules)`

For a supported fragment collection `E`, a supported permutation `P(E)`, and a fixed resolver version `v`:

`R_v(P(E)) = R_v(E)`

When two nodes hold the same deduplicated supported fragment set and use the same resolver rules:

`D(E_i) = D(E_j) -> R_v(E_i) = R_v(E_j)`

Where:

- `R_v` is the versioned resolver  
- `E` is a finite supported fragment collection  
- `P(E)` is a permutation of the same collection  
- `D(E)` is the exact-duplicate absorption step used by the current reference model  

This is a claim about the declared model and supported inputs.

It is not a universal theorem about every ledger architecture.

---

## ⚡ **What the Current Demonstration Establishes**

For the declared examples, the current Python and browser demonstrations exhibit the following behavior:

- three nodes can begin with different local fragments  
- the resolver does not read timestamps or wall-clock values  
- the resolver does not consult fragment arrival position when classifying the supported example transactions  
- exact duplicate entries are absorbed  
- matching declared debit and credit fragments can resolve  
- a missing counterpart remains `INCOMPLETE`  
- declared mismatch or multiplicity conflict can produce `ABSTAIN`  
- nodes given the same merged fragment set produce the same demonstrated state summary  

The current demonstrations assume well-formed example inputs.

They do not yet provide a complete validation layer for malformed identifiers, unsupported side values, invalid amount types, amount ranges, authorization, account ownership, or available funds.

---

## 🛡 **Resolution Compatibility Within the Declared Model**

ORL does not redefine debit and credit arithmetic.

For a supported example transaction containing one declared debit and one declared credit with matching amount values:

`declared_debit_amount = declared_credit_amount -> RESOLVED`

For missing supported structure:

`missing_counterpart -> INCOMPLETE`

For the conflict forms demonstrated by the current reference model:

`debit_credit_mismatch OR demonstrated_same_transaction_multiplicity_conflict -> ABSTAIN`

Other malformed, unsupported, or untested conflict forms remain outside the current conformance claim.

Only transactions classified as `RESOLVED` contribute to the demonstrated balance projection.

Transactions classified as `INCOMPLETE` or `ABSTAIN` do not contribute a balance effect in the reference demos.

This establishes explicit non-resolution for the demonstrated missing and conflicting cases.

It does not establish that every resolved input is authorized, legitimate, funded, final, or safe for real-world settlement.

---

## ⚡ **Why This Matters**

Distributed and intermittently connected systems often receive partial information.

A resolver that forces every partial state into a result can create ambiguity or conceal disagreement.

ORL instead preserves three distinct outcomes:

- enough compatible structure is present  
- required structure is still missing  
- declared structure conflicts  

This makes absence and conflict visible instead of allowing arrival sequence to silently choose a result.

Potential research value includes:

- deterministic reconciliation  
- disconnected record comparison  
- delayed evidence exchange  
- audit-oriented classification  
- replicated-state experiments  
- order-invariance testing  
- explicit refusal under incomplete or conflicting declarations  

---

## 🚀 **Quick Start**

Run the Python reference demo:

```text
python demo/orl_demo_reference.py
```

Or open the browser demonstration:

```text
demo/orl_demo_v3.html
```

### **Observe**

- different nodes begin with different fragments  
- no timestamp or wall-clock value is used by the resolver  
- exact duplicate fragments are absorbed  
- incomplete and conflicting transaction states remain explicit  
- the same merged fragment set produces the same demonstrated resolver output  

The intended observation is:

`same supported structure + same rules -> same bounded resolution`

---

## 🔗 **Quick Links**

### 📘 **Docs**

- [Quickstart](docs/Quickstart.md)
- [FAQ](docs/FAQ.md)
- [Test Guide](docs/Test-Guide.md)
- [Structural Overview](docs/ORL-Structural-Overview.png)

---

### ⚡ **Demos**

- [Python Reference Demo](demo/orl_demo_reference.py)
- [Visual Demo (HTML)](demo/orl_demo_v3.html)

---

### 🔍 **Verification**

- [Verify Instructions](verify/VERIFY.txt)
- [Demo Hash Freeze](verify/FREEZE_DEMO_SHA256.txt)

---

### 📂 **Repository**

- [demo/](demo/) — Python and browser reference demonstrations  
- [docs/](docs/) — conceptual and usage documentation  
- [verify/](verify/) — artifact-identity and reproducibility material  

---

## 🧩 **Structural Transaction Model**

In the current reference demonstrations, a transaction is represented by declared fragments rather than by their arrival sequence.

Example:

`ORL100 = {debit(Alice,500), credit(Bob,500)}`

The resolver does not ask:

**Which supported fragment arrived first?**

It asks:

**What supported fragments are present under this transaction identifier?**

For the declared model, the relevant structural questions are:

- Is a debit declaration present?  
- Is a credit declaration present?  
- Do the declared amount values match?  
- Are multiple incompatible debit or credit declarations present?  
- Is required structure missing?  

The current model is intentionally small. It does not establish source authenticity, authorization, sufficient funds, external completeness, or settlement finality.

---

## 🧭 **Three Resolution States**

- **RESOLVED** — the demonstrated required declarations are present and compatible  
- **INCOMPLETE** — a required counterpart declaration is missing  
- **ABSTAIN** — the demonstrated declarations contain a mismatch or multiplicity conflict  

### **Meaning**

- compatible supported structure resolves  
- missing supported structure is not guessed  
- conflicting supported structure is not forced  

These are resolver states, not legal, accounting, settlement, or regulatory conclusions.

---

## 🌐 **Canonical Demonstration**

### **Scenario**

- 3 independent node views  
- different local fragment collections  
- no shared global arrival order  
- no synchronized clock input  
- no coordinator result used by the resolver  
- a scripted bounded-sharing phase  
- identical resolver rules  

### **Outcome**

After every node receives the same demonstrated fragment collection, every node produces the same balance projection and transaction-state map.

The sharing phase makes evidence available.

It is not presented as:

- consensus  
- leader election  
- reliable broadcast  
- Byzantine agreement  
- network finality  
- settlement execution  

The current bounded claim is:

`same demonstrated fragment set + same resolver -> same demonstrated output`

---

## 📊 **Current Demo Result**

`R:2 I:1 A:2`

Meaning:

- 2 transactions are `RESOLVED`  
- 1 transaction is `INCOMPLETE`  
- 2 transactions are `ABSTAIN`  

### **Demonstrated Transactions**

- `ORL100` — resolves after its debit and credit fragments become jointly visible  
- `ORL200` — resolves after its differently distributed fragments become jointly visible  
- `ORL300` — remains incomplete because its counterpart is missing  
- `ORL400` — abstains because the declared debit and credit amounts differ  
- `ORL500` — abstains because one transaction identifier contains incompatible multiple-credit structure  

`ORL500` is a same-transaction multiplicity-conflict example.

It is not a complete demonstration of general double-spend prevention.

---

## 🔁 **Multi-Node Same-Evidence Convergence**

Each node begins with:

- a different local fragment collection  
- a different local visibility boundary  
- a different local resolution snapshot  

The current demonstration then distributes the union of the example fragments to every node.

After that sharing phase:

- supported matching structures resolve  
- supported missing structure remains incomplete  
- supported conflicts abstain  
- every node produces the same demonstrated snapshot  

The convergence condition is not merely that nodes waited long enough.

The relevant condition is:

`same deduplicated supported evidence + same rules -> same resolver output`

ORL does not claim convergence when nodes permanently hold materially different evidence.

---

## 🛡 **Explicit Incompleteness and Abstention**

ORL does not force every observed transaction identifier into a balance effect.

- **INCOMPLETE** preserves the fact that required demonstrated structure is absent  
- **ABSTAIN** preserves the fact that demonstrated structure is incompatible  

Within the current examples:

`INCOMPLETE OR ABSTAIN -> no demonstrated balance effect`

These states are protective resolver outcomes.

They are not proof that all undisclosed, malformed, fraudulent, or externally conflicting information has been detected.

---

## 🔎 **No Time / No Order / No Coordinator — Precise Meaning**

### **No Time as Resolution Authority**

The resolver does not use:

- timestamps  
- synchronized clocks  
- wall-clock time  
- GPS time  
- NTP state  

Time may still exist operationally outside the resolver.

### **No Arrival Order as Resolution Authority**

The supported transaction classification is based on the present demonstrated fragment collection rather than on which fragment arrived first.

Operational systems may still use logs, queues, sequence numbers, or ordered transport.

### **No Coordinator State as Resolution Authority**

The resolver does not accept a coordinator's decision as an input to classification.

The demonstration still uses scripted code to distribute fragments. That script is a test mechanism, not a consensus protocol.

### **No Continuous Internet Requirement**

The reference demos run locally after download.

Real distributed deployments would still require some mechanism for transport, storage, authentication, recovery, and evidence exchange.

---

## 📈 **Practical Meaning**

A sequence-authoritative question is:

**Which declaration arrived first?**

The ORL reference question is:

**What compatible supported declarations are present now?**

This distinction can matter when:

- fragments arrive through different channels  
- connectivity is intermittent  
- duplicate records are common  
- partial evidence must remain visible  
- conflicting declarations must not be silently collapsed  
- deterministic reconciliation is more important than arrival chronology  

---

## 🧠 **Why This Was Easy to Miss**

Many systems are naturally implemented through:

- event streams  
- transaction logs  
- ordered queues  
- synchronized services  
- replay pipelines  
- coordinator decisions  

These mechanisms are often operationally useful or necessary.

The ORL question is not whether they must disappear.

The question is whether arrival sequence must remain the sole authority over every bounded reconciliation result.

ORL separates:

`operational sequence != structural resolution authority`

---

## 🧭 **Relationship to the Shunyaya Framework**

ORL follows a recurring Shunyaya discipline:

- preserve the declared operational domain  
- make structural sufficiency explicit  
- keep incomplete structure unresolved  
- keep conflicting structure visible  
- separate observation, resolution, certification, and activation  
- state the implementation boundary precisely  

Representative progression:

- **SSUM-Time** — structural continuity without making wall-clock synchronization the sole authority  
- **STOCRS** — deterministic resolution from complete compatible computation structure  
- **ORL** — deterministic classification from complete compatible ledger declarations  

The current ORL repository is a bounded reference implementation of this direction.

---

## 🧪 **Appropriate Adoption Path**

### **Immediate Reference Uses**

- deterministic reconciliation experiments  
- order-invariance testing  
- duplicate-absorption demonstrations  
- partial-state classification  
- audit-oriented evidence comparison  
- disconnected-node teaching and research  
- structural-resolution prototyping  

### **Possible Integration Research**

- offline record reconciliation  
- distributed recovery tooling  
- replicated evidence comparison  
- telecom or device-state reconciliation  
- financial-state observation layers that remain separate from settlement  

### **Not Yet Appropriate**

- direct payment execution  
- custody or account posting  
- core banking finality  
- regulated settlement  
- fraud authorization  
- production consensus  
- safety-critical financial activation  

Any production-domain use requires independent validation, complete input rules, security controls, durable evidence, failure handling, and domain-specific authority.

---

## 🧠 **Determinism and Trust Boundary**

Within the declared demonstration, ORL is:

- deterministic  
- rule-based  
- non-probabilistic  
- locally executable  
- inspectable  
- reproducible for the supplied examples  

Trust should come from:

- explicit supported-input rules  
- frozen resolver behavior  
- assertion-based conformance tests  
- cross-implementation agreement  
- canonical serialization  
- versioned evidence  
- independent verification  

The current repository provides reference demonstrations and artifact hashes.

A file hash establishes artifact identity:

`same bytes -> same hash`

It does not by itself establish behavioral correctness:

`artifact identity != behavioral proof`

---

## 🛡 **Conflict Handling**

The reference model distinguishes:

- compatible demonstrated structure  
- missing demonstrated structure  
- conflicting demonstrated structure  

Its current purpose is to prevent the resolver from silently choosing among the demonstrated incompatible alternatives.

For the conflict forms included in the current demonstrations:

`declared amount mismatch OR demonstrated same-transaction multiplicity conflict -> ABSTAIN`

Other malformed, unsupported, or untested conflict shapes remain outside the current conformance claim.

This does not replace:

- cryptographic authenticity  
- identity verification  
- access control  
- authorization  
- funds validation  
- fraud detection  
- legal review  
- accounting controls  
- settlement controls  

---

## 📊 **Current Reference Boundary**

| Property | Current Reference Model |
|---|---|
| Supported fragment permutation changes the demonstrated resolver output | No |
| Timestamp or wall-clock input used by the resolver | No |
| Exact duplicate entry changes the demonstrated output | No |
| Missing counterpart state | `INCOMPLETE` |
| Demonstrated mismatch or multiplicity conflict | `ABSTAIN` |
| Only `RESOLVED` transactions affect demonstrated balances | Yes |
| Malformed-input validation fully specified and certified | No |
| Cross-language conformance fully certified | No |
| Authorization verified | No |
| Account ownership verified | No |
| Available funds verified | No |
| General double-spend prevention implemented | No |
| Consensus implemented | No |
| Network protocol implemented | No |
| Settlement executed | No |
| Immutable finality implemented | No |
| Production readiness claimed | No |

---

## 🧭 **Architectural Shift**

Sequence-authoritative model:

`arrival sequence -> selected result`

ORL reference model:

`present supported structure -> bounded classification`

A more complete deployment architecture would separate:

`collection -> validation -> resolution -> certification -> activation`

The current repository focuses on the resolution demonstration.

---

## 🔐 **Future Direction — ORL Structural Closure**

A transaction can appear resolved under currently visible fragments and later become conflicting when new fragments arrive.

Therefore:

`currently RESOLVED != permanently final`

A future ORL extension can add a separate closure lane:

`resolution_state = RESOLVED | INCOMPLETE | ABSTAIN`

`closure_state = OPEN | SEALED`

A certified outcome would reach structural finality within its declared evidence boundary only when:

`STRUCTURALLY_FINAL iff RESOLVED AND SEALED AND EVIDENCE_ROOT_VERIFIED`

This future direction can preserve the existing resolver state while making evidence-boundary closure explicit.

A possible certificate form is:

`ORLCERT = hash(schema_version, ruleset_version, transaction_id, canonical_fragment_root, resolution_state, closure_state)`

This structural-closure model is not implemented by the current public demos.

---

## 🔍 **Verification Model**

The repository currently provides two distinct verification layers.

### **Artifact Identity**

[Demo Hash Freeze](verify/FREEZE_DEMO_SHA256.txt) allows the committed demonstration files to be checked for byte identity.

`artifact bytes -> SHA-256 identity`

### **Demo Execution**

[Verify Instructions](verify/VERIFY.txt) describe how to run the supplied reference material.

`supplied demo -> observable reference output`

A stronger future verification release should additionally include:

- assertion-based expected outputs  
- permutation conformance vectors  
- malformed-input refusal vectors  
- Python and browser cross-engine equality tests  
- canonical serialization  
- versioned resolver receipts  
- independent certificate reconstruction  

Until those layers are committed, the workflow badge should be read as evidence that the configured reference verification process completed, not as universal proof of ledger correctness.

---

## 📜 **License**

See: [LICENSE](LICENSE)

The repository is a publicly available reference implementation under its stated license terms.

Architecture documentation is subject to the licensing terms declared in the repository, including CC BY-NC 4.0 where stated.

The repository does not claim recognition as a formal technical standard.

---

## 🔗 **Related Projects**

**STOCRS**  
https://github.com/OMPSHUNYAYA/STOCRS

**SSUM-Time**  
https://github.com/OMPSHUNYAYA/SSUM-Time

---

## 🌍 **Long-Horizon Implication**

Where a domain can define complete, compatible, authenticated, and independently verifiable structure, some resolution decisions may be separated from:

- fragment arrival order  
- wall-clock synchronization  
- continuous connectivity  
- coordinator-selected truth  

Operational sequence, transport, and coordination may still remain necessary.

The long-horizon opportunity is not:

**remove order from every system**

It is:

**identify where order is operational and where structure can safely govern bounded resolution**

---

## ⭐ **One-Line Summary**

ORL is a public reference model demonstrating that independent nodes can begin with different supported transaction fragments and, after receiving the same deduplicated fragment set, produce the same deterministic bounded resolution without using timestamps, fragment arrival order, GPS, NTP, or coordinator state as the authority over classification — while preserving explicit `INCOMPLETE` and `ABSTAIN` outcomes and making clear that authorization, consensus, settlement, and immutable finality remain outside the current implementation.
