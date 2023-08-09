# Perform Fetal MRI 3D Brain reconstruction

import logging
import os
import subprocess

import monai.deploy.core as md
from monai.deploy.core import DataPath, ExecutionContext, InputContext, IOType, Operator, OutputContext


@md.input("nii_dataset", DataPath, IOType.DISK)
@md.output("svrtk_output", DataPath, IOType.DISK)
@md.env(pip_packages=["pydicom >= 2.3.0", "highdicom >= 0.18.2"])
class FetalMri3dBrainOperator(Operator):
    """
    Fetal MRI 3D Brain Reconstruction Operator
    """

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):

        logging.info(f"Begin {self.compute.__name__}")

        operator_workdir = os.getcwd()

        nii_stacks_path = op_input.get("nii_dataset").path

        # TODO(tomaroberts) test and confirm working
        # Run 3D Fetal Brain MRI reconstruction
        # subprocess.run(["/home/scripts/docker-recon-brain-auto.bash", nii_stacks_path, "-1", "-1"])

        # Local testing:
        # create dummy SVR-output.nii.gz file in same location as output from docker-recon-brain-auto.bash
        subprocess.run(["touch", os.path.join(operator_workdir, 'SVR-output.nii.gz')])

        # Set output path for next operator
        op_output.set(DataPath(operator_workdir, "svrtk_output"))

        logging.info(f"End {self.compute.__name__}")
