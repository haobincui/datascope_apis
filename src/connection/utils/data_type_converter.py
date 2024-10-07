import re

import pandas as pd


class DataTypeConverter:
    """
    convert data from one type to other types
    """

    @staticmethod
    def from_text_to_dataframe(input_data: str) -> pd.DataFrame:
        text = re.split('[\r\t]', input_data)
        text_list = [text[i: -1] for i in range(0, len(text))]

        df = pd.DataFrame(data = text_list[1:-1], columns=text_list[0])
        return df

