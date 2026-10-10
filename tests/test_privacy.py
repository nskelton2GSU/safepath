import socket
from pathlib import Path

import pytest

import privacy


def test_session_has_no_forbidden_fields():
    schema = privacy.get_session_schema()
    violations = schema & privacy.FORBIDDEN_FIELDS
    assert not violations, f"Forbidden fields found: {violations}"


def test_new_session_passes_validation():
    s = privacy.new_session()
    privacy.validate_session(s)


def test_session_rejects_pii_if_someone_adds_it():
    s = privacy.new_session()
    s["email"] = "someone@example.com"
    with pytest.raises(ValueError, match="forbidden"):
        privacy.validate_session(s)


def test_session_rejects_unknown_fields():
    s = privacy.new_session()
    s["mystery_field"] = "surprise"
    with pytest.raises(ValueError, match="unexpected"):
        privacy.validate_session(s)


def test_session_is_pure_dict_no_io(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    s = privacy.new_session()
    privacy.validate_session(s)
    s["origin"] = (33.7756, -84.3963)
    s["destination"] = (33.7780, -84.3940)
    s["route"] = [(33.7756, -84.3963), (33.7780, -84.3940)]
    privacy.validate_session(s)
    files_created = list(tmp_path.rglob("*"))
    assert files_created == [], f"Unexpected files written: {files_created}"


def test_no_db_files_in_project_root():
    for name in ("history.db", "sessions.db", "users.db", "safepath.db"):
        assert not Path(name).exists(), f"Unexpected DB file: {name}"


def test_routing_code_does_not_open_sockets(monkeypatch):
    try:
        import graph
    except ImportError:
        pytest.skip("graph.py not landed yet")

    def _blocked(*args, **kwargs):
        raise AssertionError("Routing attempted a network connection")

    monkeypatch.setattr(socket, "socket", _blocked)
    monkeypatch.setattr(socket, "create_connection", _blocked)

    G = graph.load_graph()
    G = graph.add_safety_weights(G)
    assert G is not None


def test_schema_is_whitelist_not_blacklist():
    assert privacy.ALLOWED_FIELDS.isdisjoint(privacy.FORBIDDEN_FIELDS)
    assert len(privacy.ALLOWED_FIELDS) == len(privacy.new_session())