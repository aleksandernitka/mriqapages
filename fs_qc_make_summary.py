# -*- coding: utf-8 -*-
"""
Run this after the freesurfers qa-tools.py, it will:
    - Create some auxillary plots with freeview
    - make html pages for all participants and 
"""

import os
import pandas as pd
import subprocess as sb


## CONSTANTS
# Where are the outputs of QA-tools.py
qadir = '/home/aleksander/Documents/fs_qa/fsqc_20220308/'
# Where are FS data
fadir = '/mnt/nasips/COST_mri/derivatives/freesurfer/'
# Where to put the html overview files
html = '/home/aleksander/Documents/fs_qa/fsqc_20220308/'


# read outputs
summary = pd.read_csv(os.path.join(qadir, 'qatools-results.csv'))
outl_aseg = pd.read_csv(os.path.join(qadir, 'outliers', 'all.aseg.stats'))
outl_norms = pd.read_csv(os.path.join(qadir, 'outliers', 'all.outliers.norms.stats'))
outl_sample_nonparam = pd.read_csv(os.path.join(qadir, 'outliers', 'all.outliers.sample.nonpar.stats'))
outl_sample_param = pd.read_csv(os.path.join(qadir, 'outliers', 'all.outliers.sample.param.stats'))


# TODO make some group wide plots
subs =[f for f in os.listdir(os.path.join(qadir, 'screenshots')) if 'sub-' in f]

# TODO single subject plots - with subproces
for s in subs:
    
    #Get folders
    ss_dir = os.path.join(fadir, s)
    #so_dir = os.path.join(qadir, 'screenshots', s)
    so_dir = os.path.join(qadir, 'test')
    
    # set freview commands + run
    for ori in ['axial', 'sagittal', 'coronal']:
        fw_cmd_tissue_separation = f"freeview -v {ss_dir}/mri/T1.mgz:grayscale=10,100 -f {ss_dir}/surf/lh.white:color=red:edgecolor=red -f {ss_dir}/surf/rh.white:color=red:edgecolor=red -f {ss_dir}/surf/lh.pial:color=white:edgecolor=white -f {ss_dir}/surf/rh.pial:color=white:edgecolor=white -layout 3 -viewport {ori} -ss {so_dir}/{s}_tissuessep_{ori}.png 3 1"
        fw_cmd_brain_extraction = f"freeview -v {ss_dir}/mri/T1.mgz:opacity=.6 -v {ss_dir}/mri/brain.mgz:opacity=.7:colormap=jet -layout 3 -viewport {ori} -ss {so_dir}/{s}_brainextract_{ori}.png 3 1"
        
        sb.call(fw_cmd_tissue_separation, shell=True)
        
# TODO make html pages for each participant

# summary table as html code
summary_html = summary.to_html()
# TODO replace sub-x with link to subjects page
text_file = open("summary.html", "w")
text_file.write(summary_html)
text_file.close()
