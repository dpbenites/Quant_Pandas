import pandas as pd

def load_gold_data(file_gold_production, file_gold_price):
    df_gold = pd.read_csv(file_gold_production)
    df_gold.rename(columns={'Gold Production (Clio-Infra & USGS)': 'Gold Production'}, inplace=True)
    df_price = pd.read_csv(file_gold_price)
    df_price['Date'] = pd.to_datetime(df_price['Date'])
    return df_gold, df_price

def filter_gold_production_data(df_gold, start_year, end_year):
    return df_gold[(df_gold['Year'] >= start_year) & (df_gold['Year'] <= end_year)]

def group_gold_production_by_country(df_filtered):
    return df_filtered.groupby('Entity')['Gold Production'].sum().reset_index()

def sort_and_rank_countries(df_grouped, n_top_producers):
    df_grouped.rename(columns={'Gold Production': 'Total Gold Production'}, inplace=True)
    df_ranked = df_grouped.sort_values(by='Total Gold Production', ascending=False).reset_index(drop=True)
    df_ranked = df_ranked.iloc[:n_top_producers + 1]
    return df_ranked

def calculate_rest_of_world_production(df_ranked):
    total_top_countries = df_ranked.loc[1:, 'Total Gold Production'].sum()
    rest_of_world_production = df_ranked.loc[0, 'Total Gold Production'] - total_top_countries
    rest_of_world_df = pd.DataFrame({'Entity': ['Rest of World'], 'Total Gold Production': [rest_of_world_production]})
    return rest_of_world_df

def ranking(df_gold, start_year, end_year, n_top_producers):
    df_filtered = filter_gold_production_data(df_gold, start_year, end_year)
    df_grouped = group_gold_production_by_country(df_filtered)
    df_ranked = sort_and_rank_countries(df_grouped, n_top_producers)
    rest_of_world_df = calculate_rest_of_world_production(df_ranked)
    df_ranked = pd.concat([df_ranked, rest_of_world_df], ignore_index=True)
    return df_ranked

def gold_hist(df_gold, start_year, end_year, n_top_producers):
    df_ranked = ranking(df_gold, start_year, end_year, n_top_producers)
    top_countries = df_ranked['Entity'].tolist()
    top_countries.pop(0)  # Remove 'Total' row
    top_countries.pop(-1)  # Remove 'Rest of World' row

    df_filtered = df_gold[df_gold['Entity'].isin(top_countries)]
    df_filtered = df_filtered[(df_gold['Year'] >= start_year) & (df_gold['Year'] <= end_year)]
    return df_filtered

def gold_price(df_price):
    return df_price

# Exemplo de uso das funções
# file_gold_production = 'path_to_gold_production.csv'
# file_gold_price = 'path_to_gold_price.csv'
# start_year = 2000
# end_year = 2020
# n_top_producers = 10

# df_gold, df_price = load_gold_data(file_gold_production, file_gold_price)
# ranking_df = ranking(df_gold, start_year, end_year, n_top_producers)
# gold_hist_df = gold_hist(df_gold, start_year, end_year, n_top_producers)
# gold_price_df = gold_price(df_price)
