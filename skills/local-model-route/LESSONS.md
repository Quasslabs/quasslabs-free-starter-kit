# Lessons Learned — local-model-route

| Lesson | Why it matters | Source |
|---|---|---|
| Audience and artifact format drive the workflow. | The same facts need different outputs depending on whether the consumer is a client, PM, developer, or viewer. | SKILL.md role and output sections |
| Extract deterministic helpers before calling AI for local-model-route. | Parsing, validation, routing, and manifests are cheaper and safer as pure functions. | FUNCTIONS.md classification |
| Make handoffs explicit instead of relying on chat context. | Downstream skills and agents need paths, payloads, and auth assumptions recorded in files. | SKILL.md handoffs |
