# Install — ollama-task-router

Standalone (requires kit `lib/_lib_llm.py`):

```bash
cp -r skills/ollama-task-router/ /path/to/your/project/skills/
cp lib/_lib_llm.py /path/to/your/project/lib/
pip install requests
```

Set:

```bash
export OLLAMA_HOST=http://localhost:11434
```

Slash trigger:

```bash
cp skills/ollama-task-router/commands/ollama-task-router.toml ~/.claude/commands/
```

Verify (requires Ollama running with phi4-mini pulled):

```bash
python -m skills.ollama-task-router "classify this email"
```
