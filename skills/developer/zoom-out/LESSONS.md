# LESSONS — zoom-out

_(Seeded 2026-05-14 from mattpocock/skills import.)_

## Why we imported this

A one-prompt discipline skill. We have plenty of "do something specific" skills; this is the rare "stop doing the specific thing and tell me the map" skill. Cheap to have, high-value when needed.

## Usage pattern

- Often invoked mid-session when an agent is stuck. The user types "zoom out" and the agent switches modes.
- Pairs naturally with `improve-codebase-architecture` (architect mode) and `arch-decision` (lock-the-seam mode).
- The `disable-model-invocation: true` flag in the frontmatter means the model shouldn't decide to invoke this on its own — it's a human-triggered escape hatch.

## Integration

- **Triggers**: "zoom out", "give me the map", "what calls this", "I don't know this area"
- **Don't pair with**: ug-ug-ultra in the same response — the output IS the map, it needs to be readable.
