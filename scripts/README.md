# Scripts Layout

`scripts/` is split into two groups:

- `scripts/examples/`: runnable usage examples and exploratory snippets.
- `scripts/jobs/`: batch jobs, replay tasks, and dated production snapshots.

## Conventions

1. Use `src.*` imports only.
2. Do not use `sys.path.insert(...)`.
3. Keep generated outputs under local `output/` folders and out of tracked source logic.
4. Prefer moving shared logic into `src/` instead of duplicating it across scripts.
