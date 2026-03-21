from collections import defaultdict
from copy import deepcopy


def entry_key(entry):
    return (entry["tx"], entry["side"], entry["account"], entry["amount"])


def deduplicate(entries):
    unique = {}
    for entry in entries:
        unique[entry_key(entry)] = entry
    return list(unique.values())


def resolve(entries):
    """
    Orderless Ledger (ORL)

    A structure-driven ledger resolver with three explicit resolution states:

    - RESOLVED: exactly one debit and one credit with matching amount
    - INCOMPLETE: missing counterpart structure
    - ABSTAIN: conflicting or inconsistent structure

    Duplicates are absorbed automatically during structural deduplication
    and do not appear as a final resolver state.
    """
    unique_entries = deduplicate(entries)
    by_tx = defaultdict(list)

    for entry in unique_entries:
        by_tx[entry["tx"]].append(entry)

    balances = defaultdict(int)
    tx_state = {}

    for tx in sorted(by_tx):
        group = by_tx[tx]
        debits = {(e["account"], e["amount"]) for e in group if e["side"] == "debit"}
        credits = {(e["account"], e["amount"]) for e in group if e["side"] == "credit"}

        if len(debits) == 1 and len(credits) == 1:
            (from_acct, debit_amt), = debits
            (to_acct, credit_amt), = credits

            if debit_amt == credit_amt:
                balances[from_acct] -= debit_amt
                balances[to_acct] += credit_amt
                tx_state[tx] = {
                    "state": "RESOLVED",
                    "from": from_acct,
                    "to": to_acct,
                    "amount": debit_amt,
                }
            else:
                tx_state[tx] = {
                    "state": "ABSTAIN",
                    "reason": "debit_credit_mismatch",
                }

        elif not debits or not credits:
            tx_state[tx] = {
                "state": "INCOMPLETE",
                "reason": "missing_counterpart",
            }
        else:
            tx_state[tx] = {
                "state": "ABSTAIN",
                "reason": "conflicting_structure",
            }

    return dict(sorted(balances.items())), dict(sorted(tx_state.items()))


def ledger_signature(balances, tx_state):
    return (
        tuple(sorted(balances.items())),
        tuple(sorted((tx, tuple(sorted(info.items()))) for tx, info in tx_state.items()))
    )


def bounded_union(node_entries, incoming_entries):
    return deduplicate(node_entries + incoming_entries)


def summarize_states(tx_state):
    counts = defaultdict(int)
    for info in tx_state.values():
        counts[info["state"]] += 1
    return dict(sorted(counts.items()))


def print_header(title):
    print("\n" + "=" * 84)
    print(title)
    print("=" * 84)


def print_balances(balances):
    print("Balances")
    print("-" * 84)
    if not balances:
        print("  (no resolved balances)")
        return
    for account, amount in balances.items():
        print(f"  {account:>8} : {amount:+}")


def print_states(tx_state):
    print("\nTransaction States")
    print("-" * 84)
    for tx, info in tx_state.items():
        state = info["state"]
        if state == "RESOLVED":
            print(f"  {tx:<6} {state:<11} {info['from']} -> {info['to']}  amount={info['amount']}")
        else:
            print(f"  {tx:<6} {state:<11} reason={info['reason']}")


def print_node_snapshot(name, entries):
    balances, tx_state = resolve(entries)
    print_header(f"{name} | local structural view")
    print_balances(balances)
    print_states(tx_state)
    print(f"\nState Summary: {summarize_states(tx_state)}")
    return balances, tx_state


def print_convergence_table(before_signatures, after_signatures):
    print_header("Convergence Check")
    print("Node        Before Match    After Match")
    print("-" * 84)
    reference_before = before_signatures[0]
    reference_after = after_signatures[0]

    for idx, (before_sig, after_sig) in enumerate(zip(before_signatures, after_signatures), start=1):
        before_match = before_sig == reference_before
        after_match = after_sig == reference_after
        print(f"Node-{idx:<6} {str(before_match):<15} {str(after_match):<10}")


def scenario():
    """
    Three isolated nodes begin with different fragments.

    Transactions:
    - ORL100 resolves across Node-1 and Node-2
    - ORL200 resolves across Node-2 and Node-3
    - ORL300 remains incomplete
    - ORL400 is an explicit adversarial mismatch
    - ORL500 is a double-credit conflict attempt
    """
    node_1 = [
        {"tx": "ORL100", "side": "debit",  "account": "Alice", "amount": 500},
        {"tx": "ORL300", "side": "credit", "account": "Cara",  "amount": 200},
        {"tx": "ORL500", "side": "debit",  "account": "Evan",  "amount": 600},
    ]

    node_2 = [
        {"tx": "ORL100", "side": "credit", "account": "Bob",   "amount": 500},
        {"tx": "ORL200", "side": "debit",  "account": "Bob",   "amount": 300},
        {"tx": "ORL500", "side": "debit",  "account": "Evan",  "amount": 600},
    ]

    node_3 = [
        {"tx": "ORL200", "side": "credit", "account": "Dina",  "amount": 300},
        {"tx": "ORL400", "side": "debit",  "account": "Alice", "amount": 700},
        {"tx": "ORL400", "side": "credit", "account": "Faye",  "amount": 900},
        {"tx": "ORL500", "side": "credit", "account": "Gina",  "amount": 600},
        {"tx": "ORL500", "side": "credit", "account": "Hank",  "amount": 600},
        {"tx": "ORL100", "side": "credit", "account": "Bob",   "amount": 500},
    ]

    return [node_1, node_2, node_3]


def simulate():
    nodes = scenario()
    node_names = ["Node-1", "Node-2", "Node-3"]

    print_header("Orderless Ledger (ORL)")
    print("A structure-driven convergence demo")
    print("\nPrinciple:")
    print("  correctness does not depend on time, order, or synchronization")
    print("  correctness emerges only from sufficient and consistent structure")

    before_signatures = []
    after_signatures = []

    for name, entries in zip(node_names, nodes):
        balances, tx_state = print_node_snapshot(name, entries)
        before_signatures.append(ledger_signature(balances, tx_state))

    print_header("Bounded Sharing Phase")
    print("Each node receives fragments from the other two nodes.")
    print("No timestamps are used. No global ordering is used. No coordinator is used.")

    merged_nodes = []
    for i in range(len(nodes)):
        combined = deepcopy(nodes[i])
        for j in range(len(nodes)):
            if i != j:
                combined = bounded_union(combined, nodes[j])
        merged_nodes.append(combined)

    for name, entries in zip(node_names, merged_nodes):
        balances, tx_state = print_node_snapshot(name + " | after bounded sharing", entries)
        after_signatures.append(ledger_signature(balances, tx_state))

    print_convergence_table(before_signatures, after_signatures)

    final_balances, final_state = resolve(merged_nodes[0])

    print_header("Final Shared Truth")
    print_balances(final_balances)
    print_states(final_state)

    print("\nOutcome Summary")
    print("-" * 84)
    print("  ORL100  RESOLVED   split across isolated nodes, later converged correctly")
    print("  ORL200  RESOLVED   split differently, later converged correctly")
    print("  ORL300  INCOMPLETE missing counterpart, therefore not forced into a false result")
    print("  ORL400  ABSTAIN    mismatch detected, therefore no balance corruption")
    print("  ORL500  ABSTAIN    double-credit conflict detected, therefore no double-spend style corruption")

    print("\nFinal Equality Proof")
    print("-" * 84)
    print(f"  all_nodes_match_after_sharing = {len(set(after_signatures)) == 1}")
    print(f"  resolved_balance_accounts     = {list(final_balances.keys())}")
    print(f"  state_summary                 = {summarize_states(final_state)}")


if __name__ == "__main__":
    simulate()