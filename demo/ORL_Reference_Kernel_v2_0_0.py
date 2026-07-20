from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import re
import sys
import unicodedata
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

ARCHITECTURE_VERSION = "2.0.0"
SCHEMA_PROFILE = "ORL-FRAGMENT-2-D01"
RULESET_PROFILE = "ORL-RESOLUTION-2-D01"
CANONICAL_PROFILE = "ORL-CANON-1-D01"
FRAGMENT_SET_PROFILE = "ORL-FRAGMENT-SET-1-D01"
TX_EVIDENCE_PROFILE = "ORL-TX-EVIDENCE-1-D01"
RECEIPT_PROFILE = "ORL-RECEIPT-1-D01"
PROJECTION_PROFILE = "ORL-PROJECTION-1-D01"
BUNDLE_PROFILE = "ORL-BUNDLE-1-D01"
BOUNDARY_PROFILE = "ORL-BOUNDARY-1-D01"
REFUSAL_PROFILE = "ORL-REFUSAL-1-D01"
AUDIT_PROFILE = "ORL-AUDIT-1-D01"

EXACT_FIELDS = ("schema", "tx", "side", "account", "amount_minor", "unit")
SIDES = ("debit", "credit")
UNIT_PATTERN = re.compile(r"^[A-Z][A-Z0-9._:-]{0,31}$")
AMOUNT_PATTERN = re.compile(r"^[1-9][0-9]{0,77}$")

RULESET_FIELDS = (
    ("schema_profile", SCHEMA_PROFILE),
    ("canonical_profile", CANONICAL_PROFILE),
    ("exact_fields", ",".join(EXACT_FIELDS)),
    ("supported_sides", ",".join(SIDES)),
    ("text_normalization", "NFC"),
    ("amount_domain", "positive_decimal_integer_string_1_to_78_digits"),
    ("unit_domain", "uppercase_ascii_identifier_1_to_32"),
    ("unknown_fields", "REFUSE"),
    ("invalid_batch_policy", "REFUSE_WHOLE_BATCH"),
    ("duplicate_policy", "ABSORB_EXACT_CANONICAL_DUPLICATES"),
    ("conflict_precedence", "MULTIPLE_BOTH>MULTIPLE_DEBITS>MULTIPLE_CREDITS>MISSING_DEBIT>MISSING_CREDIT>SELF_TRANSFER_UNSUPPORTED>AMOUNT_MISMATCH>UNIT_MISMATCH>RESOLVED"),
    ("projection_policy", "RESOLVED_ONLY"),
    ("closure_policy", "EXACT_DECLARED_FRAGMENT_ID_SET"),
)


def utf8(value: str) -> bytes:
    return value.encode("utf-8")


def normalize_text(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def utf8_sort_key(value: str) -> bytes:
    return utf8(value)


def frame(label: str, value: str) -> bytes:
    label_bytes = utf8(label)
    value_bytes = utf8(value)
    return (
        str(len(label_bytes)).encode("ascii")
        + b":"
        + label_bytes
        + str(len(value_bytes)).encode("ascii")
        + b":"
        + value_bytes
    )


def canonical_record(profile: str, fields: Sequence[Tuple[str, str]]) -> bytes:
    payload = frame("profile", profile)
    for label, value in fields:
        payload += frame(label, value)
    return payload


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def ruleset_id() -> str:
    return sha256_hex(canonical_record(RULESET_PROFILE, RULESET_FIELDS))


RULESET_ID = ruleset_id()


def has_forbidden_control(value: str) -> bool:
    for char in value:
        code = ord(char)
        if code < 32 or code == 127 or 0xD800 <= code <= 0xDFFF:
            return True
    return False


def refusal(index: int, code: str, field: str = "", detail: str = "") -> Dict[str, str]:
    witness = {
        "profile": REFUSAL_PROFILE,
        "index": str(index),
        "code": code,
        "field": field,
        "detail": detail,
    }
    witness["refusal_id"] = sha256_hex(
        canonical_record(
            REFUSAL_PROFILE,
            [
                ("index", witness["index"]),
                ("code", code),
                ("field", field),
                ("detail", detail),
            ],
        )
    )
    return witness


def validate_fragment(raw: Any, index: int = 0) -> Tuple[Optional[Dict[str, str]], List[Dict[str, str]]]:
    errors: List[Dict[str, str]] = []
    if not isinstance(raw, dict):
        return None, [refusal(index, "FRAGMENT_NOT_OBJECT")]

    keys = set(raw.keys())
    required = set(EXACT_FIELDS)
    missing = sorted(required - keys)
    extra = sorted(keys - required)

    for field in missing:
        errors.append(refusal(index, "MISSING_REQUIRED_FIELD", field))
    for field in extra:
        errors.append(refusal(index, "UNKNOWN_FIELD", str(field)))

    if errors:
        return None, errors

    for field in EXACT_FIELDS:
        if not isinstance(raw[field], str):
            errors.append(refusal(index, "FIELD_NOT_STRING", field))

    if errors:
        return None, errors

    item = {field: normalize_text(raw[field]) for field in EXACT_FIELDS}

    if item["schema"] != SCHEMA_PROFILE:
        errors.append(refusal(index, "UNSUPPORTED_SCHEMA", "schema", item["schema"]))

    for field in ("tx", "account", "unit"):
        value = item[field]
        if value == "":
            errors.append(refusal(index, "EMPTY_FIELD", field))
        if value != value.strip():
            errors.append(refusal(index, "EDGE_WHITESPACE", field))
        if has_forbidden_control(value):
            errors.append(refusal(index, "CONTROL_CHARACTER", field))

    if len(utf8(item["tx"])) > 128:
        errors.append(refusal(index, "FIELD_TOO_LONG", "tx"))
    if len(utf8(item["account"])) > 256:
        errors.append(refusal(index, "FIELD_TOO_LONG", "account"))

    if item["side"] not in SIDES:
        errors.append(refusal(index, "UNSUPPORTED_SIDE", "side", item["side"]))

    if not AMOUNT_PATTERN.fullmatch(item["amount_minor"]):
        errors.append(refusal(index, "INVALID_AMOUNT_MINOR", "amount_minor", item["amount_minor"]))

    if not UNIT_PATTERN.fullmatch(item["unit"]):
        errors.append(refusal(index, "INVALID_UNIT", "unit", item["unit"]))

    if errors:
        return None, errors

    return item, []


def canonical_fragment_bytes(fragment: Dict[str, str]) -> bytes:
    return canonical_record(
        SCHEMA_PROFILE,
        [
            ("tx", fragment["tx"]),
            ("side", fragment["side"]),
            ("account", fragment["account"]),
            ("amount_minor", fragment["amount_minor"]),
            ("unit", fragment["unit"]),
        ],
    )


def fragment_id(fragment: Dict[str, str]) -> str:
    return sha256_hex(canonical_fragment_bytes(fragment))


def validate_batch(raw_fragments: Any) -> Dict[str, Any]:
    if not isinstance(raw_fragments, list):
        witness = refusal(0, "BATCH_NOT_ARRAY")
        return {
            "validation_state": "REFUSED",
            "accepted": [],
            "refusals": [witness],
        }

    accepted: List[Dict[str, str]] = []
    refusals: List[Dict[str, str]] = []

    for index, raw in enumerate(raw_fragments):
        item, errors = validate_fragment(raw, index)
        if errors:
            refusals.extend(errors)
        elif item is not None:
            accepted.append(item)

    if refusals:
        return {
            "validation_state": "REFUSED",
            "accepted": [],
            "refusals": sorted(refusals, key=lambda item: (int(item["index"]), item["code"], item["field"])),
        }

    return {
        "validation_state": "ACCEPTED",
        "accepted": accepted,
        "refusals": [],
    }


def deduplicate_validated(fragments: Sequence[Dict[str, str]]) -> List[Dict[str, str]]:
    by_id: Dict[str, Dict[str, str]] = {}
    for item in fragments:
        by_id[fragment_id(item)] = item
    return [by_id[item_id] for item_id in sorted(by_id)]


def deduplicate(raw_fragments: List[Dict[str, Any]]) -> Dict[str, Any]:
    validated = validate_batch(raw_fragments)
    if validated["validation_state"] == "REFUSED":
        return validated
    unique = deduplicate_validated(validated["accepted"])
    return {
        "validation_state": "ACCEPTED",
        "accepted": unique,
        "refusals": [],
    }


def bounded_union(*collections: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    merged: List[Dict[str, Any]] = []
    for collection in collections:
        merged.extend(collection)
    return deduplicate(merged)


def fragment_set_id_from_ids(ids: Sequence[str]) -> str:
    fields = [("fragment_id", item_id) for item_id in sorted(ids)]
    return sha256_hex(canonical_record(FRAGMENT_SET_PROFILE, fields))


def transaction_evidence_id(tx: str, ids: Sequence[str]) -> str:
    fields = [("tx", tx)] + [("fragment_id", item_id) for item_id in sorted(ids)]
    return sha256_hex(canonical_record(TX_EVIDENCE_PROFILE, fields))


def canonical_projection_bytes(projection: Dict[str, Dict[str, str]]) -> bytes:
    fields: List[Tuple[str, str]] = []
    for unit in sorted(projection, key=utf8_sort_key):
        fields.append(("unit", unit))
        accounts = projection[unit]
        for account in sorted(accounts, key=utf8_sort_key):
            fields.append(("account", account))
            fields.append(("delta_minor", accounts[account]))
    return canonical_record(PROJECTION_PROFILE, fields)


def projection_id(projection: Dict[str, Dict[str, str]]) -> str:
    return sha256_hex(canonical_projection_bytes(projection))


def canonical_boundary_bytes(expected_ids: Sequence[str]) -> bytes:
    fields = [
        ("schema_profile", SCHEMA_PROFILE),
        ("ruleset_id", RULESET_ID),
        ("expected_count", str(len(expected_ids))),
    ]
    fields.extend(("fragment_id", item_id) for item_id in sorted(expected_ids))
    return canonical_record(BOUNDARY_PROFILE, fields)


def boundary_id(expected_ids: Sequence[str]) -> str:
    return sha256_hex(canonical_boundary_bytes(expected_ids))


def declare_boundary(raw_fragments: List[Dict[str, Any]]) -> Dict[str, Any]:
    validated = validate_batch(raw_fragments)
    if validated["validation_state"] == "REFUSED":
        return {
            "boundary_state": "REFUSED",
            "refusals": validated["refusals"],
        }

    unique = deduplicate_validated(validated["accepted"])
    ids = sorted(fragment_id(item) for item in unique)
    return {
        "profile": BOUNDARY_PROFILE,
        "schema_profile": SCHEMA_PROFILE,
        "ruleset_id": RULESET_ID,
        "expected_fragment_ids": ids,
        "expected_fragment_set_id": fragment_set_id_from_ids(ids),
        "expected_count": str(len(ids)),
        "boundary_id": boundary_id(ids),
    }


def validate_boundary(boundary: Any) -> Tuple[bool, str]:
    if not isinstance(boundary, dict):
        return False, "BOUNDARY_NOT_OBJECT"

    required = {
        "profile",
        "schema_profile",
        "ruleset_id",
        "expected_fragment_ids",
        "expected_fragment_set_id",
        "expected_count",
        "boundary_id",
    }

    if set(boundary.keys()) != required:
        return False, "BOUNDARY_FIELDS_INVALID"
    if boundary["profile"] != BOUNDARY_PROFILE:
        return False, "BOUNDARY_PROFILE_INVALID"
    if boundary["schema_profile"] != SCHEMA_PROFILE:
        return False, "BOUNDARY_SCHEMA_INVALID"
    if boundary["ruleset_id"] != RULESET_ID:
        return False, "BOUNDARY_RULESET_INVALID"
    if not isinstance(boundary["expected_fragment_ids"], list):
        return False, "BOUNDARY_IDS_INVALID"
    if any(not isinstance(item, str) or not re.fullmatch(r"[0-9a-f]{64}", item) for item in boundary["expected_fragment_ids"]):
        return False, "BOUNDARY_IDS_INVALID"

    ids = sorted(set(boundary["expected_fragment_ids"]))
    if ids != boundary["expected_fragment_ids"]:
        return False, "BOUNDARY_IDS_NOT_CANONICAL"
    if boundary["expected_count"] != str(len(ids)):
        return False, "BOUNDARY_COUNT_MISMATCH"
    if boundary["expected_fragment_set_id"] != fragment_set_id_from_ids(ids):
        return False, "BOUNDARY_SET_ID_MISMATCH"
    if boundary["boundary_id"] != boundary_id(ids):
        return False, "BOUNDARY_ID_MISMATCH"

    return True, "BOUNDARY_VALID"


def closure_for(fragment_ids: Sequence[str], boundary: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if boundary is None:
        return {
            "state": "OPEN",
            "reason": "NO_BOUNDARY",
            "boundary_id": "",
        }

    valid, reason = validate_boundary(boundary)
    if not valid:
        return {
            "state": "OPEN",
            "reason": reason,
            "boundary_id": "",
        }

    current = sorted(fragment_ids)
    expected = boundary["expected_fragment_ids"]
    if current == expected:
        return {
            "state": "SEALED",
            "reason": "DECLARED_BOUNDARY_SATISFIED",
            "boundary_id": boundary["boundary_id"],
        }

    return {
        "state": "OPEN",
        "reason": "DECLARED_BOUNDARY_NOT_SATISFIED",
        "boundary_id": boundary["boundary_id"],
    }


def classify_transaction(group: Sequence[Dict[str, str]]) -> Dict[str, str]:
    debits = [item for item in group if item["side"] == "debit"]
    credits = [item for item in group if item["side"] == "credit"]

    if len(debits) > 1 and len(credits) > 1:
        return {"state": "ABSTAIN", "reason": "MULTIPLE_DEBITS_AND_CREDITS"}
    if len(debits) > 1:
        return {"state": "ABSTAIN", "reason": "MULTIPLE_DEBITS"}
    if len(credits) > 1:
        return {"state": "ABSTAIN", "reason": "MULTIPLE_CREDITS"}
    if not debits:
        return {"state": "INCOMPLETE", "reason": "MISSING_DEBIT"}
    if not credits:
        return {"state": "INCOMPLETE", "reason": "MISSING_CREDIT"}

    debit = debits[0]
    credit = credits[0]

    if debit["account"] == credit["account"]:
        return {"state": "ABSTAIN", "reason": "SELF_TRANSFER_UNSUPPORTED"}
    if debit["amount_minor"] != credit["amount_minor"]:
        return {"state": "ABSTAIN", "reason": "AMOUNT_MISMATCH"}
    if debit["unit"] != credit["unit"]:
        return {"state": "ABSTAIN", "reason": "UNIT_MISMATCH"}

    return {
        "state": "RESOLVED",
        "reason": "COMPATIBLE_PAIR",
        "from": debit["account"],
        "to": credit["account"],
        "amount_minor": debit["amount_minor"],
        "unit": debit["unit"],
    }


def make_receipt(
    tx: str,
    tx_ids: Sequence[str],
    classification: Dict[str, str],
    closure: Dict[str, str],
) -> Dict[str, str]:
    receipt = {
        "profile": RECEIPT_PROFILE,
        "schema_profile": SCHEMA_PROFILE,
        "ruleset_profile": RULESET_PROFILE,
        "ruleset_id": RULESET_ID,
        "transaction_id": tx,
        "transaction_evidence_id": transaction_evidence_id(tx, tx_ids),
        "state": classification["state"],
        "reason": classification["reason"],
        "from_account": classification.get("from", ""),
        "to_account": classification.get("to", ""),
        "amount_minor": classification.get("amount_minor", ""),
        "unit": classification.get("unit", ""),
        "closure_state": closure["state"],
        "closure_reason": closure["reason"],
        "boundary_id": closure["boundary_id"],
    }
    receipt["receipt_id"] = sha256_hex(
        canonical_record(
            RECEIPT_PROFILE,
            [
                ("schema_profile", receipt["schema_profile"]),
                ("ruleset_profile", receipt["ruleset_profile"]),
                ("ruleset_id", receipt["ruleset_id"]),
                ("transaction_id", receipt["transaction_id"]),
                ("transaction_evidence_id", receipt["transaction_evidence_id"]),
                ("state", receipt["state"]),
                ("reason", receipt["reason"]),
                ("from_account", receipt["from_account"]),
                ("to_account", receipt["to_account"]),
                ("amount_minor", receipt["amount_minor"]),
                ("unit", receipt["unit"]),
                ("closure_state", receipt["closure_state"]),
                ("closure_reason", receipt["closure_reason"]),
                ("boundary_id", receipt["boundary_id"]),
            ],
        )
    )
    return receipt


def verify_receipt(receipt: Any) -> bool:
    if not isinstance(receipt, dict):
        return False

    required = {
        "profile",
        "schema_profile",
        "ruleset_profile",
        "ruleset_id",
        "transaction_id",
        "transaction_evidence_id",
        "state",
        "reason",
        "from_account",
        "to_account",
        "amount_minor",
        "unit",
        "closure_state",
        "closure_reason",
        "boundary_id",
        "receipt_id",
    }

    if set(receipt.keys()) != required:
        return False
    if receipt["profile"] != RECEIPT_PROFILE:
        return False
    if receipt["schema_profile"] != SCHEMA_PROFILE:
        return False
    if receipt["ruleset_profile"] != RULESET_PROFILE:
        return False
    if receipt["ruleset_id"] != RULESET_ID:
        return False

    expected = sha256_hex(
        canonical_record(
            RECEIPT_PROFILE,
            [
                ("schema_profile", receipt["schema_profile"]),
                ("ruleset_profile", receipt["ruleset_profile"]),
                ("ruleset_id", receipt["ruleset_id"]),
                ("transaction_id", receipt["transaction_id"]),
                ("transaction_evidence_id", receipt["transaction_evidence_id"]),
                ("state", receipt["state"]),
                ("reason", receipt["reason"]),
                ("from_account", receipt["from_account"]),
                ("to_account", receipt["to_account"]),
                ("amount_minor", receipt["amount_minor"]),
                ("unit", receipt["unit"]),
                ("closure_state", receipt["closure_state"]),
                ("closure_reason", receipt["closure_reason"]),
                ("boundary_id", receipt["boundary_id"]),
            ],
        )
    )
    return expected == receipt["receipt_id"]


def project(receipts: Sequence[Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    values: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for receipt in receipts:
        if receipt["state"] != "RESOLVED":
            continue
        unit = receipt["unit"]
        amount = int(receipt["amount_minor"])
        values[unit][receipt["from_account"]] -= amount
        values[unit][receipt["to_account"]] += amount

    output: Dict[str, Dict[str, str]] = {}
    for unit in sorted(values, key=utf8_sort_key):
        accounts: Dict[str, str] = {}
        for account in sorted(values[unit], key=utf8_sort_key):
            value = values[unit][account]
            if value != 0:
                accounts[account] = str(value)
        if accounts:
            output[unit] = accounts

    return output


def state_summary(receipts: Sequence[Dict[str, str]]) -> Dict[str, int]:
    counts = {"RESOLVED": 0, "INCOMPLETE": 0, "ABSTAIN": 0}
    for receipt in receipts:
        counts[receipt["state"]] += 1
    return counts


def make_bundle_id(
    fragment_set_id: str,
    closure: Dict[str, str],
    receipts: Sequence[Dict[str, str]],
    projection_hash: str,
) -> str:
    fields = [
        ("architecture_version", ARCHITECTURE_VERSION),
        ("schema_profile", SCHEMA_PROFILE),
        ("ruleset_profile", RULESET_PROFILE),
        ("ruleset_id", RULESET_ID),
        ("fragment_set_id", fragment_set_id),
        ("closure_state", closure["state"]),
        ("closure_reason", closure["reason"]),
        ("boundary_id", closure["boundary_id"]),
        ("projection_id", projection_hash),
    ]
    for receipt_id_value in sorted(receipt["receipt_id"] for receipt in receipts):
        fields.append(("receipt_id", receipt_id_value))
    return sha256_hex(canonical_record(BUNDLE_PROFILE, fields))


def resolve(raw_fragments: Any, boundary: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    validated = validate_batch(raw_fragments)
    if validated["validation_state"] == "REFUSED":
        return {
            "architecture_version": ARCHITECTURE_VERSION,
            "schema_profile": SCHEMA_PROFILE,
            "ruleset_profile": RULESET_PROFILE,
            "ruleset_id": RULESET_ID,
            "validation_state": "REFUSED",
            "refusals": validated["refusals"],
            "fragment_count_input": len(raw_fragments) if isinstance(raw_fragments, list) else 0,
            "fragment_count_unique": 0,
            "fragment_set_id": "",
            "closure": {"state": "OPEN", "reason": "VALIDATION_REFUSED", "boundary_id": ""},
            "transactions": {},
            "projection": {},
            "projection_id": projection_id({}),
            "state_summary": {"RESOLVED": 0, "INCOMPLETE": 0, "ABSTAIN": 0},
            "bundle_id": "",
        }

    unique = deduplicate_validated(validated["accepted"])
    ids = [fragment_id(item) for item in unique]
    set_id = fragment_set_id_from_ids(ids)
    closure = closure_for(ids, boundary)

    grouped: Dict[str, List[Tuple[str, Dict[str, str]]]] = defaultdict(list)
    for item in unique:
        grouped[item["tx"]].append((fragment_id(item), item))

    transactions: Dict[str, Dict[str, str]] = {}
    receipts: List[Dict[str, str]] = []

    for tx in sorted(grouped, key=utf8_sort_key):
        pairs = grouped[tx]
        tx_ids = [item_id for item_id, _ in pairs]
        group = [item for _, item in pairs]
        classification = classify_transaction(group)
        receipt = make_receipt(tx, tx_ids, classification, closure)
        transactions[tx] = receipt
        receipts.append(receipt)

    projection = project(receipts)
    projection_hash = projection_id(projection)
    summary = state_summary(receipts)
    bundle_hash = make_bundle_id(set_id, closure, receipts, projection_hash)

    return {
        "architecture_version": ARCHITECTURE_VERSION,
        "schema_profile": SCHEMA_PROFILE,
        "ruleset_profile": RULESET_PROFILE,
        "ruleset_id": RULESET_ID,
        "validation_state": "ACCEPTED",
        "refusals": [],
        "fragment_count_input": len(raw_fragments),
        "fragment_count_unique": len(unique),
        "fragment_set_id": set_id,
        "closure": closure,
        "transactions": transactions,
        "projection": projection,
        "projection_id": projection_hash,
        "state_summary": summary,
        "bundle_id": bundle_hash,
    }


def fragment(tx: str, side: str, account: str, amount_minor: str, unit: str = "UNIT") -> Dict[str, str]:
    return {
        "schema": SCHEMA_PROFILE,
        "tx": tx,
        "side": side,
        "account": account,
        "amount_minor": amount_minor,
        "unit": unit,
    }


def reference_nodes() -> List[List[Dict[str, str]]]:
    return [
        [
            fragment("ORL100", "debit", "Alice", "500"),
            fragment("ORL300", "credit", "Cara", "200"),
            fragment("ORL500", "debit", "Evan", "600"),
        ],
        [
            fragment("ORL100", "credit", "Bob", "500"),
            fragment("ORL200", "debit", "Bob", "300"),
            fragment("ORL500", "debit", "Evan", "600"),
        ],
        [
            fragment("ORL200", "credit", "Dina", "300"),
            fragment("ORL400", "debit", "Alice", "700"),
            fragment("ORL400", "credit", "Faye", "900"),
            fragment("ORL500", "credit", "Gina", "600"),
            fragment("ORL500", "credit", "Hank", "600"),
            fragment("ORL100", "credit", "Bob", "500"),
        ],
    ]


def reference_union() -> List[Dict[str, str]]:
    nodes = reference_nodes()
    result = bounded_union(*nodes)
    if result["validation_state"] != "ACCEPTED":
        raise RuntimeError("reference scenario validation failed")
    return result["accepted"]


def reference_scenario(sealed: bool = True) -> Dict[str, Any]:
    nodes = reference_nodes()
    before = [resolve(node) for node in nodes]
    merged = reference_union()
    boundary = declare_boundary(merged) if sealed else None
    after = [resolve(merged, boundary) for _ in nodes]
    return {
        "nodes_before": before,
        "shared_fragment_count": len(merged),
        "boundary": boundary,
        "nodes_after": after,
        "all_nodes_match_after_sharing": len({item["bundle_id"] for item in after}) == 1,
        "final": after[0],
    }


def growth_scenario() -> List[Dict[str, Any]]:
    stages = [
        [fragment("ORL600", "debit", "Iris", "125")],
        [
            fragment("ORL600", "debit", "Iris", "125"),
            fragment("ORL600", "credit", "Juno", "125"),
        ],
        [
            fragment("ORL600", "debit", "Iris", "125"),
            fragment("ORL600", "credit", "Juno", "125"),
            fragment("ORL600", "credit", "Kora", "125"),
        ],
        [
            fragment("ORL600", "debit", "Iris", "125"),
            fragment("ORL600", "credit", "Juno", "125"),
            fragment("ORL600", "credit", "Kora", "125"),
            fragment("ORL600", "debit", "Liam", "125"),
        ],
    ]
    return [resolve(stage) for stage in stages]


class Audit:
    def __init__(self) -> None:
        self.groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def check(self, group: str, name: str, condition: bool, detail: str = "") -> None:
        self.groups[group].append(
            {
                "name": name,
                "pass": bool(condition),
                "detail": detail,
            }
        )

    def summary(self) -> Dict[str, Any]:
        groups: Dict[str, Dict[str, Any]] = {}
        total = 0
        passed = 0

        for group in self.groups:
            checks = self.groups[group]
            group_passed = sum(1 for item in checks if item["pass"])
            groups[group] = {
                "passed": group_passed,
                "total": len(checks),
                "status": "PASS" if group_passed == len(checks) else "FAIL",
                "checks": checks,
            }
            total += len(checks)
            passed += group_passed

        return {
            "profile": AUDIT_PROFILE,
            "architecture_version": ARCHITECTURE_VERSION,
            "passed": passed,
            "total": total,
            "status": "PASS" if passed == total else "FAIL",
            "groups": groups,
        }


def run_audit() -> Dict[str, Any]:
    audit = Audit()

    valid = fragment("T1", "debit", "Alice", "1")
    validation_cases = [
        ("valid fragment accepted", [valid], "ACCEPTED"),
        ("batch object refused", {"x": 1}, "REFUSED"),
        ("fragment non-object refused", ["x"], "REFUSED"),
        ("missing field refused", [{k: v for k, v in valid.items() if k != "unit"}], "REFUSED"),
        ("unknown field refused", [{**valid, "extra": "x"}], "REFUSED"),
        ("wrong schema refused", [{**valid, "schema": "OLD"}], "REFUSED"),
        ("unsupported side refused", [{**valid, "side": "hold"}], "REFUSED"),
        ("boolean amount refused", [{**valid, "amount_minor": True}], "REFUSED"),
        ("integer amount refused", [{**valid, "amount_minor": 1}], "REFUSED"),
        ("zero amount refused", [{**valid, "amount_minor": "0"}], "REFUSED"),
        ("negative amount refused", [{**valid, "amount_minor": "-1"}], "REFUSED"),
        ("decimal amount refused", [{**valid, "amount_minor": "1.0"}], "REFUSED"),
        ("leading zero refused", [{**valid, "amount_minor": "01"}], "REFUSED"),
        ("79 digit amount refused", [{**valid, "amount_minor": "9" * 79}], "REFUSED"),
        ("empty tx refused", [{**valid, "tx": ""}], "REFUSED"),
        ("empty account refused", [{**valid, "account": ""}], "REFUSED"),
        ("edge whitespace refused", [{**valid, "account": " Alice"}], "REFUSED"),
        ("control character refused", [{**valid, "account": "Ali\nce"}], "REFUSED"),
        ("lowercase unit refused", [{**valid, "unit": "usd"}], "REFUSED"),
        ("invalid unit separator refused", [{**valid, "unit": "US D"}], "REFUSED"),
    ]

    for name, value, expected in validation_cases:
        audit.check("VALIDATION", name, validate_batch(value)["validation_state"] == expected)

    nfc = fragment("N1", "debit", "Café", "5")
    nfd = fragment("N1", "debit", unicodedata.normalize("NFD", "Café"), "5")
    nfc_result = deduplicate([nfc, nfd])
    audit.check("CANONICALIZATION", "NFC and NFD collapse to one canonical fragment", nfc_result["validation_state"] == "ACCEPTED" and len(nfc_result["accepted"]) == 1)
    audit.check("CANONICALIZATION", "separator text remains safe", validate_batch([fragment("N2", "debit", "A|B:42", "5")])["validation_state"] == "ACCEPTED")

    base_id = fragment_id(valid)
    for field, value in [
        ("tx", "T2"),
        ("side", "credit"),
        ("account", "Bob"),
        ("amount_minor", "2"),
        ("unit", "ALT"),
    ]:
        changed = dict(valid)
        changed[field] = value
        audit.check("CANONICALIZATION", "identity changes with " + field, fragment_id(changed) != base_id)

    audit.check("CANONICALIZATION", "dictionary field insertion order does not affect identity", fragment_id(dict(reversed(list(valid.items())))) == base_id)

    huge = "9" * 78
    huge_pair = [
        fragment("BIG", "debit", "A", huge),
        fragment("BIG", "credit", "B", huge),
    ]
    huge_result = resolve(huge_pair)
    audit.check("EXACT_AMOUNTS", "78 digit amount resolves exactly", huge_result["transactions"]["BIG"]["state"] == "RESOLVED")
    audit.check("EXACT_AMOUNTS", "78 digit projection exact debit", huge_result["projection"]["UNIT"]["A"] == "-" + huge)
    audit.check("EXACT_AMOUNTS", "78 digit projection exact credit", huge_result["projection"]["UNIT"]["B"] == huge)

    js_boundary_amount = "9007199254740993"
    exact_result = resolve([
        fragment("SAFE", "debit", "A", js_boundary_amount),
        fragment("SAFE", "credit", "B", js_boundary_amount),
    ])
    audit.check("EXACT_AMOUNTS", "above JavaScript safe integer resolves exactly", exact_result["transactions"]["SAFE"]["amount_minor"] == js_boundary_amount)
    audit.check("EXACT_AMOUNTS", "above JavaScript safe integer projection exact", exact_result["projection"]["UNIT"]["B"] == js_boundary_amount)

    cases = {
        "resolved": [
            fragment("R", "debit", "A", "10"),
            fragment("R", "credit", "B", "10"),
        ],
        "missing_debit": [fragment("MD", "credit", "B", "10")],
        "missing_credit": [fragment("MC", "debit", "A", "10")],
        "amount_mismatch": [
            fragment("AM", "debit", "A", "10"),
            fragment("AM", "credit", "B", "11"),
        ],
        "unit_mismatch": [
            fragment("UM", "debit", "A", "10", "USD"),
            fragment("UM", "credit", "B", "10", "EUR"),
        ],
        "multiple_debits": [
            fragment("MDE", "debit", "A", "10"),
            fragment("MDE", "debit", "C", "10"),
        ],
        "multiple_credits": [
            fragment("MCR", "credit", "B", "10"),
            fragment("MCR", "credit", "C", "10"),
        ],
        "multiple_both": [
            fragment("MB", "debit", "A", "10"),
            fragment("MB", "debit", "C", "10"),
            fragment("MB", "credit", "B", "10"),
            fragment("MB", "credit", "D", "10"),
        ],
        "self_transfer": [
            fragment("SELF", "debit", "A", "10"),
            fragment("SELF", "credit", "A", "10"),
        ],
    }

    expected = {
        "resolved": ("RESOLVED", "COMPATIBLE_PAIR"),
        "missing_debit": ("INCOMPLETE", "MISSING_DEBIT"),
        "missing_credit": ("INCOMPLETE", "MISSING_CREDIT"),
        "amount_mismatch": ("ABSTAIN", "AMOUNT_MISMATCH"),
        "unit_mismatch": ("ABSTAIN", "UNIT_MISMATCH"),
        "multiple_debits": ("ABSTAIN", "MULTIPLE_DEBITS"),
        "multiple_credits": ("ABSTAIN", "MULTIPLE_CREDITS"),
        "multiple_both": ("ABSTAIN", "MULTIPLE_DEBITS_AND_CREDITS"),
        "self_transfer": ("ABSTAIN", "SELF_TRANSFER_UNSUPPORTED"),
    }

    for name, items in cases.items():
        result = resolve(items)
        tx = next(iter(result["transactions"].values()))
        state, reason = expected[name]
        audit.check("RESOLUTION", name + " state", tx["state"] == state)
        audit.check("RESOLUTION", name + " reason", tx["reason"] == reason)

    duplicate_pair = [
        fragment("DUP", "debit", "A", "10"),
        fragment("DUP", "debit", "A", "10"),
        fragment("DUP", "credit", "B", "10"),
    ]
    duplicate_result = resolve(duplicate_pair)
    audit.check("DEDUPLICATION", "exact duplicate does not create multiplicity conflict", duplicate_result["transactions"]["DUP"]["state"] == "RESOLVED")
    audit.check("DEDUPLICATION", "input count preserved", duplicate_result["fragment_count_input"] == 3)
    audit.check("DEDUPLICATION", "unique count reduced", duplicate_result["fragment_count_unique"] == 2)

    ref = reference_scenario(sealed=False)["final"]
    audit.check("REFERENCE_SCENARIO", "reference validation accepted", ref["validation_state"] == "ACCEPTED")
    audit.check("REFERENCE_SCENARIO", "two resolved", ref["state_summary"]["RESOLVED"] == 2)
    audit.check("REFERENCE_SCENARIO", "one incomplete", ref["state_summary"]["INCOMPLETE"] == 1)
    audit.check("REFERENCE_SCENARIO", "two abstain", ref["state_summary"]["ABSTAIN"] == 2)
    audit.check("REFERENCE_SCENARIO", "Alice projection exact", ref["projection"]["UNIT"]["Alice"] == "-500")
    audit.check("REFERENCE_SCENARIO", "Bob projection exact", ref["projection"]["UNIT"]["Bob"] == "200")
    audit.check("REFERENCE_SCENARIO", "Dina projection exact", ref["projection"]["UNIT"]["Dina"] == "300")
    audit.check("REFERENCE_SCENARIO", "ORL300 excluded from projection", "Cara" not in ref["projection"]["UNIT"])
    audit.check("REFERENCE_SCENARIO", "ORL400 excluded from projection", "Faye" not in ref["projection"]["UNIT"])
    audit.check("REFERENCE_SCENARIO", "ORL500 excluded from projection", "Evan" not in ref["projection"]["UNIT"])

    permutation_vector = [
        fragment("P1", "debit", "A", "10"),
        fragment("P1", "credit", "B", "10"),
        fragment("P2", "debit", "B", "4"),
        fragment("P2", "credit", "C", "4"),
        fragment("P3", "debit", "D", "7"),
    ]
    baseline = resolve(permutation_vector)
    for index, perm in enumerate(itertools.permutations(permutation_vector)):
        result = resolve(list(perm))
        audit.check("PERMUTATION_INVARIANCE", "permutation " + str(index + 1), result["bundle_id"] == baseline["bundle_id"])

    a = [
        fragment("U1", "debit", "A", "10"),
        fragment("U1", "credit", "B", "10"),
    ]
    b = [
        fragment("U2", "debit", "C", "3"),
        fragment("U1", "credit", "B", "10"),
    ]
    c = [
        fragment("U2", "credit", "D", "3"),
    ]

    union_ab = bounded_union(a, b)
    union_ba = bounded_union(b, a)
    audit.check("SET_ALGEBRA", "union commutative identity", fragment_set_id_from_ids([fragment_id(x) for x in union_ab["accepted"]]) == fragment_set_id_from_ids([fragment_id(x) for x in union_ba["accepted"]]))

    union_aa = bounded_union(a, a)
    union_a = bounded_union(a)
    audit.check("SET_ALGEBRA", "union idempotent identity", fragment_set_id_from_ids([fragment_id(x) for x in union_aa["accepted"]]) == fragment_set_id_from_ids([fragment_id(x) for x in union_a["accepted"]]))

    ab_then_c = bounded_union(union_ab["accepted"], c)
    bc = bounded_union(b, c)
    a_then_bc = bounded_union(a, bc["accepted"])
    audit.check("SET_ALGEBRA", "union associative identity", fragment_set_id_from_ids([fragment_id(x) for x in ab_then_c["accepted"]]) == fragment_set_id_from_ids([fragment_id(x) for x in a_then_bc["accepted"]]))

    growth = growth_scenario()
    growth_states = [stage["transactions"]["ORL600"]["state"] for stage in growth]
    audit.check("EVIDENCE_GROWTH", "incomplete to resolved", growth_states[0:2] == ["INCOMPLETE", "RESOLVED"])
    audit.check("EVIDENCE_GROWTH", "resolved to abstain", growth_states[1:3] == ["RESOLVED", "ABSTAIN"])
    audit.check("EVIDENCE_GROWTH", "abstain remains abstain", growth_states[2:4] == ["ABSTAIN", "ABSTAIN"])

    universe = [
        fragment("GX", "debit", "A", "10"),
        fragment("GX", "credit", "B", "10"),
        fragment("GX", "credit", "C", "10"),
        fragment("GX", "debit", "D", "11"),
    ]
    allowed = {
        "INCOMPLETE": {"INCOMPLETE", "RESOLVED", "ABSTAIN"},
        "RESOLVED": {"RESOLVED", "ABSTAIN"},
        "ABSTAIN": {"ABSTAIN"},
    }

    subset_states: Dict[int, str] = {}
    for mask in range(1, 1 << len(universe)):
        subset = [universe[i] for i in range(len(universe)) if mask & (1 << i)]
        result = resolve(subset)
        subset_states[mask] = result["transactions"]["GX"]["state"]

    for left in sorted(subset_states):
        for right in sorted(subset_states):
            if left & right == left:
                audit.check(
                    "EVIDENCE_GROWTH_EXHAUSTIVE",
                    "subset " + str(left) + " to " + str(right),
                    subset_states[right] in allowed[subset_states[left]],
                )

    merged = reference_union()
    open_result = resolve(merged)
    boundary = declare_boundary(merged)
    sealed_result = resolve(merged, boundary)
    audit.check("CLOSURE", "no boundary remains open", open_result["closure"]["state"] == "OPEN")
    audit.check("CLOSURE", "exact declared boundary seals", sealed_result["closure"]["state"] == "SEALED")
    audit.check("CLOSURE", "sealed reason explicit", sealed_result["closure"]["reason"] == "DECLARED_BOUNDARY_SATISFIED")
    audit.check("CLOSURE", "boundary stable under permutation", declare_boundary(list(reversed(merged)))["boundary_id"] == boundary["boundary_id"])
    audit.check("CLOSURE", "subset does not seal against larger boundary", resolve(merged[:-1], boundary)["closure"]["state"] == "OPEN")
    audit.check("CLOSURE", "superset does not seal against smaller boundary", resolve(merged + [fragment("EXTRA", "debit", "X", "1")], boundary)["closure"]["state"] == "OPEN")

    for tx, receipt_value in sealed_result["transactions"].items():
        audit.check("RECEIPTS", tx + " receipt verifies", verify_receipt(receipt_value))

    first_receipt = sealed_result["transactions"]["ORL100"]
    tampered = dict(first_receipt)
    tampered["amount_minor"] = "501"
    audit.check("RECEIPTS", "tampered receipt rejected", not verify_receipt(tampered))
    audit.check("RECEIPTS", "open and sealed receipt identities differ", open_result["transactions"]["ORL100"]["receipt_id"] != sealed_result["transactions"]["ORL100"]["receipt_id"])

    malformed_with_valid_pair = [
        fragment("BAD", "debit", "A", "10"),
        fragment("BAD", "credit", "B", "10"),
        {**fragment("BAD", "credit", "C", "10"), "side": "unsupported"},
    ]
    malformed_result = resolve(malformed_with_valid_pair)
    audit.check("KNOWN_REGRESSIONS", "unsupported side cannot be silently ignored", malformed_result["validation_state"] == "REFUSED")

    two_debits_only = [
        fragment("REG1", "debit", "A", "10"),
        fragment("REG1", "debit", "B", "10"),
    ]
    audit.check("KNOWN_REGRESSIONS", "multiple debits without credit abstain", resolve(two_debits_only)["transactions"]["REG1"]["reason"] == "MULTIPLE_DEBITS")

    two_credits_only = [
        fragment("REG2", "credit", "A", "10"),
        fragment("REG2", "credit", "B", "10"),
    ]
    audit.check("KNOWN_REGRESSIONS", "multiple credits without debit abstain", resolve(two_credits_only)["transactions"]["REG2"]["reason"] == "MULTIPLE_CREDITS")

    unsafe_separator = [
        fragment("REG3", "debit", "A|B:1", "10"),
        fragment("REG3", "credit", "C", "10"),
    ]
    audit.check("KNOWN_REGRESSIONS", "separator-bearing account resolves safely", resolve(unsafe_separator)["transactions"]["REG3"]["state"] == "RESOLVED")

    return audit.summary()


def compact_summary(bundle: Dict[str, Any]) -> str:
    summary = bundle["state_summary"]
    return "R:{0} I:{1} A:{2}".format(
        summary["RESOLVED"],
        summary["INCOMPLETE"],
        summary["ABSTAIN"],
    )


def print_reference() -> None:
    scenario = reference_scenario(sealed=True)
    final = scenario["final"]

    print("ORL v" + ARCHITECTURE_VERSION)
    print("Validation       :", final["validation_state"])
    print("Closure          :", final["closure"]["state"])
    print("State Summary    :", compact_summary(final))
    print("Fragment Set ID  :", final["fragment_set_id"])
    print("Ruleset ID       :", final["ruleset_id"])
    print("Projection ID    :", final["projection_id"])
    print("Bundle ID        :", final["bundle_id"])
    print("Node Equality    :", scenario["all_nodes_match_after_sharing"])
    print("")
    print("Transactions")
    for tx, receipt_value in final["transactions"].items():
        print(
            "  {0:<8} {1:<10} {2:<30} {3}".format(
                tx,
                receipt_value["state"],
                receipt_value["reason"],
                receipt_value["receipt_id"],
            )
        )
    print("")
    print("Projection")
    if not final["projection"]:
        print("  (empty)")
    else:
        for unit, accounts in final["projection"].items():
            print("  " + unit)
            for account, amount in accounts.items():
                sign = "+" if not amount.startswith("-") else ""
                print("    {0:<12} {1}{2}".format(account, sign, amount))


def print_audit(audit: Dict[str, Any]) -> None:
    print("ORL AUDIT " + audit["profile"])
    for group, info in audit["groups"].items():
        print("{0:<30} {1}/{2} {3}".format(group, info["passed"], info["total"], info["status"]))
        if info["status"] == "FAIL":
            for check in info["checks"]:
                if not check["pass"]:
                    print("  FAIL:", check["name"], check["detail"])
    print("TOTAL {0}/{1} {2}".format(audit["passed"], audit["total"], audit["status"]))


def main() -> int:
    parser = argparse.ArgumentParser(prog="ORL_Reference_Kernel_v2_0_0.py")
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-json", metavar="PATH")
    args = parser.parse_args()

    if args.audit:
        result = run_audit()
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        else:
            print_audit(result)
        return 0 if result["status"] == "PASS" else 1

    result = reference_scenario(sealed=True)
    if args.write_json:
        with open(args.write_json, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(result, handle, indent=2, ensure_ascii=False, sort_keys=True)
            handle.write("\n")

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print_reference()

    return 0


if __name__ == "__main__":
    sys.exit(main())
