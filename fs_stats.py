#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 16:07:55 2022

Runs stats for ASEG and APARC, and for the more precise methods

@author: aleksander
"""

import subprocess as sb
import os

fsd = '/mnt/nasips/COST_mri/derivatives/freesurfer/'
pth = '/home/aleksander/Documents/fs_qa/'

subs = [f for f in os.listdir(fsd) if 'sub-' in f]

# check if all dirs have aseg
for f in subs:
    if os.path.exists(os.path.join(fsd, f, 'mri', 'aseg.mgz')) == False:
        subs.remove(f)
        print(f"{f} removed as there was no aseg.mgz")

# Write all subject ids to file
with open('participants.txt', 'w') as p:
    for s in subs:
        p.write(f"{s}\n")

p.close()

# dir for output of stats
if os.path.exists('fsStats') == False:
    os.mkdir('fsStats')

### ASEG - WM segmentation stats
# do stats for subcortical data --> asegstats2table, measure volume in mm^3
cmd = f'SUBJECTS_DIR={fsd}; asegstats2table --subjectsfile=participants.txt --skip -d comma -t fsStats/aseg.csv'
print('---- ASEG ----')
sb.run(cmd, shell=True)

# report volume as percent estimated total intracranial volume
cmd = f'SUBJECTS_DIR={fsd}; asegstats2table --subjectsfile=participants.txt --skip -d comma --etiv -t fsStats/aseg_etiv.csv'
print('---- ASEG ETIV ----')
sb.run(cmd, shell=True)


### APARC - GM parcelation stats
# do stats Cortical data --> aparcstats2table
hemis = ['lh', 'rh']
m_apa = ['area', 'volume', 'thickness', 'foldind', 'thicknessstd', 'meancurv', 'gauscurv', 'thickness.T1', 'curvind']
parct = ['aparc', 'aparc.a2009s']

for p in parct:
    for m in m_apa:
        for h in hemis:
            
            print(f'---- {p.upper()} {h.upper()} {m.upper()} ----')
            cmd = f'SUBJECTS_DIR={fsd}; aparcstats2table --subjectsfile=participants.txt -p {p} --hemi={h} -t fsStats/{p}_{m}_{h}.csv -m {m} --delimiter comma --skip'
            sb.run(cmd, shell=True)
            
            if m == 'volume':
                # report volume as percent estimated total intracranial volume
                print(f'---- {p.upper()} {h.upper()} {m.upper()} ----')
                cmd = f'SUBJECTS_DIR={fsd}; aparcstats2table --subjectsfile=participants.txt -p {p} --hemi={h} --etiv -t fsStats/{p}_{m}-etiv_{h}.csv -m {m} --delimiter comma --skip'
                sb.run(cmd, shell=True)
    
    
# run for Thalamic Nuclei, HPC + AMG
for h in ['lh', 'rh']:
    print(f'---- THALAMUS {h.upper()} VOLUME ----')
    cmd = f'SUBJECTS_DIR={fsd}; asegstats2table --subjectsfile=participants.txt --statsfile=thalamic-nuclei.{h}.v12.T1.stats -t fsStats/thalamic-nuclei_volume_{h}.csv --delimiter comma --skip'
    sb.run(cmd, shell=True)
    cmd = f'SUBJECTS_DIR={fsd}; asegstats2table --subjectsfile=participants.txt --statsfile=thalamic-nuclei.{h}.v12.T1.stats -t fsStats/thalamic-nuclei_volume-etiv_{h}.csv --delimiter comma --skip --etiv'
    sb.run(cmd, shell=True)
    
    print(f'---- HPC {h.upper()} VOLUME ----')
    cmd =f'SUBJECTS_DIR={fsd}; asegstats2table --subjectsfile=participants.txt --statsfile=hipposubfields.{h}.T1.v21.stats -t fsStats/hipposubfields_volume_{h}.csv --delimiter comma --skip'
    sb.run(cmd, shell=True)
    cmd =f'SUBJECTS_DIR={fsd}; asegstats2table --subjectsfile=participants.txt --statsfile=hipposubfields.{h}.T1.v21.stats -t fsStats/hipposubfields_volume-etiv_{h}.csv --delimiter comma --skip --etiv'
    sb.run(cmd, shell=True)
    
    print(f'---- AMG {h.upper()} VOLUME ----')
    cmd =f'SUBJECTS_DIR={fsd}; asegstats2table --subjectsfile=participants.txt --statsfile=amygdalar-nuclei.{h}.T1.v21.stats -t fsStats/amygdalar-nuclei_volume_{h}.csv --delimiter comma --skip'
    sb.run(cmd, shell=True)
    cmd =f'SUBJECTS_DIR={fsd}; asegstats2table --subjectsfile=participants.txt --statsfile=amygdalar-nuclei.{h}.T1.v21.stats -t fsStats/amygdalar-nuclei_volume-etiv_{h}.csv --delimiter comma --skip --etiv'
    sb.run(cmd, shell=True)

# Brain Stem
print(f'---- BRAIN STEM VOLUME ----')
cmd = 'asegstats2table -subjectsfile=participants.txt --statsfile=brainstem.v12.stats -t fsStats/brainstem_volume.csv --delimiter comma --skip'
sb.run(cmd, shell=True)
cmd = 'asegstats2table -subjectsfile=participants.txt --statsfile=brainstem.v12.stats -t fsStats/brainstem_volume-etiv.csv --delimiter comma --skip --etiv'
sb.run(cmd, shell=True)

# for thalamus, bs, amg and hpc we can also get summary
# TODO does not work - requires a file to write to?

print(f'---- THALAMUS SUMMARY ----')
cmd = f'quantifyThalamicNuclei.sh {pth}fsStats/thalamic-nuclei_summary.csv Summary {fsd}'
sb.run(cmd, shell=True)

print(f'---- HPC SUMMARY ----')
cmd = f'quantifyHAsubregions.sh hippoSf T1 {pth}fsStats/hipposubfields_summary.csv Summary {fsd}'
sb.run(cmd, shell=True)

print(f'---- AMG SUMMARY ----')
cmd = f'quantifyHAsubregions.sh amygNuc T1 {pth}fsStats/amygdalar-nuclei_summary.csv Summary {fsd}'
sb.run(cmd, shell=True)

print(f'---- BRAIN STEM SUMMARY ----')
cmd = f'quantifyBrainstemStructures.sh {pth}fsStats/brainstem_summary.csv {fsd}'
sb.run(cmd, shell=True)

