"""
portfolio/walk_forward/validation_v154.py — Walk-forward Validation v1.5.4
[!] Research Only. No Real Orders. Historical Simulation Only.
"""
from __future__ import annotations
from typing import Any, Dict

RESEARCH_ONLY = True
HISTORICAL_SIMULATION_ONLY = True
VALIDATION_VERSION = "1.5.4"


def validate_walk_forward_config(config) -> Dict[str, Any]:
    """Validate a WalkForwardConfiguration. Returns dict with is_valid, errors, warnings."""
    errors = []
    warnings = []

    if config is None:
        return {"is_valid": False, "errors": ["config is None"], "warnings": []}

    # Date validation
    start = getattr(config, "start_date", None)
    end = getattr(config, "end_date", None)
    if start and end and start >= end:
        errors.append(f"start_date ({start}) must be before end_date ({end})")

    # Length validations
    training = getattr(config, "training_length", 0)
    validation = getattr(config, "validation_length", 0)
    step = getattr(config, "step_length", 0)
    purge = getattr(config, "purge_length", 0)
    embargo = getattr(config, "embargo_length", 0)
    min_windows = getattr(config, "minimum_windows", 0)
    min_obs = getattr(config, "minimum_observations", 0)

    if training <= 0:
        errors.append(f"training_length must be > 0, got {training}")
    if validation <= 0:
        errors.append(f"validation_length must be > 0, got {validation}")
    if step <= 0:
        errors.append(f"step_length must be > 0, got {step}")
    if purge < 0:
        errors.append(f"purge_length must be >= 0, got {purge}")
    if embargo < 0:
        errors.append(f"embargo_length must be >= 0, got {embargo}")
    if min_windows <= 0:
        errors.append(f"minimum_windows must be > 0, got {min_windows}")

    # Safety flag
    research_only = getattr(config, "research_only", None)
    if research_only is not True:
        errors.append("research_only must be True — production trading is permanently blocked")

    auto_apply = getattr(config, "auto_apply_enabled", None)
    if auto_apply is True:
        errors.append("auto_apply_enabled must be False — auto apply is permanently blocked")

    if training < 21:
        warnings.append("training_length < 21 days — very short training window")
    if validation < 5:
        warnings.append("validation_length < 5 days — very short validation window")
    if step > training:
        warnings.append("step_length > training_length — windows may not overlap meaningfully")

    return {"is_valid": len(errors) == 0, "errors": errors, "warnings": warnings}


def validate_window(window) -> Dict[str, Any]:
    """Validate a WalkForwardWindow. Returns dict with is_valid, errors, warnings."""
    errors = []
    warnings = []

    if window is None:
        return {"is_valid": False, "errors": ["window is None"], "warnings": []}

    train_start = getattr(window, "training_start", None)
    train_end = getattr(window, "training_end", None)
    val_start = getattr(window, "validation_start", None)
    val_end = getattr(window, "validation_end", None)

    if train_start and train_end and train_start >= train_end:
        errors.append(f"training_start ({train_start}) must be before training_end ({train_end})")

    if train_end and val_start and train_end > val_start:
        errors.append(f"training_end ({train_end}) must be <= validation_start ({val_start})")

    if val_start and val_end and val_start >= val_end:
        errors.append(f"validation_start ({val_start}) must be before validation_end ({val_end})")

    return {"is_valid": len(errors) == 0, "errors": errors, "warnings": warnings}
