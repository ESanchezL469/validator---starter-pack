from app.metadata.tracker import find_previous_version, version_exists

# ----------------------------
# Successful tests
# ----------------------------


def test_version_exists(tmp_path, monkeypatch):
    monkeypatch.setattr("app.metadata.tracker.METADATA_DIR", str(tmp_path))

    version = "abc123"
    file = tmp_path / f"{version}_metadata.json"
    file.write_text("{}")

    assert version_exists(version) is True


def test_find_previous_version_found(tmp_path, monkeypatch):
    monkeypatch.setattr("app.metadata.tracker.METADATA_DIR", str(tmp_path))

    version = "abc123"
    file = tmp_path / f"{version}_metadata.json"
    file.write_text("{}")

    result = find_previous_version(version)
    assert result == f"{version}_metadata.json"


# ----------------------------
# Error tests
# ----------------------------


def test_version_exists_false(tmp_path, monkeypatch):
    monkeypatch.setattr("app.metadata.tracker.METADATA_DIR", str(tmp_path))

    assert version_exists("nonexistent") is False


def test_find_previous_version_none(tmp_path, monkeypatch):
    monkeypatch.setattr("app.metadata.tracker.METADATA_DIR", str(tmp_path))

    assert find_previous_version("nonexistent") == ""
