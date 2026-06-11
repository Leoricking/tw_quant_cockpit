# Error Report Template

> **Research Only. No Real Orders. Production Trading BLOCKED.**
> **Broker Execution Disabled. VALIDATED does not enable trading.**
> **Not Investment Advice.**

---

## Date: [YYYY-MM-DD]

## Error ID: [ERR-YYYY-MM-DD-NNN]

## 一、Error Summary

| Field | Value |
|-------|-------|
| Error Type | ImportError / ValueError / FileNotFoundError / Other |
| Component | [module/command name] |
| Severity | Critical / High / Medium / Low |
| Classification | KNOWN_WARNING / NEW_ISSUE |

## 二、Error Message

```
[paste full error message here]
```

## 三、Steps to Reproduce

1. 
2. 
3. 

Command that triggered the error:

```
python main.py [command] [args]
```

## 四、Diagnosis

Root cause (if known):

- 

Related files:

- 

## 五、Resolution Steps

Steps taken to resolve:

1. 
2. 

## 六、Verification

After fix, verify with:

```
python main.py safety-scan --target all
```

```
python main.py regression-run --suite release_gate --mode real
```

Expected: 0 BLOCKED, all tests pass.

## 七、Prevention

Steps to prevent recurrence:

- 

## 八、Safety Confirmation

- [ ] Fix does not introduce real trading actions
- [ ] Safety scan passes after fix
- [ ] Regression passes after fix
- [ ] Fix committed with correct git -C format (not git add .)

---

## Safety Declaration

This template is Research Only. No Real Orders. Production Trading BLOCKED.
Broker Execution Disabled. Templates do not enable trading.

---

*TW Quant Cockpit v1.0.6 — Example Workflows & Templates — Research Only — Not Investment Advice*
