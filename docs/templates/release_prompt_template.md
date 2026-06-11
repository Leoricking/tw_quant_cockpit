# Release Prompt Template

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## Release: v[VERSION] — [RELEASE_NAME]

## 一、Release Summary

| Field | Value |
|-------|-------|
| Version | v[VERSION] |
| Release Name | [RELEASE_NAME] |
| Type | Maintenance / Feature / Documentation |
| Base Version | v1.0.0 Research Trading Cockpit Stable |
| No Real Orders | True |
| Production Trading | BLOCKED |

## 二、Changes

- [List changes here]
- [Each change on its own line]

## 三、Files to Add (Never git add .)

List files to add individually:

```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" add [file1]
```

```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" add [file2]
```

**Rule: Always add files individually. Never use `git add .`**

## 四、Commit Command (Multiple -m Flags, No Heredoc, No Chain Commands)

```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" commit -m "[type]: [short description] v[VERSION]" -m "[longer description. Research Only. No Real Orders.]"
```

**Rules:**
- Use `git -C "path" commit` — never `cd path && git commit`
- Use multiple `-m` flags — never heredoc (`<<EOF`)
- Do not chain commands with `&&`, `;`, `||`, or `|`
- Do not use `git add .`

## 五、Tag Command

```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" tag -a v[VERSION] -m "v[VERSION]: [RELEASE_NAME]"
```

## 六、Push Commands (Separate, Never Chained)

```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" push origin main
```

```
git -C "C:/Users/Rossi/Documents/Claude/trading_master" push origin v[VERSION]
```

**Rule: Push main and tag as separate commands. Never chain with `&&`.**

## 七、Pre-Release Validation Checklist

Run each command separately:

```
python main.py safety-scan --target all
```

```
python main.py research-cockpit-stable --mode real
```

```
python main.py regression-run --suite release_gate --mode real
```

```
python main.py stable-v060-check --mode real
```

Expected:
- safety-scan: 0 BLOCKED
- research-cockpit-stable: all checks PASS or acceptable WARN
- regression-run: all required tests PASS

## 八、Files Never to Commit

- `reports/*.md` — runtime report outputs
- `data/backtest_results/**` — runtime data
- `.env` — secrets
- `*.db` — databases
- `*.csv` in data directories

## 九、Safety Confirmation

- [ ] No real trading actions in any changed files
- [ ] Safety scan returns 0 BLOCKED
- [ ] Regression tests pass
- [ ] No runtime outputs committed
- [ ] git -C format used throughout
- [ ] No chain commands used
- [ ] No heredoc in commit message

---

## Safety Declaration

This template is Research Only. No Real Orders. Production Trading BLOCKED.
Broker Execution Disabled. Release templates do not enable trading.

---

*TW Quant Cockpit v1.0.6 — Example Workflows & Templates — Research Only — Not Investment Advice*
