# DICOM to NIfTI conversion operator

import glob
import logging
import os
import shutil
import subprocess

import monai.deploy.core as md
from monai.deploy.core import DataPath, ExecutionContext, InputContext, IOType, Operator, OutputContext


@md.input("input_files", DataPath, IOType.DISK)
@md.output("input_files", DataPath, IOType.DISK)
@md.env(pip_packages=["pydicom >= 2.3.0", "highdicom >= 0.18.2"])
class Dcm2NiiOperator(Operator):
    """
    DICOM to NIfTI Operator
    """

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):

        logging.info(f"Begin {self.compute.__name__}")

        input_path = op_input.get("input_files").path
        input_files = [f for f in input_path.iterdir() if f.is_file()]

        dcm_stacks_path = os.path.join(input_path, 'dcm_stacks')
        if not os.path.exists(dcm_stacks_path):
            os.makedirs(dcm_stacks_path)

        for f in input_files:
            shutil.copy(f, dcm_stacks_path)

        nii_path = os.path.join(input_path, 'nii_processing')
        if not os.path.exists(nii_path):
            os.makedirs(nii_path)
        op_output.set(DataPath(nii_path))

        # TODO: add check to see if DICOM files exist

        # Run dcm2niix
        subprocess.run(["dcm2niix", "-z", "y", "-o", nii_path, "-f", "stack-%s", dcm_stacks_path])

        # Delete superfluous .json files
        json_files = glob.glob(nii_path + "/*.json")
        for json_file in json_files:
            os.remove(json_file)

        logging.info(f"Performed dcm2niix conversion inside {self.compute.__name__}")

        logging.info(f"End {self.compute.__name__}")
