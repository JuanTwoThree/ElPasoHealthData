from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import json

#from census import Census
#from us import states

#c = Census('417237a07b9eedf31a9aa0ba592bb8b839de64ae', year=2020)

def get_ep_zips_codes_data_map() -> pd.DataFrame:
    zip_code_site_url = 'https://www.zipdatamaps.com/en/us/zip-maps/tx/city/borders/el-paso-zip-code-map'

    content = get(url=zip_code_site_url).content
    soup = BeautifulSoup(content, 'html.parser')
    body = soup.body
    zip_data = body.find(id="zip-code-data")
    zip_table = zip_data.div.div.div.table

    zip_list = []

    for i, zip_code_object in enumerate(zip_table):
        if i % 2 == 1:
            a_tags = zip_code_object.find_all('a')
            zip_code = (a_tags[1].string).split(' ')[-1]
            city = (a_tags[2].string)
            zip_type = zip_code_object.find_all('td')[-1].string
            zip_dict = {'zip_code': zip_code, 'city': city, 'zip_type': zip_type}
            zip_list.append(zip_dict)

    return pd.DataFrame(zip_list)

def get_ep_zips_codes() -> pd.DataFrame:
    zip_code_site_url = 'https://www.zip-codes.com/county/tx-el-paso.asp'

    content = get(url=zip_code_site_url).content
    soup = BeautifulSoup(content, 'html.parser')
    body = soup.body
    table = body.find_all("table", class_="statTable")
    tr_list = table[0].find_all('tr')
    
    zip_list = []
    for i, tr_tag in enumerate(tr_list):
        if i > 0:
            zip_code = (tr_tag.find_all("td", class_="label")[0].string).split(' ')[-1]
            rest_td = tr_tag.find_all("td", class_="info")
            classification = rest_td[0].string
            city = rest_td[1].string
            population = int((rest_td[2].string).replace(',',''))
            zip_dict = {'zip_code': zip_code, 'city': city, 'classification': classification, 'population': population}
            zip_list.append(zip_dict)
    
    return pd.DataFrame(zip_list)

def save_ep_zip_codes():
    df = get_ep_zips_codes()
    df.to_csv('./ep_zip_codes.csv')


def get_census_population(zip_list:list) -> list:
    population_list = []
    for zip_code in zip_list:
        population_url = f'https://api.census.gov/data/2020/dec/dhc?get=group(P1)&ucgid=860Z200US{zip_code}'
        content = get(url=population_url).content
        content_list = json.loads(content)
        population = int(content_list[1][2])
        population_list.append({'zip_code': zip_code, 'population': population})
    return population_list

def get_census_hispanic_population(zip_list:list) -> list:
    population_list = []
    for zip_code in zip_list:
        population_url = f'https://api.census.gov/data/2020/dec/dhc?get=group(P9)&ucgid=860Z200US{zip_code}'
        content = get(url=population_url).content
        content_list = json.loads(content)
        total_population = int(content_list[1][2])
        hispanic_population = int(content_list[1][4])
        population_list.append({'zip_code': zip_code, 'population': total_population, 'hipanic_population':hispanic_population})

    return population_list

def save_hispanic_population(zip_list:list):
    hispanic_population_list = get_census_hispanic_population(zip_list=zip_list)
    df = pd.DataFrame(hispanic_population_list)
    df.to_csv('./hispanic_population.csv')


#print(save_ep_zip_codes())

zip_list = [79853,
79908,
79938,
79838,
79836,
79934,
79821,
79928,
79849,
79835,
79922,
79906,
79911,
79927,
79932,
79930,
79925,
79916,
79902,
79912,
79905,
79904,
79907,
79936,
79915,
79901,
79924,
79935,
79903,
79920]

save_hispanic_population(zip_list)