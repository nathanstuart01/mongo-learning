from data_tools.data_extractor import DataExtractor
from data_sources.data_urls import data_urls

class PecotaDataModel(DataExtractor):

    def extract_pecota_data(self, data_frame):
        team_pecota_data = []
        for data in data_frame:
            for d in data.values:
                team_pecota_data.append(list(d))
        return team_pecota_data

    def transform_pecota_data(self, pecota_data):
        all_team_pecota_data = []
        for data in pecota_data:
            keys = ['team', 'pecota_wins']
            values = []
            for d in data[:2]:
                values.append(d)
            team_info_dict = dict(zip(keys, values))
            all_team_pecota_data.append(team_info_dict)
        return all_team_pecota_data
