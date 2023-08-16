#!/usr/bin/env python
""" Python script to manage different components of the reporting of Serious Adverse Events (SAEs) in the ICARIA
Clinical Trial. These components are: (1) SAE numbering, etc."""

import params
import mrs

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

    #### MRS T2 SUMMARY TOOL ####
    mrs.MRS_T2_FUNCTIONS().mrs_t2_control_sheet()

    #### MRS T3 SUMMARY TOOL AND LIST OF T3 CANDIDATES ####
    for proj in params.PROJECTS:
        print("MRS T3 SUMMARY TOOL AND LIST OF T3 CANDIDATES for {}\n".format(proj))
        mrs.MRS_T3_FUNCTIONS().mrs_t3_summary_tool(proj)
     #   mrs.MRS_T3_FUNCTIONS().list_of_candidates_t3(proj)
    print("\nFINISHED!!")