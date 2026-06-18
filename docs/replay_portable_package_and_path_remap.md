# Replay Portable Package & Path Remap — v1.2.8

> [!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
> [!] Packages must never contain secrets, .env, API tokens, broker credentials, or absolute paths.

---

## Portable Packages

A portable package bundles a dataset manifest, metadata, and optional files for cross-computer transfer.

### Path Modes

| Mode | Description |
|------|-------------|
| `MANIFEST_ONLY` | Manifest only, no files |
| `METADATA_ONLY` | Manifest + metadata, no raw data |
| `FULL_PORTABLE` | All files included |
| `RELATIVE_ONLY` | **Default** — all paths must be relative (no absolute paths) |

> `RELATIVE_ONLY` is always enforced. Packages with absolute paths are **blocked**.

### Secret Scan

Before packaging, the system automatically scans for:

```
.env, secret, credential, token, api_key, password,
broker, shioaji, megabroker
```

If any secret pattern is detected, the package is **blocked**.

### CLI

```bash
python main.py replay-package-export-preview --dataset-id DS-001
python main.py replay-package-export --dataset-id DS-001 --execute --allow-write
python main.py replay-package-import-preview --package-path /path/to/package.zip
python main.py replay-package-import --package-path /path/to/package.zip --execute --allow-write
```

---

## Path Remap

When importing a package on a different machine, paths must be remapped from the portable relative paths to the local absolute paths.

### Remap Process

1. **Preview** — show what will be remapped (never writes)
2. **Execute** — apply remapping (requires `--allow-write`)
3. **Validate** — confirm no absolute paths remain in stored metadata

### Rules

- `strip_absolute()` removes absolute path components
- `validate_no_absolute()` fails if any absolute path survives
- `remap_history()` records all remap operations
- Remapping does **not** move raw data files

### CLI

```bash
python main.py replay-package-import-preview --package-path /path/to/package.zip
```

---

## Conflict Detection

When importing a package, conflicts are detected automatically:

| Conflict Type | Description |
|---------------|-------------|
| `DUPLICATE_FINGERPRINT` | Same fingerprint already exists |
| `DUPLICATE_DATASET_ID` | Same dataset ID already registered |
| `FINGERPRINT_MISMATCH` | Fingerprint doesn't match manifest |
| `VERSION_CONFLICT` | Version already exists for this dataset |
| `BROKEN_LINEAGE` | Lineage references missing dataset |
| `INCOMPATIBLE_MODE` | Mode mismatch (REAL vs MOCK) |
| `INCOMPATIBLE_QUALIFICATION` | Qualification mismatch |
| `STALE_HASH` | File hashes don't match registry |
| `MISSING_REQUIRED_FILE` | Required file not in package |
| `SECRET_DETECTED` | Secret pattern found in package |
| `ABSOLUTE_PATH_DETECTED` | Absolute path found in package |
| `REGISTRY_LOCK` | Registry locked for maintenance |
| `CUSTOM` | User-defined conflict |

> `AUTO_REGISTRY_CONFLICT_RESOLUTION_ENABLED = False`
> Conflicts are **never** auto-resolved. All resolutions require explicit user action.

---

## Safety Checklist for Package Export

Before exporting, verify:

- [ ] No `.env` files included
- [ ] No API tokens, secrets, or credentials
- [ ] No broker credentials (`shioaji`, `megabroker`)
- [ ] Path mode is `RELATIVE_ONLY`
- [ ] All paths validated — no absolute paths
- [ ] Fingerprint hash matches registry record

---

*[!] Research Only. No Real Orders. Not Investment Advice.*
