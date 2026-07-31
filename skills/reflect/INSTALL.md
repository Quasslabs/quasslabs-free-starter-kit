# Install — reflect

Standalone (without the rest of the kit):

```bash
cp -r skills/reflect/ /path/to/your/project/skills/
# No external dependencies.
```

Slash trigger:

```bash
cp skills/reflect/commands/reflect.toml ~/.claude/commands/
```

Verify:

```bash
python -m skills.reflect --notes-path .
```
