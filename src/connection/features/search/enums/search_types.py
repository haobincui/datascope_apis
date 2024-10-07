from enum import Enum


class SearchTypes(Enum):
    BenchmarkSearch = 'BenchmarkSearch'
    CmoAbsSearch = 'CmoAbsSearch'
    CommoditySearch = 'CommoditySearch'
    EntitySearch = 'EntitySearch'
    EquitySearch = 'EquitySearch'
    FundSearch = 'FundSearch'
    FuturesAndOptionsSearch = 'FuturesAndOptionsSearch'
    GovCorpSearch = 'GovCorpSearch'
    InstrumentSearch = 'InstrumentSearch'
    LoanSearch = 'LoadnSearch'
    MifidSubclassSearch = 'MifidSubclassSearch'
    MorgageSearch = 'MorgageSearch'
    OtcsSearch = 'OtcsSearch'
    ReferenceHistory = 'ReferenceHistroy'
    UsMunicipalSearch = 'UsMunicipalSearch'


class HistoricalSearchTypes(Enum):
    HistoricalBulkSearch = 'HistoricalBulkSearch'
    HistoricalChainResolution = 'HistoricalChainResolution'
    HistoricalCriteriaSearch = 'HistoricalCriteriaSearch'
    HistoricalSearch = 'HistoricalSearch'






