import os
import re
import config
import constants
import transform
import numpy as np
import pandas as pd
import matplotlib as mpl
from scipy.spatial import distance_matrix
import plotly as py

files_location = config.data_source_file_location
files = os.listdir(files_location)


def extract_data_ci(years):
	pass
def extract_data_pi(years):
	pass
def extract_data_gi(years):
	pass

###############################################
# Read in the datasets, this would be a good future location 
# to abstract away from 2016 and have a general year or subset here. 
# Or to create a function which would be given the desired frame
# to be processed.


def extract_all_lazy():
	""" This is a temporary file which utilizes the 2016 data.
	In the future this should use database connection and call directly from the DB.
	Returns a dictionary of data frames that have been moderately transformed. Moderately transformed is subsetting rather than direct manipulation. """

	#Construct filepaths: Data COMP_INFO_1
	data_ci1_name = "DATA_2016_COMP_INFO_1.csv"
	data_ci1_fullname = os.path.join(files_location, data_ci1_name)
	#Data COMP_INFO_2
	data_ci2_name = "DATA_2016_COMP_INFO_2.csv"
	data_ci2_fullname = os.path.join(files_location, data_ci2_name)
	#Data PROPERTY INFO
	data_pi_name = "DATA_2016_PROPERTY_INFO_ST.csv"
	data_pi_fullname = os.path.join(files_location, data_pi_name)
	#Data General Info
	data_gi_name = "DATA_2016_GENERAL_INFO.csv"
	data_gi_fullname = os.path.join(files_location, data_gi_name)

	#Read & Process COMP_INFO
	data_ci1 = pd.read_csv(data_ci1_fullname, skiprows=2, usecols = constants.keep_columns_CI, encoding='ISO-8859-1')
	data_ci2 = pd.read_csv(data_ci2_fullname, skiprows=2, usecols = constants.keep_columns_CI, encoding='ISO-8859-1')

	data_ci = data_ci1.append(data_ci2)
	data_ci['QUESTION'] = data_ci['QUESTION'].replace(constants.ci_mapping)
	# Take only the survey questions mapped
	data_ci = data_ci[data_ci['QUESTION'].isin(constants.ci_mapping.values())]
	data_ci = data_ci.set_index(['PROPERTY_CODE','PROPERTY_NAME','JOB_CODE','POSITION'])
	data_ci = data_ci.pivot(columns="QUESTION")
	data_ci.columns = ["_".join(pair) for pair in data_ci.columns]
	data_ci = data_ci.reset_index()

	#Read & Process Property Info data
	data_pi = pd.read_csv(data_pi_fullname, usecols = constants.keep_columns_PI, encoding='ISO-8859-1')
	#survey_type_transformed = transform.surveytype_categorical(data_pi)
	#data_pi = pd.merge(data_pi, survey_type_transformed, on=['PROPERTY_CODE'])

	#Read & Process General Info
	data_gi = pd.read_csv(data_gi_fullname, skiprows = 2, usecols = constants.keep_columns_GI, encoding='ISO-8859-1')
	data_gi['QUESTION'] = data_gi['QUESTION'].replace(constants.gi_mapping)
	# Take onl the survey questions mapped
	data_gi = data_gi[data_gi['QUESTION'].isin(constants.gi_mapping.values())]
	data_gi = data_gi.set_index(['PROPERTY_CODE','PROPERTY_NAME'])
	data_gi = data_gi.pivot(columns="QUESTION")
	data_gi.columns = ["_".join(pair) for pair in data_gi.columns]
	data_gi = data_gi.reset_index()

	#This frame needs to be reworked
	d_ci = pd.merge(data_gi, data_pi, on = ['PROPERTY_CODE','PROPERTY_NAME'])
	d_ci = pd.merge(d_ci, data_ci, on = ['PROPERTY_CODE','PROPERTY_NAME'],suffixes= ['_ci','_gi'])

	#Observations by Dimensions to determine top X markets
	#Can this be in a better position?
	d_ci = d_ci[~(d_ci['PROPERTY_NAME'].isin(constants.del_rows_property_name))]
	d_ci['POSITION'] = d_ci['POSITION'].astype(str)

	payload = {}
	payload['gi'] = data_gi
	payload['pi'] = data_pi
	payload['ci'] = data_ci
	payload['d_ci'] = d_ci

	return payload
