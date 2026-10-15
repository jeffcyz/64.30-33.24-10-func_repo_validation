"""Severity normalization and comparisons (Python 2.7 / IronPython-friendly syntax)."""

SEVERITIES = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
RANKS = dict((name, index) for index, name in enumerate(SEVERITIES))


def normalize_severity(value):
    if not isinstance(value, str):
        raise ValueError("Severity must be a string")
    severity = value.strip().upper()
    if severity not in RANKS:
        raise ValueError("Unknown severity: %s" % value)
    return severity


def meets_threshold(severity, threshold):
    return RANKS[normalize_severity(severity)] >= RANKS[normalize_severity(threshold)]
