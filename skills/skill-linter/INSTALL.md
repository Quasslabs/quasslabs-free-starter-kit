# Install — skill-linter

Standalone (without the rest of the kit):

```bash
cp -r skills/skill-linter/ /path/to/your/project/skills/
```

Slash trigger:

```bash
cp skills/skill-linter/commands/skill-linter.toml ~/.claude/commands/
```

Verify:

```bash
python -m skill_linter skills/skill-linter/SKILL.md
```
