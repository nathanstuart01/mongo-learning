from data_models.pecota_data_model import PecotaDataModel
from data_models.fangraphs_data_model import FangraphsDataModel
from data_models.bovada_data_model import BovadaDataModel
from data_tools.data_transformer import DataTransformer

from data_sources.data_urls import data_urls

# get fangraphs data
fangraphs_worker = FangraphsDataModel(data_urls['fangraphs_data_url'])
fangraphs_html = fangraphs_worker.get_html_content(fangraphs_worker.url)
fangraphs_data_frame = fangraphs_worker.create_data_frame_from_html(fangraphs_html)
extract_fangraphs_data = fangraphs_worker.extract_fangraphs_data(fangraphs_data_frame)
transform_fangraphs_data = fangraphs_worker.transform_fangraphs_data(extract_fangraphs_data)

# get pecota data
pecota_worker = PecotaDataModel(data_urls['pecota_data_url'])
pecota_html = pecota_worker.get_html_content(pecota_worker.url)
pecota_data_frame = pecota_worker.create_data_frame_from_html(pecota_html)
extract_pecota_data = pecota_worker.extract_pecota_data(pecota_data_frame)
transform_pecota_data = pecota_worker.transform_pecota_data(extract_pecota_data)

# get bovada data
bovada_worker = BovadaDataModel(data_urls['bovada_data_url'])
bovada_html = bovada_worker.get_html_content(bovada_worker.url)
extract_bovada_json = bovada_worker.extract_bovada_json(bovada_html)
bovada_data_frame = bovada_worker.create_data_frame_from_json(extract_bovada_json)
extract_bovada_data = bovada_worker.extract_bovada_data(bovada_data_frame, 29)
transform_bovada_data = bovada_worker.transform_bovada_data(extract_bovada_data)

# analyze data for value teams 
data_transformer = DataTransformer(transform_fangraphs_data, transform_pecota_data, transform_bovada_data)
merge_data = data_transformer.merge_all_data_sources(data_transformer.fangraphs_data, data_transformer.pecota_data, data_transformer.bovada_data)
transform_data = data_transformer.transform_final_data(merge_data)
analyze_data = data_transformer.find_value_teams(transform_data)
print(analyze_data)

# prepare data to send to db
