import logging
from datetime import date
import sys
import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, '/home/haobin_cui/option_data_processor')
# sys.path.insert(0, '/Users/haobincui/Documents/option_data_processor')


from connection.apis.get_chunk_data import ChunkDataCreator
from connection.features.extraction.enums.content_field_names.tick_history.intraday_content_field_names import \
    IntradaySummariesContentFieldNames
from connection.features.extraction.enums.extraction_base_enums import IdentifierType
from connection.utils.condition.condition import TickHistorySummaryInterval
from src.multi_thread import ExtractionImp

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


def main(contract_id: str, output_path: str, query_start_date: date, query_end_date: date) -> None:
    identifier_type = IdentifierType.ChainRIC

    content_field_names = [
        IntradaySummariesContentFieldNames.Close.Ask,
        IntradaySummariesContentFieldNames.Close.Bid,
        # IntradaySummariesContentFieldNames.Close.MidPrice,
    ]
    num_of_chunks = 1
    extractions, output_files = ChunkDataCreator.tick_history(
        contract_id, identifier_type, content_field_names, TickHistorySummaryInterval.OneMinute,
        output_path, query_start_date, query_end_date, num_of_chunks
    )

    s = 0
    n = 0
    f = 0
    total = num_of_chunks
    f_list = []

    for idx in range(len(extractions)):
        print('Start downloading data')

        threaders = ExtractionImp(extractions[idx])
        try:
            threaders.save_files(output_files[idx])
            s += 1
            n += 1
            print(f'Success: [{s}] , No.: [{n}], Left: [{total - n}], ids: [{output_files[idx]}]')
        except Exception as e:
            f_list = f_list + output_files[idx]
            f += 1
            print(f'Fail: [{f}], No.: [{n}], Left: [{total - n}], Message: [{e}], ,ids: [{output_files[idx]}]')
            continue
    print('Finished All')


if __name__ == '__main__':
    # 2023 / 2 / 2
    # 2022 / 9 / 22
    query_start_date = date(2022, 9, 22)
    query_end_date = date(2022, 10, 22)
    # query_end_date = date(2020, 5, 1)
    identifier = '0#TY+'
    output_path = './output'
    main(identifier, output_path, query_start_date, query_end_date)
