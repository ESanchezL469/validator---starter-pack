from app.validators.rule import validate_rule_structure


def test_valid_rules():
    rules = [
        {"column": "email", "rule": "regex", "pattern": r"[^@]+@[^@]+\.[^@]+"},
        {"column": "age", "rule": "range", "min": 18, "max": 99},
        {"column": "name", "rule": "not_null"},
        {"column": "id", "rule": "unique"},
    ]

    errors = validate_rule_structure(rules)
    assert errors == []


def test_not_dict_rule():
    rules = ["not_a_dict"]
    errors = validate_rule_structure(rules)
    assert "Regla #0 no es un diccionario." in errors


def test_missing_column_or_rule():
    rules = [
        {"column": "email"},  # Falta "rule"
        {"rule": "not_null"},  # Falta "column"
        {"column": 123, "rule": "regex"},  # column no es string
    ]
    errors = validate_rule_structure(rules)

    assert "Regla #0: 'rule' debe existir y ser string." in errors
    assert "Regla #1: 'column' debe existir y ser string." in errors
    assert "Regla #2: 'column' debe existir y ser string." in errors


def test_invalid_range_fields():
    rules = [
        {"column": "age", "rule": "range"},
        {"column": "age", "rule": "range", "min": "low", "max": 99},
    ]
    errors = validate_rule_structure(rules)

    assert "Regla #0: tipo 'range' incompleto." in errors
    assert "Regla #1: 'min' y 'max' erroneos." in errors


def test_invalid_regex_pattern():
    rules = [
        {"column": "email", "rule": "regex"},
        {"column": "email", "rule": "regex", "pattern": 123},
    ]
    errors = validate_rule_structure(rules)

    assert "Regla #0: tipo 'regex' requiere 'pattern'." in errors
    assert "Regla #1: 'pattern' debe ser string." in errors


def test_unknown_rule_type():
    rules = [{"column": "status", "rule": "invalid_rule"}]
    errors = validate_rule_structure(rules)

    assert "Regla : tipo de regla desconocido." in errors
