PROJECTS = ['HF08','HF11','HF12','HF13','HF16','HF17']

# T2 EXPECTED NUMBER OF CANDIDATES PER PHASE
phase1_sample_size = 102
phase1_mgh = ["41.18", "42", "7", "8", "7", "7", "7", "7"]
phase1_redcross = ['11.76', '12', '2', '2', '2', '2', '2', '2']
phase1_magburaka = ['41.18', "42", "7", "7", "7", "7", "7", "7"]
phase1_loreto = ['5.88', '6', '1', '0', '1', '1', '1', '1']
total_phase1 = ['100','102','17','17','17','17','17','17']

phase2_sample_size = 102
phase2_mgh = ["41.18", "42", "7", "6", "7", "7", "8", "7"]
phase2_redcross = ['11.76', '12', '2', '2', '2', '2', '2', '2']
phase2_magburaka = ['41.18', '42',  "7", "7", "7", "7", "7", "7"]
phase2_loreto = ['5.88', '6', '1', '2', '1', '1', '0', '1']
total_phase2 = ['100', '102','17','17','17','17','17','17']

phase3_sample_size = 894
phase3_magburaka = ['30.20', '270', '45', '45', '45', '45', '45', '45']
phase3_mgh = ["37.58", "336", "56", "56", "56", "56", "56", "56" ]
phase3_redcross = ['11.41', '102', '17', '17', '17', '17', '17', '17']
phase3_loreto = ['11.41', '102', '17', '17', '17', '17', '17', '17']
phase3_masuba = ['4.70', '42', '7', '7', '7', '7', '7', '7']
phase3_stocco = ['4.70', '42', '7', '7', '7', '7', '7', '7']
total_phase3 = ['100','894','149','149','149','149','149','149']


# T3 TOTAL NUMBER OF CANDIDATES [Sample size | phase1 | phase2 | phase3]
HF_cohort_sample_size = {'HF08':[342,30,30,282],'HF11':[756,72,72,612],'HF12':[756,72,72,612],'HF13':[756,72,72,612],
               'HF16':[756,72,72,612],'HF17':[756,72,72,612]}

### PARAMS FOR T3 18 MoA participants
about_to_turn_18 = 17
days_before_18 = 0

# DATA DICTIONARY FIELDS USED TO IMPROVE PERFORMANCE OF API CALLS
ALERT_LOGIC_FIELDS = [
    'record_id', 'child_dob', 'int_azi', 'int_date', 'hh_child_seen','hh_why_not_child_seen',
    'study_number', 'reachable_status', 'int_random_letter', 'death_date', 'phone_child_status','wdrawal_date'
]



