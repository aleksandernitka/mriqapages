#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 15:47:19 2022

MPM process leaves some pngs and one html output that is unfinished
this fns create a single html which embed the data

@author: aleksander
"""

### IMPORT
import os

### DEFs
def plot_mpm_maps(sub, hmridir = '/mnt/nasips/COST_mri/derivatives/hMRI/'):
    
    from nilearn import plotting
    from os.path import join
    from os import listdir as ls
    import cmocean
    
    hmridir = '/mnt/nasips/COST_mri/derivatives/hMRI/'
    sub = 'sub-13000'
    mpm_maps = [f for f in ls(join(hmridir, sub, 'Results')) if f.endswith('.nii')]
    
    # for a better plotting, some maps need thresholds to be set
    bounds = dict(PD=[5, 200], 
                  T1w=[0, 150],
                  R1=[0,2],
                  R2s_OLS=[0,50],
                  MTsat=[0,10])
    
    for m in mpm_maps:
        n = m.split('.')[0].split('_')[-1]
        if n == 'OLS':
            n = 'R2s_OLS'
        
        plotting.plot_anat(join(hmridir, sub, 'Results', m), \
                           title = f'{sub} {n}', display_mode='z', \
                               cut_coords=[-50, -25, 0, 25, 50], black_bg=True,\
                               cmap = cmocean.cm.tarn,\
                               vmin = bounds[n][0], vmax = bounds[n][1],
                               output_file = join())




def mk_thumbnail(image_path, x, y, save_path, subject_id):
    from PIL import Image
    try:
        img = Image.open(image_path)
        img.thumbnail((x,y))
        img_name = image_path.split('/')[-1].replace('.png','_thumb.png')
        img_name = subject_id +"_"+img_name
        img.save(f"{save_path}/{img_name}")
        
        return img_name
    
    except IOError:
        pass

### CONSTANTS

hMRI = '/mnt/nasips/COST_mri/derivatives/hMRI/'
html_out_dir = '/home/aleksander/Documents/fs_qa/qaPages/hmri/'
pngs_out = os.path.join(html_out_dir, 'png')

### DIR SETUP

if os.path.exists(pngs_out) == False:
    os.mkdir(pngs_out)

### DO

hMRI_dirs = [f for f in os.listdir(hMRI) if 'sub-' in f]


for f in hMRI_dirs:
    print(f"\n================ {f} ================\n")
    
    # PROTOCOL CHECK FIX
    try:
       pc_html = open(os.path.join(hMRI, f, 'protocol_check.htm'), 'r')
       pc_code = pc_html.read()
       pc_html.close()
        
        # rm /home/aleksander/mritmp/tmp/ keep just the sub id
        
        # inputs.mat link and all_protocols_seetings.mat in the same level - fix link to relative
        
        # can save this file as new
         
    except:
        print(f"Cannot open or read protocol_check.htm for {f}")
        
    
    # QA plots etc
    try:
        qa_html = open(os.path.join(hMRI, f, 'Results', 'Supplementary', 'quality_report.htm'), 'r')
        qa_code = qa_html.read()
        qa_html.close()
        
        #med_qlt = [f for f in os.listdir(os.path.join(hMRI, f, 'Results', 'MultiEchoData_Qlt')) if f.endswith('png')]
        mpm_qlt = [f for f in os.listdir(os.path.join(hMRI, f, 'Results', 'MPM_Quality4')) if f.endswith('png') and f != 'MPMqlt_full.png']
        
        #med_qlt.sort()
        mpm_qlt.sort()
        
        # Make screens for all nii in mpm_quality4
        niis = [f for f in os.listdir(os.path.join(hMRI, f, 'Results')) if f.endswith('.nii')]
        
        # final page html code
        mpm_html = ""
        
        # these screens are accessible from pngs_out + sub-XXXXX_WM.png
        mpm_brains_html = ''
        
        for i in niis:
            nii_anat_plot(os.path.join(hMRI, f, 'Results', i), pngs_out, i)
            # temp filename
            tfn = os.path.join(pngs_out,i.replace('nii', 'png'))
            n = i.split('_')[-1].split('.')[0]
            
            mpm_brains_html += f'<center><a id = "{n}"><h2>{n}</h2></a><br><img src="{tfn}"><br><br></center>'
            
        mpm_html += mpm_brains_html
        
        # 3. Multi-echo data quality
        # (Will be added later.) 

        directory = os.path.join(hMRI, f, 'Results', 'MPM_Quality4')
        
        # TMPM_Quality4/MPMqlt_full.png to the top and reduce its size
        mpm_qlt_full_img = f'{directory}/MPMqlt_full.png'
        
        mpm_qlt_thum_img = os.path.join(pngs_out, mk_thumbnail(mpm_qlt_full_img, 1167, 875, pngs_out, f))
        
        mpm_html += f"<a id='mpm_plots'><h2>4. MPM Quality Plots</h2></a><br><center><a href='{mpm_qlt_full_img}'><img src='{mpm_qlt_thum_img}'></a><br><br>\n"
        for i in mpm_qlt:
            title = i.split('.')[0]
            image = i
            mpm_html += f"<center><h3>{title}</h3><br><a href='{directory}/{image}'><img src='{directory}/{image}' width = '584' height = '438'></a><br><br>\n"
        
        # add images to the old report by replacing the text
        qa_code = qa_code.replace('(Will be added later.)', mpm_html)
        
        with open(os.path.join(html_out_dir, f'{f}_quality_report_clab.html'), "w") as qa_html_out:
            qa_html_out.write(qa_code)
            qa_html_out.close
        
        
    except:
        print(f"Cannot open or read quality_report.htm for {f}")
