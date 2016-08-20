"""OpenSourceBrain Model Validation and Testing
============================================

  Usage:
    omv all [-V | --verbose] [--engine=engine]
    omv test <testMe.omt> [-V | --verbose]
    omv autogen [options]
    omv install <engine>
    omv find
    omv list-engines
    omv validate-mep <mepfile>
    omv validate-omt <omtfile>
    omv (-h | --help)
    omv --version

  Options:
    -h --help     Show this screen.
    -d --dryrun   Generate dry-run tests only [default: False].
    -V --verbose  Display additional diagnosis messages [default: False].
    --version     Show version.
    -y            Auto-select default options (non-interactive mode)
"""
from docopt import docopt
from find_tests import test_all, test_one
from validation import validate_mep
from autogen import autogen
from engines import OMVEngines
import os

import common.inout

def main():
    arguments = docopt(__doc__, version='OpenSourceBrain Model Validation 0.0')

    set_env_vars()

    if arguments['--verbose']:
        common.inout.__VERBOSITY__ = 1

    if arguments['test']:
        try:
            test_one(arguments['<testMe.omt>'])
        except AssertionError:
            print("Failed due to non passing tests")
            exit(1)

    elif arguments['all']:
        try:
            test_all(only_this_engine=arguments['--engine'])
        except AssertionError:
            print("Failed due to non passing tests")
            exit(1)
            
    elif arguments['find']:
        try:
            test_all(do_not_run=True)
        except AssertionError:
            print("Failed due to non passing tests")
            exit(1)

    elif arguments['validate-mep']:
        validate_mep.validate(arguments['<mepfile>'])

    elif arguments['validate-omt']:
        print('OMT validation not implemented yet!')
        exit(1)

    elif arguments['install']:
        common.inout.__VERBOSITY__ = 1
        engine = arguments['<engine>']
        if engine not in OMVEngines:
            print('Engine ' + engine + ' unknown!')
        else:
            eng = arguments['<engine>']
            print('Trying to install: %s'% eng)
            already_installed = False
            
            if eng == 'NEURON':
                from engines.neuron import NeuronEngine
                if not NeuronEngine.is_installed(''):
                    from engines.getnrn import install_neuron
                    install_neuron()
                else:
                    already_installed = True
                    
            elif eng == 'jLEMS':
                from engines.jlems import JLemsEngine as ee
                if ee.is_installed(None):
                    already_installed = True
                else:
                    from engines.getjlems import install_jlems
                    install_jlems()
                    
            elif eng == 'jNeuroML':
                from engines.jneuroml import JNeuroMLEngine as ee
                if ee.is_installed(None):
                    already_installed = True
                else:
                    from engines.getjnml import install_jnml
                    install_jnml()
                    
            elif eng == 'neuroConstruct' or eng == 'Py_neuroConstruct':
                from engines.pyneuroconstruct import PyneuroConstructEngine as ee
                if ee.is_installed(None):
                    already_installed = True
                else:
                    from engines.getneuroconstruct import install_neuroconstruct
                    install_neuroconstruct()

            elif eng == 'pyNeuroML':
                from engines.pyneuroml_ import PyNeuroMLEngine as ee
                if ee.is_installed(None):
                    already_installed = True
                else:
                    from engines.getpyneuroml import install_pynml
                    install_pynml() 
                    
            elif eng == 'PyLEMS_NeuroML2':
                from engines.getpylems import install_pylems
                install_pylems()
                from engines.getnml2 import install_nml2
                install_nml2()
            elif eng == 'genesis':
                from engines.getgenesis import install_genesis
                install_genesis()
            elif eng == 'NetPyNE':
                from engines.getnetpyne import install_netpyne
                install_netpyne()
            elif eng == 'Brian':
                from engines.getbrian1 import install_brian
                install_brian()
            elif eng == 'Brian2':
                from engines.getbrian2 import install_brian2
                install_brian2()
            elif eng == 'Py_neuroConstruct' or eng == 'neuroConstruct':
                from engines.getneuroconstruct import install_neuroconstruct
                install_neuroconstruct()
            else:
                print('Code not implemented yet for installing %s using: omv install! Try running a test using this engine.'%eng)
                exit(1)
            if already_installed:
                print('Engine %s was already installed'%eng)
                
                
            

    elif arguments['list-engines']:
        engines = sorted(OMVEngines.keys())
        
        installed = {}
        for engine in engines:
            installed[engine] = OMVEngines[engine].is_installed('')
            
        print('\n\nThe following engines are currently supported by OMV:\n')
        for engine in engines:
            print('  %s%s(installed: %s)'%(engine, ' '*(30-len(engine)), installed[engine]))
        print('')

    elif arguments['autogen']:
        print('Automatically generating model validation files')
        dry = arguments['--dryrun']
        auto = arguments['-y']
        autogen(auto, dry)

def set_env_vars():

    if os.name == 'nt':

        # Windows does not have a HOME var defined by default
        os.environ['HOME'] = os.environ['USERPROFILE']

if __name__ == '__main__':
    main()
