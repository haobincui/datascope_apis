from connection.client import post_extractions_request, get_extraction_result_value, get_job_id_by_location, \
    get_extraction_data_by_job_id, get_data_file_id_by_job_id
from src.connection.features.extraction.enums.extraction_types import ExtractionTypes

# %% example of get location url

# body = {
#     "ExtractionRequest": {
#         "@odata.type": "#DataScope.Select.Api.Extractions.ExtractionRequests.TickHistoryMarketDepthExtractionRequest",
#         "MarketDepthContentFieldNames": [
#             "Ask Price",
#             "Bid Price"
#         ],
#         "IdentifierList": {
#             "@odata.type": "#DataScope.Select.Api.Extractions.ExtractionRequests.InstrumentIdentifierList",
#             "InstrumentIdentifiers": [
#                 {
#                     "Identifier": "JPY1MD=",
#                     "IdentifierType": "Ric"
#                 }
#             ],
#             "ValidationOptions": None,
#             "UseUserPreferencesForValidationOptions": False
#         },
#         "Condition": {
#             "View": "NormalizedLL2",
#             "NumberOfLevels": 2,
#             "MessageTimeStampIn": "GmtUtc",
#             "ReportDateRangeType": "Range",
#             "QueryStartDate": "2019-01-18T00:00:00.000Z",
#             "QueryEndDate": "2020-09-19T00:00:00.000Z",
#             "DisplaySourceRIC": True
#         }
#     }
# }
body = {
    "ExtractionRequest": {
        "@odata.type": "#DataScope.Select.Api.Extractions.ExtractionRequests.TickHistoryTimeAndSalesExtractionRequest",
        "MarketDepthContentFieldNames": [
            "Quote - Bid Size"
        ],
        "IdentifierList": {
            "@odata.type": "#DataScope.Select.Api.Extractions.ExtractionRequests.InstrumentIdentifierList",
            "InstrumentIdentifiers": [
                {
                    "Identifier": "IBM.N",
                    "IdentifierType": "Ric"
                }
            ],
            "ValidationOptions": None,
            "UseUserPreferencesForValidationOptions": False
        },
        "Condition": {
            "MessageTimeStampIn": "GmtUtc",
            "ApplyCorrectionsAndCancellations": False,
            "ReportDateRangeType": "Range",
            "QueryStartDate": "2016-11-20T20:21:56.000Z",
            "QueryEndDate": "2016-11-23T20:21:56.000Z",
            "DisplaySourceRIC": False
        }
    }
}

extraction_type = ExtractionTypes.ExtractRaw

res = post_extractions_request(extraction_type=extraction_type,
                               body=body)

print(res)

# %% example of get job id via location url

location = "https://selectapi.datascope.refinitiv.com/RestApi/v1/Extractions/ExtractRawResult(ExtractionId='0x085491b952187c9e')"

job_id = get_job_id_by_location(location=location)
print(job_id)

# %% example of get data via job id
job_id = '0x085491b952187c9e'

data_1 = get_extraction_data_by_job_id(extraction_type=extraction_type,
                                       job_id=job_id)

print(data_1)

# %% example of get the data via one function

data_2 = get_extraction_result_value(extraction_type, body)

print(data_2)

# %% example of get the completed files
job_id = '0x085491b952187c9e'
files = get_data_file_id_by_job_id(job_id)
print(files)
