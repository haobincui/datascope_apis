
# Extraction processes

## process for on demand extraction

body -> send extraction request -> send location -> send job id -> get data

```flow
Title: Process for On Demand Extraction
Local->Server: Post Instrument Id
Server-->: Return Location

Local->Server: Get Location url
Server-->Local: Return JobId

Local->Server: Get JobId
Server-->Local: Result data

Note righ of Server: DataScope Server
Note left of Local: Local User
```

body: 
```python
from connection.features.extraction.on_demand_extractioner.on_demand_extractioner import OnDemandExtractioner
type(body) = OnDemandExtractioner()

```

## APIs for extraction

Three steps for getting Extraction data:
1. send (post request) the input, and return the location id if (respond-async) else job id (use location id in this function)
    response for location id is much faster
```python
from connection.client import post_extractions_request
location = post_extractions_request(extraction_type, body, token)
```

2. send (get request) the location id via the location id
[e.g. https://selectapi.datascope.refinitiv.com/RestApi/v1/Extractions/ExtractRawResult(ExtractionId='0x0854280de7887be2')]
    to get the job id and notes.
```python
from connection.client import get_job_id_by_location
job_id = get_job_id_by_location(location, token)
```
3. send (get request) the job id via ./RawExtractionResults('job id')/$value, return the results

```python
from connection.client import get_extraction_data_by_job_id

data = get_extraction_data_by_job_id(extraction_types, job_id, token)
```

All the steps are packaged into one step:
```python
from connection.client import get_extraction_result_value
data = get_extraction_result_value(extraction_type, body, token)
```