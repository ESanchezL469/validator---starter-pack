def validate_rule_structure(rules: list[dict]) -> list[dict]:
    
    errors = []

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
                errors.append(f"Regla #{i}: tipo 'range' requiere 'min' y 'max'.")
            elif not isinstance(min_val, (int, float)) or not isinstance(max_val, (int, float)):
                errors.append(f"Regla #{i}: 'min' y 'max' deben ser numéricos.")

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
            errors.append(f"Regla #{i}: tipo de regla desconocido: '{rule_type}'.")

    return errors