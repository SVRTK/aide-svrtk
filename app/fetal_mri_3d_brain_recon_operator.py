# Perform Fetal MRI 3D Brain reconstruction

import glob
import logging
import os
import subprocess

import monai.deploy.core as md
from monai.deploy.core import DataPath, ExecutionContext, InputContext, IOType, Operator, OutputContext


@md.input("nifti_files", DataPath, IOType.DISK)
@md.output("nifti_3d_files", DataPath, IOType.DISK)
@md.env(pip_packages=["pydicom >= 2.3.0", "highdicom >= 0.18.2"])
class FetalMri3dBrainOperator(Operator):
    """
    Fetal MRI 3D Brain Reconstruction Operator
    """

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):

        logging.info(f"Begin {self.compute.__name__}")

        input_path = op_input.get("nifti_files").path

        op_output_folder_path = op_output.get().path
        op_output_folder_path.mkdir(parents=True, exist_ok=True)

        with open(os.path.join(op_output_folder_path, 'results.txt'), 'w') as f:
            f.write('Test: resultant file')

        logging.info(f"End {self.compute.__name__}")
