# REDCap parameters
CHOICE_SEP = " | "
CODE_SEP = ", "

group1_sample_size = 102
group1_mgh = ["41.18", "42", "7", "8", "7", "7", "7", "7"]
group1_redcross = ['11.76', '12', '2', '2', '2', '2', '2', '2']
group1_magburaka = ['29.41', "42", "7", "7", "7", "7", "7", "7"]
group1_loreto = ['17.65', '6', '1', '0', '1', '1', '1', '1']
total_group1 = ['100','102','17','17','17','17','17','17']

group2_sample_size = 102
group2_mgh = ["41.18", "42", "7", "6", "7", "7", "8", "7"]
group2_redcross = ['11.76', '12', '2', '2', '2', '2', '2', '2']
group2_magburaka = ['29.41', '42',  "7", "7", "7", "7", "7", "7"]
group2_loreto = ['17.65', '6', '1', '2', '1', '1', '0', '1']
total_group2 = ['100', '102','17','17','17','17','17','17']

group3_sample_size = 894
group3_mgh = ["42.28", "378", "63", "63", "63", "63", "63", "63" ]
group3_redcross = ['11.41', '102', '17', '17', '17', '17', '17', '17']
group3_magburaka = ['30.20', '270', '45', '45', '45', '45', '45', '45']
group3_loreto = ['16.11', '144', '24', '24', '24', '24', '24', '24']
total_group3 = ['100','894','149','149','149','149','149','149']

# DATA DICTIONARY FIELDS USED TO IMPROVE PERFORMANCE OF API CALLS
MRS_LOGIC_FIELDS = ['record_id', 'child_dob','mrs_study_number_t2','study_number','mrs_t2_photo_labels']




# PARAMS FOR T3 SUMMARY TOOL

t3_sample_size = 1098
t3_phase1_sample_size = 102
t3_phase2_sample_size = 102
t3_phase3_sample_size = 894

t3_p1_group1 = ["41.18", "10", "2", "2", "2", "2", "2", "2"]
t3_p1_group2 = ["41.18", "80", "14", "14", "14", "14", "14", "14"]
t3_p1_total = ["100", "102", "17", "17", "17", "17", "17", "17"]
t3_p2_group1 = ["41.18", "10", "2", "2", "2", "2", "2", "2"]
t3_p2_group2 = ["41.18", "80", "14", "14", "14", "14", "14", "14"]
t3_p2_total = ["41.18", "102", "17", "17", "17", "17", "17", "17"]
t3_p3_group1 = ["41.18", "89", "15", "15", "15", "15", "15", "15"]
t3_p3_group2 = ["41.18", "697", "116", "116", "116", "116", "116", "116"]
t3_p3_total = ["100", "894", "149", "149", "149", "149", "149", "149"]

MAK_sample_size = 756
MAK_phase1_sample_size = 72
MAK_phase2_sample_size = 72
MAK_phase3_sample_size = 612

MAK_p1_group1 = ["21.27", "18", "3", "3", "3", "3", "3", "3"]
MAK_p1_group2 = ["79.43", "54", "9", "9", "9", "9", "9", "9"]
MAK_p1_total = ["100", "72", "12", "12", "12", "12", "12", "12"]
MAK_p2_group1 = ["21.27", "18", "3", "3", "3", "3", "3", "3"]
MAK_p2_group2 = ["79.43", "54", "9", "9", "9", "9", "9", "9"]
MAK_p2_total = ["100", "72", "12", "12", "12", "12", "12", "12"]
MAK_p3_group1 = ["21.27", "132", "22", "22", "22", "22", "22", "22"]
MAK_p3_group2 = ["79.43", "480", "80", "80", "80", "80", "80", "80"]
MAK_p3_total = ["100", "612", "102", "102", "102", "102", "102", "102"]

MAG_sample_size = 342
MAG_phase1_sample_size = 30
MAG_phase2_sample_size = 30
MAG_phase3_sample_size = 282

MAG_p1_group1 = ["21.27", "6", "1", "1", "1", "1", "1", "1"]
MAG_p1_group2 = ["79.43", "24", "4", "4", "4", "4", "4", "4"]
MAG_p1_total = ["100", "30", "5", "5", "5", "5", "5", "5"]
MAG_p2_group1 = ["21.27", "6", "1", "1", "1", "1", "1", "1"]
MAG_p2_group2 = ["79.43", "24", "4", "4", "4", "4", "4", "4"]
MAG_p2_total = ["100", "30", "5", "5", "5", "5", "5", "5"]
MAG_p3_group1 = ["21.27", "60", "10", "10", "10", "10", "10", "10"]
MAG_p3_group2 = ["79.43", "222", "37", "37", "37", "37", "37", "37"]
MAG_p3_total = ["100", "282", "47", "47", "47", "47", "47", "47"]


### PARAMS FOR LIST OF CANDIDATES
about_to_turn_18 = 17
days_before_18 = 0

ALERT_LOGIC_FIELDS = ['record_id', 'child_dob', 'screening_date', 'child_fu_status', 'community', 'int_azi',
                      'int_next_visit', 'int_date', 'int_sp', 'intervention_complete', 'hh_child_seen','hh_why_not_child_seen',
                      'hh_date','study_number', 'call_caretaker','reachable_status',
                      'household_follow_up_complete', 'a1m_date', 'comp_date','phone_success','child_weight_birth',
                      'child_birth_weight_known','phone_success','fu_type','hh_drug_react','hh_health_complaint',
                      'hh_mother_caretaker','hh_drug_react','hh_health_complaint','int_random_letter', 'death_reported_date',
                      'hh_date', 'ae_date','sae_awareness_date','ms_date','unsch_date','mig_date','comp_date','ch_his_date',
                      'phone_child_status']
