# Install — ug-ug

Standalone (without the rest of the kit):

```bash
cp -r skills/ug-ug/ /path/to/your/project/skills/
# No lib dependency — pure rule-based transformer.
```

Slash trigger:

```bash
cp skills/ug-ug/commands/ug-ug.toml ~/.claude/commands/
```

Verify:

```bash
python -m skills.ug-ug --level full < input.md
```
