#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def nii_anat_plot(nii, png, filename):
    
    """
    Created on Fri Mar 25 15:27:57 2022

    @author: aleksander
    
    plotting function, takes nii file path and path where to save pngs (x,y,z) to a specified dir
    """

    from nilearn import plotting
    import nibabel as nb
    import matplotlib.pyplot as plt
    import os
    import warnings
    
    warnings.filterwarnings("ignore")
    
    img = nb.load(nii)
    
    t = filename.split('/')[-1].split('.')[0]
    print(f'Processing screens for {t}')
    
    fig, axes = plt.subplots(nrows = 3, ncols=1, figsize = (20, 10))
    plt.tight_layout()
    fig.set_tight_layout(True)
    
    for n, p in enumerate(['x','y','z']):
        
        plotting.plot_anat(img, \
                            title=None, \
                            display_mode=p, \
                            draw_cross = True, \
                            dim = 0,\
                            axes = axes[n],\
                            cut_coords=[-30, -20, -10, 0, 10, 20, 30])
            

    fig.savefig(os.path.join(png, t), transparent = True, bbox_inches = 'tight')
