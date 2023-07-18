#!/usr/bin/env python
""" Python script to manage different components of the reporting of Serious Adverse Events (SAEs) in the ICARIA
Clinical Trial. These components are: (1) SAE numbering, etc."""

import pandas as pd
import redcap
import params
import tokens
import mrs
from datetime import datetime

__author__ = "Andreu Bofill Pumarola"
__copyright__ = "Copyright 2023, ISGlobal Maternal, Child and Reproductive Health"
__credits__ = ["Andreu Bofill Pumarola"]
__license__ = "MIT"
__version__ = "0.0.1"
__date__ = "20230523"
__maintainer__ = "Andreu Bofill"
__email__ = "andreu.bofill@isglobal.org"
__status__ = "Dev"

if __name__ == '__main__':

    #### MRS T2 ####
    PROJECTS = tokens.REDCAP_PROJECTS_ICARIA
    group1_expected, group2_expected,group3_expected = mrs.expected_mrs()

    group1_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])
    group2_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])
    group3_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])
    for project_key in PROJECTS:

        print("[{}] Getting MRS records from {}...".format(datetime.now(), project_key))

        project = redcap.Project(tokens.URL, tokens.REDCAP_PROJECTS_ICARIA[project_key])
        group1_df = mrs.export_records(project,project_key,['mrs_study_number_t2'],"([mrs_study_number_t2]!='' or [mrs_t2_photo_labels]!='') and [mrs_nasophar_swab_a_t2]='1' and [mrs_nasophar_swab_b_t2]='1' and [mrs_rectal_swab_t2]='1' and [mrs_t2_group]='1'",group1_df).fillna(0)
        group2_df = mrs.export_records(project,project_key,['mrs_study_number_t2'],"([mrs_study_number_t2]!='' or [mrs_t2_photo_labels]!='')  and [mrs_nasophar_swab_a_t2]='1' and [mrs_rectal_swab_t2]='1' and [mrs_t2_group]='2'",group2_df).fillna(0)
        group3_df = mrs.export_records(project,project_key,['mrs_study_number_t2'],"([mrs_study_number_t2]!='' or [mrs_t2_photo_labels]!='')  and [mrs_nasophar_swab_a_t2]='1' and [mrs_t2_group]='3'",group3_df).fillna(0)

    print ("Groups Preparation . . . ")
    group1_df = mrs.groups_preparation(group1_df,params.group1_sample_size,group1_expected)
    group2_df = mrs.groups_preparation(group2_df, params.group2_sample_size,group2_expected)
    group3_df = mrs.groups_preparation(group3_df, params.group3_sample_size,group3_expected)
    print("Saving tables on Google Drive . . .")
    mrs.file_to_drive('Phase 1',group1_df,tokens.drive_file_name_t2,tokens.drive_folder)
    mrs.file_to_drive('Phase 2',group2_df,tokens.drive_file_name_t2,tokens.drive_folder)
    mrs.file_to_drive('Phase 3',group3_df,tokens.drive_file_name_t2,tokens.drive_folder)
    print ("DONE\n")





    #### MRS T3 ####

    print ("MRS T3\n")

    PROJECTS = tokens.REDCAP_PROJECTS_ICARIA


    MAG_phase1_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])
    MAG_phase2_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])
    MAG_phase3_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])
    MAK_phase1_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])
    MAK_phase2_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])
    MAK_phase3_df = pd.DataFrame(columns=['A', 'B', 'C', 'D', 'E', 'F'])


    MAG_phase1_expected, MAG_phase2_expected,MAG_phase3_expected = mrs.expected_mrs_t3(group_name='MAGBURAKA')
    MAK_phase1_expected, MAK_phase2_expected,MAK_phase3_expected = mrs.expected_mrs_t3(group_name='MAKENI')
    for project_key in tokens.REDCAP_PROJECTS_MAGBURAKA:
        print("[{}] Getting MRS records from {}...".format(datetime.now(), project_key))

        project = redcap.Project(tokens.URL, tokens.REDCAP_PROJECTS_MAGBURAKA[project_key])
        MAG_phase1_df = mrs.export_records(project,project_key,['mrs_study_number_t2_t3'],"([mrs_study_number_t2_t3]!='') and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_nasophar_swab_b_t2_t3]='1' and [mrs_rectal_swab_t2_t3]='1' and [mrs_t2_group_t3]='1' and [epipenta1_v0_recru_arm_1][int_azi]='1' and (([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]!='1') or ([epimvr1_v4_iptisp4_arm_1][int_azi]='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]!='1') or ([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'))",MAG_phase1_df,index='Group 1').fillna(0)
        MAG_phase1_df = mrs.export_records(project,project_key,['mrs_study_number_t2_t3'],"([mrs_study_number_t2_t3]!='') and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_nasophar_swab_b_t2_t3]='1' and [mrs_rectal_swab_t2_t3]='1' and [mrs_t2_group_t3]='1' and [epipenta1_v0_recru_arm_1][int_azi]='1' and [epimvr1_v4_iptisp4_arm_1][int_azi]='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'",MAG_phase1_df,index='Group 2').fillna(0)
        MAG_phase1_df['Phase'] = 'Phase 1'
        MAG_phase2_df = mrs.export_records(project,project_key,['mrs_study_number_t2_t3'],"([mrs_study_number_t2_t3]!='')  and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_rectal_swab_t2_t3]='1' and [mrs_t2_group_t3]='2' and [epipenta1_v0_recru_arm_1][int_azi]='1' and (([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]!='1') or ([epimvr1_v4_iptisp4_arm_1][int_azi]='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]!='1') or ([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'))",MAG_phase2_df,index='Group 1').fillna(0)
        MAG_phase2_df = mrs.export_records(project,project_key,['mrs_study_number_t2_t3'],"([mrs_study_number_t2_t3]!='')  and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_rectal_swab_t2_t3]='1' and [mrs_t2_group_t3]='2' and [epipenta1_v0_recru_arm_1][int_azi]='1' and [epimvr1_v4_iptisp4_arm_1][int_azi]='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'",MAG_phase2_df,index='Group 2').fillna(0)
        MAG_phase2_df['Phase'] = 'Phase 2'

        MAG_phase3_df = mrs.export_records(project,project_key,['mrs_study_number_t2_t3'],"([mrs_study_number_t2_t3]!='')  and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_t2_group_t3]='3' and [epipenta1_v0_recru_arm_1][int_azi]='1' and (([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]!='1') or ([epimvr1_v4_iptisp4_arm_1][int_azi]='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]!='1') or ([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'))",MAG_phase3_df,index='Group 1').fillna(0)
        MAG_phase3_df = mrs.export_records(project,project_key,['mrs_study_number_t2_t3'],"([mrs_study_number_t2_t3]!='') and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_t2_group_t3]='3' and [epipenta1_v0_recru_arm_1][int_azi]='1' and [epimvr1_v4_iptisp4_arm_1][int_azi]='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'",MAG_phase3_df,index='Group 2').fillna(0)
        MAG_phase3_df['Phase'] = 'Phase 3'

    for project_key in tokens.REDCAP_PROJECTS_MAKENI:
        print("[{}] Getting MRS records from {}...".format(datetime.now(), project_key))

        project = redcap.Project(tokens.URL, tokens.REDCAP_PROJECTS_MAKENI[project_key])
        MAK_phase1_df = mrs.export_records(project, project_key, ['mrs_study_number_t2_t3'],"([mrs_study_number_t2_t3]!='') and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_nasophar_swab_b_t2_t3]='1' and [mrs_rectal_swab_t2_t3]='1' and [mrs_t2_group_t3]='1' and [epipenta1_v0_recru_arm_1][int_azi]='1' and (([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]!='1') or ([epimvr1_v4_iptisp4_arm_1][int_azi]='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]!='1') or ([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'))",MAK_phase1_df, index='Group 1').fillna(0)
        MAK_phase1_df = mrs.export_records(project, project_key, ['mrs_study_number_t2_t3'],"([mrs_study_number_t2_t3]!='') and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_nasophar_swab_b_t2_t3]='1' and [mrs_rectal_swab_t2_t3]='1' and [mrs_t2_group_t3]='1' and [epipenta1_v0_recru_arm_1][int_azi]='1' and [epimvr1_v4_iptisp4_arm_1][int_azi]='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'",MAK_phase1_df, index='Group 2').fillna(0)
        MAK_phase1_df['Phase'] = 'Phase 1'
        MAK_phase2_df = mrs.export_records(project, project_key, ['mrs_study_number_t2_t3'],"([mrs_study_number_t2_t3]!='')  and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_rectal_swab_t2_t3]='1' and [mrs_t2_group_t3]='2' and [epipenta1_v0_recru_arm_1][int_azi]='1' and (([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]!='1') or ([epimvr1_v4_iptisp4_arm_1][int_azi]='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]!='1') or ([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'))",MAK_phase2_df, index='Group 1').fillna(0)
        MAK_phase2_df = mrs.export_records(project, project_key, ['mrs_study_number_t2_t3'],"([mrs_study_number_t2_t3]!='')  and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_rectal_swab_t2_t3]='1' and [mrs_t2_group_t3]='2' and [epipenta1_v0_recru_arm_1][int_azi]='1' and [epimvr1_v4_iptisp4_arm_1][int_azi]='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'",MAK_phase2_df, index='Group 2').fillna(0)
        MAK_phase2_df['Phase'] = 'Phase 2'
        MAK_phase3_df = mrs.export_records(project, project_key, ['mrs_study_number_t2_t3'],"([mrs_study_number_t2_t3]!='')  and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_t2_group_t3]='3' and [epipenta1_v0_recru_arm_1][int_azi]='1' and (([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]!='1') or ([epimvr1_v4_iptisp4_arm_1][int_azi]='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]!='1') or ([epimvr1_v4_iptisp4_arm_1][int_azi]!='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'))",MAK_phase3_df, index='Group 1').fillna(0)
        MAK_phase3_df = mrs.export_records(project, project_key, ['mrs_study_number_t2_t3'],"([mrs_study_number_t2_t3]!='') and [mrs_nasophar_swab_a_t2_t3]='1' and [mrs_t2_group_t3]='3' and [epipenta1_v0_recru_arm_1][int_azi]='1' and [epimvr1_v4_iptisp4_arm_1][int_azi]='1' and [epimvr2_v6_iptisp6_arm_1][int_azi]='1'",MAK_phase3_df, index='Group 2').fillna(0)
        MAK_phase3_df['Phase'] = 'Phase 3'

    print("Groups Preparation . . . ")

    MAG_phase1_group_df = mrs.groups_preparation_t3(MAG_phase1_df, params.MAG_phase1_sample_size, MAG_phase1_expected, group_name='Phase 1')
    MAG_phase2_group_df = mrs.groups_preparation_t3(MAG_phase2_df, params.MAG_phase2_sample_size, MAG_phase2_expected, group_name='Phase 2')
    MAG_phase3_group_df = mrs.groups_preparation_t3(MAG_phase3_df, params.MAG_phase3_sample_size, MAG_phase3_expected, group_name='Phase 3')
    MAG_all_df = pd.concat([MAG_phase1_group_df,MAG_phase2_group_df,MAG_phase3_group_df])

    MAK_phase1_group_df = mrs.groups_preparation_t3(MAK_phase1_df, params.MAK_phase1_sample_size, MAK_phase1_expected, group_name='Phase 1')
    MAK_phase2_group_df = mrs.groups_preparation_t3(MAK_phase2_df, params.MAK_phase2_sample_size, MAK_phase2_expected, group_name='Phase 2')
    MAK_phase3_group_df = mrs.groups_preparation_t3(MAK_phase3_df, params.MAK_phase3_sample_size, MAK_phase3_expected, group_name='Phase 3')
    MAK_all_df = pd.concat([MAK_phase1_group_df,MAK_phase2_group_df,MAK_phase3_group_df])

    print("MAGBURAKA SUMMARY")
    print(MAG_all_df.reset_index(drop=True))
    print("MAKENI SUMMARY")
    print(MAK_all_df.reset_index(drop=True))

    print("Saving tables on Google Drive . . .")
    mrs.file_to_drive('MAGBURAKA',MAG_all_df,tokens.drive_file_name_t3,tokens.drive_folder,index_included=False)
    mrs.file_to_drive('MAKENI',MAK_all_df,tokens.drive_file_name_t3,tokens.drive_folder,index_included=False)


    print ("DONE\n")



    print ("LIST OF PARTCIPANTS\n")
    mrs.drive_candidates_list(tokens.REDCAP_PROJECTS_MAGBURAKA,'Magburaka')
    mrs.drive_candidates_list(tokens.REDCAP_PROJECTS_MAKENI ,'Makeni')

