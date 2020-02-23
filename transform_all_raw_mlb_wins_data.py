from extract_all_raw_mlb_wins_data import get_html_content, create_data_frame, extract_historical_team_data
from math import isnan
import requests
from io import StringIO
from pandas import pd

def prepare_raw_data_for_transformation():
    html = get_html_content()
    df = create_data_frame(html)
    data = extract_historical_team_data(df)
    return data

# turn all values into floats, for later dealing with nan values
def convert_values_to_numbers(raw_data):
    all_number_data = []
    for d in raw_data:
        single_year_clean_data = {}
        year = int(d['Year'])
        # years before 1999 not relevant to now based on free agency, lack of advanced metrics, higher usage of steroids, who cares about them
        if year > 1999:
            for k, v in d.items():
                single_year_clean_data[k] = float(v)
            all_number_data.append(single_year_clean_data)
        else:
            break
    return all_number_data

# remove nan values
def remove_nan_values(sorta_raw_data):
    nan_free_data = []
    for year in sorta_raw_data:
        nan_free_year = {k: year[k] for k in year if not isnan(year[k])}
        nan_free_data.append(nan_free_year)
    return nan_free_data
# compare the following wins totals to baseball prospectus projected win totals
def get_win_percentage_above_replacement(data):
    """
    current replacement level winning percentage .294 or 47 wins / 162 total games
    .294 according to following source:
    https://www.baseball-reference.com/about/war_explained.shtml
    """
    replacement_level_wins = 47

def get_daily_war_data(url):
    r = requests.get(url)
    df = pd.read_csv(StringIO(r.text))
    return df

def save_daily_war_data_to_db(war_data):
    # each day get data and save it to db

def get_team_rosters():
    # get each teams 40 man roster 

x = prepare_raw_data_for_transformation()
y = convert_values_to_numbers(x)
z = remove_nan_values(y)
#a = get_average_wins_per_team_by_season(z)
a = get_win_percentage_above_replacement(z)
print('x')

# continue developing out things using this link:
# talks about how many wins a team has if only replacement level players, and how fangraphs fwar is useful for predicting teams win loses
#https://en.wikipedia.org/wiki/Wins_Above_Replacement#Cameron2009
# already created list using fangraphs WAR:
#https://www.fangraphs.com/depthcharts.aspx?position=Team
# compare this list to baseball reference war list which i will compile with above functions
# also compare to PECOTA projected wins
# do an average of all three, and compare to projected wins

# alert if 5 win difference
# data structure 
#baseball_data = [ 
#                   {'year': year, 
#                   data[{'team': team, 
#                       'pecota_wins': pecota_wins, 
#                       'fangraphs_wins': fangraphs_wins, 
#                       'avg_predicted_wins': avg_predicted_wins, 
#                       'projected_wins': projected_wins,
#                       'predicted_vs_projected_win_difference': predicted_vs_projected_win_difference, 
#                       }]
#                   }
#               ]

# maybe final stat is use baesball-reference projcted runs scored/allowed to calcualte each teams pythagorean win total?
"https://www.baseball-reference.com/teams/SEA/2019-projections.shtml"
# if not confident in this, could go back and see what their projections stood up to the actual results, to get a STD and a regression
# use this calculator to determine each teams PWL:
# http://baerwcb.tripod.com/pwl.html
# do a regression analysis
