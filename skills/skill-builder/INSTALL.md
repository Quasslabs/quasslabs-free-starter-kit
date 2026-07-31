# Install — skill-builder

Standalone (without the rest of the kit):

```bash
cp -r skills/skill-builder/ /path/to/your/project/skills/
```

Slash trigger:

```bash
cp skills/skill-builder/commands/skill-builder.toml ~/.claude/commands/
```

Verify:

```bash
python -m skill_builder "my-new-skill" "Does X for Y"
```
