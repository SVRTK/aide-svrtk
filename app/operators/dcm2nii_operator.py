# DICOM to NIfTI conversion operator

import glob
import logging
import os
import subprocess

import monai.deploy.core as md
from monai.deploy.core import DataPath, ExecutionContext, InputContext, IOType, Operator, OutputContext


@md.input("dicom_files", DataPath, IOType.DISK)
@md.output("nifti_files", DataPath, IOType.DISK)
@md.env(pip_packages=["pydicom >= 2.3.0", "highdicom >= 0.18.2"])
class Dcm2NiiOperator(Operator):
    """
    DICOM to NIfTI Operator
    """

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):

        logging.info(f"Begin {self.compute.__name__}")

        dcm_path = op_input.get("dicom_files").path

        nii_path = os.path.join(dcm_path, 'nii_stacks')
        if not os.path.exists(nii_path):
            os.makedirs(nii_path)
        op_output.set(DataPath(nii_path))

        # Run dcm2niix
        subprocess.run(["dcm2niix", "-z", "y", "-o", nii_path, "-f", "stack-%s", dcm_path])

        # Delete superfluous .json files
        json_files = glob.glob(nii_path + "/*.json")
        for json_file in json_files:
            os.remove(json_file)

        logging.info(f"Performed dcm2niix conversion inside {self.compute.__name__}")

        logging.info(f"End {self.compute.__name__}")
