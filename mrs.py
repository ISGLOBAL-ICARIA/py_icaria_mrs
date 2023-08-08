import numpy as np
import pandas as pd

import params
import tokens
import gspread
from datetime import datetime

from gspread_dataframe import set_with_dataframe
import redcap

from dateutil.relativedelta import relativedelta


def file_to_drive(worksheet,df,drive_file_name,folder_id,index_included=True):
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

def export_records(project,project_key,fields_,filter_logic,final_df, index=False):
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
        letters = df_letters.groupby('int_random_letter')[['study_number']].count()
        letters = letters.rename(columns={'study_number': index.split(".")[0]})


        final_df = pd.concat([final_df, letters.T])
    except:
        noletters =pd.DataFrame(columns=['A','B','C','D','E','F'],index=[index])
        noletters.loc[index] = [0,0,0,0,0,0]
        final_df= pd.concat([final_df,noletters])
    return final_df


class MRS_T2_FUNCTIONS:
    """
    T2 Project functions
    """

    def __init__(self):
        pass

    def mrs_t2_control_sheet(self):
        # Expected number of recruitments per Phase in MRS T2
        print("\nMRS T2 SUMMARY TOOL\n")
        print("Extracting expected number of recruitments per HF and letter . . .")
        phase1_expected, phase2_expected,phase3_expected = MRS_T2_FUNCTIONS().expected_mrs_t2()
        phase1_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])
        phase2_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])
        phase3_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])

        for project_key in tokens.REDCAP_PROJECTS_ICARIA:
            print("[{}] Getting MRS records from {}...".format(datetime.now(), project_key))
            project = redcap.Project(tokens.URL, tokens.REDCAP_PROJECTS_ICARIA[project_key])

            if project_key not in ['HF13','HF17']:
                phase1_df = export_records(project,project_key,['mrs_study_number_t2'],"([mrs_study_number_t2]!='' or [mrs_t2_photo_labels]!='') and [mrs_nasophar_swab_a_t2]='1' and [mrs_nasophar_swab_b_t2]='1' and [mrs_rectal_swab_t2]='1' and [mrs_t2_group]='1'",phase1_df).fillna(0)
                phase2_df = export_records(project,project_key,['mrs_study_number_t2'],"([mrs_study_number_t2]!='' or [mrs_t2_photo_labels]!='')  and [mrs_nasophar_swab_a_t2]='1' and [mrs_rectal_swab_t2]='1' and [mrs_t2_group]='2'",phase2_df).fillna(0)
            phase3_df = export_records(project,project_key,['mrs_study_number_t2'],"([mrs_study_number_t2]!='' or [mrs_t2_photo_labels]!='')  and [mrs_nasophar_swab_a_t2]='1' and [mrs_t2_group]='3'",phase3_df).fillna(0)

        print ("Groups Preparation . . . ")

        phase1_df = MRS_T2_FUNCTIONS().groups_preparation_t2(phase1_df, params.phase1_sample_size,phase1_expected)
        phase2_df = MRS_T2_FUNCTIONS().groups_preparation_t2(phase2_df, params.phase2_sample_size,phase2_expected)
        phase3_df = MRS_T2_FUNCTIONS().groups_preparation_t2(phase3_df, params.phase3_sample_size,phase3_expected)

        print("Saving tables on Google Drive . . .")

        file_to_drive('Phase 1',phase1_df,tokens.drive_file_name_t2,tokens.drive_folder)
        file_to_drive('Phase 2',phase2_df,tokens.drive_file_name_t2,tokens.drive_folder)
        file_to_drive('Phase 3',phase3_df,tokens.drive_file_name_t2,tokens.drive_folder)
        print ("\nFINISHED.\n")

    def expected_mrs_t2(self):
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

        print("SUMMARY TOOL for {}\n".format(proj))

        expected_numbers = pd.read_excel(tokens.PATH_TO_EXPECTED_NUMBERS)
        proj_expected = expected_numbers[expected_numbers['HF'] == proj].T[2:].T
        phase1_expected = proj_expected[proj_expected['Phase'] == 'Phase 1']
        phase2_expected = proj_expected[proj_expected['Phase'] == 'Phase 2']
        phase3_expected = proj_expected[proj_expected['Phase'] == 'Phase 3']

        phase1_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])
        phase2_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])
        phase3_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])

        for subproj in tokens.REDCAP_PROJECTS_ICARIA:
            if str(proj) in str(subproj):
                print("[{}] Getting MRS records from {}...".format(datetime.now(), subproj))
                project = redcap.Project(tokens.URL, tokens.REDCAP_PROJECTS_ICARIA[subproj])

                phase1_df = export_records(project, subproj, ['mrs_study_number_t2_t3'], "([mrs_study_number_t2_t3]!='') and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_nasophar_swab_b_t2_t3]='1' and [mrs_rectal_swab_t2_t3]='1' and [mrs_t2_group_t3]='1' and [epipenta1_v0_recru_arm_1][int_azi]='1' and (([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]!='1') or ([epimvr1_v4_iptisp4_arm_1][int_azi]='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]!='1') or ([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'))", phase1_df, index='Group 1').fillna(0)
                phase1_df = export_records(project, subproj, ['mrs_study_number_t2_t3'], "([mrs_study_number_t2_t3]!='') and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_nasophar_swab_b_t2_t3]='1' and [mrs_rectal_swab_t2_t3]='1' and [mrs_t2_group_t3]='1' and [epipenta1_v0_recru_arm_1][int_azi]='1' and [epimvr1_v4_iptisp4_arm_1][int_azi]='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'", phase1_df, index='Group 2').fillna(0)
                phase1_df['Phase'] = 'Phase 1'
                phase2_df = export_records(project, subproj, ['mrs_study_number_t2_t3'], "([mrs_study_number_t2_t3]!='')  and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_rectal_swab_t2_t3]='1' and [mrs_t2_group_t3]='2' and [epipenta1_v0_recru_arm_1][int_azi]='1' and (([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]!='1') or ([epimvr1_v4_iptisp4_arm_1][int_azi]='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]!='1') or ([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'))", phase2_df, index='Group 1').fillna(0)
                phase2_df = export_records(project, subproj, ['mrs_study_number_t2_t3'], "([mrs_study_number_t2_t3]!='')  and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_rectal_swab_t2_t3]='1' and [mrs_t2_group_t3]='2' and [epipenta1_v0_recru_arm_1][int_azi]='1' and [epimvr1_v4_iptisp4_arm_1][int_azi]='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'", phase2_df, index='Group 2').fillna(0)
                phase2_df['Phase'] = 'Phase 2'
                phase3_df = export_records(project, subproj, ['mrs_study_number_t2_t3'], "([mrs_study_number_t2_t3]!='')  and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_t2_group_t3]='3' and [epipenta1_v0_recru_arm_1][int_azi]='1' and (([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]!='1') or ([epimvr1_v4_iptisp4_arm_1][int_azi]='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]!='1') or ([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'))", phase3_df, index='Group 1').fillna(0)
                phase3_df = export_records(project, subproj, ['mrs_study_number_t2_t3'], "([mrs_study_number_t2_t3]!='') and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_t2_group_t3]='3' and [epipenta1_v0_recru_arm_1][int_azi]='1' and [epimvr1_v4_iptisp4_arm_1][int_azi]='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'", phase3_df, index='Group 2').fillna(0)
                phase3_df['Phase'] = 'Phase 3'

        print("Groups Preparation . . . ")

        phase1_group_df = MRS_T3_FUNCTIONS().groups_preparation_t3(phase1_df, params.HF_cohort_sample_size[proj][1], phase1_expected, group_name='Phase 1')
        phase2_group_df = MRS_T3_FUNCTIONS().groups_preparation_t3(phase2_df, params.HF_cohort_sample_size[proj][2], phase2_expected, group_name='Phase 2')
        phase3_group_df = MRS_T3_FUNCTIONS().groups_preparation_t3(phase3_df, params.HF_cohort_sample_size[proj][3], phase3_expected, group_name='Phase 3')
        all_df = pd.concat([phase1_group_df, phase2_group_df, phase3_group_df])

        print("Saving tables on Google Drive . . .")
         file_to_drive(proj, all_df, tokens.drive_file_name_t3, tokens.drive_folder, index_included=False)

        print("Done.\n")

    def groups_preparation_t3(self,group,sample_size_group, expected,group_name):
        group = group.reset_index()
        group['index'] = group['index'].str.split(".").str[0]
        group = group.groupby('index').sum(numeric_only=True)
        ##group = group.groupby('index').sum().astype(int) ## OLD VERSION THAT GIVES A FUTUREWARNING ADVICE

        group1_total = [group['A'].sum(),group['B'].sum(),group['C'].sum(),group['D'].sum(),group['E'].sum(),group['F'].sum()]
        group.loc['Total'] = group1_total

        sample_size = []
        for k in group.index:
            sample_size.append(group.T[k].sum())
        group['Sample Size'] = sample_size
        group['Proportion'] = ["%.2f"%(x/(sample_size_group/100)) for x in sample_size]

        group['Phase'] = group_name
        group['Group'] = group.index
        #print(group.sort_index()[['Phase','Group','Proportion','Sample Size','A','B','C','D','E','F'])
        #print(expected)
        group = pd.concat([group.sort_index()[['Phase','Group','Proportion','Sample Size','A','B','C','D','E','F']],expected])
        group = group.sort_values('Group').reset_index(drop=True)
        #print(group)

        return group


    def list_of_candidates_t3(self,proj):

        print("LIST OF PARTICIPANTS for {}\n".format(proj))

        records_letter = pd.DataFrame()
        for project_key in tokens.REDCAP_PROJECTS_ICARIA:
            if proj in str(project_key):

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
                # First: Filter those older than 17 months old
                about_18m = dobs[dobs.apply(calculate_age_months) >= params.about_to_turn_18]
                if about_18m.size > 0:
                    about_18m = about_18m[about_18m.apply(days_to_birthday, fu=18) < params.days_before_18]

                # Filter those childs with last azi dose > 2.5 months (75 days)
                less_than_75_days = x[x['int_azi']==1]
                less_than_75_days = less_than_75_days.reset_index()[['record_id','int_date']]
                gb = less_than_75_days.groupby('record_id')['int_date'].apply(np.max)
                less_than_75_days = []
                for k,el in gb.items():
                    days_from = datetime.today() - datetime.strptime(el, "%Y-%m-%d %H:%M:%S")

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

                if len(about_18m_not_seen) > 0:
                    df_letters = project.export_records(
                        format='df',
                        records=list(about_18m_not_seen.drop_duplicates()),
                        fields=["study_number", "int_random_letter","record_id"],
                        filter_logic="[study_number] != '' and [event-name]='epipenta1_v0_recru_arm_1'"
                    )
                    # Group the study_numbers per letter
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

        print("\tCreating sheet DataFrame . . .")
        # In order to write into the Google Sheet, we need to determine all the space used to save it in a square matrix
        new_dict = {}
        max_size = 0
        for k, el in records_letter.items():
            if len(el) > max_size:
                max_size = len(el)

        # We add 30 more rows in order to delete all fields in case we had lots of old candidates
        max_size += 30
        for k, el in records_letter.items():
            new_dict[k] = list(el)
            for i in range(max_size - len(el)):
                new_dict[k].append("")

        blank_df = pd.DataFrame(index=np.arange(100),columns=['A','B','C','D','E','F'])
        dict_to_excel = pd.DataFrame(data=new_dict)
        entire_excel_sheet = pd.concat([dict_to_excel,blank_df],ignore_index=True)[['A','B','C','D','E','F']]
        #print(entire_excel_sheet.head())

        print("\tSaving sheet on Google Drive . . .")

        file_to_drive(proj,entire_excel_sheet,tokens.drive_candidates_name_t3,tokens.drive_folder,index_included=False)
        print ("\tDone.\n")

