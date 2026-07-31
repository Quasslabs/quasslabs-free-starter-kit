# Install — notify

Standalone (without the rest of the kit):

```bash
cp -r skills/notify/ /path/to/your/project/skills/
pip install requests
```

Slash trigger:

```bash
cp skills/notify/commands/notify.toml ~/.claude/commands/
```

Set env vars (see SETUP.md):

```bash
export TELEGRAM_BOT_TOKEN=...
export TELEGRAM_CHAT_ID=...
```

Verify:

```bash
python -m skills.notify --level report --message "notify ready"
```
