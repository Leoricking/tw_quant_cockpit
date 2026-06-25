"""portfolio/stable_rollup/compatibility_registry_v159.py — Compatibility registry v1.5.9."""


def _parse_ver(v):
    """Parse version string to tuple, ignoring label text."""
    return tuple(int(x) for x in str(v).split()[0].split(".")[:4] if x.isdigit())


COMPATIBILITY_REGISTRY = {
    "current_version": "1.5.9",
    "schema_versions": {
        "portfolio": "1.5.0",
        "sizing": "1.5.1",
        "correlation": "1.5.2",
        "risk": "1.5.3",
        "walk_forward": "1.5.4",
    },
    "supported_version_range": {"min": "1.5.0", "max_major": 1, "max_minor": 6},
    "deprecated_versions": [],
    "incompatible_versions": [],
    "notes": "Versions 1.5.0+ are compatible. v2.0.0 is NOT automatically accepted.",
}


class CompatibilityRegistryV159:
    def get_registry(self):
        return dict(COMPATIBILITY_REGISTRY)

    def is_compatible(self, version: str) -> dict:
        """Check if version is compatible. Uses semantic range, not whitelist."""
        try:
            v = _parse_ver(version)
            if len(v) < 2:
                return {"compatible": False, "reason": "MALFORMED_VERSION", "version": version}
            major, minor = v[0], v[1]
            if major == 1 and minor >= 5:
                return {"compatible": True, "reason": "WITHIN_SUPPORTED_RANGE", "version": version}
            elif major >= 2:
                return {"compatible": False, "reason": "FUTURE_MAJOR_NOT_AUTO_ACCEPTED", "version": version}
            elif major == 1 and minor < 5:
                return {"compatible": False, "reason": "BELOW_MINIMUM_1_5_0", "version": version}
            else:
                return {"compatible": False, "reason": "OUT_OF_RANGE", "version": version}
        except Exception as e:
            return {"compatible": False, "reason": f"MALFORMED_VERSION:{e}", "version": version}

    def validate(self):
        issues = []
        result = self.is_compatible("1.5.9")
        if not result["compatible"]:
            issues.append("CURRENT_VERSION_NOT_COMPATIBLE")
        result_future = self.is_compatible("2.0.0")
        if result_future["compatible"]:
            issues.append("FUTURE_MAJOR_AUTO_ACCEPTED")
        return {"valid": len(issues) == 0, "issues": issues}
