# Project Structure and Naming Rules

This project uses `src/` as the application package root and keeps runnable examples under `scripts/`.

## Directory Layout

```text
.
├── src/
│   ├── calendar/               # Date/time conversion and holiday logic
│   ├── connection/             # Datascope API client + extraction/search domain
│   │   ├── apis/               # High-level API facades
│   │   ├── features/           # Business features (search, extraction)
│   │   ├── utils/              # Reusable domain utilities
│   │   │   ├── comparisons/    # Comparison models/operators (canonical)
│   │   │   └── condition/      # Extraction/search conditions
│   │   └── client.py           # HTTP access and auth token management
│   ├── market_data/            # Market data domain logic
│   ├── multi_thread/           # Multi-thread orchestration
│   └── error/                  # Project-specific exceptions
├── scripts/                    # Runnable scripts and ad-hoc jobs
├── tests/                      # Unit and integration tests
├── documents/                  # Project docs
└── README.md
```

## Naming Rules

1. Use `snake_case` for all folder names and Python modules.
2. Use full words; avoid typos and abbreviations in directory/module names.
3. Use role-based suffixes for domain modules:
   - `*_extractor.py`
   - `*_condition.py`
   - `*_comparison.py`
4. Keep package names singular unless the directory is a true collection (for example, `features`, `utils`, `tests`).
5. New code should import canonical packages only; compatibility aliases are for legacy scripts.

## Canonical Paths Introduced

- `connection.utils.comparisons` (replaces misspelled `camparsions`)
- `connection.features.extraction.on_demand_extractor` (replaces `on_demand_extractioner`)
- `tick_history_time_and_sales_condition.py` (replaces `tick_history_time_and_sales_condtion.py`)
- `futures_and_options_searcher.py` (replaces `funtures_and_options_searcher.py`)

## Backward Compatibility Policy

Legacy misspelled modules are kept as alias wrappers so old scripts continue to run. New development must use canonical paths above.
