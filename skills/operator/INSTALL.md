# Install — operator

Standalone (without the rest of the kit):

```bash
cp -r skills/operator/ /path/to/your/project/skills/
```

Slash trigger:

```bash
cp skills/operator/commands/operator.toml ~/.claude/commands/
```

Verify:

```bash
python -m operator_skill "lint this skill"
```
