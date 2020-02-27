from data_tools.data_extractor import DataExtractor
import json

class BovadaDataModel(DataExtractor):

    def extract_bovada_json(self, bv_html):
        bv_json = json.loads(bv_html)
        bv_json = bv_json[0]['events']
        return bv_json

    def extract_bovada_data(self, df):
        bv_teams = list(df['description'][0:30])
        bv_wins = [float(wins[0]['markets'][0]['outcomes'][0]['description'].strip('Over ')) for wins in df['displayGroups'][0:30]]
        bv_data = dict(zip(bv_teams, bv_wins))
        return bv_data

    def transform_bovada_data(self, extracted_data):
        transformed_data = []
        for k, v in extracted_data.items():
            transformed_data.append({'team': k, 'bovada_wins':v})
        return transformed_data
    
