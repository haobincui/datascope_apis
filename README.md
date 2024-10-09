# datascope_apis

## development environment
python 3.8

```bash
conda create -n py38 python=3.8
conda activate py38
conda install requests scipy python-dateutil pandas==1.5.2 numpy==1.23.5
```

## Flow
consist of datascope's API, quantlib, and risk engine.  

```flow
start=>start: Input
connection=>operation: Connection
market_data=>operation: Market Data Obj
quant_lib=>operation: Quant Lib
risk_engine=>operation: Risk Engine
end=>end: Results


environment=>operation: Vol Surface and Rate Curve
start->connection(DTO)->market_data
markt_data(Instrument Obj)->quant_lib
market_date->environment
environment->quant_lib
quant_lib(Pricer)->risk_engine->end
```

## Examples:
### 1. Market Depth Extraction example: [scripts.script_market_depth_example.py]  

#### Input informations: 
```python
identifier = 'CLZ24'
identifier_type = IdentifierType.Ric

# %% dates (%Y, %M, %D, %h, %s, %ms):
query_start_date = datetime(2022, 11, 21, 0, 0, 0)
query_end_date = datetime(2022, 11, 24, 0, 0, 0)
```

#### Required informations:
```python
bid_price = MarketDepthContentFieldNames.BidPrice
ask_price = MarketDepthContentFieldNames.AskPrice
num_of_buyer = MarketDepthContentFieldNames.NumberOfBuyers
num_of_seller = MarketDepthContentFieldNames.NumberOfSellers
bid_size = MarketDepthContentFieldNames.BidSize
ask_size = MarketDepthContentFieldNames.AskSize
exchange_time = MarketDepthContentFieldNames.ExchangeTime

# %% content filed names here:
content_field_names = [bid_price,
                       # bid_size,
                       # ask_price,
                       # ask_size,
                       # num_of_buyer,
                       # num_of_seller,
                       # exchange_time
                       ]
# %% data view conditions :
nums_of_levels = 10
view = TickHistoryMarketDepthViewOptions.NormalizedLL2
```

#### Output file path: 
```python
output_file_name = f'./output_docs/{identifier}_{view.value}_{nums_of_levels}_{query_start_date.isoformat()}.csv.gz'
```

output file name must end with .csv.gz  
e.g. [./output_dosc/2022-11-10.csv.gz]  
The parent dictionary will be created automatically.   

### 2. MultiThreads Extractions:
Send multi-extractions using multi threads, the maximum number of threads per request is 50  
[scripts.script_multi_threads_extraction.py]  

```python
# %% multi threads obj:
extractioners_imp = ExtractionImp(extractioners)
```
MultiThreads Extraction obj, extractioners is a list of extractioner  
Each extractioner is independent of others, so they can have different start/end query time, ids, or content fields  

```python
# %% send the requests and download files
s = time.time()
file_dirs = extractioners_imp.save_files(output_file_paths, token)
e = time.time()
```
output_file_paths is a list of paths, each path need to be ended with .csv.gz  
e.g. [./output_docs/2022-11/2022-11-20T00:00:00.csv.gz, ./output_docs/2022-11/2022-11-21T00:00:00.csv.gz]  
The parent dictionary will be created automatically.   


## Condtion
Preview mode:  = 
PreviewMode.NONE => return a .csv.gz file, 
PreviewMode.CONTENT => return part data for preview, in .csv formate

## Market depth data need to extracted daily by daily

## TODO:
1. scheduled extraction
Used to extract large data size. 

2. coroutine for on demand extraction
Used to increase the speed of on demand extraction
Save the location, job id, and extracted file id locally

[//]: # (tex ,listing, lstinoutlisting in the latex tikz blockdiagram, )

##  codes:
clm{0 - 9}, clh{0-9}, clu{0-9}, clz{0-9}, quarterly

```json
{
  "H": "Mar",
  "M": "Jun",
  "U": "Sep",
  "Z": "Dec"
}
```




2023 => EDH{28}

20100101 - 20230302
fgnvjkqx{0-9} monthly
es{*}{0-9} s&p futures
ed{*}{0-9} eurodollor; Chain ric: 0#ED+ (quarterly contracts for 40 maturities)
zqff{0-9} vendor code,
bzz
ff fed fund futures, ff++ options on futures; chain ric: 0#FF: (monthly contracts for 60 maturities)
```json
{
  "F": "Jan",
  "G": "Feb",
  "H": "Mar",
  "J": "Apr",
  "K": "May",
  "M": "Jun",
  "N": "Jul",
  "Q": "Aug",
  "U": "Sep",
  "V": "Oct",
  "X": "Nov",
  "Z": "Dec"
}
```



ty{*} 10-y t-bill









