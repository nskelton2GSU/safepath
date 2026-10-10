from __future__ import annotations

ALLOWED_FIELDS = frozenset({
    "origin", "destination", "preferences", "route",
    "score_breakdown", "costs",
})

FORBIDDEN_FIELDS = frozenset({
    "name", "full_name", "first_name", "last_name",
    "email", "phone", "address", "ssn",
    "user_id", "device_id", "session_id", "cookie",
    "ip", "ip_address", "mac_address",
    "history", "timestamp", "location_history",
    "password", "token", "api_key",
})

def new_session() -> dict:
    return {
        "origin": None,
        "destination": None,
        "preferences": {},
        "route": [],
        "score_breakdown": {},
        "costs": {},
    }

def validate_session(session: dict) -> None:
    keys = set(session.keys())
    forbidden_present = keys & FORBIDDEN_FIELDS
    if forbidden_present:
        raise ValueError(f"Privacy violation: forbidden fields present: {forbidden_present}")
    unexpected = keys - ALLOWED_FIELDS
    if unexpected:
        raise ValueError(f"Privacy violation: unexpected fields: {unexpected}")

def get_session_schema() -> set[str]:
    return set(new_session().keys())
