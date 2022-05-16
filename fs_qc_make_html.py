#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
After running qa module of freesurfer the remaining files should be put into something that is easy to view

This takes care of building page per each participant in qa processed dir. Furhtermore, the numerical output is laoded and put converted to a series of interactive plotsax 

Created on Mon Mar 28 12:49:05 2022

@author: aleksander
"""

import os
import datetime as dt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# DIRS
dir_fsqa = '/home/aleksander/Documents/fs_qa/fsqc_20220328/'
dir_fsqa_fornix = os.path.join(dir_fsqa, 'fornix')
dir_fsqa_screen = os.path.join(dir_fsqa, 'screenshots')
dir_fsqa_outlrs = os.path.join(dir_fsqa, 'outliers')

dir_mainqa = '/home/aleksander/Documents/fs_qa/qaPages/'
dir_subs_fs = os.path.join(dir_mainqa, 'fs')
dir_qa_plts = os.path.join(dir_mainqa, 'plts')

# PAGES
#sub = 0 # init so that f string is not complaining
web_main = os.path.join(dir_mainqa, 'index.html')
web_main_fs = os.path.join(dir_mainqa, 'freesurfer-template.html')
web_temp_fs = os.path.join(dir_mainqa, 'fs_sub-template.html')

# Load subject level html template
fs_sub_tmpl = open(web_temp_fs, 'r')
shtml = fs_sub_tmpl.read()
fs_sub_tmpl.close()

# Load main fs
fs_main = open(web_main_fs, 'r')
mhtml = fs_main.read()
fs_main.close()

#### === FREESURFER DATA QA === ###


# load aseg stats and other
aseg_stats = pd.read_csv(os.path.join(dir_fsqa_outlrs, 'all.aseg.stats'))
outl_stats_norms = pd.read_csv(os.path.join(dir_fsqa_outlrs, 'all.outliers.norms.stats'))
outl_stats_nonpa = pd.read_csv(os.path.join(dir_fsqa_outlrs, 'all.outliers.sample.nonpar.stats'))
outl_stats_param = pd.read_csv(os.path.join(dir_fsqa_outlrs, 'all.outliers.sample.param.stats'))

bilateral = ['Accumbens-area', 'Amygdala', 'Caudate', 'Cerebellum-Cortex', 'Cerebellum-White-Matter', 
'Hippocampus', 'Inf-Lat-Vent', 'Lateral-Ventricle', 'Pallidum', 'Putamen', 'VentralDC', 'choroid-plexus', 
'vessel']

bilateralr = ['CerebralWhiteMatter', 'SurfaceHoles', 'CerebralWhiteMatter', 'Cortex']

unilateral_violin = ['3rd-Ventricle', '4th-Ventricle', '5th-Ventricle',
'Brain-Stem', 'BrainSeg', 'BrainSegNotVent', 'BrainSegVol_to_eTIV',
'CC_Anterior', 'CC_Central', 'CC_Mid_Anterior', 'CC_Mid_Posterior',
'CC_Posterior', 'CSF', 'CerebralWhiteMatter', 'Cortex',
'EstimatedTotalIntraCranialVol', 'Mask', 'MaskVol_to_eTIV', 'Optic-Chiasm', 
'SubCortGray', 'SupraTentorial','SupraTentorialNotVent', 'TotalGray', 'VentricleChoroidVol']

# Plot left/right

for a in bilateral:
    fig = go.Figure(data=go.Scatter(y=aseg_stats['Left-'+f'{a}'],
                                    x=aseg_stats['Right-'+f'{a}'],
                                    mode='markers',
                                    marker_color=aseg_stats['TotalGray'],
                                    text=aseg_stats['subject'])) # hover text goes here
    
    fig.update
    fig.update_layout(
        title=f"{a} volume mm^3",
        yaxis_title="Left HS",
        xaxis_title="Right HS")
    fig.write_html(os.path.join(dir_qa_plts, f'fs_lr{a}_plot.html'))


# plot lr
for a in bilateralr:
    
    fig = go.Figure(data=go.Scatter(y=aseg_stats[f'lh{a}'],
                                x=aseg_stats[f'rh{a}'],
                                mode='markers',
                                marker_color=aseg_stats['TotalGray'],
                                text=aseg_stats['subject'])) # hover text goes here

    fig.update
    fig.update_layout(
        title=f"{a} volume mm^3",
        yaxis_title="Left HS",
        xaxis_title="Right HS")
    
    fig.write_html(os.path.join(dir_qa_plts, f'fs_lr{a}_plot.html'))



# plot unilateral violin
for a in unilateral_violin:
    fig = px.violin(aseg_stats, y=f"{a}", box=True, points='all', hover_name=aseg_stats['subject'])
    fig.update_layout(
        title=f"{a} volume mm^3",
        xaxis_title=f"{a}",
        yaxis_title="volume")
    fig.write_html(os.path.join(dir_qa_plts, f'fs_{a}_plot.html'))




#### === SUBPAGES === ###

subs = [f for f in os.listdir(dir_fsqa_screen) if 'sub-' in f]

for s in subs:
    
    print(os.path.join(dir_subs_fs, f"{s}_fsqa.html"))
    
    this_shtml = shtml
    
    # add correct sub-id
    this_shtml = this_shtml.replace('sub-x', s)
    
    # check if we have png available in screenshots and in fornix 
    this_ssm = os.path.join(dir_fsqa_screen, s, f"{s}.png")
    this_ssf = os.path.join(dir_fsqa_fornix, s, "cc.png")
    
    
    
    if os.path.exists(this_ssm):
        #img_ssm = f'<div class="container"><div class="row"><div class="col-4"><div class="col text-center"><img src="{this_ssm}"></div></div></div></div>'
        img_ssm = f'<center><h2><a id = "pngaseg">Control ASEG</a></h2><br><a href="{this_ssm}" target="_blank"><img src = "{this_ssm}" width="1200px"></a></center>' 
        this_shtml = this_shtml.replace('[[mainscreen]]', img_ssm)
        
    if os.path.exists(this_ssf):
        img_ssf = f'<center><h2><a id = "pngcc">Control CC</a></h2><br><a href="{this_ssf}" target="_blank"><img src = "{this_ssf}" width="1200px"></a></center>'
        this_shtml = this_shtml.replace('[[ccscreen]]', img_ssf)
    
    
    # datetimespaceholder as current datetime
    dtn = dt.datetime.now()
    this_shtml = this_shtml.replace('datetimespaceholder', str(dtn))
    
    # add any outlier flag
    
    #Save
    with open(os.path.join(dir_subs_fs, f"{s}_fsqa.html"), 'w') as spage:
        spage.write(this_shtml)
        spage.close()

#### === FREESURFER MAIN === ###


# list all plots 
plts = [p for p in os.listdir(dir_qa_plts) if p.endswith('.html')]

# Add embeds for all plots

# list all subjects
pgsub = [s for s in os.listdir(dir_subs_fs) if s.endswith('.html')]
thml= ""

# index all subject pages
for i in range(1,10):
    l = [s for s in pgsub if f'sub-{i}' in s]
    l.sort()
    thml = f'<h4 class="display-5"><a id = "s{i}">{i}</a></h4><br>'
    
    for s in l:
        sub = s.split('_')[0]
        thml += f"<a href='fs/{s}'>{sub}</a> "
    thml += '<br><br>'
    mhtml = mhtml.replace(f'[list{i}]', thml)
    
# save
with open(os.path.join(dir_mainqa, 'freesurfer.html'), 'w') as mpage:
    mpage.write(mhtml)
    mpage.close()
