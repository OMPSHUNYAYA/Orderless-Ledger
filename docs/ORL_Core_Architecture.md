# 🧭 ORL Core Architecture

## Orderless Ledger v2.0.0

**Deterministic Structural Reconciliation Reference Architecture**

**Architecture Version: 2.0.0**

---

## 1. Purpose

ORL is a bounded structural-reconciliation reference implementation.

It separates the classification of declared transaction structure from fragment arrival order, clock metadata, and coordinator-selected result state.

The central implementation relation is:

`same validated canonical fragment set + same ruleset + same declared boundary context -> same bounded resolution bundle`

The architecture is designed around explicit boundaries:

`validation != resolution`

`resolution != projection`

`resolution != closure`

`closure != authorization`

`projection != posting`

`receipt != settlement`

ORL does not execute payments, establish authorization, verify ownership, determine available funds, provide consensus, or create immutable financial finality.

Its implemented responsibility is narrower:

`validated evidence -> deterministic bounded structural result`

---

## 2. Architectural Pipeline

The ORL v2.0.0 pipeline is:

`raw fragments`

`-> validate`

`-> canonicalize`

`-> accept OR refuse`

`-> deduplicate`

`-> group by transaction`

`-> resolve`

`-> project resolved effects`

`-> evaluate declared closure boundary`

`-> create transaction receipts`

`-> create bounded resolution bundle`

The resolver is entered only after the complete input batch passes validation.

A malformed or unsupported fragment is not converted into `INCOMPLETE` or silently ignored.

The batch instead produces:

`validation_state = REFUSED`

For an accepted batch:

`validation_state = ACCEPTED`

and each transaction receives one of three resolution states:

`RESOLVED`

`INCOMPLETE`

`ABSTAIN`

Closure is evaluated independently:

`OPEN`

or:

`SEALED`

---

## 3. Architecture Profiles

ORL v2.0.0 uses explicit profile identifiers.

| Architectural Role | Profile |
|---|---|
| Fragment schema | `ORL-FRAGMENT-2-D01` |
| Resolution rules | `ORL-RESOLUTION-2-D01` |
| Canonical framing | `ORL-CANON-1-D01` |
| Fragment-set identity | `ORL-FRAGMENT-SET-1-D01` |
| Transaction-evidence identity | `ORL-TX-EVIDENCE-1-D01` |
| Resolution receipt | `ORL-RECEIPT-1-D01` |
| Projection identity | `ORL-PROJECTION-1-D01` |
| Resolution bundle | `ORL-BUNDLE-1-D01` |
| Declared evidence boundary | `ORL-BOUNDARY-1-D01` |
| Refusal witness | `ORL-REFUSAL-1-D01` |
| Audit profile | `ORL-AUDIT-1-D01` |

The architecture version is:

`2.0.0`

The ruleset identity for the current release is:

`389eb1062a4cf7668450c475fd84c7611c3ab6c7c402f9e34ac37698fea09909`

A ruleset identity binds the declared resolver contract rather than the presentation layer.

---

## 4. Supported Fragment Contract

Every accepted fragment has exactly six fields:

`schema`

`tx`

`side`

`account`

`amount_minor`

`unit`

Example:

```text
{
  "schema": "ORL-FRAGMENT-2-D01",
  "tx": "ORL100",
  "side": "debit",
  "account": "Alice",
  "amount_minor": "500",
  "unit": "UNIT"
}
```

No additional semantic field is silently ignored.

The current exact-field rule is:

`accepted_fields = {schema, tx, side, account, amount_minor, unit}`

Therefore:

`missing required field -> REFUSED`

`unknown field -> REFUSED`

This keeps fragment identity and resolver meaning aligned.

---

## 5. Validation Boundary

Validation is a separate architectural lane.

### 5.1 Batch rule

The input must be an array of fragments.

`non-array batch -> REFUSED`

The current policy is:

`one invalid fragment -> REFUSE_WHOLE_BATCH`

The resolver never mixes accepted fragments with rejected fragments from the same input batch.

---

### 5.2 Field type rule

All six fragment fields must be strings.

Examples:

`amount_minor = "500" -> potentially valid`

`amount_minor = 500 -> REFUSED`

`amount_minor = true -> REFUSED`

This avoids language-dependent implicit coercion.

---

### 5.3 Text normalization

Accepted text is normalized using Unicode NFC before canonical identity is computed.

Conceptually:

`normalized_text = NFC(input_text)`

This allows canonically equivalent text representations to produce the same canonical fragment identity.

Normalization does not make unsupported syntax valid.

Validation rules are applied to the normalized values.

---

### 5.4 Transaction identifier

The current transaction identifier rules include:

- string value
- non-empty
- no leading or trailing whitespace
- no forbidden control characters
- maximum 128 UTF-8 bytes

The architecture does not assign financial or legal meaning to the identifier.

It is the structural grouping key within the declared resolver model.

Under the current schema, distinct real-world transfers must use distinct `tx` identifiers. Repeated canonically identical fragments under the same `tx` are treated as the same declaration after exact duplicate absorption.

---

### 5.5 Account identifier

The current account identifier rules include:

- string value
- non-empty
- no leading or trailing whitespace
- no forbidden control characters
- maximum 256 UTF-8 bytes

Account identifiers may contain ordinary separator characters because canonical framing does not rely on ambiguous delimiter concatenation.

---

### 5.6 Supported sides

The supported sides are exactly:

`debit`

`credit`

Therefore:

`unsupported side -> REFUSED`

An unsupported side cannot be silently ignored and cannot be reclassified as missing structure.

---

### 5.7 Exact amount domain

Amounts are represented as positive decimal integer strings:

`[1-9][0-9]{0,77}`

The current supported domain is therefore:

`1 to 78 decimal digits`

Examples:

`"1" -> valid`

`"500" -> valid`

`"9007199254740993" -> valid`

`"0" -> REFUSED`

`"-1" -> REFUSED`

`"1.0" -> REFUSED`

`"01" -> REFUSED`

The browser uses exact integer arithmetic rather than JavaScript floating-point arithmetic for projection values.

The Python implementation uses arbitrary-precision integer arithmetic.

The shared serialized representation remains the decimal string.

---

### 5.8 Unit identifier

The unit must match:

`[A-Z][A-Z0-9._:-]{0,31}`

Examples may include identifiers such as:

`UNIT`

`USD`

`ASSET_1`

The unit field is a declared structural identifier.

ORL does not independently establish the external economic, legal, or accounting meaning of a unit.

---

## 6. Refusal Model

Validation failure produces explicit refusal witnesses.

A refusal witness records:

- input index
- refusal code
- affected field where applicable
- detail where applicable
- deterministic refusal identity

The refusal profile is:

`ORL-REFUSAL-1-D01`

Examples of refusal conditions include:

`FRAGMENT_NOT_OBJECT`

`MISSING_REQUIRED_FIELD`

`UNKNOWN_FIELD`

`FIELD_NOT_STRING`

`UNSUPPORTED_SCHEMA`

`EMPTY_FIELD`

`EDGE_WHITESPACE`

`CONTROL_CHARACTER`

`FIELD_TOO_LONG`

`UNSUPPORTED_SIDE`

`INVALID_AMOUNT_MINOR`

`INVALID_UNIT`

The validation result is distinct from transaction resolution:

`REFUSED != INCOMPLETE`

`REFUSED != ABSTAIN`

A refused batch does not enter transaction resolution.

---

## 7. Canonical Byte Framing

ORL identities are computed from explicit canonical byte records rather than ambiguous delimiter-joined strings.

Each field is framed using UTF-8 byte lengths.

Conceptually:

`frame(label, value) = len_utf8(label) + ":" + label + len_utf8(value) + ":" + value`

A canonical record begins with its profile and then appends fields in a profile-defined order:

`canonical_record = frame("profile", profile) + ordered_field_frames`

The ordering of fields is determined by the profile implementation.

The insertion order of keys in an input object does not determine fragment identity.

This design prevents separator-bearing text from changing field boundaries.

For example, an account value containing:

`A|B:42`

remains one account value rather than being interpreted as additional structural fields.

---

## 8. Hash Identity Layer

ORL uses SHA-256 over canonical bytes to produce deterministic identities.

The architecture uses hash identities for reproducibility and structural comparison.

A matching hash demonstrates matching hashed bytes under the declared construction.

It does not by itself establish authorization, truth, legitimacy, or production safety.

---

## 9. Fragment Identity

A validated canonical fragment receives:

`fragment_id = SHA256(canonical_fragment_bytes)`

The fragment identity binds the current supported semantic fields:

`tx`

`side`

`account`

`amount_minor`

`unit`

under:

`ORL-FRAGMENT-2-D01`

Changing any supported semantic field changes the fragment identity.

Canonically equivalent NFC text produces the same canonical fragment identity.

---

## 10. Exact Duplicate Absorption

ORL deduplicates by canonical fragment identity.

For a validated fragment collection `E`:

`D(E) = unique fragments by fragment_id`

An exact duplicate therefore does not create multiplicity conflict.

Under the current schema, repeated canonically identical fragments under the same `tx` are treated as the same declaration.

ORL does not infer that two canonically identical fragments were intended to represent separate real-world movements. Distinct real-world transfers must therefore use distinct `tx` identifiers.

A future schema that needs to preserve multiple otherwise identical declarations within one transaction would require an additional distinguishing field.

The core idempotence relation is:

`D(E union E) = D(E)`

Duplicate absorption does not mean that declarations with merely similar content are merged.

Only exact canonical identity is absorbed.

---

## 11. Fragment-Set Identity

The current deduplicated evidence set receives an order-independent identity.

Let:

`F(E) = sorted(fragment_id values in D(E))`

Then conceptually:

`fragment_set_id = SHA256(canonical_fragment_set_record(F(E)))`

The fragment-set profile is:

`ORL-FRAGMENT-SET-1-D01`

For the current reference scenario:

`fragment_set_id = 7a37a07d4a83a0235199b2846da6a68d045d7dde458520fdf91c9504943b6a6f`

The intended invariant is:

`fragment_set_id(P(E)) = fragment_set_id(E)`

for any permutation `P(E)` of the same accepted fragment collection.

---

## 12. Transaction Grouping

After validation and deduplication, fragments are grouped by normalized transaction identifier:

`group(tx) = all unique accepted fragments with transaction identifier tx`

Transaction grouping does not consult:

- timestamp
- wall-clock time
- fragment arrival index
- coordinator decision state

The resolver classifies the present canonical transaction group under the fixed ruleset.

---

## 13. Deterministic Resolution Precedence

Each transaction group is classified according to explicit precedence.

The current precedence is:

`MULTIPLE_DEBITS_AND_CREDITS`

`> MULTIPLE_DEBITS`

`> MULTIPLE_CREDITS`

`> MISSING_DEBIT`

`> MISSING_CREDIT`

`> SELF_TRANSFER_UNSUPPORTED`

`> AMOUNT_MISMATCH`

`> UNIT_MISMATCH`

`> COMPATIBLE_PAIR`

The first applicable condition governs the result.

This removes ambiguity between missing structure and already-present conflict structure.

---

## 14. Resolution States and Reason Codes

### 14.1 RESOLVED

A transaction is `RESOLVED` when the deduplicated transaction group contains:

- exactly one debit
- exactly one credit
- different debit and credit accounts
- matching `amount_minor`
- matching `unit`

The reason code is:

`COMPATIBLE_PAIR`

Conceptually:

`one debit + one credit + compatible amount + compatible unit -> RESOLVED`

`RESOLVED` is a structural resolver state.

It does not mean:

- authorized
- funded
- settled
- immutable
- legally valid
- globally complete

---

### 14.2 INCOMPLETE

A transaction is `INCOMPLETE` when required supported structure is absent and no higher-priority multiplicity conflict is present.

Current reason codes include:

`MISSING_DEBIT`

`MISSING_CREDIT`

The resolver does not invent the missing declaration.

---

### 14.3 ABSTAIN

A transaction is `ABSTAIN` when the accepted structure contains a supported conflict or an unsupported resolution shape.

Current reason codes include:

`MULTIPLE_DEBITS_AND_CREDITS`

`MULTIPLE_DEBITS`

`MULTIPLE_CREDITS`

`SELF_TRANSFER_UNSUPPORTED`

`AMOUNT_MISMATCH`

`UNIT_MISMATCH`

The resolver does not silently choose one conflicting declaration.

---

## 15. Transaction-Evidence Identity

Each transaction receives an evidence identity built from:

- transaction identifier
- sorted fragment IDs belonging to that transaction

Conceptually:

`transaction_evidence_id = SHA256(canonical(tx + sorted transaction fragment IDs))`

The profile is:

`ORL-TX-EVIDENCE-1-D01`

This identity binds the evidence used for that transaction's current structural classification.

---

## 16. Resolution Receipts

Every resolved, incomplete, or abstaining transaction receives a deterministic receipt.

The receipt profile is:

`ORL-RECEIPT-1-D01`

A receipt binds:

- fragment schema profile
- ruleset profile
- ruleset identity
- transaction identifier
- transaction-evidence identity
- resolution state
- reason code
- resolved source account, when applicable
- resolved destination account, when applicable
- resolved amount, when applicable
- resolved unit, when applicable
- closure state
- closure reason
- boundary identity, when applicable

Conceptually:

`receipt_id = SHA256(canonical_receipt_fields)`

Receipt verification recomputes the canonical receipt identity and rejects tampered content.

A receipt is evidence of the declared resolver output under the bound structure and rules.

It is not:

- a payment authorization
- a signature of external truth
- a settlement confirmation
- a regulatory certificate

---

## 17. Resolved-Only Structural Projection

ORL computes a current structural projection only from `RESOLVED` transaction receipts.

The projection rule is:

`RESOLVED -> contributes declared debit and credit delta`

`INCOMPLETE -> zero projection contribution`

`ABSTAIN -> zero projection contribution`

For a resolved transfer:

`from_account -= amount_minor`

`to_account += amount_minor`

Projection arithmetic is exact integer arithmetic.

The projection is grouped by unit.

Accounts whose resulting delta is zero are omitted from the serialized projection.

The projection receives:

`projection_id = SHA256(canonical_projection_bytes)`

The projection profile is:

`ORL-PROJECTION-1-D01`

For the current reference scenario:

`projection_id = 9c714030a7a333a4018fc610a6e086e3b64a106a2cbc957b6b58a8253653c3ff`

A projection is a structural output of the current accepted evidence set.

It is not account posting or settlement.

---

## 18. Resolution Is Not Finality

A transaction can change state when additional valid evidence is appended.

For example:

`INCOMPLETE -> RESOLVED`

when a compatible missing counterpart appears.

A currently resolved transaction can later become conflicting:

`RESOLVED -> ABSTAIN`

Therefore:

`currently RESOLVED != permanently final`

ORL keeps closure separate from resolution for this reason.

---

## 19. Append-Only Evidence-Growth Model

Under the current fixed ruleset and append-only valid evidence model, the supported state transitions are constrained.

The tested transition envelope is:

`INCOMPLETE -> INCOMPLETE | RESOLVED | ABSTAIN`

`RESOLVED -> RESOLVED | ABSTAIN`

`ABSTAIN -> ABSTAIN`

The final relation is an absorbing-conflict property for the current resolver profile:

`ABSTAIN + additional valid append-only evidence -> ABSTAIN`

This property does not claim that every future ORL ruleset, evidence-removal model, revocation system, or remediation process must preserve the same transition relation.

The invariant applies to:

- the current ruleset
- accepted fragments
- append-only evidence growth
- no fragment removal
- no supersession mechanism
- no ruleset change

The current exhaustive evidence-growth audit verifies the declared transition constraints across the committed generated subset relationships.

---

## 20. Set-Algebra Properties

The bounded union layer is tested for three core properties.

### Idempotence

`D(E union E) = D(E)`

### Commutativity

`D(A union B) = D(B union A)`

### Associativity

`D((A union B) union C) = D(A union (B union C))`

These properties apply to accepted fragments under canonical exact-duplicate absorption.

They do not imply that every downstream domain operation is commutative or order-independent.

---

## 21. Permutation Invariance

For an accepted fragment collection `E`, a permutation `P(E)`, and the fixed current ruleset:

`R(P(E)) = R(E)`

The current reference implementation tests 120 permutations in both Python and browser audit paths.

The invariant applies to the bounded ORL resolver output for the same accepted canonical fragment set after exact duplicate absorption.

It does not claim that:

- network delivery is orderless
- historical records require no order
- execution has no sequence
- all ledger architectures are order-independent

The precise architectural claim is:

`fragment arrival order is not ORL resolution authority`

---

## 22. Multi-Node Same-Evidence Convergence

Nodes may begin with different local evidence.

Therefore, while evidence differs:

`E_i != E_j`

the resulting bounded snapshots are not required to match.

After nodes possess the same validated canonical fragment set and use the same ruleset:

`D(E_i) = D(E_j) AND ruleset_i = ruleset_j`

the deterministic structural relation is:

`R(E_i) = R(E_j)`

For equality of the complete bounded bundle, the declared boundary context must also match.

The reference demonstration verifies equality of final bounded bundle identity after each node receives the same reference evidence set under the same boundary state.

This is same-evidence deterministic convergence.

It is not:

- consensus
- reliable broadcast
- leader election
- Byzantine agreement
- network finality

ORL does not define how evidence must be transported between nodes.

---

## 23. Bounded Closure

Closure is a separate lane from transaction resolution.

The closure states are:

`OPEN`

`SEALED`

### 23.1 OPEN

A result is `OPEN` when:

- no valid declared boundary is supplied, or
- the current canonical fragment ID set does not exactly match the declared boundary

Common closure reasons include:

`NO_BOUNDARY`

`DECLARED_BOUNDARY_NOT_SATISFIED`

---

### 23.2 SEALED

A result becomes `SEALED` only when the current sorted canonical fragment ID set exactly matches a valid declared expected fragment ID set.

The relation is:

`current fragment ID set = declared expected fragment ID set -> SEALED`

The current closure reason is:

`DECLARED_BOUNDARY_SATISFIED`

`SEALED` means:

> the current canonical fragment set exactly satisfies the declared bounded evidence commitment.

It does not mean:

> no additional evidence exists anywhere.

This distinction is fundamental.

---

## 24. Boundary Identity

A declared boundary binds:

- fragment schema profile
- current ruleset identity
- expected fragment count
- sorted expected fragment IDs
- expected fragment-set identity

The boundary receives:

`boundary_id = SHA256(canonical_boundary_bytes)`

The boundary profile is:

`ORL-BOUNDARY-1-D01`

For the current reference scenario:

`boundary_id = ba855c228a92ea9414bc3b4ad354aba92f92e62c767b9f2535a0db3d2188806b`

Boundary validation rejects malformed, non-canonical, mismatched, or ruleset-incompatible boundary structures.

A subset does not seal against a larger declared boundary.

A superset does not seal against a smaller declared boundary.

---

## 25. Closure and Receipt Identity

Closure is included in each transaction receipt.

Therefore, the same transaction evidence can produce different receipt identities under:

`OPEN`

and:

`SEALED`

while the underlying transaction resolution state remains unchanged.

This is intentional.

It distinguishes:

`what the transaction structure resolves to`

from:

`whether the current overall evidence set satisfies a declared boundary`

Thus:

`same transaction evidence + different closure state -> different receipt identity`

The projection can remain unchanged while receipt and bundle identities change.

---

## 26. Bundle Identity

The final bounded resolution bundle binds:

- architecture version
- fragment schema profile
- ruleset profile
- ruleset identity
- fragment-set identity
- closure state
- closure reason
- boundary identity
- projection identity
- sorted transaction receipt identities

Conceptually:

`bundle_id = SHA256(canonical_bundle_fields)`

The profile is:

`ORL-BUNDLE-1-D01`

For the current reference scenario:

`open_bundle_id = 046d1de963dcb4b4ab05aeb4e7e81afaca56b9a8fceb6bb50f22d8c087c2d973`

`sealed_bundle_id = 857564e4e9f24a77ef1a9550e385d203c5e41e55b8fae624f37b82ee684c39f5`

The difference demonstrates that closure state is part of the bounded result identity.

---

## 27. Identity Hierarchy

The ORL identity hierarchy is:

`validated fragment`

`-> fragment_id`

`canonical transaction evidence`

`-> transaction_evidence_id`

`canonical unique fragment set`

`-> fragment_set_id`

`resolved-only structural projection`

`-> projection_id`

`declared evidence boundary`

`-> boundary_id`

`transaction result + closure`

`-> receipt_id`

`complete bounded result`

`-> bundle_id`

Each identity has a different scope.

No single hash is presented as proof of all system properties.

---

## 28. Current Reference Scenario

The committed reference scenario contains five transaction groups.

### ORL100

`debit Alice 500 UNIT`

`credit Bob 500 UNIT`

Result:

`RESOLVED`

Reason:

`COMPATIBLE_PAIR`

---

### ORL200

`debit Bob 300 UNIT`

`credit Dina 300 UNIT`

Result:

`RESOLVED`

Reason:

`COMPATIBLE_PAIR`

---

### ORL300

Only a credit declaration is present.

Result:

`INCOMPLETE`

Reason:

`MISSING_DEBIT`

---

### ORL400

Debit and credit amounts differ.

Result:

`ABSTAIN`

Reason:

`AMOUNT_MISMATCH`

---

### ORL500

One debit and two distinct credits are present.

Result:

`ABSTAIN`

Reason:

`MULTIPLE_CREDITS`

---

The reference summary is:

`R:2 I:1 A:2`

The resolved-only projection is:

`Alice = -500 UNIT`

`Bob = +200 UNIT`

`Dina = +300 UNIT`

The reference projection does not include `ORL300`, `ORL400`, or `ORL500`.

---

## 29. Structural Laboratory

The browser implementation includes an interactive Structural Laboratory.

The current actions demonstrate:

### Shuffle Evidence

`same evidence set + different input permutation -> same canonical bounded result`

### Add Exact Duplicate

`exact duplicate -> same canonical unique fragment set`

### Complete ORL300

`INCOMPLETE -> RESOLVED`

### Conflict ORL100

`RESOLVED -> ABSTAIN`

The earlier ORL100 projection contribution is removed from the new current structural projection.

### Add Evidence After Conflict

`ABSTAIN -> ABSTAIN`

under the current append-only valid evidence model.

### Inject Malformed Fragment

`invalid batch -> REFUSED`

The resolver is not entered.

### Declare and Seal Current Set

`exact current canonical set = declared boundary -> SEALED`

Evidence identity remains unchanged while closure-dependent receipt and bundle identities change.

### Reset Laboratory

The reference evidence set is restored with:

`closure = OPEN`

---

## 30. Cross-Engine Contract

ORL v2.0.0 provides:

- a Python reference kernel
- a browser Structural Laboratory

Both implementations use the same declared:

- fragment schema
- canonical framing
- normalization rule
- ruleset manifest
- exact amount representation
- identity construction
- resolution precedence
- projection rules
- receipt construction
- boundary semantics
- bundle construction

The browser audit contains frozen comparisons against identities reproduced by the Python implementation.

The current frozen cross-engine checks cover:

- ruleset identity
- reference fragment-set identity
- open bundle identity
- boundary identity
- sealed bundle identity
- projection identity

The verified result is:

`CROSS_ENGINE_FROZEN 6/6 PASS`

Cross-engine equality strengthens reproducibility of the declared reference contract.

It is not independent third-party certification.

---

## 31. Current Audit Evidence

### Python reference kernel

Audit profile:

`ORL-AUDIT-1-D01`

Current verified result:

`TOTAL 272/272 PASS`

Groups:

- `VALIDATION 20/20 PASS`
- `CANONICALIZATION 8/8 PASS`
- `EXACT_AMOUNTS 5/5 PASS`
- `RESOLUTION 18/18 PASS`
- `DEDUPLICATION 3/3 PASS`
- `REFERENCE_SCENARIO 10/10 PASS`
- `PERMUTATION_INVARIANCE 120/120 PASS`
- `SET_ALGEBRA 3/3 PASS`
- `EVIDENCE_GROWTH 3/3 PASS`
- `EVIDENCE_GROWTH_EXHAUSTIVE 65/65 PASS`
- `CLOSURE 6/6 PASS`
- `RECEIPTS 7/7 PASS`
- `KNOWN_REGRESSIONS 4/4 PASS`

---

### Browser Structural Laboratory

Current verified result:

`TOTAL 286/286 PASS`

The browser includes all Python-side behavior groups plus:

- `INTERACTIVE_FLOWS 8/8 PASS`
- `CROSS_ENGINE_FROZEN 6/6 PASS`

The audit evidence supports the behavior tested by the committed suites.

It does not establish universal ledger correctness or production certification.

---

## 32. Permanent Regression Coverage

The current known-regression group permanently covers earlier structural weaknesses:

- unsupported side cannot be silently ignored
- multiple debits without a credit produce `ABSTAIN`
- multiple credits without a debit produce `ABSTAIN`
- separator-bearing account identifiers remain structurally safe

The browser interactive-flow group additionally covers:

- shuffle preserves canonical bounded result
- exact duplicate preserves canonical bounded result
- completing ORL300 resolves it
- conflicting ORL100 causes abstention
- conflict removes ORL100 projection contribution
- additional append-only evidence preserves existing abstention
- malformed laboratory input is refused
- declaring the current exact set seals without changing evidence identity

---

## 33. Authority Separation

ORL deliberately separates structural resolution from surrounding system authorities.

| Concern | ORL v2.0.0 Authority |
|---|---|
| Fragment syntax validation | Implemented |
| Canonical fragment identity | Implemented |
| Exact duplicate absorption | Implemented |
| Transaction structural classification | Implemented |
| Resolved-only structural projection | Implemented |
| Resolution receipts | Implemented |
| Declared bounded closure | Implemented |
| Bundle identity | Implemented |
| Timestamp authority | Not used by resolver |
| Fragment arrival-order authority | Not used by resolver |
| Coordinator-selected result authority | Not used by resolver |
| Identity authentication | Not implemented |
| Cryptographic signatures | Not implemented |
| Account ownership verification | Not implemented |
| Transaction authorization | Not implemented |
| Available-funds verification | Not implemented |
| Fraud-control authority | Not implemented |
| Network dissemination | Not implemented |
| Consensus | Not implemented |
| Byzantine fault tolerance | Not implemented |
| Reliable broadcast | Not implemented |
| Account posting | Not implemented |
| Payment execution | Not implemented |
| Settlement | Not implemented |
| Regulatory compliance authority | Not implemented |
| Immutable global finality | Not implemented |

This boundary is intentional.

A production-domain system may place ORL-like structural reconciliation inside a larger authenticated and authorized architecture, but those surrounding controls are not supplied by the ORL core.

---

## 34. Deployment Interpretation

The reference architecture may be studied for use in domains where:

- evidence can be represented as validated bounded fragments
- duplicate observations are possible
- input arrival order should not silently decide structural classification
- incomplete structure must remain explicit
- conflicting structure should not be forced into a positive result
- deterministic evidence identities are useful
- bounded closure commitments can be declared separately from resolution

Any deployment beyond the reference model requires domain-specific analysis.

Production use may require, among other controls:

- authenticated evidence sources
- authorization policy
- durable storage
- key management
- transport security
- recovery procedures
- concurrency design
- dispute handling
- revocation or supersession rules
- operational monitoring
- regulatory and legal review
- independent security assessment

---

## 35. What ORL Does Not Claim

ORL v2.0.0 does not claim:

- universal ledger correctness
- universal order independence
- that time is unnecessary in every system
- that operational sequence disappears
- that communication disappears
- that coordination disappears
- general double-spend prevention
- authenticated truth of submitted fragments
- authorization
- available-funds correctness
- fraud prevention
- consensus
- Byzantine fault tolerance
- reliable broadcast
- settlement
- immutable global finality
- production readiness
- formal-standard status

The bounded implemented claim is:

`same validated canonical fragment set + same ruleset + same declared boundary context -> same bounded resolution bundle`

subject to the declared ORL v2.0.0 profiles and implementation boundary.

---

## 36. Relationship Between Evidence, Resolution, and Closure

The architecture can be summarized as three independent questions.

### Question 1: May this evidence enter the resolver?

`validation_state = ACCEPTED | REFUSED`

### Question 2: What does the accepted transaction structure currently support?

`resolution_state = RESOLVED | INCOMPLETE | ABSTAIN`

### Question 3: Does the complete current canonical set exactly satisfy a declared bounded commitment?

`closure_state = OPEN | SEALED`

These questions must not be collapsed.

A transaction may be:

`ACCEPTED + RESOLVED + OPEN`

or:

`ACCEPTED + RESOLVED + SEALED`

The first means compatible transaction structure is currently present without a satisfied declared evidence boundary.

The second means compatible transaction structure is present and the current full canonical fragment set exactly satisfies the declared bounded evidence commitment.

Neither state independently establishes authorization or settlement.

---

## 37. Compact Architectural Summary

ORL v2.0.0 can be expressed as:

`raw evidence`

`-> strict batch validation`

`-> NFC normalization`

`-> canonical length-framed bytes`

`-> SHA-256 fragment identities`

`-> exact duplicate absorption`

`-> order-independent fragment-set identity`

`-> deterministic transaction grouping`

`-> explicit resolution precedence`

`-> RESOLVED | INCOMPLETE | ABSTAIN`

`-> resolved-only exact projection`

`-> OPEN | SEALED bounded closure`

`-> deterministic transaction receipts`

`-> deterministic bundle identity`

The resulting architecture keeps operational and authority boundaries explicit:

`evidence identity != evidence authenticity`

`structural resolution != authorization`

`bounded closure != universal completeness`

`projection != posting`

`receipt != settlement`

---

## 38. External Technical Foundations

ORL uses established technical primitives for specific bounded purposes:

- Unicode NFC normalization for canonical text normalization
- UTF-8 byte encoding for canonical framing
- SHA-256 for deterministic digest identities

These primitives support reproducible representation and identity construction.

They do not provide the domain authorities that ORL explicitly leaves outside the core.

---

## ⭐ Final Architectural Relation

`same validated canonical fragment set + same ruleset + same declared boundary context -> same bounded resolution bundle`

ORL v2.0.0 implements this relation as a bounded, inspectable, cross-engine structural-reconciliation reference architecture with explicit validation, explicit incompleteness, conflict abstention, deterministic evidence identities, transaction receipts, exact projection, and separately declared bounded closure.
