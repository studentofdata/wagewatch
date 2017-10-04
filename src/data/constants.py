###############################################
# Variable Mapping & Selection
# Here we map over the survey questions we believe will be of use 

ci_mapping = {'# of Employees in this Position':'num_employees_pos',
        'Current Base Pay':'cur_base_pay',
        'Exempt or Non-exempt':'e_or_ne',
        'Incentive/Bonus/Commission (Other Cash) Eligible':'inc_bonus_comm',
        'Pay Increase Type':'pay_increase_type',
        "Highest Paid Employee's Base Pay":'high_base_pay',
        "Lowest Paid Employee's Base Pay":'low_base_pay',
        'Starting Rate':'start_pay',
        'Unionized':'union',
        'Pay Range Maximum':'pay_max',
        'Pay Range Minimum':'pay_min',
        'Target Incentive (% of Base)':'target_inc'}

gi_mapping = {"What was the location's total annual operating revenue for the last fiscal year?": 'ann_op_rev',
             "What is the budgeted wage/salary increase for exempt positions this fiscal year?": 'bt_inc_e',
             "What is the budgeted wage/salary increase for non-exempt positions this fiscal year?":'bt_inc_ne',
             "Approximately what percentage of your workforce works full-time?":'perc_full_time',
             "What is the annual turnover rate?":'turnover_rater',
             "What is the total number of guest rooms at this location?":'num_rooms',
             "What is the night shift premium amount?":'night_shift_prem',
             "When did the wages provided in this survey become effective for your employees (past date)?":'eff_wage_date',
             "What is the indoor meeting space in square feet (include prefunction space)?":'sq_ft_meeting',
             "What was your locations's annual food & beverage revenue for the last fiscal year?":"ann_food_bev",
             "What percentage of operating expenses are wages and benefits?":'perc_op_labor',
             "Does the location have flexibility in hiring rates?":'flex_hire_wage',
             "Do hiring managers (vs. HR) set wages?":'hr_set_wage',
             "What was your location's annual rooms revenue for the last fiscal year?":'ann_revenue',
             "How many guest rooms is a housekeeper expected to clean in a standard 8 hour shift?":'rooms_quota_shift',
             "What is the monetary bonus given per room cleaned over quota?":'bonus_rooms_quota',
             "What amount is paid to a housekeeper for cleaning a rollaway bed per occurrence?":'paid_rollaway_bed',
             "What is the housekeeper turnover rate?":'housekeeper_turnover_rate'}

#Columns Needed
keep_columns_CI = ['PROPERTY_CODE',
                   'PROPERTY_NAME',
                   'JOB_CODE',
                   'POSITION',
                   'QUESTION',
                   'ANSWER']

keep_columns_PI = ['PROPERTY_CODE',
                  'PROPERTY_NAME',
                  'INDUSTRY_NAME',
                  'ADDRESS1',
                  'ADDRESS2',
                  'CITY',
                  'STATE',
                  'ZIP',
                  'CITYMARKET',
                  'BINGLATITUDE',
                  'BINGLONGITUDE']

keep_columns_GI = ['PROPERTY_CODE',
                  'PROPERTY_NAME',
                  'QUESTION',
                  'ANSWER']

#Rows to eliminate
del_rows_property_name = ['HOTEL DOMAIN']


#Number of hours in a working year
hours_per_year = 2080


#Determine the type of position for future processing if they have a 4 digit current base pay. Is it monthly or annual?
# In the future create a survey that has this type of validation on the front end. Come-on.
exec_jobs = ['Director','Manager','Controller','Account','Executive','Purchasing','Supervisor']
