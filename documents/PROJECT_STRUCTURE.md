# Project Structure and Naming Rules

## Directory Layout

```text
.
├── src/
│   ├── calendar/                  # Date/time conversion, schedules, holiday logic
│   ├── connection/                # DataScope domain
│   │   ├── apis/                  # High-level creators/facades
│   │   ├── extraction/            # Extraction models and extractors
│   │   ├── search/                # Search models and searchers
│   │   ├── shared/                # Shared abstractions/settings
│   │   ├── infra/http/            # HTTP clients (auth/search/extraction/download)
│   │   └── utils/                 # Reusable connection-domain utilities
│   ├── market_data/
│   │   ├── contract/              # Contract parsing and maturity rules
│   │   ├── dto/                   # Market data DTOs
│   │   └── processing/            # Data merge/filter/validation
│   ├── multi_thread/
│   ├── math_tools/
│   └── error/
├── scripts/
│   ├── examples/
│   └── jobs/
├── tests/
└── documents/
```

## Naming Rules

1. Use `snake_case` for files/modules.
2. Use canonical class names:
   - `*Extractor` (not `*Extractioner`)
   - `DatetimeSplitter` (not `DatetimeSpliter`)
3. Use `src.*` imports only.
4. Keep legacy compatibility aliases out of new code.

## Configuration Rules

1. Credentials must come from environment variables (`DATASCOPE_USERNAME`, `DATASCOPE_PASSWORD`).
2. `src/application.ini` is allowed only as local fallback without committed secrets.
3. Use `src/application.example.ini` as onboarding template.

## Testing Rules

1. Offline/unit tests run by default.
2. Network/integration tests must be explicitly enabled (`DATASCOPE_RUN_INTEGRATION=1`).
