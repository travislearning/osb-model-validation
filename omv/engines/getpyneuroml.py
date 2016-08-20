import os
from ..common.inout import inform, check_output

from utils.wdir import working_dir

def install_pynml():
    
    install_root = os.environ['HOME']
    
    with working_dir(install_root):
        check_output(['git', 'clone', 'https://github.com/NeuralEnsemble libNeuroML.git@development'])
        inform('Successfully cloned libNeuroML', indent=2, verbosity=1)

	check_output(['git', 'clone', 'https://github.com/NeuroML/pyNeuroML.git'])
        inform('Successfully cloned PyNeuroML', indent=2, verbosity=1)

    
    path = os.path.join(install_root,'pynml')
    
    with working_dir(path):
        check_output(['python', 'setup.py', 'install'])
        inform('Successfully installed PyNeuroML', indent=2, verbosity=1)
