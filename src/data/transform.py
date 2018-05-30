import os
import config
import constants
import pandas as pd
import numpy as np
from sklearn import cluster



t_meta_data = {}

# Utility/summarizing functions
def top_markets_by_property(property_data_frame, number_of_markets, dimension):
    """ A function which returns the top number_of_markets per dataframe
    I: dataframe, the number of markets to return
    O: list of the top markets sorted by number of observations"""

    markets = property_data_frame.groupby([dimension]).count().reset_index()
    markets = markets.copy()
    markets = markets.sort(markets.columns[2],ascending=False)
    top_markets = markets.head(number_of_markets)
    return top_markets[dimension].tolist()

def surveytype_categorical(dataframe):
    """take in the data_pi frame and transform single categorical surveytype column into
     numeric for clustering. This is a very specific function, will need to be adapted for general use
     if it stays"""

    dataframe_v2 = dataframe[dataframe.duplicated(['PROPERTY_CODE']) == False]
    d_pivot = dataframe_v2[['PROPERTY_CODE','SURVEYTYPE']]
    d_pivoted = d_pivot.pivot(columns='SURVEYTYPE')
    d_pivoted_v2 = d_pivoted.applymap(lambda x: 0 if np.isnan(x) else 1)
    d_pivoted_v2.columns = d_pivoted_v2.columns.droplevel(0)
    d_pivoted_v2['PROPERTY_CODE'] = dataframe['PROPERTY_CODE'].astype(object)

    dataframe_v3 = pd.merge(dataframe, d_pivoted_v2, on=['PROPERTY_CODE'])

    return dataframe_v3

# Create a class to collect meta information on data transformations
def create_Executive(dataframe):
    """ Take the exec_jobs from the constant.py file and subset for jobs containing text in the list exec_jobs. The purpose for this is to  """
    dataframe['CREATED_executive'] = dataframe.apply(lambda x: 'yes' if any(pd.Series(x['POSITION']).str.contains('|'.join(constants.exec_jobs))) else 'no', axis=1)
    return dataframe

def answer_num_rooms(dataframe):
    """ Subset out the null data and ensure that the field is numeric """
    dataframe = dataframe[~(dataframe['ANSWER_num_rooms'].isnull())]
    dataframe = dataframe[dataframe['ANSWER_num_rooms'].str.contains('[0-9]')]
    return dataframe

def answer_ann_op_rev(dataframe):
    """ Subset out the null data """
    dataframe = dataframe[~(dataframe['ANSWER_ann_op_rev'].isnull())]
    return dataframe

def answer_ann_revenue(dataframe):
    """ subset out the null data """
    dataframe = dataframe[~(dataframe['ANSWER_ann_revenue'].isnull())]
    return dataframe

def answer_num_employees_pos(dataframe):
    """ subset out the null data """
    ane_dataframe = dataframe
    ane_dataframe = ane_dataframe[~(ane_dataframe['ANSWER_num_employees_pos'].isnull())]
    return ane_dataframe

def answer_cur_base_pay(dataframe):
    """ Take the current base pay and normalize so all data is in hours """
    temp = dataframe['ANSWER_cur_base_pay'].astype(str)
    temp_v1 = temp.str.partition('.')
    dataframe['ANSWER_cur_base_pay'] = dataframe['ANSWER_cur_base_pay'].astype(float)
    dataframe['CREATED_base_pay_digits'] = temp_v1.iloc[:,0].apply(lambda x: len(str(x)))
    dataframe['CREATED_cur_base_pay_hrs'] = dataframe.apply(lambda x: x['ANSWER_cur_base_pay']/constants.hours_per_year if (x['CREATED_base_pay_digits'] == 4 and x['CREATED_executive'] == 'no') else
                                                           (x['ANSWER_cur_base_pay']*12)/constants.hours_per_year if (x['CREATED_base_pay_digits'] == 4 and x['CREATED_executive'] == 'yes') else 
                                                                      x['ANSWER_cur_base_pay']/constants.hours_per_year if x['CREATED_base_pay_digits'] > 4 else x['ANSWER_cur_base_pay'], axis=1)
    return dataframe


def create_RevPAR(dataframe):
    """Calculate revpar from answer_num_rooms converted to supply of 
    room nights divided by answer_ann_revenue"""
    dataframe['CREATED_revpar'] = dataframe['ANSWER_ann_revenue'].astype(float)/(dataframe['ANSWER_num_rooms'].astype(float)*365)
    return dataframe


def clean_model(dataframe, column_operations):
    """ This is meant to be a better way to 'register' and work with functions intended
	for columnar transformations. Exploring different ways of thinking through a pipeline"""
    
    temp_payload = []
    payload = {}
    masterdataframe = dataframe
    for operation in column_operations.keys():
        prior_data = ''
        post_data = ''
        # Here is where we can initialize some meta data
        # Take the shape of the data to start. Plenty more in the future. Consider proper interface/object
        prior_data = operation + "_PRIOR :: Rows: %s, Columns: %s" % (masterdataframe.shape[0], masterdataframe.shape[1])
        print operation
        masterdataframe = column_operations[operation](masterdataframe)
        post_data = operation + "_POST :: Rows: %s, Columns: %s" % (masterdataframe.shape[0], masterdataframe.shape[1])

        temp_payload.append(prior_data)
        temp_payload.append(post_data)

    payload['data'] = masterdataframe
    payload['metadata'] = temp_payload

    return payload


def run_model(dataframe, features_norm, number_of_clusters):
    """ A very specific function. This needs to be restructured in a refactoring, but need to power through to viz """

    model_feature = []
    for feature in features_norm:
        model_feature.append(dataframe[feature].T.values)
    matrix = np.matrix(zip(*model_feature))
    k_means = cluster.KMeans(n_clusters=number_of_clusters)
    k_means.fit(matrix)
    dataframe['clusters'] = k_means.labels_
    dataframe['intertia'] = k_means.inertia_
    return dataframe