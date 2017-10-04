import os
import config
import constants
import pandas as pd

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
    """ Placeholder for additional functions """
    return dataframe

def answer_cur_base_pay(dataframe):
    """ Take the current base pay and normalize so all data is in hours """
    temp = dataframe['ANSWER_cur_base_pay']#.astype(float)
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


def clean_hotel_model(dataframe, column_operations):
	""" This is meant to be a better way to 'register' and work with functions intended
	for columnar transformation, but liking this less over time. why?"""
	dataframe = column_operations['ANSWER_num_rooms'](dataframe)
#    dataframe = column_operations['ANSWER_ann_op_rev'](dataframe)
	dataframe = column_operations['ANSWER_ann_revenue'](dataframe)
	dataframe = column_operations['ANSWER_num_employees_pos'](dataframe)
	dataframe = column_operations['create_Executive'](dataframe)
	dataframe = column_operations['ANSWER_cur_base_pay'](dataframe)
	dataframe = column_operations['create_RevPAR'](dataframe)
	return dataframe


