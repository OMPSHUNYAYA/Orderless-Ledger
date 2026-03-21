# ⭐ **ORL — Test Guide**

**Orderless Ledger (ORL)**  

**Deterministic • Orderless • Time-Independent Ledger**

**Powered by Shunyaya Framework (STOCRS + SSUM-Time)**

---

## ⚡ **Start Here — Run the Demo (Recommended)**

Open:

`demo/orl_demo_v3.html`

Then:

Click **Run Full Demo**

That’s it.

---

## 👀 **What You Will See**

- Three independent nodes  
- Each node starts with different transaction fragments  
- No timestamps anywhere  
- No ordering enforced  
- No coordination between nodes  

Then:

- Nodes begin sharing partial information  
- Transactions start resolving structurally  
- Conflicts are detected and isolated  
- All nodes converge to the same final state  

---

## 🧭 **What This Demo Is Showing**

ORL is **not a traditional ledger**.

Instead of:

- ordering transactions  
- using timestamps  
- enforcing global sequence  

It:

- evaluates transaction **structure**  
- resolves only when structure is **complete**  
- rejects conflicts safely  
- converges deterministically  

---

## 🎮 **Main Controls**

### **Next Step**

Moves the system forward one stage.

Use this to observe:

- partial convergence  
- intermediate states  

---

### **Run Full Demo**

Automatically runs all stages.

Best for:

- quick understanding  
- presentations  

---

### **Reset**

Returns to initial state.

All nodes go back to:

- fragmented views  
- unresolved transactions  

---

### **Jump to Sharing**

Skips directly to:

- final convergence stage  

---

## 🔬 **Demo Stages**

### **1. Local Views Only**

Each node has:

- incomplete transactions  
- missing counterparts  

Result:

- most transactions → **INCOMPLETE**  
- nodes do **NOT match**  

---

### **2. Partial Sharing**

Nodes begin exchanging fragments.

Result:

- some transactions resolve  
- some remain incomplete  
- some conflicts become visible  

---

### **3. Full Sharing**

All nodes now have the same structure.

Result:

- all valid transactions → **RESOLVED**  
- incomplete ones remain **INCOMPLETE**  
- conflicts → **ABSTAIN**  

All nodes now match exactly.

---

## ⚖️ **Transaction States**

### **RESOLVED**

Valid structure exists:

Exactly one debit and one credit with equal amount

Example:

Alice -500  
Bob   +500  

---

### **INCOMPLETE**

Missing structure:

Only debit OR only credit  

---

### **ABSTAIN**

Conflicting structure:

- multiple debits  
- multiple credits  
- mismatched amounts  

👉 This is a **key safety feature**

---

## 🔍 **Key Transactions in Demo**

### **ORL100**

- resolves after sharing  
- shows normal convergence  

---

### **ORL200**

- initially incomplete  
- resolves after counterpart appears  

---

### **ORL300**

- remains incomplete  
- missing structure never arrives  

---

### **ORL400**

- debit/credit mismatch  
- → **ABSTAIN**  

---

### **ORL500**

- conflicting credits  
- → **ABSTAIN**  

👉 Demonstrates **conflict safety**

---

## 📊 **What to Observe Carefully**

### **1. No Time Anywhere**

There are:

- no timestamps  
- no clocks  
- no ordering  

---

### **2. Different Start States**

Each node begins differently.

---

### **3. Same Final State**

After sharing:

All nodes → identical result  

---

### **4. Conflict Safety**

Conflicts do **NOT corrupt the system**.

They are:

isolated → **ABSTAIN**

---

## 🔁 **Deterministic Behavior**

Run the demo multiple times.

You will observe:

- identical results  
- identical transaction states  
- identical balances  

---

### **Convergence Condition**

ORL guarantees convergence only when **sufficient and consistent structure** is available across nodes.

Incomplete or conflicting structure will remain **safely unresolved**.

---

## 📌 **Key Insight**

ORL does **not require**:

- time  
- order  
- synchronization  

It requires only:

**structure**

---

## 🔁 **Invariant**

Given sufficient and consistent structure:

`arrival_structure_A != arrival_structure_B → resolved_result_A == resolved_result_B`

---

## ⚡ **Suggested 1-Minute Demo Flow**

Click:

**Reset**

Then:

**Run Full Demo**

Observe:

- Local mismatch  
- Partial resolution  
- Final convergence  

Then:

Click **Reset** → use **Next Step** manually  

---

## ⭐ **One-Line Summary**

ORL demonstrates that a ledger can start with incomplete and conflicting fragments and still converge deterministically to the same final truth — without using time, order, or synchronization.
