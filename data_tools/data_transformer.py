from datetime import datetime 
from typing import List, Dict, Union

class DataTransformer:
    def __init__(self, fangraphs_data={}, pecota_data={}, bovada_data={}):
        self.fangraphs_data = fangraphs_data
        self.pecota_data = pecota_data
        self.bovada_data = bovada_data


    def merge_all_data_sources(self, fangraphs_data, pecota_data, bovada_data) -> List:
        final_data = []
        for f_data in fangraphs_data:
            for p_data in pecota_data:
                for b_data in bovada_data:
                    if f_data['team'] in p_data['team'] and f_data['team'] in b_data['team']:
                        final_data.append({'team': f_data['team'], 'fangraphs_wins': f_data['fangraphs_wins'], 'pecota_wins': p_data['pecota_wins'], 'bovada_wins': b_data['bovada_wins']})
        return final_data

    def transform_final_data(self, merged_final_data) -> Dict:
        for data in merged_final_data:
            data['avg_predicted_wins'] = (data['pecota_wins'] + data['fangraphs_wins']) / 2
            data['predicted_vs_projected_win_diff'] = abs(data['avg_predicted_wins'] - data['bovada_wins'])
        return merged_final_data

    def find_value_teams(self, final_data) -> Dict:
        all_teams_info = {}
        value_teams = []
        non_value_teams = []
        for teams in final_data:
            if teams['predicted_vs_projected_win_diff'] >= 5:
                value_teams.append(teams)
            else:
                non_value_teams.append(teams)
        all_teams_info['value_teams'] = value_teams
        all_teams_info['non_value_teams'] = non_value_teams
        return all_teams_info
            
    def update_final_data_structure_with_current_year(self, data_structure: Dict, final_data: Union[List[Dict[str, float]]]) -> bool:
        x = len(data_structure)
        current_year = datetime.datetime.now()
        current_year = current_year.year
        data_structure['year'] = current_year 
        data_structure['data'] = final_data
        y = len(data_structure)
        if y > x:
            return True
        else:
            return False
