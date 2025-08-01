import pandas as pd
from datetime import datetime
import pycountry

## Agriculture Sector
def crop_production(input_path, output_path):
    df = pd.read_csv(input_path)

    # Standardise columns
    df['date'] = pd.to_datetime(df['marketYear'].astype(str) + '-06-01')
    df['country'] = df['countryCode']
    df['sector'] = 'agriculture'
    df['indicator'] = df['attributeId']
    df['commodity'] = df['commodityName']
    df['unit'] = df['unitId']
    df['source'] = 'USDA PSD'

    # Reorder columns
    final_df = (df[['date', 'country', 'sector', 'indicator', 'commodity', 'value', 'unit', 'source']]
        .sort_values(by=['commodity', 'country', 'date']))

    # Save
    final_df.to_csv(output_path, index=False)
    print(f'Saved cleaned data to {output_path}')

## Defence Sector
def bid_info(input_path, output_path):
    df = pd.read_csv(input_path, encoding='utf-8-sig')

    # Standardise columns
    df['date'] = pd.to_datetime(df['orderPrearngeMt'].astype(str) + '01', format='%Y%m%d')
    df['country'] = 'South Korea'
    df['sector'] = 'defence'
    df['indicator'] = df['progrsSttus']
    df['category'] = df['excutTy']
    df['value'] = pd.to_numeric(df['budgetAmount'], errors='coerce')
    df['unit'] = 'KRW'
    df['agency'] = df['ornt']
    df['item'] = df['reprsntPrdlstNm']
    df['source'] = 'DAPA KOREA'

    # Reorder columns
    final_df = df[[
        'date', 'country', 'sector', 'indicator',
        'category', 'item','value', 'unit', 'agency', 'source'
    ]].sort_values(by=['date', 'agency', 'value'])

    # Save
    final_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f'Saved cleaned data to {output_path}')

## Economy Sector
def confidence(input_path, output_path):
    df = pd.read_csv(input_path)

    # Standardise columns
    df = df.rename(columns={
        'STAT_CODE': 'category',
        'ITEM_NAME1': 'indicator',
        'DATA_VALUE': 'value'
    })

    df['date'] = pd.to_datetime(df['TIME'].astype(str) + '01', format='%Y%m%d')
    df['country'] = 'South Korea'
    df['sector'] = 'economy'
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df['unit'] = 'index'
    df['source'] = 'ECOS'

    # Reorder columns
    final_df = (df[['date', 'country', 'sector', 'category', 'indicator', 'value', 'unit', 'source']]
                .sort_values(by=['date', 'category','indicator']))

    # Save
    final_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f'Saved cleaned data to {output_path}')

def fxrate(input_path, output_path):
    df = pd.read_csv(input_path)

    # Standardise columns
    df = df.rename(columns={
        'DATE': 'date',
        'EXCHANGE_RATE': 'exchange_rate',
        'UNIT_NAME': 'unit'
    })

    df[['quote', 'currency']] = df['CURRENCY'].apply(
        lambda x: pd.Series(x.split('/') if '/' in x else ['KRW', x])
    )

    df['date'] = pd.to_datetime(df['date'])
    df['country'] = 'South Korea'
    df['sector'] = 'economy'
    df['source'] = 'ECOS'

    # Reorder columns
    final_df = (df[[ 'date', 'country','sector', 'currency', 'quote', 'exchange_rate', 'unit', 'source']]
                .sort_values(by=['date', 'currency']))

    # Save
    final_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f'Saved cleaned data to {output_path}')

def economic_indicator(input_path, output_path):
    df = pd.read_csv(input_path)

    # Standardise columns
    df = df.rename(columns={'datetime' : 'date'})
    df['date'] = pd.to_datetime(df['date'])

    df['country'] = 'South Korea'
    df['sector'] = 'economy'
    df['source'] = 'ECOS'
    df['unit'] = 'index'

    df_long = df.melt(
        id_vars=['date', 'country', 'sector', 'source', 'unit'],
        var_name='indicator',
        value_name='value'
    )

    df_long['indicator'] = pd.Categorical(
        df_long['indicator'],
        categories=['KOSPI', '동행지수순환변동치', '선행지수순환변동치', '선행-동행'],
        ordered=True
    )

    final_df = (df_long[['date', 'country', 'sector', 'indicator', 'value', 'unit', 'source']].sort_values(by=['date', 'indicator']))

    final_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f'Saved cleaned data to {output_path}')

## Energy Sector
def iea_oil_stocks(input_path, output_path):
    df = pd.read_csv(input_path)

    # Standardise columns
    df['date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'] + '-01')

    df = df.rename(columns={'countryName': 'country'})
    df = df[df['total'] != 'Net Exporter']

    df['value'] = pd.to_numeric(df['total'], errors='coerce')
    df['sector'] = 'energy'
    df['source'] = 'IEA'
    df['unit'] = 'kb/d'

    final_df = df[['date', 'country', 'sector', 'source', 'value', 'unit']].sort_values(by=['date', 'country', 'value'])

    final_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f'Saved cleaned data to {output_path}')

def oil_import_summary(input_path, output_path):
    df = pd.read_csv(input_path)

    # Date
    df = df[df['Month'] != 'Total']
    df['date'] = pd.to_datetime(df['Month'].astype(str) + '-01')

    df_long = df.melt(
        id_vars=['date'],
        var_name='country_unit',
        value_name='value'
    )

    df_long[['country', 'unit']] = df_long['country_unit'].str.extract(r'^(.*?)\s*\((.*?)\)$')

    # Region mapping
    region_map = {
        'Asia': ['필리핀', '말레이시아', '인도네시아', '호주', '뉴질랜드', '파푸아뉴기니', '카자흐스탄'],
        'Africa': ['알제리', '콩고', '나이지리아', '적도기니', '모잠비크', '가봉'],
        'America': ['캐나다', '미국', '멕시코', '브라질', '에콰도르'],
        'MiddleEast': ['이라크', '쿠웨이트', '카타르', '아랍에미레이트', '사우디아라비아', '오만', '중립지대'],
        'Europe': ['노르웨이', '영국'],
        'Total': ['합 계']
    }
    country_to_region = {country: region for region, countries in region_map.items() for country in countries}
    df_long['region'] = df_long['country'].map(country_to_region).fillna(df_long['country'])

    # English
    country_name_map = {'필리핀': 'Philippines','말레이시아': 'Malaysia','인도네시아': 'Indonesia',
        '호주': 'Australia','뉴질랜드': 'New Zealand','파푸아뉴기니': 'Papua New Guinea',
        '카자흐스탄': 'Kazakhstan','알제리': 'Algeria','콩고': 'Congo','나이지리아': 'Nigeria','적도기니': 'Equatorial Guinea',
        '모잠비크': 'Mozambique','캐나다': 'Canada','미국': 'United States','멕시코': 'Mexico','브라질': 'Brazil',
        '에콰도르': 'Ecuador','이라크': 'Iraq','쿠웨이트': 'Kuwait','카타르': 'Qatar','아랍에미레이트': 'UAE',
        '사우디아라비아': 'Saudi Arabia','오만': 'Oman','중립지대': 'Neutral Zone',
        '노르웨이': 'Norway','영국': 'United Kingdom', '가봉': 'Gabon', '합 계': 'Total'
    }
    df_long['country'] = df_long['country'].map(country_name_map).fillna(df_long['country'])

    # Convert % strings to float
    mask_percent = df_long['unit'] == '%'
    df_long.loc[mask_percent, 'value'] = (df_long.loc[mask_percent, 'value']
                                          .astype(str).str.replace('%', '', regex=False)
                                          .astype(float))

    df_long['sector'] = 'energy'
    df_long['source'] = 'PETRONET'

    df_long['unit'] = pd.Categorical(
        df_long['unit'],
        categories=['%', 'Value', 'Vol', 'Price'],
        ordered=True
    )
    unit_map = {
        'Value': 'thousand USD',
        'Price': 'USD/bbl',
        'Vol': 'thousand bbl',
        '%': 'percentage'
    }
    df_long['unit'] = df_long['unit'].map(unit_map)

    df_long = df_long[['date', 'region', 'country', 'value', 'unit', 'sector', 'source']].sort_values(by=['date', 'country', 'unit'])

    # Drop rows where both 'region' and 'country' columns are missing or empty
    if 'region' in df_long.columns and 'country' in df_long.columns:
        df_long = df_long[~(df_long['region'].fillna('').eq('') & df_long['country'].fillna('').eq(''))]

    df_long.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f'Saved cleaned data to: {output_path}')

# Industry Sector
def manufacture_inventory(input_path, output_path):
    df = pd.read_csv(input_path)

    # Standardise columns
    df = df.rename(columns={
        'STAT_NAME': 'category',
        'DATA_VALUE': 'value'
    })
    rename_map = {
        '8.1.3. 설비투자지수': '설비투자지수',
        '8.3.5. 제조업 재고율': '제조업 재고율'
    }
    df['category'] = df['category'].map(rename_map)


    df['date'] = pd.to_datetime(df['TIME'].astype(str) + '01', format='%Y%m%d')
    df['country'] = 'South Korea'
    df['sector'] = 'industry'
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df['unit'] = 'index (2020=100)'
    df['source'] = 'ECOS'

    # Reorder columns
    final_df = (df[['date', 'country', 'sector', 'category', 'value', 'source']]
                .sort_values(by=['date', 'category']))

    # Save
    final_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f'Saved cleaned data to {output_path}')

def steel_combined(input_path, output_path):
    df = pd.read_csv(input_path)

    # Drop and Standardise
    df.drop(columns=['Scope'], inplace=True)
    df['sector'] = 'industry'
    df['source'] = 'World Steel Association'
    df['unit'] = 'percentage'
    df['region'] = df['Region']

    # Rename Turkey
    df['region'] = df['region'].replace('Türkiye', 'Turkey')

    # Melt the DataFrame first
    yoy_cols = [col for col in df.columns if 'YoY' in col]

    df_long = df.melt(
        id_vars=['region', 'sector', 'unit', 'source'],
        value_vars=yoy_cols,
        var_name='indicator',
        value_name='value'
    )

    # Now extract date from melted 'indicator' column
    month_strs = df_long['indicator'].str.split().str[0]
    year_strs = df_long['indicator'].str.split().str[1]
    month_nums = month_strs.str[:3].apply(lambda x: datetime.strptime(x, '%b').month)

    df_long['date'] = pd.to_datetime(year_strs + '-' + month_nums.astype(str).str.zfill(2) + '-01', errors='coerce')

    # Final cleanup and save
    final_df = df_long[['date', 'region', 'sector', 'indicator', 'value', 'unit', 'source']]
    final_df = final_df.sort_values(by=['date', 'region'])

    final_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f'Saved cleaned data to: {output_path}')


# Trade Sector
# KOTRA Global Trade Variation Top 5
def global_trade_variation_top5(input_path, output_path):
    df = pd.read_csv(input_path)

    # Date
    df['date'] = pd.to_datetime(df['baseYr'].astype(str) + '-01-01')

    # Drop
    df.drop(columns=['expItcNatCd', 'impItcNatCd', 'expCountryNm', 'impCountryNm', 'hscd', 'cmdltDisplayNm', 'rank'], inplace=True)

    # Convert ISO codes to country names
    ISO2_TO_COUNTRY = {c.alpha_2: c.name for c in pycountry.countries} # type: ignore
    df['country'] = df['expIsoWd2NatCd'].map(ISO2_TO_COUNTRY).fillna(df['expIsoWd2NatCd'])
    df['partner'] = df['impIsoWd2NatCd'].map(ISO2_TO_COUNTRY).fillna(df['impIsoWd2NatCd'])

    # Rename indicators
    indicator_rename = {
        'expAmt': 'export_amount',
        'expVaritnRate': 'export_yoy',
        'expMkshRate': 'export_share',
        'impMkshRate': 'import_share'
    }
    df = df.rename(columns=indicator_rename)

    # Melt indicators
    melt_cols = list(indicator_rename.values())

    df_long = df.melt(
        id_vars=['date', 'country', 'partner'],
        value_vars=melt_cols,
        var_name='indicator',
        value_name='value'
    )

    # Assign units based on indicator
    unit_map = {
        'export_amount': 'thousand USD',
        'export_yoy': '%',
        'export_share': '%',
        'import_share': '%'
    }
    df_long['unit'] = df_long['indicator'].map(unit_map)

    # Add static columns
    df_long['sector'] = 'trade'
    df_long['source'] = 'KOTRA'

    # Sort and save
    df_long = df_long.sort_values(by=['date', 'country', 'partner', 'indicator'])
    df_long.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Saved cleaned file to: {output_path}")

# Global Trade
def global_trade_trend(input_path, output_path):
    df = pd.read_csv(input_path)

    # Date
    df['date'] = pd.to_datetime(df['baseYr'].astype(str) + '-01-01')

    # Drop unused columns
    df.drop(columns=['expItcNatCd', 'impItcNatCd', 'expCountryNm', 'impCountryNm', 'hscd', 'cmdltDisplayNm'], inplace=True)

    # Ensure 'rank' is clean and sortable
    df['rank'] = pd.to_numeric(df['rank'], errors='coerce')
    df = df.dropna(subset=['rank'])
    df['rank'] = df['rank'].astype(int)

    # Convert ISO codes to country names
    ISO2_TO_COUNTRY = {c.alpha_2: c.name for c in pycountry.countries}  # type: ignore
    df['country'] = df['expIsoWd2NatCd'].map(ISO2_TO_COUNTRY).fillna(df['expIsoWd2NatCd'])
    df['partner'] = df['impIsoWd2NatCd'].map(ISO2_TO_COUNTRY).fillna(df['impIsoWd2NatCd'])

    # Rename indicators
    indicator_rename = {
        'expAmt': 'export_amount',
        'expVaritnRate': 'export_yoy',
        'expMkshRate': 'export_share',
        'impMkshRate': 'import_share'
    }
    df = df.rename(columns=indicator_rename)

    # Melt indicators
    melt_cols = list(indicator_rename.values())
    df_long = df.melt(
        id_vars=['date', 'country', 'partner', 'rank'],
        value_vars=melt_cols,
        var_name='indicator',
        value_name='value'
    )

    # Assign units
    unit_map = {
        'export_amount': 'thousand USD',
        'export_yoy': '%',
        'export_share': '%',
        'import_share': '%'
    }
    df_long['unit'] = df_long['indicator'].map(unit_map)

    # Add metadata
    df_long['sector'] = 'trade'
    df_long['source'] = 'KOTRA'

    # Sort and save
    df_long = df_long.sort_values(by=['date', 'rank', 'country', 'partner', 'indicator'])
    df_long.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Saved cleaned file to: {output_path}")

# Global Export Increase and Decrease Items Top 5
def global_export(input_path, output_path, direction):
    df = pd.read_csv(input_path)
    
    # Date
    df['date'] = pd.to_datetime(df['baseYr'].astype(str) + '-01-01')

    # Drop
    df.drop(columns=['expItcNatCd', 'impItcNatCd', 'expMkshRate','impMkshRate','rank'], inplace=True)

    # Add static info
    df['sector'] = 'trade'
    df['source'] = 'KOTRA'
    df['country'] = 'World'

     # Rename columns
    df = df.rename(columns={
        'expAmt': 'export_amount',
        'expVaritnRate': 'export_yoy',
        'cmdltNm': 'commodity_name',
        'cmdltParentNm': 'parent',
        'cmdltGrParentNm': 'group',
        'cmdltDisplayNm': 'full_label'
    })

    # Melt the export indicators (values only)
    df_long = df.melt(
        id_vars=['date', 'country', 'commodity_name', 'parent', 'group', 'full_label'],
        value_vars=['export_amount', 'export_yoy'],
        var_name='indicator',
        value_name='value'
    )

    # Assign units
    df_long['unit'] = df_long['indicator'].map({
        'export_amount': 'thousand USD',
        'export_yoy': '%'
    })
    
    df_long['change_type'] = direction

    # Sort and save
    df_long = df_long.sort_values(by=['date', 'country', 'indicator'])
    df_long.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Saved cleaned file to: {output_path}")

# Korea Trade Trend
def korea_trade_trend(input_path, output_path, direction):
    df = pd.read_csv(input_path)
    
    # Drop rows with only baseYm and no other data
    df = df.dropna(how='all', subset=[col for col in df.columns if col != 'baseYm'])
    
    # Date
    df['date'] = pd.to_datetime(df['baseYm'].astype(str) + '-01', format='%Y%m-%d')

    # Drop unused columns if they exist
    df = df.drop(columns=[col for col in ['hscd', 'countryNm', 'expEntpCnt'] if col in df.columns])

    # Rename
    rename_map = {
        'expAmt': 'export_amount',
        'impAmt': 'import_amount',
        'varitnRate': 'trade_yoy',
        'mkshRate': 'trade_share'
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
    
    # Convert ISO codes to country names
    ISO2_TO_COUNTRY = {c.alpha_2: c.name for c in pycountry.countries}  # type: ignore
    df['partner'] = df['isoWd2NatCd'].map(ISO2_TO_COUNTRY).fillna(df['isoWd2NatCd'])
    df['partner'] = df['partner'].replace('ALL', 'World')

    # Add static info
    df['country'] = 'South Korea'
    df['sector'] = 'trade'
    df['source'] = 'KOTRA'
    df['indicator'] = direction
    
    # Select columns dynamically based on existing data
    base_cols = ['date', 'country', 'partner', 'indicator']
    value_cols = [col for col in ['export_amount', 'import_amount', 'trade_yoy', 'trade_share'] if col in df.columns]
    static_cols = ['sector', 'source']
    final_cols = base_cols + value_cols + static_cols

    df = df[final_cols]

    # Save
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Saved cleaned file to: {output_path}")

# Korea Export and Import Items
def korea_export_import_items(input_path, output_path, direction):
    df = pd.read_csv(input_path)
    
    # Drop rows with only baseYm and no other data
    df = df.dropna(how='all', subset=[col for col in df.columns if col != 'baseYm'])
    
    # Date
    df['date'] = pd.to_datetime(df['baseYm'].astype(str) + '-01', format='%Y%m-%d')

    # Drop unused columns if they exist
    df = df.drop(columns=[col for col in ['isoWd2NatCd','mkshRate','expEntpCnt'] if col in df.columns])

    # Rename
    rename_map = {
        'cmdltNm': 'commodity_name',
        'expAmt': 'export_amount',
        'impAmt': 'import_amount',
        'varitnRate': 'trade_yoy'
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Add static info
    df['country'] = 'South Korea'
    df['partner'] = 'World'
    df['sector'] = 'trade'
    df['source'] = 'KOTRA'
    df['indicator'] = direction
    
    # Select columns dynamically based on existing data
    value_cols = [col for col in ['export_amount', 'import_amount'] if col in df.columns]
    final_cols = ['date', 'country', 'partner', 'indicator', 'commodity_name'] + value_cols + ['trade_yoy', 'sector', 'source']
    df = df[final_cols]

    # Save
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Saved cleaned file to: {output_path}")

# ECOS Trade Overview
def ecos_trade_detail(input_path, output_path):
    df = pd.read_csv(input_path)
    
    # Clean YoY column safely
    df['yoy'] = df['yoy'].str.replace('%', '', regex=False).astype(float)

    # Replace STAT_CODE values
    df['STAT_CODE'] = df['STAT_CODE'].replace({'901Y011': 'Total Exports','901Y012': 'Total Imports'})

    # Drop unused columns
    df.drop(columns=['STAT_NAME', 'ITEM_CODE1', 'TIME'], inplace=True)

    # Rename columns
    df = df.rename(columns={
        'datetime': 'date',
        'STAT_CODE': 'category',
        'ITEM_NAME1': 'indicator',
        'DATA_VALUE': 'value',
        'UNIT_NAME': 'unit',
        'yoy': 'yoy_change'
    })

    # Standardise unit
    df['unit'] = df['unit'].replace('천달러', 'thousand USD')

    # Extract partner from indicator:
    # If contains "(관세청)" → 'World'
    # If format is like "수출총액(독일)" → extract "독일"
    df['partner'] = df['indicator'].apply(
    lambda x: 'World' if '관세청' in x 
    else (x[x.rfind('(')+1:x.rfind(')')] if '(' in x and ')' in x and x.rfind('(') < x.rfind(')') 
    else 'World')
    )

    # Rename partner
    korean_to_english = {
    '독일': 'Germany',
    '러시아': 'Russia',
    '미국': 'United States',
    '인도네시아': 'Indonesia',
    '중국': 'China',
    '캐나다': 'Canada',
    '태국': 'Thailand',
    '필리핀': 'Philippines',
    '호주': 'Australia',
    '말레이지아': 'Malaysia',
    '싱가포르': 'Singapore',
    '아랍에미레이트': 'United Arab Emirates',
    '이탈리아': 'Italy',
    '인도': 'India',
    '프랑스': 'France'
    }

    # Apply to the `partner` column
    df['partner'] = df['partner'].replace(korean_to_english)

    # Add static metadata
    df['country'] = 'South Korea'
    df['sector'] = 'trade'
    df['source'] = 'ECOS'

    # Reorder and sort
    df = df[['date', 'country', 'partner', 'sector', 'category', 'indicator', 'value', 'unit', 'yoy_change', 'source']]
    df = df.sort_values(by=['date', 'category', 'indicator'])

    # Save
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Saved cleaned file to {output_path}")

def ecos_trade_items(input_path, output_path):
    df = pd.read_csv(input_path)
       
    # Clean YoY column safely
    df['yoy'] = df['yoy'].str.replace('%', '', regex=False).astype(float)

    # Replace STAT_CODE values
    df['STAT_CODE'] = df['STAT_CODE'].replace({'수출금액지수': 'Export Value Index','수입금액지수': 'Import Value Index'})

    # Drop unused columns
    df.drop(columns=['STAT_NAME', 'ITEM_CODE1', 'TIME'], inplace=True)

    # Rename columns
    df = df.rename(columns={
        'datetime': 'date',
        'STAT_CODE': 'category',
        'ITEM_NAME1': 'indicator',
        'DATA_VALUE': 'value',
        'UNIT_NAME': 'unit',
        'yoy': 'yoy_change'
    })

    # Standardise unit
    df['unit'] = 'index (2020=100)'

    # Add static metadata
    df['country'] = 'South Korea'
    df['sector'] = 'trade'
    df['source'] = 'ECOS'

    # Reorder and sort
    df = df[['date', 'country', 'sector', 'category', 'indicator', 'value', 'unit', 'yoy_change', 'source']]
    df = df.sort_values(by=['date', 'category', 'indicator'])

    # Save
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Saved cleaned file to {output_path}")

# Shipping indcies
def shipping_indices(input_path, output_path):
    df = pd.read_csv(input_path)

    # Date
    df['Date'] = pd.to_datetime(df['Date'], format='%Y.%m.%d', errors='coerce')
    df = df.rename(columns={'Date': 'date'})

    # Strip and rename columns
    df.columns = [col.strip().replace('_Value', '') for col in df.columns]
    
    # Melt
    df_long = df.melt(
        id_vars=['date'],
        var_name='indicator',
        value_name='value'
    )

    # Add metadata
    df_long['country'] = 'World'
    df_long['sector'] = 'trade'
    df_long['unit'] = 'index'
    df_long['source'] = 'KCLA'

    # Sort and reorder
    df_long = df_long[['date', 'country', 'sector', 'indicator', 'value', 'unit', 'source']]
    df_long = df_long.sort_values(by=['date', 'indicator'])

    # Save
    df_long.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Saved cleaned file to {output_path}")

# WSTS Billings Semiconductors
def wsts_billings(input_path, output_path):
    df = pd.read_excel(input_path, sheet_name='Monthly Data', header=3)

    # Define the columns
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    total_year = 'Total Year'

    # Create a clean dataframe with year and region info
    result_rows = []
    current_year = None
    
    for idx, row in df.iterrows():
        first_col = str(row.iloc[0]).strip()
        
        # Check if this row contains a year
        if first_col.isdigit() and len(first_col) == 4:
            current_year = int(first_col)
            continue
            
        # Check if this row contains region data
        regions = ['Americas', 'Europe', 'Japan', 'Asia Pacific', 'Worldwide']
        if first_col in regions and current_year is not None:
            region = first_col
            
            # Extract monthly values
            for month in months:
                value = row[month]
                if pd.notna(value) and value != '':
                    try:
                        # Convert value to numeric, handling potential formatting
                        if isinstance(value, str):
                            value = value.replace(',', '').replace('$', '')
                        value = float(value)
                        
                        result_rows.append({
                            'year': current_year,
                            'period': month,
                            'period_type': 'month',
                            'region': region,
                            'value': value
                        })
                    except (ValueError, TypeError):
                        # Skip invalid values
                        continue
            
            # Extract quarterly values
            for quarter in quarters:
                value = row[quarter]
                if pd.notna(value) and value != '':
                    try:
                        # Convert value to numeric, handling potential formatting
                        if isinstance(value, str):
                            value = value.replace(',', '').replace('$', '')
                        value = float(value)
                        
                        result_rows.append({
                            'year': current_year,
                            'period': quarter,
                            'period_type': 'quarter',
                            'region': region,
                            'value': value
                        })
                    except (ValueError, TypeError):
                        # Skip invalid values
                        continue
            
            # Extract total year value
            if total_year:
                value = row[total_year]
                if pd.notna(value) and value != '':
                    try:
                        # Convert value to numeric, handling potential formatting
                        if isinstance(value, str):
                            value = value.replace(',', '').replace('$', '')
                        value = float(value)
                        
                        result_rows.append({
                            'year': current_year,
                            'period': 'Total Year',
                            'period_type': 'annual',
                            'region': region,
                            'value': value
                        })
                    except (ValueError, TypeError):
                        # Skip invalid values
                        continue
    
    # Create DataFrame from results
    df_long = pd.DataFrame(result_rows)

    # Create proper date column for monthly data only
    df_long['date'] = None
    monthly_mask = df_long['period_type'] == 'month'
    df_long.loc[monthly_mask, 'date'] = pd.to_datetime(
        df_long.loc[monthly_mask, 'year'].astype(str) + '-' + 
        df_long.loc[monthly_mask, 'period'] + '-01',
        errors='coerce'
    )
    
    # For quarterly data, create approximate dates (middle of quarter)
    quarterly_mask = df_long['period_type'] == 'quarter'
    quarter_to_month = {'Q1': '02-15', 'Q2': '05-15', 'Q3': '08-15', 'Q4': '11-15'}
    for quarter, month_day in quarter_to_month.items():
        mask = quarterly_mask & (df_long['period'] == quarter)
        df_long.loc[mask, 'date'] = pd.to_datetime(
            df_long.loc[mask, 'year'].astype(str) + '-' + month_day,
            errors='coerce'
        )
    
    # For annual data, use middle of year
    annual_mask = df_long['period_type'] == 'annual'
    df_long.loc[annual_mask, 'date'] = pd.to_datetime(
        df_long.loc[annual_mask, 'year'].astype(str) + '-07-01',
        errors='coerce'
    )
    df_long['date'] = pd.to_datetime(df_long['date'], errors='coerce')
    df_long['date'] = df_long['date'].dt.strftime('%Y-%m-%d')

    # Clean up and rename columns
    df_long = df_long.rename(columns={'region': 'country'})
    
    # Standardise country names
    df_long['country'] = df_long['country'].replace({
        'Americas': 'Americas',
        'Europe': 'Europe', 
        'Japan': 'Japan',
        'Asia Pacific': 'Asia Pacific',
        'Worldwide': 'World'
    })
    
    # Add metadata columns
    df_long['sector'] = 'semiconductors'
    df_long['indicator'] = 'billings'
    df_long['unit'] = 'thousand USD'
    df_long['source'] = 'WSTS'
    
    # Drop rows with missing dates or values
    df_long = df_long.dropna(subset=['date', 'value'])
    
    # Sort and reorder columns
    df_long = df_long[['date', 'country', 'period',  'value', 'unit', 'period_type', 'sector', 'indicator','source']]
    df_long = df_long.sort_values(by=['date', 'country'])
    
    # Save to CSV
    df_long.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Saved cleaned file to {output_path}")
 