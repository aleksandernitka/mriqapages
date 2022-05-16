#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 13:09:52 2022

@author: aleksander
"""

import os


### 
hMRI_dir = '/mnt/nasips/COST_mri/derivatives/hMRI' # where to look for synthetic T1s
TMP_dir = '/home/aleksander/Documents/gif_tmp/' # where to process, tmp dir
OUT_dir = '/mnt/nasips/COST_mri/qa/sT1_gif/' # where to save
GYN_sif = '/opt/sifs/gif_your_nifti.simg' # where is the singularity container of gif your nifti
###

def gif_this_nii(i, hMRI_dir, TMP_dir, OUT_dir, GYN_sif):
    
    import subprocess as sb
    import shutil as sh
    
    # copy synth T1 is present; try/except
    try:
        print(f"{i}")
        sh.copy(os.path.join(hMRI_dir, i, 'Results', i + '_synthetic_T1w.nii'), 
                os.path.join(TMP_dir, i + '_T1.nii'))
    except:
        print(f'File copy error: {i}')
    
    # run fsl_reorient
    sb.call(f"fslreorient2std {TMP_dir}{i}_T1.nii {TMP_dir}{i}_T1", shell=True)
    sb.call(f"rm -rf {TMP_dir}{i}_T1.nii", shell=True)
    
    # run singularity with gif_your_nifty sb
    sb.call(f"singularity run {GYN_sif} --fps 20 --size 1 {TMP_dir}{i}_T1.nii.gz", shell=True)
    
    # move gif to dir - TBC where
    # sh.copy(os.path.join(TMP_dir, f"{i}_T1.gif"), os.path.join(OUT_dir, f"{i}_T1.gif"))
    
    sb.call(f"rm -rf {TMP_dir}{i}_T1.nii.gz", shell=True)
    

subs_hMRI = [f for f in os.listdir(hMRI_dir) if 'sub-' in f]

for i in subs_hMRI:
    
    gif_this_nii(i, hMRI_dir, TMP_dir, OUT_dir, GYN_sif)
    

    
    
