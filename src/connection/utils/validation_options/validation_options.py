from dataclasses import dataclass, field
from typing import Any

_AllowDuplicateInstruments = 'AllowDuplicateInstruments'
_AllowOpenAccessInstruments = 'AllowOpenAccessInstruments'
_AllowHistoricalInstruments = 'AllowHistoricalInstruments'
_AllowLimitedTermInstruments = 'AllowLimitedTermInstruments'
_AllowInactiveInstruments = 'AllowInactiveInstruments'
_AllowUnsupportedInstruments = 'AllowUnsupportedInstruments'
_ExcludeFinrAsPricingSourceForBonds = 'ExcludeFinrAsPricingSourceForBonds'
_UseExchangeCodeInsteadOfLipper = 'UseExchangeCodeInsteadOfLipper'
_UseUsQuoteInsteadOfCanadian = 'UseUsQuoteInsteadOfCanadian'
_UseConsolidatedQuoteSourceForUsa = 'UseConsolidatedQuoteSourceForUsa'
_UseConsolidatedQuoteSourceForCanada = 'UseConsolidatedQuoteSourceForCanada'
_UseDebtOverEquity = 'UseDebtOverEquity'
_UseOtcPqSource = 'UseOtcPqSource'
_AllowSubclassImport = 'AllowSubclassImport'


@dataclass()
class ValidationOptions:
    dict_form: Any = field(init=False)

