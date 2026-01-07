import numpy as np
import pandas as pd
import params
import tokens
import gspread
from datetime import datetime
import math
from gspread_dataframe import set_with_dataframe
import redcap
from dateutil.relativedelta import relativedelta


def file_to_drive(worksheet,df,drive_file_name,folder_id,index_included=True):
    """
        Used to upload a Pandas DataFrame into a specific drive file and worksheet

    :param worksheet: GDrive worksheet to be updated
    :param df: dataframe to be uplodaed into Gdrive
    :param drive_file_name: GDrive file name
    :param folder_id: Gdrive folder ID needed to connect to Gdrive.
    """
    gc = gspread.oauth(tokens.path_credentials)
    sh = gc.open(title=drive_file_name,folder_id=folder_id)
    set_with_dataframe(sh.worksheet(worksheet), df,include_index=index_included)

def calculate_age_months(dob):
    """Compute the age in years from a date of birth.
    :param dob: Date of birth
    :type dob: Datetime
    :return: Date of birth in years
    :rtype: int
    """

    today = datetime.today()
    months = (today.year - dob.year) * 12 + (today.month - dob.month)
    return months

def days_to_birthday(dob, fu):
    """For a date which is about to its birthday, i.e. this/coming month, compute the number of days to the birthday.

    :param dob: Date of birth
    :type dob: Datetime
    :param fu: Months of study follow up
    :type fu: int
    :return: Days to birthday
    :rtype: int
    """
    today = datetime.today()
    return (dob + relativedelta(months=+fu) - today).days

def export_records(project,project_key,fields_,filter_logic,final_df, index=False,print_=False):
    """
    Function to export all records with specific fields and filter logic, defined as params
    :return: dataframe filled with records and defined fields, with specific logic.
    """
    if index == False:
        index = project_key

    try:
        df_mrs = project.export_records(format='df', fields=fields_,filter_logic=filter_logic)
        record_ids = df_mrs.index.get_level_values('record_id')
        df_letters = project.export_records(
            format='df',
            records=list(record_ids.drop_duplicates()),
            fields=["study_number", "int_random_letter"],
            filter_logic="[study_number] != ''"
        )
        if print_:
            print(df_letters.index)
        letters = df_letters.groupby('int_random_letter')[['study_number']].count()
        letters = letters.rename(columns={'study_number': index.split(".")[0]})

        final_df = pd.concat([final_df, letters.T])
    except:
        noletters =pd.DataFrame(columns=['A','B','C','D','E','F'],index=[index])
        noletters.loc[index] = [0,0,0,0,0,0]
        final_df= pd.concat([final_df,noletters])

    return final_df.fillna(0)

class MRS_T2_FUNCTIONS:
    """
    T2 Project functions
    """

    def __init__(self):
        pass

    def mrs_t2_control_sheet(self):
        """
        Genereate the summary tool for MRS T2 from all MRS data in REDCap
        :return: Save to the Google Drive Sheet the MRS T2 summary for each Phase of the MRS project
        """

        # Expected number of recruitments per Phase in MRS T2
        print("\nMRS T2 SUMMARY TOOL\n")
        print("Extracting expected number of recruitments per HF and letter . . .")
        phase1_expected, phase2_expected,phase3_expected = MRS_T2_FUNCTIONS().expected_mrs_t2()

        # Getting all records from MRS T2  a d getting the numbers per letter
        phase1_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])
        phase2_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])
        phase3_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])

        for project_key in tokens.REDCAP_PROJECTS_ICARIA:
            print("[{}] Getting MRS records from {}...".format(datetime.now(), project_key))
            project = redcap.Project(tokens.URL, tokens.REDCAP_PROJECTS_ICARIA[project_key])

            if project_key not in ['HF13','HF17']:
                phase1_df = export_records(project,project_key,['mrs_study_number_t2'],"([mrs_date_t2]!='') and [mrs_nasophar_swab_a_t2]='1' and [mrs_nasophar_swab_b_t2]='1' and [mrs_rectal_swab_t2]='1' and [mrs_t2_group]='1'",phase1_df).fillna(0)
                phase2_df = export_records(project,project_key,['mrs_study_number_t2'],"([mrs_date_t2]!='')  and [mrs_nasophar_swab_a_t2]='1' and [mrs_rectal_swab_t2]='1' and [mrs_t2_group]='2'",phase2_df).fillna(0)
            phase3_df = export_records(project,project_key,['mrs_study_number_t2'],"([mrs_date_t2]!='')  and [mrs_nasophar_swab_a_t2]='1' and [mrs_t2_group]='3'",phase3_df).fillna(0)
        # Generating the good format, including the expected number of samples together with the wanted data

        print ("Groups Preparation . . . ")
        phase1_df = MRS_T2_FUNCTIONS().groups_preparation_t2(phase1_df, params.phase1_sample_size,phase1_expected)
        phase2_df = MRS_T2_FUNCTIONS().groups_preparation_t2(phase2_df, params.phase2_sample_size,phase2_expected)
        phase3_df = MRS_T2_FUNCTIONS().groups_preparation_t2(phase3_df, params.phase3_sample_size,phase3_expected)

        print(pd.concat([phase1_df,phase2_df,phase3_df]))
        print("Saving tables on Google Drive . . .")

        # Saving int each Google Drive sheet tab, each phase page
        file_to_drive('Phase 1',phase1_df,tokens.drive_file_name_t2,tokens.drive_folder)
        file_to_drive('Phase 2',phase2_df,tokens.drive_file_name_t2,tokens.drive_folder)
        file_to_drive('Phase 3',phase3_df,tokens.drive_file_name_t2,tokens.drive_folder)
        print ("\nFINISHED.\n")

    def expected_mrs_t2(self):
        """
        :return: 3 DataFrames, for each phase, with all expected recruitments per HF and letter
        """
        phase1_expected = pd.DataFrame(index=['HF08 exp', 'HF11 exp', 'HF12 exp', 'HF16 exp','Total exp'],columns=['Proportion', 'Sample Size', 'A', 'B', 'C', 'D', 'E', 'F'])
        phase2_expected = pd.DataFrame(index=['HF08 exp', 'HF11 exp', 'HF12 exp', 'HF16 exp','Total exp'],
                                   columns=['Proportion', 'Sample Size', 'A', 'B', 'C', 'D', 'E', 'F'])
        phase3_expected = pd.DataFrame(index=['HF08 exp', 'HF11 exp', 'HF12 exp', 'HF16 exp','Total exp'],
                                   columns=['Proportion', 'Sample Size', 'A', 'B', 'C', 'D', 'E', 'F'])

        phase1_expected.loc['HF08 exp'] = params.phase1_magburaka
        phase1_expected.loc['HF11 exp'] = params.phase1_loreto
        phase1_expected.loc['HF12 exp'] = params.phase1_redcross
        phase1_expected.loc['HF16 exp'] = params.phase1_mgh
        phase1_expected.loc['Total exp'] = params.total_phase1

        phase2_expected.loc['HF08 exp'] = params.phase2_magburaka
        phase2_expected.loc['HF11 exp'] = params.phase2_loreto
        phase2_expected.loc['HF12 exp'] = params.phase2_redcross
        phase2_expected.loc['HF16 exp'] = params.phase2_mgh
        phase2_expected.loc['Total exp'] = params.total_phase2

        phase3_expected.loc['HF08 exp'] = params.phase3_magburaka
        phase3_expected.loc['HF11 exp'] = params.phase3_loreto
        phase3_expected.loc['HF12 exp'] = params.phase3_redcross
        phase3_expected.loc['HF13 exp'] = params.phase3_stocco
        phase3_expected.loc['HF16 exp'] = params.phase3_mgh
        phase3_expected.loc['HF17 exp'] = params.phase3_masuba
        phase3_expected.loc['Total exp'] = params.total_phase3

        return phase1_expected,phase2_expected,phase3_expected

    def groups_preparation_t2(self,group,sample_size_group, expected):
        """
        This function works preparing the number of recruitments per letter, joining all different subprojects if exist
        and obtaining only one row per project. It generates the actual sample size and the actul proportion of candidates.
        The list of expected candidates per HF for this phase is also saved and put together
        :param group: DataFrame of number of recruitments per each subproject of the big project
        :type group: pandas DataFrame
        :param sample_size_group: Sample size expected for that phase
        :type sample_size_group: int
        :param expected: list of expected recruitments per each project. Same format than the group field.
        :type expected: pandas Dataframe
        :return: DataFrame with number per letter .Both expected and actual one.
        """
        group = group.reset_index()
        group['index'] = group['index'].str.split(".").str[0]
        group = group.groupby('index').sum().astype(int)
        group1_total = [group['A'].sum(),group['B'].sum(),group['C'].sum(),group['D'].sum(),group['E'].sum(),group['F'].sum()]
        group.loc['Total'] = group1_total

        sample_size = []
        for k in group.index:
            sample_size.append(group.T[k].sum())
        group['Sample Size'] = sample_size
        group['Proportion'] = ["%.2f"%(x/(sample_size_group/100)) for x in sample_size]

        group = pd.concat([group,expected]).sort_index()[['Proportion','Sample Size','A','B','C','D','E','F']]
        return group



class MRS_T3_FUNCTIONS:
    """
    MRS T3 FUNCTIONS
    """
    def __init__(self):
        pass

    def mrs_t3_summary_tool(self, proj):
        """
        Genereate the summary tool for MRS T3 from all MRS data in REDCap.
        :return: Save to the Google Drive Sheet the MRS T3 summary for each Phase of the MRS project
        """

        group1_dict = {'Phase 1': [0,0,0,0,0,0], 'Phase 2': [0,0,0,0,0,0], 'Phase 3': [0,0,0,0,0,0]}
        group2_dict = {'Phase 1': [0,0,0,0,0,0], 'Phase 2': [0,0,0,0,0,0], 'Phase 3': [0,0,0,0,0,0]}

        for proj in params.PROJECTS:
            print("MRS T3 SUMMARY TOOL AND LIST OF T3 CANDIDATES for {}\n".format(proj))

            print("SUMMARY TOOL for {}\n".format(proj))

            expected_numbers = pd.read_excel(tokens.PATH_TO_EXPECTED_NUMBERS)
            proj_expected = expected_numbers[expected_numbers['HF'] == proj].T[2:].T
            group1_expected = proj_expected[proj_expected['Group'] == 'Group 1']
            group2_expected = proj_expected[proj_expected['Group'] == 'Group 2']

            phase1_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])
            phase2_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])
            phase3_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])

            for subproj in tokens.REDCAP_PROJECTS_ICARIA:
                if str(proj) in str(subproj):
                    print("[{}] Getting MRS records from {}...".format(datetime.now(), subproj))
                    project = redcap.Project(tokens.URL, tokens.REDCAP_PROJECTS_ICARIA[subproj])
                    phase1_df = export_records(project, subproj, ['mrs_study_number_t2_t3'], "([mrs_study_number_t2_t3]!='') and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_nasophar_swab_b_t2_t3]='1' and [mrs_rectal_swab_t2_t3]='1' and [mrs_t2_group_t3]='1' and [epipenta1_v0_recru_arm_1][int_azi]='1' and ( ([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epivita_v5_iptisp5_arm_1][int_azi]!='1') or [epimvr2_v6_iptisp6_arm_1][int_azi]!='1' )", phase1_df, index='Group 1').fillna(0)
                    phase1_df = export_records(project, subproj, ['mrs_study_number_t2_t3'], "([mrs_study_number_t2_t3]!='') and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_nasophar_swab_b_t2_t3]='1' and [mrs_rectal_swab_t2_t3]='1' and [mrs_t2_group_t3]='1' and [epipenta1_v0_recru_arm_1][int_azi]='1' and  ([epimvr1_v4_iptisp4_arm_1][int_azi]='1' or [epivita_v5_iptisp5_arm_1][int_azi]='1') and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'", phase1_df, index='Group 2').fillna(0)
                    phase1_df['Phase'] = 'Phase 1'

                    phase2_df = export_records(project, subproj, ['mrs_study_number_t2_t3'], "([mrs_study_number_t2_t3]!='')  and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_rectal_swab_t2_t3]='1' and [mrs_t2_group_t3]='2' and [epipenta1_v0_recru_arm_1][int_azi]='1' and ( ([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epivita_v5_iptisp5_arm_1][int_azi]!='1') or [epimvr2_v6_iptisp6_arm_1][int_azi]!='1' )", phase2_df, index='Group 1',print_=True).fillna(0)
                    phase2_df = export_records(project, subproj, ['mrs_study_number_t2_t3'], "([mrs_study_number_t2_t3]!='')  and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_rectal_swab_t2_t3]='1' and [mrs_t2_group_t3]='2' and [epipenta1_v0_recru_arm_1][int_azi]='1' and ([epimvr1_v4_iptisp4_arm_1][int_azi]='1' or [epivita_v5_iptisp5_arm_1][int_azi]='1') and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'", phase2_df, index='Group 2').fillna(0)
                    phase2_df['Phase'] = 'Phase 2'
                    phase3_df = export_records(project, subproj, ['mrs_study_number_t2_t3'], "([mrs_study_number_t2_t3]!='')  and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_t2_group_t3]='3' and [epipenta1_v0_recru_arm_1][int_azi]='1' and ( ([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epivita_v5_iptisp5_arm_1][int_azi]!='1') or [epimvr2_v6_iptisp6_arm_1][int_azi]!='1' )", phase3_df, index='Group 1').fillna(0)
                    phase3_df = export_records(project, subproj, ['mrs_study_number_t2_t3'], "([mrs_study_number_t2_t3]!='') and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_t2_group_t3]='3' and [epipenta1_v0_recru_arm_1][int_azi]='1' and  ([epimvr1_v4_iptisp4_arm_1][int_azi]='1' or [epivita_v5_iptisp5_arm_1][int_azi]='1') and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'", phase3_df, index='Group 2').fillna(0)
                    phase3_df['Phase'] = 'Phase 3'
            phase1_df= phase1_df.reset_index().groupby('index').sum(numeric_only=True)
            phase2_df= phase2_df.reset_index().groupby('index').sum(numeric_only=True)
            phase3_df= phase3_df.reset_index().groupby('index').sum(numeric_only=True)
            phase1_df['Phase'] = 'Phase 1'
            phase2_df['Phase'] = 'Phase 2'
            phase3_df['Phase'] = 'Phase 3'

            together = pd.concat([phase1_df,phase2_df,phase3_df]).reset_index()
            group1_df = together[together['index']=='Group 1'].set_index(('index'))
            group2_df = together[together['index']=='Group 2'].set_index(('index'))

            if proj in params.MAKENI_PROJECTS:
                group1_df_to_join =group1_df.reset_index(drop=True).set_index('Phase')
                for k,el in group1_df_to_join.T.items():
                    res = list()
                    for i in range(0, len(el)):
                        res.append(el[i]+group1_dict[k][i])
                    group1_dict[k] = res

            if proj in params.MAKENI_PROJECTS:
                group2_df_to_join = group2_df.reset_index(drop=True).set_index('Phase')
                for k, el in group2_df_to_join.T.items():
                    res = list()
                    for i in range(0, len(el)):
                        res.append(el[i] + group2_dict[k][i])
                    group2_dict[k] = res

            print("Groups Preparation . . . ")
            group1_group_df = MRS_T3_FUNCTIONS().groups_preparation_per_groups_t3(group1_df, params.HF_cohort_sample_size[proj][1], group1_expected, group_name='Group 1')
            group2_group_df = MRS_T3_FUNCTIONS().groups_preparation_per_groups_t3(group2_df, params.HF_cohort_sample_size[proj][2], group2_expected, group_name='Group 2')
            all_df = pd.concat([group1_group_df,group2_group_df])

            group1_group_no_exp_df = MRS_T3_FUNCTIONS().groups_preparation_no_exp_t3(group1_group_df)
            group2_group_no_exp_df = MRS_T3_FUNCTIONS().groups_preparation_no_exp_t3(group2_group_df)
            all_no_exp_df = pd.concat([group1_group_no_exp_df,group2_group_no_exp_df])

            print("Saving tables on Google Drive . . .")
            file_to_drive(proj, all_no_exp_df, tokens.drive_file_name_t3, tokens.drive_folder, index_included=False)
            file_to_drive(proj, all_df, tokens.drive_file_name_t3_expected, tokens.drive_folder, index_included=False)

            print("Done.\n")

        """MAKENI HFs"""
        print("Groups Preparation FOR MAKENI. . . ")
        expected_numbers = pd.read_excel(tokens.PATH_TO_EXPECTED_NUMBERS)
        proj_expected = expected_numbers[expected_numbers['HF'] == 'makeni'].T[2:].T
        group1_expected = proj_expected[proj_expected['Group'] == 'Group 1']
        group2_expected = proj_expected[proj_expected['Group'] == 'Group 2']

        group1_makeni_df = pd.DataFrame.from_dict(group1_dict)
        group1_makeni_df = group1_makeni_df.T.reset_index().rename(columns={0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 'index': 'Phase'})
        group1_makeni_df['index'] = 'group 1'
        group1_makeni_df = group1_makeni_df.set_index('index')[['A', 'B', 'C', 'D', 'E', 'F', 'Phase']]

        group2_makeni_df = pd.DataFrame.from_dict(group2_dict)
        group2_makeni_df = group2_makeni_df.T.reset_index().rename(columns={0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 'index': 'Phase'})
        group2_makeni_df['index'] = 'group 2'
        group2_makeni_df = group2_makeni_df.set_index('index')[['A', 'B', 'C', 'D', 'E', 'F', 'Phase']]

        print(group1_makeni_df)
        MAK_group1_group_df = MRS_T3_FUNCTIONS().groups_preparation_per_groups_t3(group1_makeni_df,params.HF_cohort_sample_size['makeni'][1],group1_expected, group_name='Group 1',makeni_A_compensation=True)
        print(MAK_group1_group_df)
        MAK_group2_group_df = MRS_T3_FUNCTIONS().groups_preparation_per_groups_t3(group2_makeni_df,params.HF_cohort_sample_size['makeni'][2],group2_expected, group_name='Group 2')
        all_MAK_df = pd.concat([MAK_group1_group_df, MAK_group2_group_df])
        MAK_group1_group_no_exp_df = MRS_T3_FUNCTIONS().groups_preparation_no_exp_t3(MAK_group1_group_df)
        MAK_group2_group_no_exp_df = MRS_T3_FUNCTIONS().groups_preparation_no_exp_t3(MAK_group2_group_df)
        MAK_all_no_exp_df = pd.concat([MAK_group1_group_no_exp_df, MAK_group2_group_no_exp_df])

        print("Saving tables on Google Drive . . .")
        file_to_drive('Bombali', MAK_all_no_exp_df, tokens.drive_file_name_t3, tokens.drive_folder, index_included=False)
        file_to_drive('Makeni', all_MAK_df, tokens.drive_file_name_t3_expected, tokens.drive_folder, index_included=False)

        print("Done.\n")


    def groups_preparation_no_exp_t3(self,group):
        df_to_compare = group[['Sample Size','A','B','C','D','E','F']].astype(int)
        to_set = pd.concat([group[['Group','Phase']].loc[[0,2,4]].reset_index(drop=True),df_to_compare.diff().loc[[1,3,5]].reset_index(drop=True)], axis=1)
        return to_set

    def groups_preparation_per_groups_t3(self, group, sample_size_group, expected, makeni_A_compensation=False):
        """
        This function works preparing the number of recruitments per group, joining all different subprojects if exist
        and obtaining only one row per project.
        """

        expected = expected[expected['Phase'] != 'Total exp']
        expected['Proportion']  = expected['Proportion'].astype(float)
        expected = expected.round({'Proportion':2})

        group = group.reset_index()
        total = group.groupby('index').sum(numeric_only=True).reset_index()
        total['Phase'] = "Total"

        if makeni_A_compensation:
            finish = False
            to_compensate = expected['A'][50]-group['A'][2]
            compensation = math.ceil(to_compensate/2)

            if ((group['B'][2] - expected['B'][50]) >= compensation and
                    (group['C'][2] - expected['C'][50]) >= compensation and
                    (group['D'][2] - expected['D'][50]) >= compensation and
                    (group['E'][2] - expected['E'][50]) >= compensation and
                    (group['F'][2] - expected['F'][50]) >= compensation):
                print('We already get the minimum number of participants, so please, stop the recruitment.')
                finish=True
            list_values = [(group['B'][2] - expected['B'][50])-to_compensate,(group['C'][2] - expected['C'][50])-to_compensate,
                           (group['D'][2] - expected['D'][50])-to_compensate,(group['E'][2] - expected['E'][50])-to_compensate,
                           (group['F'][2] - expected['F'][50])-to_compensate]
            count = 0
            for element in list_values:
                if element >= 0:
                    count+=1

            if count >= 4:
                print('4 of the 5 letters have the A number needed, the compensation should finish')
                finish = True

            if finish == False:
                expected.loc[50,'B'] += compensation
                expected.loc[50,'C'] += compensation
                expected.loc[50,'D'] += compensation
                expected.loc[50,'E'] += compensation
                expected.loc[50,'F'] += compensation
            else:
                pass
        group = group.set_index('Phase')
        sample_size = []

        for k in group.index:
            sample_size.append(group[['A', 'B', 'C', 'D', 'E', 'F']].T[k].sum())
        group['Sample Size'] = sample_size
        group['Proportion'] = ["%.2f" % (float(x) / (sample_size_group / 100)) for x in sample_size]
        group = group.reset_index().rename(columns={'index': 'Group'})
        group = pd.concat(
            [group.sort_index()[['Group', 'Phase', 'Proportion', 'Sample Size', 'A', 'B', 'C', 'D', 'E', 'F']],
             expected])
        group = group.sort_values('Phase').reset_index(drop=True)
        return group

    def list_of_candidates_t3(self,proj):
        """
        List of candidates to be recruited in T3. It is updated every 24h.
        :return:
        """
        print("LIST OF PARTICIPANTS for {}\n".format(proj))

        records_letter_g1 = pd.DataFrame()
        records_letter_g2 = pd.DataFrame()
        for project_key in tokens.REDCAP_PROJECTS_ICARIA:
            if proj in str(project_key) and project_key != 'HF16.01':

                print("\t\t[{}] Getting MRS records from {}...".format(datetime.now(), project_key))
                project = redcap.Project(tokens.URL, tokens.REDCAP_PROJECTS_ICARIA[project_key])
                df = project.export_records(format='df', fields=params.ALERT_LOGIC_FIELDS)

                # Cast child_dob column from str to date
                x = df.copy()
                x['child_dob'] = pd.to_datetime(x['child_dob'])
                dobs = x.groupby('record_id')['child_dob'].max()
                dobs = dobs[dobs.notnull()]

                print("\t\tFiltering <18 MoA and <2.5 months from the last Azi dose participants . . .")
                # Filter those participants who are about to turn to 18 months
                # First: Filter those older than 17 months oldº
                about_18m = dobs[dobs.apply(calculate_age_months) >= params.about_to_turn_18]
                if about_18m.size > 0:
                    today = datetime.today()
                    about_18m = about_18m[about_18m.apply(days_to_birthday, fu=18) < params.days_before_18]
                # Filter those childs with last azi dose > 2.5 months (75 days)
                less_than_75_days = x[x['int_azi']==1]
                less_than_75_days = less_than_75_days.reset_index()[['record_id','int_date']]
                gb = less_than_75_days.groupby('record_id')['int_date'].apply(np.max)
                less_than_75_days = []
                for k,el in gb.items():
                    days_from = datetime.today().replace(hour=0,minute=0,second=0, microsecond=0)  - datetime.strptime(el, "%Y-%m-%d %H:%M:%S").replace(hour=0,minute=0,second=0,microsecond=0)

                    if days_from.days < 76:
                        less_than_75_days.append(k)
                print("\t\tRemoving Finalized, Unreachable, death, withdrawal participants from the candidates list . . .\n")

                # Remove those participants who have already been visited for the end of the trial follow up
                finalized = x.query(
                    "redcap_event_name == 'hhat_18th_month_of_arm_1' and "
                    "redcap_repeat_instrument == 'household_follow_up' and "
                    "(hh_child_seen == 1 or phone_child_status == 1 or phone_child_status == 4 or hh_why_not_child_seen == 1 or  "
                    "hh_why_not_child_seen == 4 or hh_why_not_child_seen == 5)"
                )
                # Remove those unreachable participants
                unreachable = x.query(
                    "redcap_event_name == 'hhat_18th_month_of_arm_1' and "
                    "redcap_repeat_instrument == 'household_follow_up' and "
                    "reachable_status == 2")


                about_18m_not_seen = about_18m.index
                if less_than_75_days is not None:
                    about_18m_not_seen = about_18m_not_seen.difference(less_than_75_days)

                if finalized is not None:
                    record_ids_seen = finalized.index.get_level_values('record_id')
                    about_18m_not_seen = about_18m_not_seen.difference(record_ids_seen)
                if unreachable is not None:
                    records_unreachable = unreachable.index.get_level_values('record_id')
                    about_18m_not_seen = about_18m_not_seen.difference(records_unreachable)

                # Remove those death or withdrawal participants
                endfu = x.query("redcap_event_name == 'end_of_fu_arm_1'")
                if endfu is not None:
                    endfu = endfu[endfu['death_date'].notnull() | endfu['wdrawal_date'].notnull()]
                    records_endfu = endfu.index.get_level_values('record_id')
                    about_18m_not_seen = about_18m_not_seen.difference(records_endfu)

                # Removing participants who received a wrong azi/Pbo administration letter
                about_18m_not_seen = about_18m_not_seen.difference(tokens.not_recruitable_participants)

                ### GET GROUP 1 OR GROUP 2
                ## GROUP 2

                group2_df = project.export_records(format='df', fields=['int_date','int_azi'], filter_logic="[int_azi] ='1' and [int_date] !='' ")
                group2_df = group2_df.groupby('record_id')['int_azi'].count()
                group2_df = group2_df.reset_index().set_index('record_id')
                group2_record_ids = group2_df[group2_df['int_azi']>2].index.unique()

                about_18m_not_seen_g2 = []
                about_18m_not_seen_g1 = []
                for l in about_18m_not_seen:
                    if l in group2_record_ids:
                        about_18m_not_seen_g2.append(l)
                    else:
                        about_18m_not_seen_g1.append(l)
                records_letter_g1 = MRS_T3_FUNCTIONS().get_letters_from_candidates_t3(project, about_18m_not_seen_g1,records_letter_g1)
                records_letter_g2 = MRS_T3_FUNCTIONS().get_letters_from_candidates_t3(project, about_18m_not_seen_g2,records_letter_g2)


        print("\tCreating sheet DataFrame . . .")
        # In order to write into the Google Sheet, we need to determine all the space used to save it in a square matrix
        MRS_T3_FUNCTIONS().create_and_upload_sheet_drive(proj,records_letter_g1,'group1')
        MRS_T3_FUNCTIONS().create_and_upload_sheet_drive(proj,records_letter_g2,'group2')
        print ("\tDone.\n")


    def get_letters_from_candidates_t3(self, project, about_18m_not_seen, records_letter):
        if len(about_18m_not_seen) > 0:
            df_letters = project.export_records(
                format='df',
                records=list(about_18m_not_seen),
                fields=["study_number", "int_random_letter", "record_id"],
                filter_logic="[study_number] != '' and [event-name]='epipenta1_v0_recru_arm_1'"
            )
            # Group the study_numbers per letter
            print(about_18m_not_seen)
            print(df_letters)
            if records_letter.empty:
                records_letter = df_letters.groupby('int_random_letter')['study_number'].apply(list)
            else:
                # Group the study_numbers per letter for these projects with subprojects
                for k, el in df_letters.groupby('int_random_letter')['study_number'].apply(list).items():
                    for l in el:
                        try:
                            records_letter[k].append(l)
                        except:
                            records_letter[k] = []
                            records_letter[k].append(l)
        return records_letter

    def create_and_upload_sheet_drive(self,proj,records_letter,group):
        new_dict = {}
        max_size = 0
        #In order to write into the Google Sheet, we need to determine all the space used to save it in a square matrix
        for k, el in records_letter.items():
            if len(el) > max_size:
                max_size = len(el)

        # We add 30 more rows in order to delete all fields in case we had lots of old candidates
        max_size += 30
        for k, el in records_letter.items():
            new_dict[k] = list(el)
            for i in range(max_size - len(el)):
                new_dict[k].append("")

        blank_df = pd.DataFrame(index=np.arange(100), columns=['A', 'B', 'C', 'D', 'E', 'F'])
        dict_to_excel = pd.DataFrame(data=new_dict)
        entire_excel_sheet = pd.concat([dict_to_excel, blank_df], ignore_index=True)[['A', 'B', 'C', 'D', 'E', 'F']]
        sheet = proj + "." + group
        print(entire_excel_sheet.head())

        file_to_drive(sheet,entire_excel_sheet,tokens.dict_files_t3[proj],tokens.drive_folder,index_included=False)


def MRS_number_participants_uptodate():
    """
    This function gives the number of MRS participants up to date for each data point (Baseline, T2 or T3)

    :return: each dataset from each timepoint is saved in a different Gdrive document to be checked
    """
    cb = 0
    ct2 = 0
    ct3 = 0
    for pr in tokens.REDCAP_PROJECTS_ICARIA_ALL:
        print(pr)
        project = redcap.Project(tokens.URL, tokens.REDCAP_PROJECTS_ICARIA_ALL[pr])
        df = project.export_records(format='df', fields=params.LOGIC_FIELDS_MRS)
        df_t1 = project.export_records(format='df', fields=params.LOGIC_FIELDS_MRS_T1)

        # MRS BASELINE
        try:
            mrsb_df = df_t1.reset_index().set_index('record_id')[['mrs_study_number','nps_a_id','mrs_date']].dropna()
            if cb == 0:
                mrsb = mrsb_df.copy()
            else:
                mrsb = pd.concat([mrsb,mrsb_df])
            cb += 1
        except:
            pass

        # MRS T2
        try:
            mrs_t2_df = df.reset_index().set_index('record_id')[['mrs_study_number_t2','mrs_date_t2','mrs_t2_group']]
            mrs_t2_df = mrs_t2_df[mrs_t2_df['mrs_study_number_t2'].notnull()]#.dropna()
            if ct2 == 0:
                mrst2 = mrs_t2_df.copy()
            else:
                mrst2 = pd.concat([mrst2, mrs_t2_df])
            ct2 += 1
        except:
            pass

        # MRS T3
        try:
            mrs_t3_df = df.reset_index().set_index('record_id')[['mrs_study_number_t2_t3','mrs_date_t3','mrs_t2_group_t3']]#.dropna()
            mrs_t3_df = mrs_t3_df[mrs_t3_df['mrs_study_number_t2_t3'].notnull()]
            if ct3 == 0:
                mrst3 = mrs_t3_df.copy()
            else:
                mrst3 = pd.concat([mrst3, mrs_t3_df])
            ct3 += 1
        except:
            pass

    mrsb = mrsb.sort_values('mrs_date')
    mrst2 = mrst2.sort_values('mrs_date_t2')
    mrst3 = mrst3.sort_values('mrs_date_t3')

    file_to_drive('MRS Baseline', mrsb, tokens.drive_file_name_mrs_counts, tokens.drive_folder)
    file_to_drive('MRS T2', mrst2, tokens.drive_file_name_mrs_counts, tokens.drive_folder)
    file_to_drive('MRS T3', mrst3, tokens.drive_file_name_mrs_counts, tokens.drive_folder)
