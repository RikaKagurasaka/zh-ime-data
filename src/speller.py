import re
import yaml
import pandas as pd
from typing import List, Dict, Union, Tuple
from paths import SPELLERS

# Global dictionary to store loaded rules
_LOADED_RULES = {}


def load_speller_rules():
    """
    Load all speller rules from the YAML file.

    Returns:
        Dictionary mapping rule names to rule lists
    """
    global _LOADED_RULES

    if not _LOADED_RULES:
        with open(SPELLERS, "r", encoding="utf-8") as file:
            _LOADED_RULES = yaml.safe_load(file)

    return _LOADED_RULES


def apply_speller_rules(
    series: Union[pd.Series, pd.DataFrame], rule_name: str, column_name: str = None
) -> Union[pd.Series, pd.DataFrame]:
    """
    Apply speller transformation rules to each element in a pandas Series.

    Args:
        series: pandas Series containing strings to transform
        rule_name: Name of the rule set to apply (e.g., 'pinyin2terra', 'terra2bopomofo')

    Returns:
        Transformed pandas Series
    """
    # Load rules if not already loaded
    rules_dict = load_speller_rules()

    if rule_name not in rules_dict:
        raise KeyError(f"Rule set '{rule_name}' not found in spellers.yaml")

    rules = rules_dict[rule_name]
    if isinstance(series, pd.Series):
        result = series.copy()
    elif isinstance(series, pd.DataFrame):
        if column_name is None:
            raise ValueError("column_name must be provided for DataFrame input")
        result = series[column_name].copy()
    else:
        raise ValueError(f"Invalid input type: {type(series)}")

    for rule in rules:
        if isinstance(rule, dict):
            # Rules loaded from yaml directly will be in dict format
            rule_type = list(rule.keys())[0]
            rule_value = rule[rule_type]
        else:
            # Parse rule string if it's not already a dict
            if "/" in rule and rule.startswith("xform"):
                rule_type = "xform"
                rule_value = rule
            elif "|" in rule and rule.startswith("xlit"):
                rule_type = "xlit"
                rule_value = rule
            else:
                raise ValueError(f"Unknown rule format: {rule}")

        if rule_type == "xform":
            # Handle xform rule (regex substitution)
            pattern, replacement = parse_xform_rule(rule_value)
            result = result.apply(
                lambda x: re.sub(pattern, replacement, x) if isinstance(x, str) else x
            )

        elif rule_type == "xlit":
            # Handle xlit rule (character mapping)
            source, target = parse_xlit_rule(rule_value)
            # Ensure source and target have the same length
            assert len(source) == len(
                target
            ), f"Source '{source}' and target '{target}' must have the same length"

            # Create translation table
            translation_map = str.maketrans(source, target)
            result = result.apply(
                lambda x: x.translate(translation_map) if isinstance(x, str) else x
            )

    if isinstance(series, pd.DataFrame):
        result_df = series.copy()
        result_df[column_name] = result
        return result_df
    return result


def parse_xform_rule(rule: str) -> Tuple[str, str]:
    """
    Parse an xform rule into pattern and replacement.
    Convert $1, $2 references to \1, \2 for Python regex.

    Args:
        rule: String in format "pattern/replacement/"

    Returns:
        Tuple of (pattern, replacement)
    """
    parts = rule.split("/")
    assert len(parts) >= 3, f"Invalid xform rule format: {rule}"

    pattern = parts[1]
    replacement = parts[2]

    # Convert $1, $2, etc. to \1, \2, etc.
    replacement = re.sub(r"\$(\d+)", r"\\1", replacement)

    return pattern, replacement


def parse_xlit_rule(rule: str) -> Tuple[str, str]:
    """
    Parse an xlit rule into source and target character sets.

    Args:
        rule: String in format "source|target|"

    Returns:
        Tuple of (source, target)
    """
    parts = rule.split("|")
    assert len(parts) >= 3, f"Invalid xlit rule format: {rule}"

    source = parts[1]
    target = parts[2]

    return source, target
