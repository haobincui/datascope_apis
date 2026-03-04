
import pandas as pd





"""
Exchange ric, Exchange Name,Exchange Code,
.DE,Xetra,GER
.xbo,MiFID - Reuters Consolidated (Frankfurt),XBO
"""



def extract_unique_exchanges(input_csv_or_df):
    """
    input:
    RIC,Company Common Name,Exchange Name,Exchange Code,ISIN
    ALVG.DE,Allianz SE,Xetra,GER,{'DE0008404005'}
    ALVGEUR.xbo,Allianz SE,MiFID - Reuters Consolidated (Frankfurt),XBO,{'DE0008404005'}

    ff_output:
    Exchange RIC,Exchange Name,Exchange Code
    DE,Xetra,GER
    xbo,MiFID - Reuters Consolidated (Frankfurt),XBO
    """
    if isinstance(input_csv_or_df, str):
        df = pd.read_csv(input_csv_or_df)
    else:
        df = input_csv_or_df.copy()

    # extract exchange RIC code
    df['Exchange RIC'] = df['RIC'].apply(lambda x: x.split('^')[0].split('.')[-1])

    # drop duplicates
    exchange_df = df[['Exchange RIC', 'Exchange Name', 'Exchange Code']].drop_duplicates().dropna()

    # rename coloumns
    exchange_df.columns = ['Exchange RIC', 'Exchange Name', 'Exchange Code']
    return exchange_df.reset_index(drop=True)


if __name__ == '__main__':
    input_csv = './input/Different_exchanges.csv'
    exchanges_df = extract_unique_exchanges(input_csv)
    exchanges_df.to_csv('input/unique_exchanges.csv', index=False)

