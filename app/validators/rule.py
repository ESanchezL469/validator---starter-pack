def validate_rule_structure(rules: list[dict]) -> list[str]:
    """
    Validates the structure of a list of validation rules.

    Each rule must be a dictionary containing at least:
    - 'column': str
    - 'rule': str

    For certain rule types, additional fields are required:
    - 'range': requires 'min' (int/float) and 'max' (int/float)
    - 'regex': requires 'pattern' (str)

    Args:
        rules (List[Dict]): A list of dictionaries representing rules.

    Returns:
        List[str]: A list of human-readable error messages found in the rule.
    """
    errors: list[str] = []

    for i, rule in enumerate(rules):
        if not isinstance(rule, dict):
            errors.append(f"Regla #{i} no es un diccionario.")
            continue

        column = rule.get("column")
        rule_type = rule.get("rule")

        if not column or not isinstance(column, str):
            errors.append(f"Regla #{i}: 'column' debe existir y ser string.")
        if not rule_type or not isinstance(rule_type, str):
            errors.append(f"Regla #{i}: 'rule' debe existir y ser string.")
        if not column or not rule_type:
            continue

        if rule_type == "range":
            min_val = rule.get("min")
            max_val = rule.get("max")

            if min_val is None or max_val is None:
                errors.append(f"Regla #{i}: tipo 'range' incompleto.")
            elif not isinstance(min_val, (int, float)) or not isinstance(
                max_val, (int, float)
            ):
                errors.append(f"Regla #{i}: 'min' y 'max' erroneos.")

        elif rule_type == "regex":
            pattern = rule.get("pattern")
            if pattern is None:
                errors.append(f"Regla #{i}: tipo 'regex' requiere 'pattern'.")
            elif not isinstance(pattern, str):
                errors.append(f"Regla #{i}: 'pattern' debe ser string.")

        elif rule_type in ["not_null", "unique"]:
            # No hay campos extra requeridos
            pass

        else:
            errors.append("Regla : tipo de regla desconocido.")

    return errors
