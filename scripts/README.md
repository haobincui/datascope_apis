# Scripts Directory Convention

## Purpose

`scripts/` contains runnable examples, one-off jobs, and data extraction workflows.

## Folder Naming

1. Use lowercase `snake_case`.
2. Use domain-first naming:
   - `market_data/...`
   - `connection/...`
   - `multi_threads/...`
3. Time-stamped folders are allowed only for frozen snapshots (for example, `tick_data_20241212`).
4. Output folders should be named `output/` (or `outputs/` when multiple variants are required).

## File Naming

1. Script files should start with `script_` and describe intent.
2. Prefer one concern per script (search, extraction, transform, validation).
3. Shared helper logic should live under `src/`, not duplicated across scripts.
