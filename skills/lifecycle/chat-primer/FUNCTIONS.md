# FUNCTIONS: chat-primer

## Pure functions (Lambda candidates)

| Function | Input | Output | Lambda? | Notes |
|---|---|---|---|---|
| `check_file_exists(path)` | str | bool | ✅ | Phase 1 detection |
| `extract_project_skills(claude_md_text)` | str | `[skill_paths]` | ✅ | Phase 1.5; regex `wip/` paths from CLAUDE.md |
| `detect_project_domains(skill_paths)` | `[str]` | `[domains]` | ✅ | Phase 1.5; maps skill names → domain labels |
| `load_registry_by_domain(registry_path, domains)` | str, `[str]` | `[{skill, domain, added, role}]` | ✅ | Phase 1.5; reads REGISTRY.md, filters by domain |
| `diff_hub_vs_project(hub_skills, project_skills, ignored_path)` | lists, str | `[candidate_skills]` | ✅ | Phase 1.5; set diff + dismissed filter |
| `write_hub_drift_md(candidates, output_path, claude_md_date)` | list, str, str | written file | ✅ | Phase 1.5 |
| `parse_handover(path)` | str | `{open, done, decisions, next}` | ✅ | Phase 3; returns empty dict if file missing |
| `select_token_mode(signals)` | `{loc_count, loop_type, doc_injection}` | `{context_mode, token_savior, token_compressor}` | ✅ | Phase 4 lookup table |
| `check_mcp_json(path)` | str | `{token_savior_present, context_mode_present}` | ✅ | Phase 4; JSON parse |
| `ping_ollama(url)` | str | `{ok: bool, models: []}` | ✅ | Phase 7; HTTP GET /api/tags |
| `parse_installed_models(api_response)` | dict | `[model_names]` | ✅ | Phase 7 |
| `check_vault_env()` | — | `{pw_set: bool}` | ✅ | Phase 6; `os.environ.get("KEEPASSXC_PASSWORD")` |
| `scaffold_references_md(claude_md_text, project_root)` | str, str | written file | ✅ | Phase 8; regex extract paths from CLAUDE.md |
| `scan_finetune_candidates(skills_list)` | `[{name, model, step}]` | `[candidates]` | ✅ | Phase 9; rule-based: classification steps using API model |
| `scaffold_test_config(project_root)` | str | written JSON | ✅ | Phase 10; template fill |
| `build_session_card(all_phase_results)` | dict | str (card text) | ✅ | Phase 12; string template |

## AI-assisted steps

None — chat-primer is fully deterministic. All phases use file reads, HTTP pings, and rule-based checks. No LLM calls required.

## External services / dependencies

| Dep | Call | Notes |
|---|---|---|
| Ollama | `GET http://localhost:11434/api/tags` | Model availability check; fail gracefully |
| KeePassXC vault | `get_secret(key)` via `keepassxc-secrets` wrapper | Smoke-test vault access; read-only |
| File system | `os.path.exists`, `open()` | CLAUDE.md, HANDOVER.md, _references.md, .mcp.json |

## Related skills (imported, not called directly)

| Skill | Why |
|---|---|
| `keepassxc-secrets` | Vault smoke-test in Phase 6 |
| `token-savior-mcp` | Configured if missing (Phase 4) |
| `context-mode` | Configured if missing (Phase 4) |
| `memory-ladder` | Memory verification (Phase 5) |
| `session-handover` | Handoff standard verification (Phase 11) |
