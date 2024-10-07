import gzip
import io
import logging
import shutil
from enum import Enum
from functools import singledispatch
from typing import NoReturn


class FileType(Enum):
    GZ = 1
    TXT = 2
    XLSX = 3
    CSV = 4
    OTHER = 9


class FileProcesser:

    @staticmethod
    def decompress(compressed_file: str, output_file: str = None, write: bool = True) -> NoReturn:
        """
        decompress .gz file
        :param write:
        :param compressed_file:
        :param output_file:
        :return:
        """
        if '.gz' not in compressed_file:
            raise ValueError(f'File [{compressed_file}] is not a .gz file')

        if not output_file:
            output_file = compressed_file.split('.gz')[0]

        decompressed_file = gzip.GzipFile(filename=compressed_file)

        if write:
            with open(output_file, 'wb') as outfile:
                outfile.write(decompressed_file.read())
            logging.info(f'Success get extraction result in [{output_file}]')
            return
        else:
            return io.BytesIO(decompressed_file.read())

    @staticmethod
    def compress(decompressed_file: str, output_file: str = None) -> None:
        if not output_file:
            output_file = decompressed_file + '.gz'

        with open(decompressed_file, 'rb') as f_in:
            with gzip.open(output_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        f_in.close()
        f_out.close()
        logging.info(f'Success compress file [{decompressed_file}] result in [{output_file}]')
        return

    @staticmethod
    @singledispatch
    def convert(output_file_type: FileType, input_file_path: str, output_file_path: str) -> NoReturn:

        raise NotImplemented
