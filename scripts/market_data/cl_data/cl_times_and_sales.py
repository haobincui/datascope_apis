import logging
import os
from datetime import date

from connection.features.extraction.enums.content_field_names.tick_history.time_and_sales_content_field_names import \
    TimeAndSalesContentFieldNames
from connection.features.extraction.enums.extraction_base_enums import IdentifierType
from connection.features.extraction.on_demand_extractioner.tick_history_time_and_sales_extractioner import \
    TickHistoryTimeAndSalesRawExtractioner
from connection.utils.condition.tick_history_time_and_sales_condtion import TickHistoryTimeAndSalesCondition
from connection.utils.instrument_identifier_list_base.instrument_identifier_list import InstrumentIdentifier, \
    InstrumentIdentifierList
from src.multi_thread import ExtractionImp
from src.calendar import plus_period, Period, TimeUnit, EomConvention

# %% setup a logger:
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


def main(contract_id: str, output_path: str) -> None:
    identifier_type = IdentifierType.ChainRIC
    quote_bid_price = TimeAndSalesContentFieldNames.Quote.BidPrice
    quote_bid_size = TimeAndSalesContentFieldNames.Quote.BidSize
    quote_ask_price = TimeAndSalesContentFieldNames.Quote.AskPrice
    quote_ask_size = TimeAndSalesContentFieldNames.Quote.AskSize

    content_field_names = [quote_ask_price, quote_ask_size,
                           quote_bid_size, quote_bid_price]

    query_start_date = date(2020, 1, 1)
    query_end_date = date(2021, 1, 1)

    query_start_dates = [query_start_date]
    # query_end_dates = [query_end_date]

    while query_start_dates[-1] < query_end_date:
        query_start_dates.append(
            plus_period(query_start_dates[-1], Period(1, TimeUnit.MONTH), eom=EomConvention.LAST_DAY))
    #
    if query_start_dates[-1] == query_end_date:
        query_start_dates.remove(query_end_date)
    query_end_dates = query_start_dates[1:] + [query_end_date]

    total_len = len(query_start_dates)
    extractions = []
    output_paths = []
    cur_ids = []

    chunks = 1
    for i in range(0, chunks):
        # start = i * 40
        # end = (i + 1) * 40
        # start_dates = query_start_dates[start: end]
        # end_dates = query_end_dates[start: end]
        chunk_extraction = []
        output_path = []
        start_dates = query_start_dates
        end_dates = query_end_dates

        for idx in range(len(start_dates)):

            identifier = InstrumentIdentifier(
                identifier=contract_id,
                identifier_type=identifier_type
            )

            instrument_list = InstrumentIdentifierList(
                identifier_list=[identifier],
                preferred_identifier_type=identifier_type
            )
            condition = TickHistoryTimeAndSalesCondition(
                query_start_date=start_dates[idx],
                query_end_date=end_dates[idx]
            )

            extractioner = TickHistoryTimeAndSalesRawExtractioner(
                identifier_list=instrument_list,
                times_and_sales_content_field_names=content_field_names,
                condition=condition
            )
            cur_id = contract_id + '-' + start_dates[idx].isoformat() + '-' + end_dates[idx].isoformat()
            cur_ids.append(cur_id)
            chunk_extraction.append(extractioner)
            output_path.append(f'{output_path}/{contract_id}_trades/{start_dates[idx].year}/{cur_id}.csv.gz')
            try:
                os.mkdir(f'{output_path}/{contract_id}_trades/{start_dates[idx].year}/')
            except:
                pass
        extractions.append(chunk_extraction)
        output_paths.append(output_path)

    s = 0
    n = 0
    f = 0
    total = chunks
    s_list = []
    f_list = []

    extractions = extractions[0]
    output_paths = output_paths[0]
    for idx in range(len(extractions)):
        print('Start downloading data')

        threaders = ExtractionImp([extractions[idx]])
        try:
            threaders.save_files([output_paths[idx]])
            s += 1
            n += 1
            slit = s_list + cur_ids
            print(f'Success: [{s}] , No.: [{n}], Left: [{total - n}], ids: [{cur_ids}]')
        except Exception as e:
            f_list = f_list + cur_ids
            f += 1
            print(f'Fail: [{f}], No.: [{n}], Left: [{total - n}], Message: [{e}], ,ids: [{cur_ids}]')
            continue
    print('Finished All')


if __name__ == '__main__':
    output_path = './output'

    contract_id = '0#CL+'
    main(contract_id, output_path)
