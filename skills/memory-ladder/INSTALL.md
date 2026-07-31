# Install — memory-ladder

Standalone (without the rest of the kit):

```bash
cp -r skills/memory-ladder/ /path/to/your/project/skills/
# No lib dependency — pure-stdlib.
```

Slash trigger:

```bash
cp skills/memory-ladder/commands/memory-ladder.toml ~/.claude/commands/
```

Verify:

```bash
python -m skills.memory-ladder --slug test --append "hello"
```
