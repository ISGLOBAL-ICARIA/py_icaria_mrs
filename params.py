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
phase3_magburaka = ['30.20', '234', '39', '39', '39', '39', '39', '39']
phase3_mgh = ["37.58", "336", "56", "56", "56", "56", "56", "56" ]
phase3_redcross = ['11.41', '102', '17', '17', '17', '17', '17', '17']
phase3_loreto = ['11.41', '102', '17', '17', '17', '17', '17', '17']
phase3_masuba = ['4.70', '42', '7', '7', '7', '7', '7', '7']
phase3_stocco = ['4.70', '42', '7', '7', '7', '7', '7', '7']
total_phase3 = ['100','894','149','149','149','149','149','149']


not_recruitable_participants = ['12010219','5010055','8010561','8021447','8021525','1010189','1010622',
                                '15010068','15010068','15010068','15010341','16010035','17010376','10010378',
                                '11010117','13010212','4010149','5010007','1010189','1010622','1020358']

# T3 TOTAL NUMBER OF CANDIDATES [Sample size | group1 | group2]
HF_cohort_sample_size = {'HF08':[318,54,264],'HF11':[101,20,81],'HF12':[112,18,93],'HF13':[90,12,78],
               'HF16':[381,64,317],'HF17':[96,18,78]}

### PARAMS FOR T3 18 MoA participants
about_to_turn_18 = 17
days_before_18 = 0

# DATA DICTIONARY FIELDS USED TO IMPROVE PERFORMANCE OF API CALLS
ALERT_LOGIC_FIELDS = [
    'record_id', 'child_dob', 'int_azi', 'int_date', 'hh_child_seen','hh_why_not_child_seen',
    'study_number', 'reachable_status', 'int_random_letter', 'death_date', 'phone_child_status','wdrawal_date'
]



