# Replay Dataset Versioning & Lineage — v1.2.8

> [!] Research Only. No Real Orders. Dataset Registry Only. No Broker.

---

## Versioning

Datasets use semantic versioning: `MAJOR.MINOR.PATCH`

- Initial version: `1.0.0`
- Create new version: requires `--execute --allow-write`
- **Frozen versions are immutable** — any hash mismatch after freeze → `CORRUPTED` status
- Frozen versions cannot be modified, extended, or re-fingerprinted silently

### Version Lifecycle

```
1.0.0 (ACTIVE) → 1.1.0 (ACTIVE) → 1.1.0 FROZEN (immutable)
                                 → CORRUPTED (if hash mismatch after freeze)
```

### CLI

```bash
python main.py replay-dataset-versions --dataset-id DS-001
python main.py replay-dataset-create-version-preview --dataset-id DS-001
python main.py replay-dataset-create-version --dataset-id DS-001 --execute --allow-write
python main.py replay-dataset-freeze-preview --dataset-id DS-001 --version 1.1.0
python main.py replay-dataset-freeze --dataset-id DS-001 --version 1.1.0 --execute --allow-write
```

---

## Dataset Lineage

Lineage tracks parent-child relationships between datasets (forks, splits, merges).

- Storage: append-only
- **No cycles allowed** — validated via DFS on every registration
- Operations: `PARENT_CHILD`, `FORK`, `SPLIT`, `MERGE`, `IMPORT`, `RESTORE`

### Lineage Tree Example

```
DS-ROOT-001
  └── DS-FORK-001 (fork of DS-ROOT-001)
        └── DS-FORK-002 (fork of DS-FORK-001)
  └── DS-SPLIT-001 (split from DS-ROOT-001)
```

### CLI

```bash
python main.py replay-dataset-lineage --dataset-id DS-001
```

---

## Deterministic Fingerprinting

Dataset fingerprints are:
- **Path-independent** (normalizes paths, strips absolute components)
- **Machine-independent** (excludes machine name, hostname)
- **Time-independent** (excludes `created_at`, `updated_at`, `frozen_at`, `archived_at`)
- **Self-excluding** (excludes the `fingerprint` field itself)

Fingerprint inputs include:
- `dataset_id`, `mode`, `symbols`, `timeframes`, `fields`
- Row counts per symbol/timeframe
- File logical roles and relative paths
- SHA-256 hashes of file content

### Excluded fields (from fingerprint calculation)

```
created_at, updated_at, frozen_at, archived_at,
fingerprint, manifest_hash, content_hash, source_reference
```

---

## Session Lineage

Session lineage tracks relationships between sessions:

| Type | Description |
|------|-------------|
| `root` | Original session, no parent |
| `fork` | Forked from a parent session |
| `duplicate` | Duplicate of a session |
| `challenge` | Challenge attempt derived from a session |
| `import` | Imported from an external package |
| `restore` | Restored from archive |

Rules:
- No cycles allowed (DFS validation)
- Challenge attempts must inherit the challenge dataset binding

---

*[!] Research Only. No Real Orders. Not Investment Advice.*
