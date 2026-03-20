from enum import Enum


class SearchTypes(Enum):
    """Represents search types."""
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
    """Represents historical search types."""
    HistoricalBulkSearch = 'HistoricalBulkSearch'
    HistoricalChainResolution = 'HistoricalChainResolution'
    HistoricalCriteriaSearch = 'HistoricalCriteriaSearch'
    HistoricalSearch = 'HistoricalSearch'






