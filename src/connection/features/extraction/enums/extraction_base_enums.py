from enum import Enum


class ExtractionBaseEnums(Enum):
    pass


class BooleanValue(ExtractionBaseEnums):
    All = 0
    No = 1
    Yes = 2


class CommodityStatus(ExtractionBaseEnums):
    Inactive = 0
    Active = 1


class EquityStatus(ExtractionBaseEnums):
    Inactive = 0
    Active = 1


class FundStatus(ExtractionBaseEnums):
    Inactive = 0
    Active = 1


class FuturesAndOptionsStatus(ExtractionBaseEnums):
    Inactive = 0
    Active = 1


class CorporateActionsCapitalChangeType(ExtractionBaseEnums):
    CapitalChangeAnnouncementDate = 0
    CapitalChangeDealDate = 1
    CapitalChangeExDate = 2
    EffectiveDate = 3
    RecordDate = 4


class CorporateActionsDividendsType(ExtractionBaseEnums):
    DividendAnnouncementDate = 0
    DividendExDate = 1
    DividendPayDate = 2
    DividendRecordDate = 3
    PeriodEndDate = 4


class CorporateActionEarningsType(ExtractionBaseEnums):
    EarningsAnnouncementDate = 0
    PeriodEndDate = 1


class CorporateActionsEquityOfferingsType(ExtractionBaseEnums):
    AllPendingDeals = 0
    FirstTradingDate = 1


class CorporateActionsMergersAcquisitionsType(ExtractionBaseEnums):
    DealAnnouncementDate = 0
    DealCancelDate = 1
    DealCloseDate = 2
    DealEffectiveDate = 3
    DealRevisedProposalDate = 4
    TenderOfferExpirationDate = 5


class CorporateActionsNominalValueType(ExtractionBaseEnums):
    NominalValueDate = 0


class CorporateActionsSharesType(ExtractionBaseEnums):
    SharesAmountDate = 0


class CorporateActionsStandardEventsEypes(ExtractionBaseEnums):
    CAP = 0
    DIV = 1
    EAR = 2
    MNA = 3
    NOM = 4
    PEO = 5
    SHO = 6
    VOT = 7
    NONE = 9


class CorporateActionStandardYearType(ExtractionBaseEnums):
    Current = 0
    Previous = 1


class CorporateActionsVotingRightsType(ExtractionBaseEnums):
    VotingRightsDate = 0


class CriteriaListType(ExtractionBaseEnums):
    Commodities = 0
    DTC = 1
    FixedIncomeNewIssuance = 2
    Loans = 3
    MifidSubclass = 4


class EstimateType(ExtractionBaseEnums):
    BPS = 0
    CPS = 1
    CPX = 2
    CSH = 3
    DPS = 4
    EBG = 5
    EBI = 6
    EBS = 7
    EBT = 8
    ENT = 9
    EPS = 10
    EPX = 11
    FFO = 12
    GPS = 13
    GRM = 14
    NAV = 15
    NDT = 16
    NET = 17
    OPR = 18
    PRE = 19
    PTG = 20
    REC = 21
    ROA = 22
    ROE = 23
    SAL = 24


class FidDisplayOptions(ExtractionBaseEnums):
    All = 0
    Matching = 1


class FidListOperators(ExtractionBaseEnums):
    AND = 0
    OR = 1


class FixedIncomeRatingSource(ExtractionBaseEnums):
    Fitch = 0
    Moodys = 1
    StandardAndPoors = 2
    NONE = 9


class FundAllocationTypes(ExtractionBaseEnums):
    Asset = 0
    Currency = 1
    DebtorDomicile = 2
    FullHoldings = 3
    FullHoldingsWithRatings = 4
    IndustrySector = 5
    InvestmentCountry = 6
    Maturity = 7
    TopTenHoldings = 8


class FundSubType(ExtractionBaseEnums):
    ClosedEndFund = 0
    ExchangeTradedFund = 1
    InsuranceFund = 2
    InvestmentFund = 3
    MutualFund = 4
    PensionFund = 5
    TassHedgeFund = 6


class FuturesAndOptionsType(ExtractionBaseEnums):
    Futures = 0
    Options = 1
    FuturesOnOptions = 2


class HistoricalFiscalYearType(ExtractionBaseEnums):
    FYNegative1 = 0
    FYNegative2 = 1
    FYNegative3 = 2
    FYNegative4 = 3
    FYNegative5 = 4
    NONE = 9


class HistoricalQuarterType(ExtractionBaseEnums):
    QNegative1 = 0
    QNegative2 = 1
    QNegative3 = 2
    QNegative4 = 3
    QNegative5 = 4
    QNegative6 = 5
    QNegative7 = 6
    QNegative8 = 7
    NONE = 9


class HistoricalSemiAnnualType(ExtractionBaseEnums):
    SNegative1 = 0
    SNegative2 = 1
    SNegative3 = 2
    SNegative4 = 3
    NONE = 9


class IdentifierType(ExtractionBaseEnums):
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


class InstrumentType(ExtractionBaseEnums):
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


class IssuerAssetClassType(ExtractionBaseEnums):
    AllSupportedAssets = 0
    Equities = 1
    GovernmentAndCorporateBonds = 2


class LookbackType(ExtractionBaseEnums):
    OneMonth = 0
    ThreeMonths = 1
    FourMonths = 2
    SixMonths = 3
    TwelveMonths = 4


class MultiValueOperator(ExtractionBaseEnums):
    NotIn = 0
    In = 1


class NewsItemsLanguageType(ExtractionBaseEnums):
    AllLanguages = 0
    English = 1
    Selected = 2


class NewsItemsSourceType(ExtractionBaseEnums):
    AllNews = 0
    ReutersNews = 1
    Selected = 2


class PremiumPricingRegionCycle(ExtractionBaseEnums):
    PremiumPricingAsia3PM = 0
    PremiumPricingAsia4PM = 1
    PremiumPricingAsia6PM = 2
    PremiumPricingAsia930PM = 3
    PremiumPricingAsia10PM = 4
    PremiumPricingEmea2PM = 5
    PremiumPricingEmea4PM = 6
    PremiumPricingEmea415PM = 7
    PremiumPricingEmea6PM = 8
    PremiumPricingEmea12PM = 9
    PremiumPricingUS3PM = 10
    PremiumPricingUS4PM = 11


class PutCall(ExtractionBaseEnums):
    Call = 0
    Put = 1


class RangeOperator(ExtractionBaseEnums):
    Between = 0
    Equal = 1
    GreaterThan = 2
    GreaterThanOrEqual = 3
    LessThan = 4
    LessThanOrEqual = 5
    NotEqual = 6


class RelativeFiscalYearType(ExtractionBaseEnums):
    FY1 = 1
    FY2 = 2
    FY3 = 3
    FY4 = 4
    FY5 = 5
    NONE = 0


class RelativeQuarterType(ExtractionBaseEnums):
    Q1 = 1
    Q2 = 2
    Q3 = 3
    Q4 = 4
    Q5 = 5
    Q6 = 6
    Q7 = 7
    Q8 = 8
    NONE = 0


class RelativeSemiAnnualType(ExtractionBaseEnums):
    S1 = 1
    S2 = 2
    S3 = 3
    S4 = 4
    NONE = 0


class ReportIsoEventType(ExtractionBaseEnums):
    ACTV = 0
    BIDS = 1
    BONU = 2
    BPUT = 3
    BRUP = 4
    CAPD = 5
    CAPG = 6
    CAPI = 7
    CHAN = 8
    CMET = 9
    CONV = 10
    DECR = 11
    DFLT = 12
    DLST = 13
    DRCA = 14
    DRIP = 15
    DVCA = 16
    DVOP = 17
    DVSE = 18
    EXOF = 19
    EXRI = 20
    EXTM = 21
    EXWA = 22
    INCR = 23
    INTR = 24
    LIQU = 25
    MCAL = 26
    MEET = 27
    MRGR = 28
    ODLT = 29
    OMET = 30
    OTHR = 31
    PARI = 32
    PCAL = 33
    PPMT = 34
    PRIO = 35
    REDM = 36
    REDO = 37
    RHDI = 38
    RHTS = 39
    SHPR = 40
    SOFF = 41
    SPLF = 42
    SPLR = 43
    SUSP = 44
    TEND = 45
    XMET = 46


class ShareAmountChoice(ExtractionBaseEnums):
    All = 1
    Default = 2
    Subset = 3
    NONE = 0


class ShareAmountType(ExtractionBaseEnums):
    Authorised = 1
    CloselyHeld = 2
    FreeFloat = 3
    Issued = 4
    Listed = 5
    Outstanding = 6
    Treasure = 7
    Unclassified = 0

class TriggerTimeoutDay(ExtractionBaseEnums):
    CurrentDay = 0
    FollowingDay = 1


class ValidityStatus(ExtractionBaseEnums):
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


class ReportTemplateTypes(ExtractionBaseEnums):
    BondRatings = 1
    BondSchedules = 2
    CommoditiesCorrectionsHistory = 3
    Composite = 4
    CorporateActions = 5
    DetailEstimateFootnotes = 6
    ElektronTimeseries = 7
    EndOfDayPricing = 8
    EstimatesActual = 9
    EstimatesADC = 10
    EstimatesCompanyFootnotes = 11
    EstimatesDetail = 12
    EstimatesSummary = 13
    FixedIncomeAnalytics = 14
    FundAllocation = 15
    HistoricalReference = 16
    IntradayPricing = 17
    LegalEntityAudit = 18
    LegalEntityDetail = 19
    LegalEntityHierachy = 20
    MNSFactorHistory = 21
    NewsItems = 22
    Owners = 23
    PremiumEndOfDayPricing = 24
    PremiumPricing = 25
    PriceHistory = 26
    Starmine = 27
    SymbolCrossReference = 28
    TechnicalIndicators = 29
    TermsAndConditions = 30
    TickHistoryIntradaySummaries = 31
    TickHistoryMarketDepth = 32
    TickHistoryRaw = 33
    TickHistoryTimeAndSales = 34
    TimeseriesPricing = 35
    TrancheFactorHistory = 36







