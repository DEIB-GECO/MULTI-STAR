import pandas as pd
import numpy as np
import mrmr
from mrmr import mrmr_classif
import seaborn as sb
from collections import OrderedDict
import warnings
warnings.filterwarnings('ignore')

def find_median_less_than_one(df, col_name):

    """Support function to find the median of the values in a column."""

    # Get only the values in the column that are less than 1
    values = df[df[col_name] < 1][col_name]
    # Compute the median of the values
    median = values.median()
    return median

def find_deviation_value(dfs, col_name):
  
    """Support function to find the waste (difference between max median and min median local)"""

    median_values = []
    for df in dfs:
        m =  find_median_less_than_one(df, col_name)
        median_values.append(m)
    return max(median_values) - min(median_values)


def sbf_analysis(X, Y, additional_link: bool=False, link_mask= None ):
  
    """Computing the correlation matrix with pearson correlation from the train set with 49k features"""
    ##### current issue -> ram crashes because computation power is not enough -> reduced to 30k
    pc_global = X.corr()
    
    # checking the scores in the pearson correlation
    print(pc_global.describe())
    # more information about the distribution of the correlations
    # print(pc_global.describe())
    # to display the correlation matrix let's plot and show them with a heatmap
    '''sb.heatmap(pearson_corr, 
                xticklabels=pearson_corr.columns,
                yticklabels=pearson_corr.columns,
                cmap='RdBu_r',
                annot=True,
                linewidth=0.5)
    '''

    # find median after removing values equal to 1 or duplicated ones 
    values = pc_global.values
    # get only the vlaues under the diagonal (since simmetric matrix with duplicated values) to compute the global stats
    lower_triangular = values[np.tril_indices(values.shape[0], -1)]
    flatten = lower_triangular.flatten()
    flatten_df = pd.DataFrame(flatten)
    flatten_df = flatten_df[flatten_df <1]
    # compute global median and save it
    global_median = np.median(flatten_df)
    print("Global median:", global_median)

    pc_global[ pc_global ==1] =  0

    print("Per class correlation with pearson: \n\n")

    local_medians_dic = {}
    local_pcs = {}
    # for each class in the classes available
    for name_class in Y.unique():
        print(name_class)
        # find the samples from the train assigned to that class
        sample_per_class = Y[Y==name_class]
        print("Samples with label:", len(sample_per_class))
        # choose the corresponding X assigned to the samples with as label the current class
        X_class = X.loc[sample_per_class.index]
        print(X_class.shape)
        # compute correlation matrix only for those samples
        class_corr = X_class.corr()
        # print("Correlation of class \n", class_corr)

        values = class_corr.values
        lower_triangular = values[np.tril_indices(values.shape[0], -1)]
        flatten = lower_triangular.flatten()
        flatten_df = pd.DataFrame(flatten)
        flatten_df = flatten_df[flatten_df <1]
        median_local = np.median(flatten_df)
        print("Local median:", median_local)

        class_corr[ class_corr ==1] =  0
        # saving in two dictionaries the information for the next steps of filtering
        # which are: pearson correlation matrices (complete) for only samples of each class
        # local median values for each of these "LOCAL" pearson correlation matrices
        local_pcs[name_class] = class_corr
        local_medians_dic[name_class]= median_local
  
    print(local_medians_dic)

    # now I have the global variables: class_corr which is the matrix with correlations and median_global which is the global median threshold
    # and the local variables which are the matrix of correlation with samples of each class and local median threshold for each one of them

    # Initialize array temp
    temp = []
    i = 0 # counter to check loop status
    # Loop through each column in matrix a
    for col in pc_global.columns:

        print("current feature: ", col, " we are ath the feature n.", i)
        i += 1
        # Check if all values in the column are less than median_a
        if all(pc_global[col] < global_median):
            print(col, "added to temp array")
            temp.append(col)
        else:
            # Find rows where values in the column are greater than or equal to the threshold
            # these means that these two features are similar and the scores have to be checked locally
            row_feats = pc_global[col][pc_global[col] >=  global_median].index.tolist() 

            for row_feat in row_feats:
                # assuimption: the two features are "also" locally similar 
                not_locally_similar = False
                # Check if all values in the corresponding columns of local matrices are less than their respective medians
                for c_name in local_pcs.keys():
                    local_pc = local_pcs[c_name]
                    local_median = local_medians_dic[c_name]
                    if local_pc[col][row_feat] < local_median: # if all(local_pc[col] < local_median):
                        # if all values in the column of the local pearson correlation matrix are under the local threshold we can add both features (row_feat and col) in the temp
                        not_locally_similar = True
                        break
                
                if not_locally_similar:
                    # print(col, row_feat, " have been added to temp since locally not similar")
                    temp.append(col)
                    temp.append(row_feat)
                else:
                    # print("Choosing by looking at higher waste between two features")
                    dev_col = find_deviation_value(list(local_pcs.values()), col)
                    dev_row = find_deviation_value(list(local_pcs.values()), row_feat)
                    # for the final choice of the feature two keep, looking at the maximum waste for each of the features and choosing the wider one
                    if dev_col > dev_row:
                        temp.append(col)
                        # removing all values from temp that correspond to the feature with less waste
                        temp = list(filter(lambda a: a != row_feat, temp))
                    else:
                        temp.append(row_feat)
                        temp = list(filter(lambda a: a != col, temp))

    print(temp)
    # removing duplicates
    temp_nodup = list(OrderedDict.fromkeys(temp))
    return temp_nodup