# DICOM Writer operator

import glob
import logging
import os
import subprocess

import monai.deploy.core as md
from monai.deploy.core import DataPath, ExecutionContext, InputContext, IOType, Operator, OutputContext


@md.input("dicom_files", DataPath, IOType.DISK)
@md.output("nifti_files", DataPath, IOType.DISK)
@md.env(pip_packages=["pydicom >= 2.3.0", "highdicom >= 0.18.2"])
class DicomWriterOperator(Operator):
    """
    DICOM writer
    """

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):

        logging.info(f"Begin {self.compute.__name__}")

        # TODO:
        #  - bring in PyDicom 3D DICOM creation code

        logging.info(f"End {self.compute.__name__}")
