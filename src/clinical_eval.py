import pandas as pd
import pickle, os
import matplotlib.pyplot as plt
import seaborn as sns
from utils import *
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import normalize

plt.style.use('ggplot')
sns.set_theme()
plt.rcParams["figure.figsize"] = (12, 4)
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]

import warnings
warnings.filterwarnings('ignore')

def main():

    # Load clinical data
    df_clinical_dfs = pd.read_excel(r'../data/OS_DFS_TCGA_TCGATEST_PANCA.xlsx', engine='openpyxl', sheet_name='ALL BREAST TCGA-PANCA DFS')
    df_clinical_os = pd.read_excel(r'../data/OS_DFS_TCGA_TCGATEST_PANCA.xlsx', engine='openpyxl', sheet_name='ALL BREAST TCGA PANCA OS')

    # Load the multilabel dataset (contains genes, correlations)
    with open('../data/dataset_multilabel.pkl', 'rb') as file:
        df_multi = pickle.load(file)

    # Set negative correlations to zero
    labels = ['LumA', 'LumB', 'Basal', 'Her2', 'Normal']
    df_multi[labels] = discard_negative_correlations(df_multi[labels])

    merged_df = pd.merge(df_clinical_dfs, df_clinical_os, on=['Patient ID', 'Study ID'])

    # Add new columns linked to time (5 years in this case)
    merged_df['DISEASE FREE FOR MORE THAN 5 YEARS'] = (merged_df['DFS_STATUS'] == 'DiseaseFree') & (merged_df['DFS_MONTHS'] > 5*12)
    merged_df['DISEASE FREE FOR LESS THAN 5 YEARS'] = (merged_df['DFS_STATUS'] == 'DiseaseFree') & (merged_df['DFS_MONTHS'] <= 5*12)
    merged_df['RECURRED AFTER 5 YEARS'] = (merged_df['DFS_STATUS'] == 'Recurred/Progressed') & (merged_df['DFS_MONTHS'] > 5*12)
    merged_df['RECURRED BEFORE 5 YEARS'] = (merged_df['DFS_STATUS'] == 'Recurred/Progressed') & (merged_df['DFS_MONTHS'] <= 5*12)
    merged_df['DECEASED WITHIN 5 YEARS'] = (merged_df['OS_STATUS'] == 'DECEASED') & (merged_df['OS_MONTHS'] <= 5*12)

    merged_df['DISEASE FREE FOR MORE THAN 10 YEARS'] = (merged_df['DFS_STATUS'] == 'DiseaseFree') & (merged_df['DFS_MONTHS'] > 10*12)
    merged_df['DISEASE FREE FOR LESS THAN 10 YEARS'] = (merged_df['DFS_STATUS'] == 'DiseaseFree') & (merged_df['DFS_MONTHS'] <= 10*12)
    merged_df['RECURRED AFTER 10 YEARS'] = (merged_df['DFS_STATUS'] == 'Recurred/Progressed') & (merged_df['DFS_MONTHS'] > 10*12)
    merged_df['RECURRED BEFORE 10 YEARS'] = (merged_df['DFS_STATUS'] == 'Recurred/Progressed') & (merged_df['DFS_MONTHS'] <= 10*12)
    merged_df['DECEASED WITHIN 10 YEARS'] = (merged_df['OS_STATUS'] == 'DECEASED') & (merged_df['OS_MONTHS'] <= 10*12)

    # Rename tcga_id columns
    df_multi.rename(columns={'tcga_id': 'Patient ID'}, inplace=True)

    # Connect the original multilabel dataset and previously formed DataFrame with DFS and OS information
    df_multi_merged = pd.merge(df_multi, merged_df, on='Patient ID', how='left')
    df_multi_merged.drop(columns=df_multi_merged.columns[2:-22], inplace=True)
    df_multi_merged.drop(columns=['MaxCorr','Basal','Her2','LumA','LumB', 'Normal', 'Study ID'], inplace=True)  

    # Mergre DISEASE FREE FOR MORE THAN 5 YEARS and RECURRED BEFORE 5 YEARS
    df_multi_merged['Reccured within 5 years'] = [False if (val_1==True and val_2==False) else True for val_1, val_2 in zip(df_multi_merged['DISEASE FREE FOR MORE THAN 5 YEARS'].values,  df_multi_merged['RECURRED BEFORE 5 YEARS'].values)]

    # Remove NaN rows and check if they are removed
    df_multi_merged.dropna(inplace=True)

    # Extract samples for disease reccured within 5 years
    recc_within_5_years_bool = ((df_multi_merged['DISEASE FREE FOR MORE THAN 5 YEARS']==False) & (df_multi_merged['RECURRED BEFORE 5 YEARS']==False))==False
    df_multi_merged_recc_within_5_years = df_multi_merged.loc[recc_within_5_years_bool, :]


    pass



if __name__ == '__main__':
    main()