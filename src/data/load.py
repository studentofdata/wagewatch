import os
import config
import pandas as pd
import numpy as np


data_processed_location = os.path.join(
    os.getcwd(), '..', '..', 'data', 'processed')


def kwik_analytics(dataframe, print_frame, markets):
    # Create analytics frame.
    # I: Dataframe with the required following columns:
    # 1. CREATED_cur_base_pay_hrs
    # 2. CITYMARKET
    # 3. POSITION
    # 4. clusters (labels)
    # O: Dictionary with two dataframes in it. The jobs dataframe and hotels dataframe
    
    payload = {}
    jobs_frame = dataframe
    jobs_frame['CREATED_cur_base_pay_hrs'] = jobs_frame['CREATED_cur_base_pay_hrs'].astype(
        float)
    j_frame = jobs_frame.groupby(['CITYMARKET', 'POSITION', 'clusters'])[
                                 'CREATED_cur_base_pay_hrs'].describe(include='all').reset_index()
    j_frame = pd.pivot_table(j_frame, index=['CITYMARKET', 'POSITION', 'clusters'], columns=[
                             'level_3'], aggfunc=np.sum).reset_index()
    j_frame.columns = ['CITYMARKET', 'POSITION', 'clusters',
        '25', '50', '75', 'count', 'max', 'mean', 'min', 'std']
    j_frame = j_frame.sort_values(
        by=['CITYMARKET', 'POSITION', 'clusters', 'count'])
    hotels_frame = dataframe[['PROPERTY_CODE', 'PROPERTY_NAME',
        'SURVEYTYPE', 'CITYMARKET', 'STATE', 'ZIP', 'POSITION', 'clusters']]
    payload['jobs'] = j_frame
    payload['hotels'] = hotels_frame

    if print_frame == True:
        # This is a basic function which takes in the output from kwik_analytics()
        #
        # This is to be turned into a function which creates the output for reporting.
        # an xlsx which will contain summary and detailed info for a 'top market' run.
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        file_name = 'ww_top_' + str(len(markets)) + '_markets_output.xlsx'
        file_location = os.path.join(data_processed_location, file_name)
        writer = pd.ExcelWriter(file_location, engine='xlsxwriter')

        for market in markets:
            jobs_sheet = j_frame[j_frame['CITYMARKET'] == market]
            jobs_sheet_name = market + "_" + "wages"
            jobs_sheet.to_excel(writer, sheet_name=jobs_sheet_name, encoding='utf8')
            hotels_sheet = hotels_frame[hotels_frame['CITYMARKET'] == market]
            hotels_sheet_name = market + "_" + "hotels"
            hotels_sheet.to_excel(writer, sheet_name=hotels_sheet_name, encoding='utf8')
        # Close the Pandas Excel writer and output the Excel file.

        writer.save()
    else:
        pass

    return payload

