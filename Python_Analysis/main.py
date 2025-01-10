import pandas as pd
import os
import numpy as np
import math

# TODOS OS DADOS FORAM FORNECIDOS PELO ATLAS BRASILEIRO DE ENERGIA SOLAR DE MANEIRA GRATUITA
# ATLAS DISPONIVEL EM: https://www.gov.br/pt-br/servicos/obter-dados-do-atlas-brasileiro-de-energia-solar-atlas-solar
# PROJETO SEM FINS LUCRATIVOS
# AUTORIA: ACHILLES MACARINI NETO
# ESTUDANTE DE ENGENHARIA ELÉTRICA - UTFPR (CURITIBA)

script_dir = os.path.dirname(__file__)
diffuse_file_path = os.path.join(script_dir, '..', 'DIFFUSE_(csv)', 'diffuse_means.csv')
direct_normal_file_path = os.path.join(script_dir, '..', 'direct_normal_(csv)', 'direct_normal_means.csv')
global_horizontal_file_path = os.path.join(script_dir, '..', 'global_horizontal_(csv)', 'global_horizontal_means.csv')
tilted_latitude_file_path = os.path.join(script_dir, '..', 'tilted_latitude_(csv)', 'tilted_latitude_means.csv')

diffuse_data_set = pd.read_csv(diffuse_file_path, sep=";")
direct_normal_data_set = pd.read_csv(direct_normal_file_path, sep=";")
global_horizontal_data_set = pd.read_csv(global_horizontal_file_path, sep=";")
tilted_latitude_data_set = pd.read_csv(tilted_latitude_file_path, sep=";")

my_lat = -25.411611
my_lon = -49.185766

if 'LAT' not in diffuse_data_set.columns or 'LON' not in diffuse_data_set.columns:
        raise ValueError(f"Colunas 'LAT' ou 'LON' não encontradas no arquivo CSV.")


def euclidean_distance(row):
        return math.sqrt((row['LAT'] - my_lat)**2 + (row['LON'] - my_lon)**2)

diffuse_data_set['DISTANCE'] = diffuse_data_set.apply(euclidean_distance, axis=1)

closest_row = diffuse_data_set['ID'].loc[diffuse_data_set['DISTANCE'].idxmin()]

diffuse_data_set.drop(columns=['DISTANCE'], inplace=True)


print(closest_row)

data_from_location_rows = []
diffuse_line = diffuse_data_set[diffuse_data_set['ID'] == closest_row].iloc[0]
diffuse_line['KIND'] = 'DIFFUSE'
direct_normal_line = direct_normal_data_set[direct_normal_data_set['ID'] == closest_row].iloc[0]
direct_normal_line['KIND'] = 'DIRECT_NORMAL'
global_horizontal_line = global_horizontal_data_set[global_horizontal_data_set['ID'] == closest_row].iloc[0]
global_horizontal_line['KIND'] = 'GLOBAL_HORIZONTAL'
tilted_latitude_line = tilted_latitude_data_set[tilted_latitude_data_set['ID'] == closest_row].iloc[0]
tilted_latitude_line['KIND'] = 'TILTED_LATITUDE'
data_from_location_rows.append(diffuse_line)
data_from_location_rows.append(direct_normal_line)
data_from_location_rows.append(global_horizontal_line)
data_from_location_rows.append(tilted_latitude_line)

data_from_location = pd.DataFrame(data_from_location_rows)

print(data_from_location)
