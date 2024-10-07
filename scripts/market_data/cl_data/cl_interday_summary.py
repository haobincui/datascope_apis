import logging
import os
from datetime import date

from connection.features.extraction.enums.content_field_names.tick_history.intraday_content_field_names import \
    IntradaySummariesContentFieldNames
from connection.features.extraction.enums.extraction_base_enums import IdentifierType
from connection.features.extraction.on_demand_extractioner.tick_history_intraday_summaries_extractioner import \
    TickHistoryIntradaySummariesExtractioner
from connection.utils.condition.condition import TickHistorySummaryInterval
from connection.utils.condition.tick_history_intraday_summaries_condition import TickHistoryIntradaySummariesCondition
from connection.utils.instrument_identifier_list_base.instrument_identifier_list import InstrumentIdentifier, \
    InstrumentIdentifierList
from src.multi_thread import ExtractionImp
from src.calendar import plus_period, Period, TimeUnit, EomConvention

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


def main(contract_id: str, query_start_date: date, query_end_date: date) -> None:
    identifier_type = IdentifierType.ChainRIC

    content_field_names = [
        IntradaySummariesContentFieldNames.Close.Ask,
        IntradaySummariesContentFieldNames.Close.AskSize,
        IntradaySummariesContentFieldNames.Close.Bid,
        IntradaySummariesContentFieldNames.Close.BidSize
    ]

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

    chunks = total_len // 40 + 1
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
            condition = TickHistoryIntradaySummariesCondition(
                query_start_date=start_dates[idx],
                query_end_date=end_dates[idx],
                summary_interval=TickHistorySummaryInterval.FiveMinutes
            )

            extractioner = TickHistoryIntradaySummariesExtractioner(
                identifier_list=instrument_list,
                intraday_summaries_content_field_names=content_field_names,
                condition=condition
            )
            cur_id = '0#CL' + '-' + start_dates[idx].isoformat() + '-' + end_dates[idx].isoformat()
            cur_ids.append(cur_id)
            chunk_extraction.append(extractioner)
            output_path.append(f'./output/0#CL_trades/{cur_id}.csv.gz')
            try:
                os.mkdir(f'./output/0#CL_trades/{start_dates[idx].year}/')
            except:
                pass
        extractions.append(chunk_extraction)
        output_paths.append(output_path)

    s = 0
    n = 0
    f = 0
    total = chunks
    f_list = []

    # extractions = extractions[0]
    # output_paths = output_paths[0]
    for idx in range(len(extractions)):
        print('Start downloading data')

        threaders = ExtractionImp(extractions[idx])
        try:
            threaders.save_files(output_paths[idx])
            s += 1
            n += 1
            print(f'Success: [{s}] , No.: [{n}], Left: [{total - n}], ids: [{cur_ids}]')
        except Exception as e:
            f_list = f_list + cur_ids
            f += 1
            print(f'Fail: [{f}], No.: [{n}], Left: [{total - n}], Message: [{e}], ,ids: [{cur_ids}]')
            continue
    print('Finished All')


if __name__ == '__main__':
    query_start_date = date(2022, 12, 1)
    # query_start_date = date(2020, 4, 1)
    # 2020-04-01 - 2020-05-01
    query_end_date = date(2024, 1, 1)
    # query_end_date = date(2020, 5, 1)
    identifier = '0#CL:'
    output_path = './output'
    main(identifier, query_start_date, query_end_date)
