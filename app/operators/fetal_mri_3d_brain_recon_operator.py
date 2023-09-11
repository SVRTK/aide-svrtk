# fetal_mri_3d_brain_recon_operator
#
# Perform Fetal MRI 3D Brain reconstruction
#

import logging
import os
import subprocess
import torch

import monai.deploy.core as md
from monai.deploy.core import DataPath, ExecutionContext, InputContext, IOType, Operator, OutputContext


@md.input("nii_dataset", DataPath, IOType.DISK)
@md.output("svrtk_output", DataPath, IOType.DISK)
@md.env(pip_packages=["pydicom >= 2.3.0"])
class FetalMri3dBrainOperator(Operator):
    """
    Fetal MRI 3D Brain Reconstruction Operator
    """

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):

        is_local_testing = False  # set True to bypass SVRTK

        logging.info(f"Begin {self.compute.__name__}")

        operator_workdir = os.getcwd()
        nii_stacks_path = op_input.get("nii_dataset").path

        logging.info("Performing SVRTK reconstruction ...")

        # Run motion corrected reconstruction
        if not is_local_testing:
#            if torch.cuda.is_available():
#                cnn_mode = "1"
#                logging.info("SVRTK reconstruction using GPU mode ...")
#            if not torch.cuda.is_available():
#                cnn_mode = "-1"
#                logging.info("SVRTK reconstruction using CPU mode ...")
#
#            motion_correction_mode = "-1"  # -1 minor, 1 severe
            logging.info("SVRTK reconstruction ...")

            subprocess.run([
                "/home/scripts/docker-recon-brain-auto.bash",
                nii_stacks_path,
                operator_workdir
            ])

        # Local testing:
        # create dummy SVR-output.nii.gz file in same location as output from docker-recon-brain-auto.bash
        if is_local_testing:
            subprocess.run(["cp", "/path/to/local/reo-SVR-output-brain.nii.gz", operator_workdir])

        logging.info("Completed SVRTK reconstruction ...")

        # Set output path for next operator
        op_output.set(DataPath(operator_workdir, "svrtk_output"))

        logging.info(f"End {self.compute.__name__}")
