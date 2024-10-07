from enum import Enum


class SearchBaseEnums(Enum):
    pass


class IdentifierType(SearchBaseEnums):
    ArgentineAfipCode = 0
    BIC = 1
    BridgeSymbol = 2
    ChainRIC = 3
    ChinaCode = 4
    Cik = 5
    Cin = 6
    CommonCode = 7
    CompanyRegistrationNumber = 8
    Cusip = 9
    Duns = 10
    FacilityId = 11
    FileCode = 12
    FundLipperId = 13
    FundServ = 14
    Isin = 15
    ISMA = 16
    Lei = 17
    LIN = 18
    LipperID = 19
    LocalCode = 20
    MIC = 21
    NONE = 22
    OCCCode = 23
    ORC = 24
    OrgId = 25
    Pid = 26
    PidQ = 27
    Pix = 28
    PpnCusip = 29
    PrimaryRegulatorId = 30
    RcpId = 31
    Ric = 32
    RICRoot = 33
    Sedol = 34
    SICC = 35
    Sicovam = 36
    Sym = 37
    TAG = 38
    TaxFileId = 39
    Ticker = 40
    UnderlyingRIC = 41
    UserDefined = 42
    Valoren = 43
    Werpapier = 44
    ZPage = 45


class InstrumentType(SearchBaseEnums):
    BankLoan = 0
    BankLoanQuote = 1
    BankLoansIdentifyingFeatures = 2
    BankQuote = 3
    Benchmark = 4
    Cash = 5
    CMOQuote = 6
    CMOTranche = 7
    Commodity = 8
    CounterParty = 9
    Derivative = 10
    DerivativeQuote = 11
    Entity = 12
    Equity = 13
    EquityParty = 14
    EquityQuote = 15
    Fund = 16
    FundClass = 17
    FundIndex = 18
    GovCorpBond = 19
    GovCorpChain = 20
    GovCorpParty = 21
    GovCorpQuote = 22
    GovCorpUnderlying = 23
    LipperBenchmark = 24
    MergersAndAcquisitions = 25
    MifidSubclass = 26
    # MifidSubclass = 27
    MoneyMarket = 28
    MoneyMarketQuote = 29
    MortAggregate = 30
    MortgagePool = 31
    MortgageTBAQuote = 32
    MortGeneric = 33
    MortPoolQuote = 34
    MortTBAs = 35
    MuniBond = 36
    MuniChain = 37
    MuniIssue = 38
    MuniParty = 39
    MuniQuote = 40
    MutualFund = 41
    MutualFundQuote = 42
    OtcDerivatives = 43
    PublicEquityOffering = 44
    RIGsCUrveChain = 45
    RIGsPointQuote = 46
    Unknown = 47


class AssetStatus(SearchBaseEnums):
    Active = 0
    All = 1
    Inactive = 2


class OtcsStatus(SearchBaseEnums):
    Active = 0
    All = 1
    Inactive = 2


class ValidityStatus(SearchBaseEnums):
    BadInstrumentType = 0
    ChainHasBadLinks = 1
    ChainNotPermitted = 2
    ChainNotReviewed = 3
    ChainOfChains = 4
    InstrumentNotPermitted = 5
    InstrumentNotReviewed = 6
    IsChainNotInstrument = 7
    IsInstrumentNotChain = 8
    NotAChain = 9
    NotAnInstrument = 10
    NotBeginningOfChain = 11
    NotFound = 12
    Valid = 13
