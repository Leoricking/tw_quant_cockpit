# API Provider Hardening & Token-Safe Setup (v0.3.18)

## v0.3.18 目標

強化 TW Quant Cockpit API provider 基礎設施：

- 讓 FinMind / TWSE / TPEx / MOPS / future Mega read-only provider 可以安全被 scheduler 使用。
- Token-safe 設定：token 只讀 `.env`，不 log，不 commit，不顯示完整值。
- Provider Health Check：所有 provider 可回報狀態，快速、安全、不 crash。
- GUI 顯示 Provider Health、Token Status（masked）、Capability Matrix。
- CLI `provider-health` 指令可快速查看狀態。

**定位：只做 read-only provider hardening。不下單。不接實盤。**

---

## Provider Health 是什麼

Provider Health 是對各個資料來源的可用性、token 設定狀態、網路狀態的定期快速檢查。

每個 provider 回報：

| 欄位 | 說明 |
|------|------|
| `status` | OK / NOT_CONFIGURED / PARTIAL / FAILED / PLANNED / DISABLED |
| `read_only` | 永遠 True |
| `no_real_orders` | 永遠 True |
| `token_required` | 是否需要 token |
| `token_configured` | token 是否已設定 |
| `token_masked` | masked token（例如 `abc****xyz`） |
| `message` | 狀態說明 |
| `recommended_action` | 建議行動 |

---

## Token-Safe Setup

### 原則

1. Token 只從 `.env` 讀取，不 hardcode 在程式碼。
2. Token 在 log / report 中只顯示 mask（例如 `abc****xyz`）。
3. `.env` 在 `.gitignore`，永遠不 commit。
4. `.env.example` 有安全範例，可 commit，不含真實 token。
5. 不自動建立或修改真實 `.env`。

### TokenSafeConfig

```python
from data.providers.token_safe_config import TokenSafeConfig

cfg = TokenSafeConfig(env_path=".env")
cfg.load_env()

# 讀取 token（不 log）
token = cfg.get_token("FINMIND_TOKEN")  # None 如果未設定

# 取得 masked 版本（可安全顯示）
masked = cfg.get_masked_token("FINMIND_TOKEN")  # "abc****xyz"

# 檢查是否設定
if cfg.has_token("FINMIND_TOKEN"):
    print("Token 已設定")

# 建立 .env.example
cfg.create_env_example(path=".env.example")
```

---

## .env / .env.example 使用方式

### 設定步驟

1. 複製 `.env.example` 為 `.env`：

```bash
cp .env.example .env
```

2. 編輯 `.env`，填入你的 token：

```
FINMIND_TOKEN=your_actual_token_here
```

3. 確認 `.env` 不在 git：

```bash
git status  # .env 不應出現
```

### .env.example 安全規則

- `.env.example` 不含真實 token，可 commit。
- `.env` 含真實 token，永遠不 commit。
- `.gitignore` 已設定 `.env` 被排除。

---

## FinMind Token 設定方式

1. 前往 [https://finmindtrade.com/](https://finmindtrade.com/) 免費申請帳號。
2. 取得 API token。
3. 在 `.env` 加入：

```
FINMIND_TOKEN=your_token_here
```

4. 不設定 token 時，FinMind 仍可存取公開資料（速率限制較嚴格）。

---

## TWSE / TPEx / MOPS Fallback

- TWSE Open API、TPEx Open API、MOPS 均為公開 API，不需 token。
- 計劃於 v0.4 啟用。
- 目前系統以本地 CSV 資料為主要資料來源，不受影響。

---

## Mega Read-Only Future Plan

- 兆豐證券（Mega Securities）API 計劃於 v0.4+ 整合。
- **只做 read-only 資料查詢（行情、歷史資料）。**
- Real order execution 永久 DISABLED。
- `submit_order()` 永遠 raise RuntimeError。
- `_MEGA_ORDER_ENABLED = False`（永遠）。

---

## 為什麼不下單

TW Quant Cockpit 是研究、模擬、決策輔助系統，不是自動交易系統。

- `TWQC_ENABLE_REAL_ORDER = False`（永久）
- 所有 provider 的 `submit_order()` 都 raise RuntimeError
- `real_order_execution = False` for ALL providers（capability matrix 可驗證）
- Automation Scheduler 的 Safety Guard 封鎖所有含 order/trade/buy/sell/execute 的 task name

---

## 為什麼不顯示完整 Token

防止 token 洩漏至：

- Log 檔案（可能被誤送出）
- 報告 Markdown（可能被分享）
- GUI 截圖（可能被公開）
- git history（最難清除）

Token 只顯示 `abc****xyz` 格式的 mask，足以確認 token 有沒有設定，但不洩漏實際值。

---

## Scheduler 如何使用 Provider

Scheduler `daily_data_update` task 會：

1. 先跑 provider health check。
2. 若 FinMind token 未設定，顯示 warning，不 crash。
3. TWSE / public fallback 可用則繼續。
4. 將 `provider_health_summary` 記錄到 `latest_status.json`。

其他 task（`daily_validation`, `daily_auto_report` 等）不需要 API token，使用本地資料。

---

## CLI 使用方式

```bash
# 查看所有 provider 狀態
python main.py provider-health

# 產生 Markdown 報告
python main.py provider-health --report

# 建立 .env.example
python main.py provider-health --create-env-example

# 查看特定 provider
python main.py provider-health --provider finmind
python main.py provider-health --provider all
```

---

## GUI 使用方式

1. 開啟 TW Quant Cockpit：`python main.py cockpit`
2. 點選 **Provider Health** tab。
3. 點 **Refresh Health** 查看最新狀態。
4. 查看 Provider Status / Token Status / Capability Matrix。
5. 可點 **Generate Provider Health Report** 產生報告。
6. 可點 **Create .env.example** 建立安全範例。

---

## Troubleshooting

| 問題 | 解決方式 |
|------|---------|
| FinMind status = NOT_CONFIGURED | 在 `.env` 加入 `FINMIND_TOKEN=xxx` |
| FinMind status = FAILED | 檢查網路連線，或 FinMind 服務狀態 |
| CSV provider = PARTIAL | 執行 `python main.py import-csv` 匯入資料 |
| provider-health crash | 確認 `data/providers/` 中所有 provider 檔案存在 |
| Token 出現在 log | 確認使用 `TokenSafeConfig.get_masked_token()` 而非直接 log token |
| .env 被 commit | 執行 `git rm --cached .env` 並確認 `.gitignore` 含 `.env` |
