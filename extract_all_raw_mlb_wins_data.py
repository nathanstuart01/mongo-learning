import pandas
import requests
import datetime
import json

pecota_url = 'https://www.baseballprospectus.com/standings/'
fangraphs_url = 'https://www.fangraphs.com/depthcharts.aspx?position=Team'
predicted_wins_url = 'https://www.bovada.lv/services/sports/event/coupon/events/A/description/baseball/mlb-season-props?marketFilterId=rank&preMatchOnly=true&lang=en'
final_data_struc_for_db = {}

def get_html_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19'}
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        return req.content
    else:
        return 'Unable to make request at this time'

def bovada_json(bv_html):
    bv_json = json.loads(bv_html)
    bv_json = bv_json[0]['events']
    return bv_json

def create_data_frame_from_html(html):
    df = pandas.read_html(html)
    return df

def create_data_frame_from_json(json):
    df = pandas.DataFrame(json)
    return df

def extract_fangraphs_war_data(df):
    if len(df[7]) == 31:
        df = df[7]
        return df
    else:
        return df

def extract_bovada_wins_data(df):
    bv_teams = list(df['description'][0:30])
    bv_wins = [float(wins[0]['markets'][0]['outcomes'][0]['description'].strip('Over ')) for wins in df['displayGroups'][0:30]]
    bv_data = dict(zip(bv_teams, bv_wins))
    return bv_data

def transform_bovada_data(extracted_data):
    transformed_data = []
    for k, v in extracted_data.items():
        transformed_data.append({'team': k, 'bovada_wins':v})
    return transformed_data

def transform_fangraphs_data(df):
    transform_data = [{'team': k, 'fangraphs_wins': (162 * .294) + v} for k, v in zip(df['Team'], df['WAR'])]
    transform_data.pop()
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

def merge_all_data_frames(bovada_data, pecota_data, fangraphs_data):
    b_df = pandas.DataFrame(bovada_data)
    p_df = pandas.DataFrame(pecota_data)
    f_df = pandas.DataFrame(fangraphs_data)
    f_df = f_df.drop(30)
    dfs = [b_df, p_df, f_df]
    merged_df = pandas.concat(dfs, join='inner', axis=1)
    return merged_df

def calculate_avg_win_predictions(merged_data):
    for team_data in merged_data:
        team_data['avg_predicted_wins'] = (team_data['pecota_wins'] + team_data['fangraphs_wins']) / 2 
    return merged_data

def merge_all_data_sources(fangraphs_data, pecota_data, bovada_data):
    final_data = []
    for f_data in fangraphs_data:
        for p_data in pecota_data:
            for b_data in bovada_data:
                if f_data['team'] in p_data['team'] and f_data['team'] in b_data['team']:
                    final_data.append({'team': f_data['team'], 'fangraphs_wins': f_data['fangraphs_wins'], 'pecota_wins': p_data['pecota_wins'], 'bovada_wins': b_data['bovada_wins']})
    return final_data

def transform_final_data(merged_final_data):
    for data in merged_final_data:
        data['avg_predicted_wins'] = (data['pecota_wins'] + data['fangraphs_wins']) / 2
        data['predicted_vs_projected_win_diff'] = abs(data['avg_predicted_wins'] - data['bovada_wins'])
    return merged_final_data

def find_value_teams(final_data):
    value_teams = []
    for teams in final_data:
        if teams['predicted_vs_projected_win_diff'] >= 5:
            value_teams.append(teams)
    return value_teams
            
def update_final_data_structure_with_current_year(data_structure, final_data):
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

p_html = get_html_content(pecota_url)
p_df = create_data_frame_from_html(p_html)
e_pdf = extract_pecota_data(p_df)
t_pdf = transform_pecota_data(e_pdf)

f_html = get_html_content(fangraphs_url)
f_df = create_data_frame_from_html(f_html)
e_fdf = extract_fangraphs_war_data(f_df)
t_fdf = transform_fangraphs_data(e_fdf)

bv_html = get_html_content(predicted_wins_url)
bv_json = bovada_json(bv_html)
bv_df = create_data_frame_from_json(bv_json)
e_bvdf = extract_bovada_wins_data(bv_df)
t_bvdf = transform_bovada_data(e_bvdf)

#merge_pecandfandata = merge_pecota_and_fangraphs_data(t_pdf, t_fdf)
#add_year_to_final_data = update_final_data_structure_with_current_year(final_data_struc_for_db, merge_pecandfandata)
#merge_data = merge_all_data_frames(t_bvdf, t_pdf, t_fdf)
merged_data = merge_all_data_sources(t_fdf, t_pdf, t_bvdf)
t_fd = transform_final_data(merged_data)
value_teams = find_value_teams(t_fd)






