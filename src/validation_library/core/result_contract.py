"""Normalize legacy validation return values; refuse ambiguous results."""

from .severity import normalize_severity, RANKS, string_types


def _record_passed(record):
    if not isinstance(record, dict):
        raise ValueError("Each validation record must be a dictionary")
    if isinstance(record.get("passed"), bool):
        return record["passed"]
    if isinstance(record.get("success"), bool):
        return record["success"]
    status = record.get("status")
    if isinstance(status, string_types) and status.upper() in ("PASS", "FAIL"):
        return status.upper() == "PASS"
    raise ValueError("Cannot determine pass/fail from record")


def normalize_validation_result(raw, key, name, default_severity="ERROR"):
    if isinstance(raw, bool):
        success, records, native_summary = raw, None, None
    elif isinstance(raw, list):
        success = all(_record_passed(item) for item in raw)
        records, native_summary = raw, None
    elif isinstance(raw, dict):
        if isinstance(raw.get("success"), bool):
            success = raw["success"]
        elif isinstance(raw.get("passed"), bool):
            success = raw["passed"]
        elif isinstance(raw.get("status"), string_types) and raw["status"].upper() in ("PASS", "FAIL"):
            success = raw["status"].upper() == "PASS"
        else:
            raise ValueError("Validation %s returned a dictionary without success/passed/status" % key)
        records = raw.get("results")
        native_summary = raw.get("summary")
        if records is not None and not isinstance(records, list):
            raise ValueError("results must be a list for %s" % key)
    else:
        raise ValueError("Unsupported validation return type for %s" % key)
    if records is not None:
        passed = sum(1 for record in records if _record_passed(record))
        failed = len(records) - passed
    else:
        passed, failed = (1, 0) if success else (0, 1)
    severity = None
    if not success:
        values = []
        if isinstance(native_summary, dict) and native_summary.get("highest_severity"):
            values.append(normalize_severity(native_summary["highest_severity"]))
        if isinstance(raw, dict) and raw.get("severity"):
            values.append(normalize_severity(raw["severity"]))
        if records is not None:
            for record in records:
                if not _record_passed(record) and record.get("severity"):
                    values.append(normalize_severity(record["severity"]))
        severity = max(values, key=lambda x: RANKS[x]) if values else normalize_severity(default_severity)
    summary = dict(native_summary) if isinstance(native_summary, dict) else {"pass": passed, "fail": failed, "total": passed + failed}
    return {"validation_key": key, "validation_name": name, "success": success, "summary": summary, "highest_severity": severity, "results": records}
