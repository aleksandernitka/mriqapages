# How to perform QA for FreeSurfer

## FreeSurfer Show - fss.py
fss.py is a simple helper script written to make loading of different FreeSurfer outputs easier. To make it work follow theses steps:
1. open terminal or terminator app.
2. Type in `nano ~/.bashrc` and press enter -- a simple text editor will open.
3. Scroll to the bottom and paste the following text: `export PATH="/opt/qa:$PATH"`, in the next line enter: `alias fss="fss.py"`, then close the editor with `ctrl+x` and save changes by pressing `y` when promped. This will add the path `opt/qa/` to the system `PATH` file and all of its contents will be available from anywhere in the system, so you will not have to navigate to the `opt/qa/` to run a script that is in there. The second line creates a 'shortcut' in the terminal, so you do not have to type `fss.py`, just `fss`.
4. Back in terminal type `source ~/.bashrc`, now the `ffs.py` script should be visible from anywhere. 
5. Type `ffs -h` to see help on how to use the script. The bottom line is that subject id, with or without the `sub-` prefix must be provided, if it does not work, it means that either the sub-id does not exist or the recon-all failed for that subject.

- fix code for plotting and move it to base location
- Run QA stuff so we have the data for QA
- Make websites for internal and move those to shaed drive.

