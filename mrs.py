import pandas as pd
import tokens
import params
import tokens
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe

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

def export_records(project,project_key,fields_,filter_logic,final_df):
    try:
        df_mrs = project.export_records(format='df', fields=fields_,filter_logic=filter_logic)
        letters = get_letter_df(project, project_key, df_mrs)
        final_df = pd.concat([final_df, letters.T])
        print(final_df)
    except:
        noletters =pd.DataFrame(columns=['A','B','C','D','E','F'],index=[project_key])
        noletters.loc[project_key] = [0,0,0,0,0,0]
        final_df= pd.concat([final_df,noletters])
    return final_df

def get_letter_df(project, project_key,df_):
    record_ids = df_.index.get_level_values('record_id')
    df_letters = project.export_records(
        format='df',
        records=list(record_ids.drop_duplicates()),
        fields=["study_number", "int_random_letter"],
        filter_logic="[study_number] != ''"
    )
    records_letter = df_letters.groupby('int_random_letter')[['study_number']].count()
    records_letter = records_letter.rename(columns={'study_number': project_key.split(".")[0]})
    return records_letter

def groups_preparation(group,sample_size_group, expected):
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



def file_to_drive(worksheet,df,index_included=True):
    gc = gspread.oauth(tokens.path_credentials)
    sh = gc.open(title=tokens.drive_file_name,folder_id=tokens.drive_folder)
    set_with_dataframe(sh.worksheet(worksheet), df,include_index=index_included)
