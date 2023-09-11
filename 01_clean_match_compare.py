import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def clean_category():
    if row['category'] != 'ผงซักฟอก/น้ำยาซักผ้า' and row['category'] in row['item']:
        row['category_in_item'] = 'Y'
    elif row['category'] == 'ผงซักฟอก/น้ำยาซักผ้า' and 'ผงซักฟอก' in row['item']:
        row['category_in_item'] = 'Y'
    elif row['category'] == 'ผงซักฟอก/น้ำยาซักผ้า' and 'น้ำยาซักผ้า' in row['item']:
        row['category_in_item'] = 'Y'
    else:
        row['category_in_item'] = 'N'

def clean_item():
    row['item'] = row['item'].replace('ml.', 'มล.')
    row['item'] = row['item'].replace('แชมเปี้ยน', 'Champion')
    if 'บรรจุ' in row['unit'] and "(" not in row['item']:
        unit = "(" + row['unit'].replace("(บรรจุ ", "")
        row['item'] = row['item'] + ' ' + unit

def clean_unit():
    row['unit'] = row['unit'].replace('/', '')
    row['unit'] = row['unit'].replace('แพ็ค', 'แพค')
    row['unit'] = row['unit'].split(" ")[0]

def clean_price():
    row['price'] = row['price'].replace('.00', '')
    row['price'] = row['price'].replace('฿', '')
    row['price'] = row['price'].split("-")[0]
    
def get_brandname():
    row['brand_name'] = row['item'].split(row['category'])[0].strip()

def get_product_details():
    if row['category'] == 'ผงซักฟอก/น้ำยาซักผ้า' and 'ผงซักฟอก' in row['item']:
        unit = "(" + row['unit'].replace("(บรรจุ ", "")
        row['product_details'] = 'ผงซักฟอก' + ' ' + row['item'].split('ผงซักฟอก')[-1].strip()
    elif row['category'] == 'ผงซักฟอก/น้ำยาซักผ้า' and 'น้ำยาซักผ้า' in row['item']:
        row['product_details'] = 'น้ำยาซักผ้า' + ' ' + row['item'].split('น้ำยาซักผ้า')[-1].strip()
    else:
        row['product_details'] = row['category'] + ' ' + row['item'].split(row['category'])[-1].strip()

df_00_dohome = pd.read_csv('./raw_dohome_product_details.csv').drop('Unnamed: 0', axis=1)
df_00_global_house = pd.read_csv('./raw_global_house_product_details.csv').drop('Unnamed: 0', axis=1)
df_raw_dohome = df_00_dohome[df_00_dohome['category'].isin(['น้ำยาล้างจาน', 'น้ำยาล้างห้องน้ำ', 'ผงซักฟอก/น้ำยาซักผ้า', 'น้ำยาปรับผ้านุ่ม', 'ถุงขยะ'])]
df_raw_global_house = df_00_global_house[df_00_global_house['category'].isin(['น้ำยาล้างจาน', 'น้ำยาล้างห้องน้ำ', 'ผงซักฟอก/น้ำยาซักผ้า', 'น้ำยาปรับผ้านุ่ม', 'ถุงขยะ'])]

df_raw_dohome['category_in_item'] = None
df_raw_dohome['brand_name'] = None
df_raw_dohome['product_details'] = None
for i, row in df_raw_dohome.iterrows():
    clean_category()
    clean_item()
    clean_unit()
    clean_price()
    get_brandname()
    get_product_details()

df_raw_global_house['category_in_item'] = None
df_raw_global_house['brand_name'] = None
df_raw_global_house['product_details'] = None
for i, row in df_raw_global_house.iterrows():
    clean_category()
    clean_item()
    clean_unit()
    clean_price()
    get_brandname()
    get_product_details()

df_raw_dohome = df_raw_dohome[(df_raw_dohome['category_in_item'] != 'N') & (df_raw_dohome['item'] != '  ')]
df_raw_global_house = df_raw_global_house[(df_raw_global_house['category_in_item'] != 'N') & (df_raw_global_house['item'] != ' ')]

col_name = ['brand', 'product_details', 'check', 'price_global_house', 'price_dohome', 'cheapest_store' ]
data = []
for i, row_i in df_raw_global_house.iterrows():
    match_score = 0
    match_price = ''
    match_info = ''
    for j, row_j in df_raw_dohome.iterrows():
        if row_i['category'] == row_j['category']:
            brand_score = fuzz.token_sort_ratio(row_i['brand_name'], row_j['brand_name'])
            product_details_score = fuzz.token_sort_ratio(row_i['item'], row_j['item'])
            if product_details_score > match_score and brand_score > 45:
                match_score = product_details_score 
                match_price = row_j['price']
                match_info = row_j['item']
    data.append([row_i['brand_name'], row_i['item'], match_info, row_i['price'], match_price, None])
            
df_match = pd.DataFrame(data, columns=col_name)

for i, row in df_match.iterrows():
    if row['price_global_house'] <= row['price_dohome']:
        row['cheapest_store'] = 'GLOBAL HOUSE'
    else:
        row['cheapest_store'] = 'DOHOME'
df_match[(df_match['check'] != '') & (df_match['brand'] != '')].to_csv('./product_price_comparison.csv')
