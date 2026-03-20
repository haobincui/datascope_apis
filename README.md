# datascope_apis

`datascope_apis` is a Python toolkit for Refinitiv DataScope extraction/search workflows plus market-data post-processing helpers.

## Requirements
- Python `>=3.10`
- Install dependencies:

```bash
pip install -e .
```

## Credentials and Settings
Credentials are loaded from environment variables first:

- `DATASCOPE_USERNAME`
- `DATASCOPE_PASSWORD`
- `DATASCOPE_GATEWAY_IP` (optional, default `selectapi.datascope.refinitiv.com/RestApi/v1`)
- `DATASCOPE_TIMEOUT_SECONDS` (optional)
- `DATASCOPE_MAX_RETRIES` (optional)
- `DATASCOPE_RETRY_BACKOFF_SECONDS` (optional)

Fallback config file: `src/application.ini`.
Use `src/application.example.ini` as a template. Do not commit real credentials.

## Project Layout

```text
src/
  calendar/
  connection/
    apis/
    extraction/
    search/
    shared/
    infra/http/
    utils/
  market_data/
    contract/
    dto/
    processing/
  multi_thread/
  math_tools/
  error/

tests/
scripts/
  examples/
  jobs/
```

## Tests
Offline tests (default):

```bash
python -m unittest discover -s tests -p 'test*.py'
```

Integration tests are skipped by default. Enable with:

```bash
DATASCOPE_RUN_INTEGRATION=1 python -m unittest discover -s tests -p 'test*.py'
```

## Script Conventions
- `scripts/examples/`: runnable demos.
- `scripts/jobs/`: batch/replay jobs and dated snapshots.
- Avoid `sys.path.insert(...)`; run scripts from repository root using `python -m` or direct module paths.
