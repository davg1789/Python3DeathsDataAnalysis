import pandas as pd
import matplotlib.pyplot as plt
import os

save_dir = "images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

def CleanOrganizeData(csv_path, columns_to_drop=None):
 
    data = pd.read_csv(csv_path)
    
    if columns_to_drop is not None:
        data.drop(columns_to_drop, axis='columns', inplace=True)
        
    data = data[data['Jurisdiction of Occurrence'] != 'United States']            
    data_grouped  = data.groupby(['Jurisdiction of Occurrence', 'MMWR Year']).sum().reset_index()

    jurisdiction_uniques  = data_grouped ['Jurisdiction of Occurrence'].unique()  
    return (jurisdiction_uniques, data_grouped)

def SaveGraph(data_grouped, jurisdiction_uniques, save_dir="images"):

    for jurisdiction in jurisdiction_uniques:
        
        df_filtered = data_grouped[data_grouped['Jurisdiction of Occurrence'] == jurisdiction]
        df_filtered = df_filtered.sort_values('MMWR Year')

        plt.figure(figsize=(14, 8))

        for column in df_filtered.columns[2:]:
            plt.plot(df_filtered['MMWR Year'], df_filtered[column], label=column)

        plt.title(f'Deaths by year - {jurisdiction}')
        plt.xlabel('MMWR Year')
        plt.ylabel('Deaths number')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
        plt.tight_layout()

        filepath = f"{save_dir}/{jurisdiction.replace('/', '')}.png"
        plt.savefig(filepath, bbox_inches='tight')
        plt.clf()


columns_to_remove = ['Data As Of', 'MMWR Week', 'Week Ending Date', 'All Cause', 
                     'Natural Cause', 'flag_allcause', 'flag_natcause', 'flag_sept', 
                     'flag_neopl', 'flag_diab', 'flag_alz', 'flag_inflpn', 'flag_clrd', 
                     'flag_otherresp', 'flag_nephr', 'flag_otherunk', 'flag_hd', 
                     'flag_stroke', 'flag_cov19mcod', 'flag_cov19ucod']

jurisdiction_uniques, data_grouped = CleanOrganizeData("Weekly_Provisional_Counts_of_Deaths_by_State_and_Select_Causes__2020-2023_20240314.csv", columns_to_remove)

SaveGraph(data_grouped, jurisdiction_uniques, save_dir)