import pandas
import requests
import datetime

pecota_url = 'https://www.baseballprospectus.com/standings/'
fangraphs_url = 'https://www.fangraphs.com/depthcharts.aspx?position=Team'
final_data_struc_for_db = {}

def get_html_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19'}
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        return req.content
    else:
        return 'Unable to make request at this time'

def create_data_frame(html):
    df = pandas.read_html(html)
    return df

def extract_fangraphs_war_data(df):
    if len(df[7]) == 31:
        df = df[7]
        return df
    else:
        return df

def transform_fangraphs_data(df):
    transform_data = [{'team': k, 'fangraphs_wins': (162 * .294) + v} for k, v in zip(df['Team'], df['WAR'])]
    return transform_data

def extract_pecota_data(data_frame):
    team_pecota_data = []
    for data in data_frame:
        for d in data.values:
            team_pecota_data.append(list(d))
    return team_pecota_data
    
def transform_pecota_data(pecota_data):
    all_team_pecota_data = []
    for data in pecota_data:
        keys = ['team', 'pecota_wins']
        values = []
        for d in data[:2]:
            values.append(d)
        team_info_dict = dict(zip(keys, values))
        all_team_pecota_data.append(team_info_dict)
    return all_team_pecota_data

def merge_pecota_and_fangraphs_data(pecota_data, fangraphs_data):
    for pecota_teams in pecota_data:
        for fangraph_teams in fangraphs_data:
                if fangraph_teams['team'] in pecota_teams['team']:
                    pecota_teams.update(fangraph_teams)
    return pecota_data

def calculate_avg_win_predictions(merged_data):
    for team_data in merged_data:
        team_data['avg_predicted_wins'] = (team_data['pecota_wins'] + team_data['fangraphs_wins']) / 2 
    return merged_data

def update_final_data_structure(data_structure, final_data):
    x = len(data_structure)
    current_year = datetime.datetime.now()
    current_year = current_year.year
    data_structure['year'] = current_year 
    data_structure['data'] = final_data
    y = len(data_structure)
    if y == x + 1:
        return True
    else:
        return False

p_html = get_html_content(pecota_url)
p_df = create_data_frame(p_html)
e_pdf = extract_pecota_data(p_df)
# t_pdf = transformed_pecota_data_frame
t_pdf = transform_pecota_data(e_pdf)

f_html = get_html_content(fangraphs_url)
f_df = create_data_frame(f_html)
e_fdf = extract_fangraphs_war_data(f_df)
# t_fdf = transformed_pecota_data_frame
t_fdf = transform_fangraphs_data(e_fdf)

merge_pecandfandata = merge_pecota_and_fangraphs_data(t_pdf, t_fdf)
avg_merge_data = calculate_avg_win_predictions(merge_pecandfandata)
import pdb;pdb.set_trace()
final_data = update_final_data_structure(final_data_struc_for_db, avg_merge_data)






