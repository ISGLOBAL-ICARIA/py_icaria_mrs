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
    mrs.file_to_drive('Phase 1',group1_df)
    mrs.file_to_drive('Phase 2',group2_df)
    mrs.file_to_drive('Phase 3',group3_df)
    print ("DONE\n")

