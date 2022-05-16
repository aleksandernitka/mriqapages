import argparse
from os import listdir as ls
from numpy import loadtxt as load


args = argparse.ArgumentParser(description="Function check all data sources - verify whether we are missing data for a subject.")
args.add_argument('--valid_subjects', help='Give path to a file with all valid subject Ids', default='/opt/validids.csv')
args.add_argument('--hmri', help='Path to hMRI derivatives', default='/mnt/nasips/COST_mri/derivatives/hMRI/')
args.add_argument('--freesurfer', help='Path to FreeSurfer derivatives', default='/mnt/nasips/COST_mri/derivatives/freesurfer/')
args.add_argument('--dwipreproc', help='Path to DWI preprocessing derivatives', default='/mnt/nasips/COST_mri/derivatives/dwi/preproc/')
args.add_argument('-w', '--write', help='Save outputs to a file.', default=None)
args.add_argument('-d', '--detail', help='Print out details of the missing files.', action='store_true', default=False)
args.add_argument('-r', '--reverse', help='Reverse the search and also print which IDs are in the dirs but are not in valid ids list', action='store_true', default=False)
args = args.parse_args()

ids = load(args.valid_subjects, delimiter='\n', dtype=str)
print(f' {args.valid_subjects} contains {len(ids)} Ids.')

# initiate file for output
if args.write is not None:
    with open(args.write, 'w') as f:
        f.close()

# add sub to each element of the list (ids)
sub_ids = ['sub-' + z for z in ids]
sub_ids.sort()

dirs = [args.hmri, args.freesurfer, args.dwipreproc]
name = ['hMRI', 'FreeSurfer', 'DWI Preprocessing']

for i, d in enumerate(dirs):
    # list ids not in given dir
    m_ids = [f for f in sub_ids if f not in ls(d)]
    print(f'\n\nNot in {name[i]}, N = {len(m_ids)}')

    if args.write is not None:
        with open(args.write, 'a') as f:
            f.write(f'Not in {name[i]}, N = {len(m_ids)}\n')
            if len(m_ids) > 0:
                for m in m_ids:
                    f.write(f'{m}\n')
            f.write('\n')
            f.close()

    if args.detail:
        if len(m_ids) > 0:
            print(f'Missing from {name[i]}:')
            for m in m_ids:
                print(m)
    if args.reverse:
        # list ids not in valid ids
        e_ids = [f for f in ls(d) if f not in sub_ids and 'sub-' in f]
        print(f'\n\nIds in {name[i]} but not in {args.valid_subjects}, N = {len(e_ids)}')

        if args.write is not None:
            with open(args.write, 'a') as f:
                f.write(f'Ids in {name[i]} but not in {args.valid_subjects}, N = {len(e_ids)}\n')
                if len(e_ids) > 0:
                    for e in e_ids:
                        f.write(f'{e}\n')
                f.write('\n')
                f.close()

        if args.detail:
            if len(e_ids) > 0:
                print(f'Ids in {name[i]} but not in {args.valid_subjects}:')
                for e in e_ids:
                    print(e)




