##################################################################################################################
#
#   This script uses freeview to make screenshots of a freesurfer segmentation.
#   These screenshots are then combined to a movie, for easy diagnosis of 
#   FreeSurfer segmentation problems. I have chosen for sagittal orientation, 
#   because this allows one to see whether the sagittal sinus is misclassified as V1 gray matter. 
# 
##################################################################################################################

# Author: https://gist.github.com/tknapen/85d9a23a09c95d15f4b23ba1965fa54d
# Adapted by Aleksander Nitka

import subprocess as sb
import os
import glob

freeview_command = 'freeview -cmd {cmd} '
cmd_txt = """ -v {anatomy}:grayscale=10,100 -f {lh_wm}:color=red:edgecolor=red:edgethickness=1 -f {rh_wm}:color=red:edgecolor=red:edgethickness=1 -f {lh_pial}:color=white:edgecolor=yellow:edgethickness=1 -f {rh_pial}:color=white:edgecolor=yellow:edgethickness=1
 -viewport sagittal
 """  

# To step through the sagittal slices this is added for every slice. 
slice_addition = ' -slice {xpos} 127 127 \n -ss {opfn} 2 1 \n  '

freesurfer_subject_dir = '/mnt/nasips/COST_mri/derivatives/freesurfer/'

subject_lists = ['sub-94393']

slices = range(90, 240)  # the slices in the anatomy to show. don't want to show a bunch of nothingness outside of the brain.


for subject in subject_lists:  # list of subject indices
    # this subject should be in the freesurfer subjects directory FS_folder

    FS_folder = os.path.join(freesurfer_subject_dir, subject)


    #target_directory = os.path.join(FS_folder, 'movie')
    target_directory = os.path.join('/home/aleksander/Documents/', 'fs_movie', subject)
    os.makedirs(target_directory, exist_ok=True)

    cmd_file = os.path.join(target_directory, 'cmd.txt')

    sj_cmd = cmd_txt.format(
        anatomy=os.path.join(FS_folder, 'mri', 'T1.mgz'),
        lh_wm=os.path.join(FS_folder, 'surf', 'lh.white'),
        lh_pial=os.path.join(FS_folder, 'surf', 'lh.pial'),
        rh_wm=os.path.join(FS_folder, 'surf', 'rh.white'),
        rh_pial=os.path.join(FS_folder, 'surf', 'rh.pial'),
        subject=subject
    )

    for sag_slice in slices:

        sj_cmd += slice_addition.format(
            xpos=sag_slice,
            opfn=os.path.join(target_directory, str(
                sag_slice).zfill(3) + '.png')
        )

    sj_cmd += ' -quit \n '

    with open(cmd_file, 'w') as f:
        f.write(sj_cmd)

    sb.call(freeview_command.format(cmd=cmd_file), shell=True)

# calling this in a separate for loop for efficiency (this can be done headlessly, the freesurfer stuff cannot)
# for sji in subject_lists:
    # subject = 'sub-' + str(sji).zfill(3)
    # target_directory = f'freesurfer_subject_dir/{subject}/movie'

    convert_command = f'ffmpeg -framerate 5 -pattern_type glob -i "{target_directory}/*.png" -b:v 2M -c:v mpeg4 {target_directory}/{subject}.mp4'
    sb.call(convert_command, shell=True)
