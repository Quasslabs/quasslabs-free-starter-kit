# FUNCTIONS: freellmapi

All callable via `<routines>/_lib_llm.py`. No separate module needed.

---

## call_free_cloud (primary entry point)

```python
def call_free_cloud(
    prompt: str,
    model: str,
    task_type: str = "bench",
    system_prompt: str = "",
    timeout: int = 60,
    allow_sensitive_override: bool = False,
) -> str:
    """
    Call freellmapi free-cloud proxy (OpenAI-compatible) — NON-SENSITIVE only.

    Guards:
      - task_type must be in {bench, experiment, scratch, public}
      - prompt + system_prompt must not match sensitive patterns
      - FREELLMAPI_KEY env var must be set

    Returns generated text, or "" on refusal/failure (never raises).
    Callers treat "" as "free-cloud unavailable" and fall back to local/Mac mini.

    Args:
        prompt:                  User prompt.
        model:                   Model ID ("auto" recommended — proxy picks best).
        task_type:               Must be allowlisted (bench | experiment | scratch | public).
        system_prompt:           Optional system prompt.
        timeout:                 Seconds before timeout.
        allow_sensitive_override: Bypass content guard (only for vetted prompts).
    """
```

**Import:**
```python
from _lib_llm import call_free_cloud
```

**Allowed task types:**
```python
_FREE_CLOUD_ALLOWED_TASKS = {"bench", "experiment", "scratch", "public"}
```

**Sensitive pattern refusal (auto-detected in prompt + system_prompt):**
```python
# Refused patterns (partial list):
# \bpassword\b, \bsecret\b, \bapi[_-]?key\b, \bvault\b, \bcredential
# \bAKIA[0-9A-Z]{16}\b  (AWS key format)
# \bsk-[A-Za-z0-9]{20,}\b  (OpenAI-style key)
# \bworklog\b, \bclient\b, \bengagement\b
# email addresses
```

---

## is_freellmapi_available (health probe)

```python
import urllib.request

def is_freellmapi_available(
    url: str = "http://localhost:3001",
    key: str = "",
    timeout: int = 3,
) -> bool:
    """Return True if freellmapi proxy is reachable and responding."""
    try:
        req = urllib.request.Request(
            f"{url}/v1/models",
            headers={"Authorization": f"Bearer {key}"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status == 200
    except Exception:
        return False
```

---

## list_available_models

```python
import json, urllib.request, os

def list_available_models(
    url: str = "http://localhost:3001",
    key: str = "",
) -> list[str]:
    """Return list of model IDs available in this freellmapi build."""
    key = key or os.getenv("FREELLMAPI_KEY", "")
    req = urllib.request.Request(
        f"{url}/v1/models",
        headers={"Authorization": f"Bearer {key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read())
            return [m["id"] for m in data.get("data", [])]
    except Exception as e:
        print(f"[freellmapi] list_models failed: {e}")
        return []
```

---

## add_provider_key (API — no auth required, CORS-gated)

```python
import json, urllib.request

def add_provider_key(
    platform: str,
    key: str,
    label: str = "",
    url: str = "http://localhost:3001",
) -> bool:
    """
    Add a free-tier provider key via freellmapi API.
    No auth required — CORS-gated to localhost.

    platform values: "google" | "groq" | "cerebras" | "openrouter" | "github"
    Returns True on success.
    """
    body = json.dumps({
        "platform": platform,
        "key": key,
        "label": label or platform,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{url}/api/keys",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status in (200, 201)
    except Exception as e:
        print(f"[freellmapi] add_key failed platform={platform}: {e}")
        return False
```

---

## Lambda / Step Functions candidates

| Function | Stateless? | Lambda? |
|---|---|---|
| `call_free_cloud` | yes | No — requires localhost proxy running; not network-accessible externally |
| `is_freellmapi_available` | yes | No — same reason |
| `list_available_models` | yes | No — same reason |
| `add_provider_key` | yes | No — same reason |

All functions require the proxy to be running locally. None are Lambda-compatible.
