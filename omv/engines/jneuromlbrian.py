import os
import subprocess as sp

from jneuroml import JNeuroMLEngine
from brian1 import Brian1Engine
from ..common.inout import inform, trim_path, check_output
from engine import EngineExecutionError


class JNeuroMLBrianEngine(JNeuroMLEngine):

    name = "jNeuroML_Brian"

    @staticmethod
    def is_installed(version):
        inform("Checking whether %s is installed..." %
               JNeuroMLBrianEngine.name, indent=1)
        return JNeuroMLEngine.is_installed(None) and Brian1Engine.is_installed(None)

    @staticmethod
    def install(version):

        if not JNeuroMLEngine.is_installed(None):
            JNeuroMLEngine.install(None)
        if not Brian1Engine.is_installed(None):
            Brian1Engine.install(None)

        JNeuroMLBrianEngine.path = JNeuroMLEngine.path + \
            ":" + BrianEngine.path
        JNeuroMLBrianEngine.environment_vars = {}
        JNeuroMLBrianEngine.environment_vars.update(
            JNeuroMLEngine.environment_vars)
        JNeuroMLBrianEngine.environment_vars.update(
            BrianEngine.environment_vars)
        inform("PATH: " + JNeuroMLBrianEngine.path)
        inform("Env vars: %s" % JNeuroMLBrianEngine.environment_vars)

    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), JNeuroMLBrianEngine.name), indent=1)
            self.stdout = check_output(['jnml', self.modelpath, '-brian'], cwd=os.path.dirname(self.modelpath))
            self.stdout += check_output(['python', self.modelpath.replace('.xml', '_brian.py'), '-nogui'], cwd=os.path.dirname(self.modelpath))
            inform("Success with running ", JNeuroMLBrianEngine.name, indent=1)
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Error with ", JNeuroMLBrianEngine.name, indent=1)
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
