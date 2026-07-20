# ⭐ **FAQ — ORL (Orderless Ledger)**

**Validated Canonical Evidence • Deterministic Structural Resolution • Reproducible Receipts • Bounded Closure**

**ORL v2.0.0**

---

`same validated canonical fragment set + same ruleset + same declared boundary context -> same bounded resolution bundle`

ORL is a bounded structural-reconciliation reference implementation developed within the Shunyaya Framework.

It separates:

`validation != resolution`

`resolution != closure`

`closure != authorization`

`projection != settlement`

---

## **SECTION A — Purpose and Positioning**

### **A1. What is ORL?**

ORL, or Orderless Ledger, is a deterministic reference implementation for bounded structural reconciliation.

It accepts a declared supported fragment schema, validates the complete input batch, canonicalizes valid evidence, absorbs exact canonical duplicates, classifies transaction structure, computes a resolved-only structural projection, evaluates the declared closure boundary, issues deterministic receipts, and produces a bounded resolution bundle.

The processing path is:

`raw fragments -> validate -> canonicalize -> deduplicate -> resolve -> project -> evaluate declared closure boundary -> receipt -> bundle`

ORL is not a complete financial ledger, payment network, settlement system, consensus protocol, or banking platform.

---

### **A2. What problem does ORL explore?**

Distributed and intermittently connected systems can receive:

- partial declarations  
- delayed declarations  
- exact duplicates  
- differently ordered inputs  
- incompatible declarations  
- malformed or unsupported inputs  

ORL explores whether a bounded supported evidence set can be classified deterministically without using fragment arrival order or clock metadata as the authority over the classification result.

The current implementation demonstrates that behavior for its declared schema, ruleset, canonicalization model, and committed test vectors.

---

### **A3. What does "orderless" mean in ORL?**

It means fragment arrival position is not an input to the current structural classification rules.

For a validated supported fragment collection `E`, a supported permutation `P(E)`, and the same fixed ruleset:

`R(P(E)) = R(E)`

The committed audit checks all:

`5! = 120`

permutations of a frozen conformance vector.

Operational order may still exist in transport, logs, queues, replay, history, execution, auditing, or settlement workflows.

ORL does not claim that every real system can eliminate sequence.

---

### **A4. Is ORL anti-time?**

No.

The current resolver does not use timestamps, synchronized clocks, GPS time, NTP state, or wall-clock values as classification inputs.

Time may still be required for:

- history  
- monitoring  
- reporting  
- legal sequencing  
- expiration  
- transport  
- operations  

The precise statement is:

`clock metadata is not structural resolution authority in the declared ORL resolver`

---

### **A5. Is ORL anti-coordination?**

No.

The resolver does not accept a coordinator's declared result as its structural classification authority.

A real deployment may still require coordination for transport, replication, access control, governance, recovery, execution, or settlement.

---

### **A6. What is the core idea in one line?**

`same validated canonical fragment set + same ruleset + same declared boundary context -> same bounded resolution bundle`

---

### **A7. Is ORL a banking or accounting system?**

No.

ORL does not provide:

- banking  
- bookkeeping authority  
- payment execution  
- settlement  
- account posting  
- custody  
- authorization  
- regulatory compliance  

It is a bounded structural-reconciliation reference implementation.

---

### **A8. Is ORL only relevant to finance?**

No.

The reusable architectural pattern is broader:

`validate evidence -> identify canonical structure -> classify complete or conflicting structure -> preserve explicit unresolved states -> issue reproducible evidence`

Possible research domains include reconciliation, disconnected records, replicated evidence comparison, device state, audit-oriented classification, recovery tooling, and other bounded structural-resolution problems.

Each domain requires its own schema, rules, security model, and authority boundary.

---

### **A9. Is ORL production ready?**

No production-readiness claim is made.

The current implementation is suitable as a reference model, executable specification, research prototype, conformance target, and structural-reconciliation demonstration.

Production use would require additional domain-specific controls including authentication, authorization, durable storage, recovery, operational security, governance, and independent review.

---

## **SECTION B — Architecture and State Separation**

### **B1. What are the three main state lanes?**

ORL keeps three state categories separate:

`validation_state = ACCEPTED | REFUSED`

`resolution_state = RESOLVED | INCOMPLETE | ABSTAIN`

`closure_state = OPEN | SEALED`

These states answer different questions.

---

### **B2. What does validation answer?**

Validation asks:

`is this input batch admitted into the resolver?`

A malformed or unsupported batch is:

`REFUSED`

A fully valid supported batch is:

`ACCEPTED`

---

### **B3. What does resolution answer?**

Resolution asks:

`what does the currently admitted transaction structure classify as under the fixed ruleset?`

The result is one of:

- `RESOLVED`  
- `INCOMPLETE`  
- `ABSTAIN`  

---

### **B4. What does closure answer?**

Closure asks:

`does the current canonical fragment-ID set exactly match an explicitly declared evidence boundary?`

The result is:

- `OPEN`  
- `SEALED`  

Closure does not determine authorization or settlement.

---

### **B5. Why are these states separated?**

Because these statements are not equivalent:

`input is valid`

`transaction structure resolves`

`declared evidence boundary is satisfied`

`transaction is authorized`

`transaction is settled`

ORL intentionally refuses to collapse them into one status.

---

## **SECTION C — Supported Fragment Contract and Validation**

### **C1. What is the current fragment schema?**

The active fragment schema is:

`ORL-FRAGMENT-2-D01`

Each fragment contains exactly:

- `schema`  
- `tx`  
- `side`  
- `account`  
- `amount_minor`  
- `unit`  

---

### **C2. What side values are supported?**

The current schema supports:

`debit`

`credit`

Unsupported side values are refused before resolution.

---

### **C3. What is the batch validation policy?**

The current policy is strict:

`any invalid fragment -> REFUSE_WHOLE_BATCH`

A refused batch does not enter the transaction resolver.

---

### **C4. Why refuse the whole batch?**

Because silently ignoring malformed structure can create a false picture of what evidence was actually submitted.

For example, an unsupported third declaration must not disappear while the remaining fragments are treated as a clean resolved pair.

The strict policy makes invalid structure explicit.

---

### **C5. What invalid inputs are covered by the audit?**

The current audit includes checks for:

- non-array batches  
- non-object fragments  
- missing required fields  
- unknown fields  
- unsupported schema identifiers  
- unsupported sides  
- non-string amounts  
- zero amounts  
- negative amounts  
- decimal amounts  
- leading zeros  
- amounts longer than 78 digits  
- empty identifiers  
- edge whitespace  
- control characters  
- lowercase units  
- invalid unit separators  

---

### **C6. Does ORL validate authorization, ownership, or funds?**

No.

Structural validation is not financial authorization.

The current validator does not establish:

- identity  
- source authenticity  
- account ownership  
- signature validity  
- available funds  
- legal permission  
- fraud absence  

---

## **SECTION D — Canonicalization and Evidence Identity**

### **D1. What is canonicalization?**

Canonicalization converts supported valid structure into a deterministic byte representation before identity is computed.

The active canonicalization profile is:

`ORL-CANON-1-D01`

---

### **D2. Why does ORL use explicit length framing?**

To avoid ambiguous delimiter-based serialization.

Values containing characters such as `|` or `:` remain safe because field identity does not depend on splitting an ad hoc concatenated string.

---

### **D3. Does field insertion order affect fragment identity?**

No.

Canonical construction uses the declared schema field order rather than object insertion order.

The browser audit explicitly checks this behavior.

---

### **D4. How is Unicode handled?**

Supported text is normalized using Unicode NFC before canonical identity is computed.

The audit verifies that canonically equivalent NFC and NFD text collapse to the same canonical fragment identity.

---

### **D5. What identities does ORL compute?**

The current implementation computes deterministic SHA-256 identities for:

- canonical fragments  
- canonical deduplicated fragment sets  
- per-transaction evidence sets  
- structural projections  
- resolution receipts  
- declared boundaries  
- complete resolution bundles  

---

### **D6. What does a content identity prove?**

It identifies canonical content under the declared profile.

It does not prove:

- who created the content  
- whether it was authorized  
- whether it is truthful  
- whether it is legally valid  

`content identity != external authenticity`

---

## **SECTION E — Deduplication and Set Algebra**

### **E1. What counts as an exact duplicate?**

Two supported fragments are exact canonical duplicates when they produce the same canonical fragment identity.

Under the current schema, repeated canonically identical fragments under the same `tx` are treated as the same declaration.

`same canonical declaration repeated under the same tx -> exact duplicate`

---

### **E2. What happens to exact duplicates?**

They are absorbed.

The implemented policy is:

`ABSORB_EXACT_CANONICAL_DUPLICATES`

An exact duplicate does not create a false multiplicity conflict.

ORL does not infer that two canonically identical fragments were intended to represent separate real-world movements. Distinct real-world transfers must therefore use distinct `tx` identifiers.

A future schema that needs to preserve multiple otherwise identical declarations within one transaction would require an additional distinguishing field.

---

### **E3. What set-algebra properties are tested?**

The committed audits check:

`D(A union B) = D(B union A)`

`D(E union E) = D(E)`

`D((A union B) union C) = D(A union (B union C))`

These are implementation invariants for the declared canonical-fragment model.

---

## **SECTION F — Resolution Rules**

### **F1. What is the active ruleset profile?**

`ORL-RESOLUTION-2-D01`

---

### **F2. When does a transaction resolve?**

A transaction resolves when the deduplicated supported structure contains:

- exactly one debit  
- exactly one credit  
- different declared accounts  
- matching exact `amount_minor` values  
- matching declared units  

The reason code is:

`COMPATIBLE_PAIR`

---

### **F3. What produces `INCOMPLETE`?**

The current reasons are:

`MISSING_DEBIT`

`MISSING_CREDIT`

The resolver does not invent the missing counterpart.

---

### **F4. What produces `ABSTAIN`?**

The current reasons are:

`MULTIPLE_DEBITS_AND_CREDITS`

`MULTIPLE_DEBITS`

`MULTIPLE_CREDITS`

`SELF_TRANSFER_UNSUPPORTED`

`AMOUNT_MISMATCH`

`UNIT_MISMATCH`

---

### **F5. Why is conflict precedence explicit?**

Because the same fragment group can satisfy more than one broad description such as "missing counterpart" and "multiple declarations."

An explicit precedence prevents implementation ambiguity.

---

### **F6. Is `RESOLVED` the same as authorized or settled?**

No.

`RESOLVED` means only that the admitted supported transaction structure is compatible under the active structural rules.

It does not mean:

- authenticated  
- authorized  
- funded  
- executed  
- posted  
- settled  
- legally final  

---

## **SECTION G — Exact Amounts and Units**

### **G1. How are amounts represented?**

The canonical representation is:

`amount_minor = positive decimal integer string`

The current profile supports 1 to 78 digits.

---

### **G2. Does ORL use floating-point arithmetic for supported amounts?**

No.

Python uses arbitrary-precision integer arithmetic.

The browser uses `BigInt` for projection arithmetic.

---

### **G3. Why is this important?**

It avoids binary floating-point rounding differences for the supported exact amount domain.

The audit includes:

- an amount above the JavaScript safe-integer boundary  
- a 78-digit exact amount  

---

### **G4. Does `amount_minor` imply a specific currency?**

No.

The meaning is determined by the declared `unit` and any domain-specific profile built above the ORL core.

---

## **SECTION H — Structural Projection**

### **H1. Which transactions affect the projection?**

Only `RESOLVED` transactions.

`RESOLVED -> projection contribution`

`INCOMPLETE OR ABSTAIN -> no projection contribution`

---

### **H2. What happens if a resolved transaction later becomes conflicting?**

The current projection is recomputed from the current admitted evidence set.

Therefore:

`RESOLVED -> ABSTAIN`

removes the earlier transaction contribution from the newly computed structural projection.

This does not claim that an executed payment was reversed.

---

### **H3. Is the projection a ledger balance or settlement result?**

No.

It is a bounded deterministic structural projection over the currently resolved subset.

---

## **SECTION I — Deterministic Receipts**

### **I1. What is an ORL receipt?**

A deterministic receipt binds a transaction result to the current declared structural context.

The active receipt profile is:

`ORL-RECEIPT-1-D01`

---

### **I2. What does a receipt include?**

The current receipt binds fields including:

- schema profile  
- ruleset profile  
- ruleset identity  
- transaction identifier  
- transaction evidence identity  
- state  
- reason code  
- resolved endpoints and amount when applicable  
- closure state  
- closure reason  
- boundary identity when applicable  

---

### **I3. Can receipts be verified?**

Yes, against the declared deterministic receipt construction.

The audit verifies all five reference receipts and rejects a tampered receipt.

---

### **I4. Do open and sealed states produce the same receipt identity?**

No.

Closure information is receipt-bound.

The audit confirms that open and sealed receipt identities differ.

---

### **I5. Does a valid ORL receipt prove external authenticity?**

No.

It proves deterministic agreement with the declared receipt construction, not identity, authorization, source authenticity, or legal validity.

---

## **SECTION J — Bounded Structural Closure**

### **J1. What is structural closure in ORL?**

Closure is a separate lane that compares the current canonical fragment-ID set with an explicitly declared exact boundary.

The active boundary profile is:

`ORL-BOUNDARY-1-D01`

---

### **J2. When is closure `OPEN`?**

Closure is `OPEN` when:

- no boundary is declared  
- the declared boundary is invalid  
- the current canonical set does not exactly match the declared expected set  

---

### **J3. When is closure `SEALED`?**

Closure is `SEALED` only when:

`current canonical fragment IDs = declared expected fragment IDs`

---

### **J4. Does `SEALED` mean no other evidence exists anywhere?**

No.

The precise meaning is:

`SEALED = declared exact boundary satisfied`

It is not a proof of universal completeness.

---

### **J5. Can a subset or superset satisfy the wrong boundary?**

No under the declared exact-set policy.

The audit checks that:

- a subset does not seal against a larger boundary  
- a superset does not seal against a smaller boundary  

---

## **SECTION K — Evidence-Growth State Model**

### **K1. Can transaction states change as valid evidence grows?**

Yes.

Under the current append-only valid-evidence model:

`INCOMPLETE -> INCOMPLETE | RESOLVED | ABSTAIN`

`RESOLVED -> RESOLVED | ABSTAIN`

`ABSTAIN -> ABSTAIN`

---

### **K2. Why can `RESOLVED` become `ABSTAIN`?**

Because additional valid evidence can reveal an incompatible declaration that was not previously present.

Therefore:

`currently RESOLVED != permanently final`

---

### **K3. Why is `ABSTAIN` absorbing in the current append-only profile?**

Because once incompatible canonical evidence is present, merely adding more evidence does not remove the already admitted conflict.

Changing that outcome would require a separate removal, revocation, supersession, or remediation model, which the current ORL core does not implement.

---

### **K4. How extensively is this tested?**

Both Python and browser audits include:

- 3 direct evidence-growth checks  
- 65 exhaustive subset-to-superset transition checks over the frozen growth corpus  

---

## **SECTION L — Multi-Node Demonstration**

### **L1. Why are three nodes used?**

They demonstrate different local evidence views.

Before sharing, local outputs may differ because the evidence sets differ.

---

### **L2. When do the nodes match?**

After every node receives the same deduplicated canonical fragment set, uses the same ruleset, and has no declared boundary:

`same canonical evidence + same ruleset + same no-boundary context -> same open bundle`

If the same exact declared boundary is also satisfied:

`same canonical evidence + same ruleset + same boundary -> same sealed bundle`

---

### **L3. Is the sharing mechanism consensus?**

No.

It is a demonstration harness.

The repository does not implement:

- consensus  
- reliable broadcast  
- leader election  
- Byzantine agreement  
- network finality  

---

## **SECTION M — Reference Scenario**

### **M1. What is the frozen reference result?**

`R:2 I:1 A:2`

---

### **M2. What are the five transaction results?**

- `ORL100 -> RESOLVED / COMPATIBLE_PAIR`  
- `ORL200 -> RESOLVED / COMPATIBLE_PAIR`  
- `ORL300 -> INCOMPLETE / MISSING_DEBIT`  
- `ORL400 -> ABSTAIN / AMOUNT_MISMATCH`  
- `ORL500 -> ABSTAIN / MULTIPLE_CREDITS`  

---

### **M3. What is the reference structural projection?**

```text
UNIT
  Alice  -500
  Bob    +200
  Dina   +300
```

`ORL300`, `ORL400`, and `ORL500` do not contribute.

---

## **SECTION N — Structural Laboratory**

### **N1. What is the browser Structural Laboratory?**

It is an interactive browser implementation of the ORL v2.0.0 core contract.

It lets a user modify the evidence set and observe invariants, state changes, refusal, projection changes, and bounded closure.

---

### **N2. What does Shuffle Evidence demonstrate?**

`same canonical evidence + unchanged ruleset and closure context -> same bundle`

when only the input permutation changes.

---

### **N3. What does Add Exact Duplicate demonstrate?**

`exact duplicate -> absorbed`

The raw input count increases while the canonical unique evidence set remains unchanged.

---

### **N4. What does Complete ORL300 demonstrate?**

`INCOMPLETE -> RESOLVED`

when the compatible missing counterpart is added.

---

### **N5. What does Conflict ORL100 demonstrate?**

`RESOLVED -> ABSTAIN`

and the previous ORL100 contribution disappears from the recomputed current projection.

---

### **N6. What does Add Evidence After Conflict demonstrate?**

`ABSTAIN -> ABSTAIN`

under the current append-only valid-evidence profile.

---

### **N7. What does Inject Malformed Fragment demonstrate?**

`invalid fragment -> REFUSED`

The strict batch policy prevents the resolver from silently ignoring unsupported structure.

---

### **N8. What does Declare + Seal Current Set demonstrate?**

`OPEN -> SEALED`

when the exact current valid canonical fragment set is explicitly declared as the boundary.

The evidence identity itself does not change merely because a matching boundary is declared.

---

## **SECTION O — Python and Browser Contract**

### **O1. Are the Python and browser implementations intended to match?**

Yes.

They implement the same declared:

- fragment schema  
- canonical framing  
- normalization rule  
- exact amount domain  
- duplicate policy  
- conflict precedence  
- projection construction  
- receipt construction  
- boundary construction  
- bundle construction  

---

### **O2. What cross-engine checks are committed?**

The browser audit compares six frozen identities with the Python reference outputs.

Current result:

`CROSS_ENGINE_FROZEN 6/6 PASS`

---

### **O3. Does that count as independent third-party verification?**

No.

It is frozen cross-engine conformance between the two committed reference implementations.

A separately implemented independent verifier is not claimed by the current ORL v2.0.0 core release unless one is explicitly added and documented.

---

## **SECTION P — Audits and Verification**

### **P1. What is the Python audit result?**

`TOTAL 272/272 PASS`

---

### **P2. What is the browser audit result?**

`ORL AUDIT TOTAL 286/286 PASS`

---

### **P3. What does the Python audit cover?**

It covers:

- validation  
- canonicalization  
- exact amounts  
- resolution  
- deduplication  
- reference scenario  
- 120 permutation checks  
- set algebra  
- evidence growth  
- 65 exhaustive growth checks  
- closure  
- receipts  
- known regressions  

---

### **P4. What additional coverage does the browser include?**

The browser adds:

`INTERACTIVE_FLOWS 8/8 PASS`

`CROSS_ENGINE_FROZEN 6/6 PASS`

---

### **P5. What are the permanent known regressions?**

They verify that:

- unsupported sides cannot be silently ignored  
- multiple debits without a credit abstain  
- multiple credits without a debit abstain  
- separator-bearing account identifiers remain safe under canonical framing  

---

### **P6. What does a passing audit prove?**

It shows that the tested implementation behavior matched the declared assertions and committed vectors during that run.

It does not prove universal ledger correctness, production safety, authorization, consensus, settlement, or regulatory suitability.

---

### **P7. What does a SHA-256 file hash establish?**

`same bytes -> same SHA-256 hash`

A matching SHA-256 value confirms that the checked artifact reproduces the recorded release digest.

It does not by itself establish behavioral correctness.

`artifact digest agreement != behavioral proof`

---

## **SECTION Q — ORL Family Direction**

### **Q1. How does this core relate to ORL-Money, ORL-Chat, and ORL-AI?**

ORL v2.0.0 is designed as a reusable structural foundation.

Domain-specific ORL-family systems can build their own schemas and rules above the same broader discipline:

`validate -> canonicalize -> resolve -> preserve explicit unresolved states -> produce inspectable evidence`

They should not silently inherit financial semantics from the ORL core when their domain is different.

---

### **Q2. Will every ORL-family project use identical rules?**

No.

Each domain should define its own supported structure, state semantics, conflict rules, and authority boundary.

The reusable part is the structural discipline, not one universal domain resolver.

---

## **SECTION R — Safety and Claim Boundary**

### **R1. What does ORL not verify?**

The current core does not verify:

- identity  
- authentication  
- signatures  
- authorization  
- account ownership  
- available funds  
- fraud absence  
- legal validity  
- regulatory compliance  
- settlement completion  
- universal evidence completeness  

---

### **R2. Is ORL a blockchain replacement?**

No.

ORL does not implement:

- consensus  
- block production  
- replicated finality  
- Byzantine fault tolerance  
- network dissemination  
- token economics  

---

### **R3. Does ORL solve double spending?**

No general double-spend-prevention claim is made.

The current resolver can expose declared multiplicity conflicts within its bounded supported evidence set.

That is not equivalent to a complete system-wide double-spend solution.

---

### **R4. Does `SEALED` mean immutable financial finality?**

No.

`SEALED` means only that the current canonical fragment-ID set exactly satisfies a declared boundary under the current profile.

---

### **R5. Does ORL guarantee no silent corruption?**

No universal guarantee is claimed.

The implementation provides explicit behavior for its declared supported and invalid inputs, including strict refusal and tested conflict handling.

Unknown external conditions remain outside the bounded claim.

---

## **SECTION S — Skeptic Questions**

### **S1. Is ORL just "wait until all data arrives"?**

No universal completeness detector is assumed.

The resolver classifies the currently admitted evidence as:

- `RESOLVED`  
- `INCOMPLETE`  
- `ABSTAIN`  

A separate declared-boundary mechanism can mark the exact current set as `SEALED` within that boundary.

---

### **S2. If a transaction is resolved and later conflicts, was the earlier result wrong?**

It was the deterministic result for the earlier admitted evidence set.

ORL makes the evidence boundary visible rather than treating a current resolution as permanent global truth.

---

### **S3. Why not silently pick one conflicting declaration?**

Because selection without an additional declared authority rule would hide structural disagreement.

The current ORL profile chooses explicit abstention instead.

---

### **S4. Why not ignore malformed fragments?**

Because silent omission can change the apparent structure of the submitted batch.

The current policy makes invalid input explicit through refusal.

---

### **S5. Is order still useful?**

Yes.

Order can remain essential for execution, history, causality, replay, transport, legal sequence, and settlement.

ORL separates those roles from the bounded structural classification authority used by its current resolver.

---

### **S6. Does ORL provide final truth?**

No universal truth claim is made.

ORL produces deterministic bounded results tied to canonical evidence, fixed rules, and optional declared closure boundaries.

---

## **SECTION T — Current Profiles**

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

---

## ⭐ **Final One-Line Summary**

ORL v2.0.0 is a bounded deterministic structural-reconciliation reference implementation in which supported input is strictly validated and canonically identified, exact duplicates are absorbed, transaction structure resolves to explicit `RESOLVED`, `INCOMPLETE`, or `ABSTAIN` states, results receive reproducible receipts, and an exact declared evidence boundary can separately produce bounded `SEALED` closure without treating arrival order, clock metadata, or coordinator state as the structural classification authority.
