import requests
import pandas

class DataExtractor:
    def __init__(self, url):
        self.url = url

    def get_html_content(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19'}
        req = requests.get(url, headers=headers)
        if req.status_code == 200:
            return req.content
        else:
            return 'Unable to make request at this time'
    
    def create_data_frame_from_html(self, html):
        df = pandas.read_html(html)
        return df
    
    def create_data_frame_from_json(self, json):
        df = pandas.DataFrame(json)
        return df

        