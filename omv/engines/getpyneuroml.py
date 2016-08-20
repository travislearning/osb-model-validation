import os
from ..common.inout import inform, check_output

from utils.wdir import working_dir

def install_pynml():
    
    install_root = os.environ['HOME']
    
    with working_dir(install_root):
        check_output(['git', 'clone', 'https://github.com/NeuroML/pyNeuroML.git'])
        inform('Successfully cloned PyNML', indent=2, verbosity=1)
    
    path = os.path.join(install_root,'pynml')
    
    with working_dir(path):
        check_output(['python', 'setup.py', 'install'])
        inform('Successfully installed PyLEMS', indent=2, verbosity=1)
    
