import numpy as np
import pandas as pd
import tokens
import params
import tokens
import gspread
from datetime import datetime, date
from datetime import timedelta

from gspread_dataframe import get_as_dataframe, set_with_dataframe
import redcap

from dateutil.relativedelta import relativedelta


def expected_mrs():
    group1_expected = pd.DataFrame(index=['HF08 exp', 'HF11 exp', 'HF12 exp', 'HF16 exp','Total exp'],columns=['Proportion', 'Sample Size', 'A', 'B', 'C', 'D', 'E', 'F'])
    group2_expected = pd.DataFrame(index=['HF08 exp', 'HF11 exp', 'HF12 exp', 'HF16 exp','Total exp'],
                               columns=['Proportion', 'Sample Size', 'A', 'B', 'C', 'D', 'E', 'F'])
    group3_expected = pd.DataFrame(index=['HF08 exp', 'HF11 exp', 'HF12 exp', 'HF16 exp','Total exp'],
                               columns=['Proportion', 'Sample Size', 'A', 'B', 'C', 'D', 'E', 'F'])

    group1_expected.loc['HF08 exp'] = params.group1_magburaka
    group1_expected.loc['HF11 exp'] = params.group1_loreto
    group1_expected.loc['HF12 exp'] = params.group1_redcross
    group1_expected.loc['HF16 exp'] = params.group1_mgh
    group1_expected.loc['Total exp'] = params.total_group1

    group2_expected.loc['HF08 exp'] = params.group2_magburaka
    group2_expected.loc['HF11 exp'] = params.group2_loreto
    group2_expected.loc['HF12 exp'] = params.group2_redcross
    group2_expected.loc['HF16 exp'] = params.group2_mgh
    group2_expected.loc['Total exp'] = params.total_group2

    group3_expected.loc['HF08 exp'] = params.group3_magburaka
    group3_expected.loc['HF11 exp'] = params.group3_loreto
    group3_expected.loc['HF12 exp'] = params.group3_redcross
    group3_expected.loc['HF16 exp'] = params.group3_mgh
    group3_expected.loc['Total exp'] = params.total_group3


    return group1_expected,group2_expected,group3_expected

def export_records(project,project_key,fields_,filter_logic,final_df, index=False):
    if index == False:
        index = project_key
    try:
        df_mrs = project.export_records(format='df', fields=fields_,filter_logic=filter_logic)
        letters = get_letter_df(project, index, df_mrs)
        final_df = pd.concat([final_df, letters.T])
    except:
        noletters =pd.DataFrame(columns=['A','B','C','D','E','F'],index=[index])
        noletters.loc[index] = [0,0,0,0,0,0]
        final_df= pd.concat([final_df,noletters])
    return final_df

def get_letter_df(project, index,df_):
    record_ids = df_.index.get_level_values('record_id')
    df_letters = project.export_records(
        format='df',
        records=list(record_ids.drop_duplicates()),
        fields=["study_number", "int_random_letter"],
        filter_logic="[study_number] != ''"
    )
    records_letter = df_letters.groupby('int_random_letter')[['study_number']].count()
    records_letter = records_letter.rename(columns={'study_number': index.split(".")[0]})
    return records_letter

def groups_preparation(group,sample_size_group, expected):
    group = group.reset_index()
    group['index'] = group['index'].str.split(".").str[0]
    group = group.groupby('index').sum().astype(int)
    print(group)
    group1_total = [group['A'].sum(),group['B'].sum(),group['C'].sum(),group['D'].sum(),group['E'].sum(),group['F'].sum()]
    group.loc['Total'] = group1_total

    sample_size = []
    for k in group.index:
        sample_size.append(group.T[k].sum())
    group['Sample Size'] = sample_size
    group['Proportion'] = ["%.2f"%(x/(sample_size_group/100)) for x in sample_size]

    group = pd.concat([group,expected]).sort_index()[['Proportion','Sample Size','A','B','C','D','E','F']]

    return group



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






"""ONLY T3 FUNCTIONS """

def expected_mrs_t3(group_name):
    phase1_expected = pd.DataFrame(index=['Group 1 exp', 'Group 2 exp','Total exp'],columns=['Phase','Group','Proportion', 'Sample Size', 'A', 'B', 'C', 'D', 'E', 'F'])
    phase2_expected = pd.DataFrame(index=['Group 1 exp', 'Group 2 exp','Total exp'],columns=['Phase','Group','Proportion', 'Sample Size', 'A', 'B', 'C', 'D', 'E', 'F'])
    phase3_expected = pd.DataFrame(index=['Group 1 exp', 'Group 2 exp','Total exp'],columns=['Phase','Group','Proportion', 'Sample Size', 'A', 'B', 'C', 'D', 'E', 'F'])

    if group_name == 'HF08':
        phase1_expected.loc['Group 1 exp'] = ["Phase 1","Group 1 exp"] + params.HF08_p1_group1
        phase1_expected.loc['Group 2 exp'] = ["Phase 1","Group 2 exp"] + params.HF08_p1_group2
        phase1_expected.loc['Total exp'] = ["Phase 1","Total exp"] + params.HF08_p1_total

        phase2_expected.loc['Group 1 exp'] = ["Phase 2","Group 1 exp"] + params.HF08_p2_group1
        phase2_expected.loc['Group 2 exp'] = ["Phase 2","Group 2 exp"] + params.HF08_p2_group2
        phase2_expected.loc['Total exp'] = ["Phase 2","Total exp"] + params.HF08_p2_total

        phase3_expected.loc['Group 1 exp'] = ["Phase 1","Group 1 exp"] + params.HF08_p3_group1
        phase3_expected.loc['Group 2 exp'] = ["Phase 2","Group 2 exp"] + params.HF08_p3_group2
        phase3_expected.loc['Total exp'] = ["Phase 3","Total exp"] + params.HF08_p3_total

    elif group_name == 'MAKENI':
        phase1_expected.loc['Group 1 exp'] = ["Phase 1","Group 1 exp"] + params.MAK_p1_group1
        phase1_expected.loc['Group 2 exp'] = ["Phase 1","Group 2 exp"] + params.MAK_p1_group2
        phase1_expected.loc['Total exp'] = ["Phase 1","Total exp"] + params.MAK_p1_total

        phase2_expected.loc['Group 1 exp'] = ["Phase 2","Group 1 exp"] + params.MAK_p2_group1
        phase2_expected.loc['Group 2 exp'] = ["Phase 2","Group 2 exp"] + params.MAK_p2_group2
        phase2_expected.loc['Total exp'] = ["Phase 2","Total exp"] + params.MAK_p2_total

        phase3_expected.loc['Group 1 exp'] = ["Phase 1","Group 1 exp"] + params.MAK_p3_group1
        phase3_expected.loc['Group 2 exp'] = ["Phase 2","Group 2 exp"] + params.MAK_p3_group2
        phase3_expected.loc['Total exp'] = ["Phase 3","Total exp"] + params.MAK_p3_total


    print(phase1_expected)


    return phase1_expected,phase2_expected,phase3_expected


def groups_preparation_t3(group,sample_size_group, expected,group_name):

#    print(group.groupby(level=0).sum())
    group = group.reset_index()
    group['index'] = group['index'].str.split(".").str[0]
    group = group.groupby('index').sum().astype(int)
 #   print(group)
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



### LIST OF CANDIDATES

def drive_candidates_list(group_projects, name_group):
    for project_key in tokens.REDCAP_PROJECTS_ICARIA:
        if name_group in str(project_key):

            print("[{}] Getting MRS records from {}...".format(datetime.now(), project_key))
            project = redcap.Project(tokens.URL, tokens.REDCAP_PROJECTS_ICARIA[project_key])
            df = project.export_records(format='df', fields=params.ALERT_LOGIC_FIELDS)

            # Cast child_dob column from str to date
            x = df.copy()
            x['child_dob'] = pd.to_datetime(x['child_dob'])
            dobs = x.groupby('record_id')['child_dob'].max()
            dobs = dobs[dobs.notnull()]
            # Filter those participants who are about to turn to 18 months
            # First: Filter those older than 17 months old

            about_18m = dobs[dobs.apply(calculate_age_months) >= params.about_to_turn_18]
            if about_18m.size > 0:
                about_18m = about_18m[about_18m.apply(days_to_birthday, fu=18) < params.days_before_18]

            less_than_75_days = x[x['int_azi']==1]
            less_than_75_days = less_than_75_days.reset_index()[['record_id','int_date']]
 #           print(less_than_75_days)
            gb = less_than_75_days.groupby('record_id')['int_date'].apply(np.max)
#            print(gb)

            less_than_75_days = []
            for k,el in gb.items():
                days_from = datetime.today() - datetime.strptime(el, "%Y-%m-%d %H:%M:%S")

                if days_from.days < 76:
                    less_than_75_days.append(k)

            print(less_than_75_days)
                # Remove those participants who have already been visited and seen at home for the end of the trial follow up
            finalized = x.query(
                "redcap_event_name == 'hhat_18th_month_of_arm_1' and "
                "redcap_repeat_instrument == 'household_follow_up' and "
                "(hh_child_seen == 1 or phone_child_status == 1 or phone_child_status == 4 or hh_why_not_child_seen == 1 or  "
                "hh_why_not_child_seen == 4 or hh_why_not_child_seen == 5)"
            )
            unreachable = x.query(
                "redcap_event_name == 'hhat_18th_month_of_arm_1' and "
                "redcap_repeat_instrument == 'household_follow_up' and "
                "reachable_status == 2")

            endfu = x.query(
                "redcap_event_name == 'end_of_fu_arm_1'"
            )
            print(endfu[endfu['death_reported_date'].notnull() | endfu['wdrawal_reported_date'].notnull()][['wdrawal_reported_date', 'death_reported_date']])


            about_18m_not_seen = about_18m.index
            record_ids_seen = None
            records_unreachable = None

            if less_than_75_days is not None:
                about_18m_not_seen = about_18m_not_seen.difference(less_than_75_days)

            if finalized is not None:
                record_ids_seen = finalized.index.get_level_values('record_id')
                about_18m_not_seen = about_18m_not_seen.difference(record_ids_seen)
            if unreachable is not None:
                records_unreachable = unreachable.index.get_level_values('record_id')
                about_18m_not_seen = about_18m_not_seen.difference(records_unreachable)
            print(about_18m_not_seen)
            if endfu is not None:
                records_endfu = endfu.index.get_level_values('record_id')
                about_18m_not_seen = about_18m_not_seen.difference(records_endfu)
            print(about_18m_not_seen)

            xres = df.reset_index()
            about_18m_study_numbers = xres[xres['record_id'].isin(list(about_18m_not_seen))][['study_number']]
            about_18m_study_numbers = about_18m_study_numbers.dropna()
            if len(about_18m_not_seen) > 0:
                df_letters = project.export_records(
                    format='df',
                    records=list(about_18m_not_seen.drop_duplicates()),
                    fields=["study_number", "int_random_letter","record_id"],
                    filter_logic="[study_number] != '' and [event-name]='epipenta1_v0_recru_arm_1'"
                )
                records_letter = df_letters.groupby('int_random_letter')['study_number'].apply(list)

    new_dict = {}
    max_size = 0
    for k, el in records_letter.items():
        if len(el) > max_size:
            max_size = len(el)
#    print(max_size)

    for k, el in records_letter.items():
        new_dict[k] = list(el)

        for i in range(max_size - len(el)):
            new_dict[k].append("")

    blank_df = pd.DataFrame(index=np.arange(100),columns=['A','B','C','D','E','F'])
    dict_to_excel = pd.DataFrame(data=new_dict)
    entire_excel_sheet = pd.concat([dict_to_excel,blank_df],ignore_index=True)[['A','B','C','D','E','F']]

    print(name_group,entire_excel_sheet,tokens.drive_candidates_name_t3,tokens.drive_folder)
    file_to_drive(name_group,entire_excel_sheet,tokens.drive_candidates_name_t3,tokens.drive_folder,index_included=False)
