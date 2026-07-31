# Install — session-handover

Standalone (without the rest of the kit):

```bash
cp -r skills/session-handover/ /path/to/your/project/skills/
# No external dependencies.
```

Slash trigger:

```bash
cp skills/session-handover/commands/session-handover.toml ~/.claude/commands/
```

Verify:

```bash
python -m skills.session-handover --out-path ./HANDOVER.md
```
