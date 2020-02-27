from data_tools.data_extractor import DataExtractor

class FangraphsDataModel(DataExtractor):

    def extract_fangraphs_data(self, df):
        if len(df[7]) == 31:
            df = df[7]
            return df
        else:
            return df

    def transform_fangraphs_data(self, df):
        transform_data = [{'team': k, 'fangraphs_wins': (162 * .294) + v} for k, v in zip(df['Team'], df['WAR'])]
        transform_data.pop()
        return transform_data
