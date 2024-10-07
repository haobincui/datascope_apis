from dataclasses import dataclass, field
from typing import Any

from src.connection.utils.validation_options.validation_options import ValidationOptions, _AllowOpenAccessInstruments, \
    _AllowHistoricalInstruments, _AllowLimitedTermInstruments, _AllowInactiveInstruments, _AllowUnsupportedInstruments, \
    _ExcludeFinrAsPricingSourceForBonds, _UseExchangeCodeInsteadOfLipper, _UseUsQuoteInsteadOfCanadian, \
    _UseConsolidatedQuoteSourceForUsa, _UseExchangeCodeInsteadOfLipper, _UseConsolidatedQuoteSourceForCanada, \
    _UseDebtOverEquity, _UseOtcPqSource, _AllowSubclassImport, _AllowDuplicateInstruments


@dataclass()
class InstrumentListValidationOptions(ValidationOptions):
    # allow_duplicate_instruments: bool = False
    allow_open_access_instruments: bool = None
    allow_historical_instruments: bool = True
    # allow_limited_term_instruments: bool = True
    # allow_inactive_instruments: bool = True
    # allow_unsupported_instruments: bool = True
    # exclude_finr_as_pricing_source_for_bonds: bool = True
    # use_exchange_code_instead_of_lipper: bool = True
    # use_us_quote_instead_of_canadian: bool = True
    # use_consolidated_quote_source_for_usa: bool = True
    # use_consolidated_quote_source_for_canada: bool = True
    # use_debt_over_equity: bool = True
    # use_otc_pq_source: bool = True
    # allow_subclass_import: bool = True
    dict_form: Any = field(init=False)

    def __post_init__(self):
        self.dict_form = {
            # _AllowDuplicateInstruments: self.allow_duplicate_instruments,
            # _AllowOpenAccessInstruments: self.allow_open_access_instruments,
            _AllowHistoricalInstruments: self.allow_historical_instruments,
            # _AllowLimitedTermInstruments: self.allow_limited_term_instruments,
            # _AllowInactiveInstruments: self.allow_inactive_instruments,
            # _AllowUnsupportedInstruments: self.allow_unsupported_instruments,
            # _ExcludeFinrAsPricingSourceForBonds: self.exclude_finr_as_pricing_source_for_bonds,
            # _UseExchangeCodeInsteadOfLipper: self.use_exchange_code_instead_of_lipper,
            # _UseUsQuoteInsteadOfCanadian: self.use_us_quote_instead_of_canadian,
            # _UseConsolidatedQuoteSourceForUsa: self.use_consolidated_quote_source_for_usa,
            # _UseConsolidatedQuoteSourceForCanada: self.use_us_quote_instead_of_canadian,
            # _UseDebtOverEquity: self.use_debt_over_equity,
            # _UseOtcPqSource: self.use_otc_pq_source,
            # _AllowSubclassImport: self.allow_subclass_import,
        }


default_instrument_list_validation_options = InstrumentListValidationOptions()




