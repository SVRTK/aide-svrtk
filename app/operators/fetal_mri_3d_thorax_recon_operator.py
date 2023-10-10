# fetal_mri_3d_thorax_recon_operator
#
# Perform Fetal MRI 3D Thorax reconstruction
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
class FetalMri3dThoraxOperator(Operator):
    """
    Fetal MRI 3D Thorax Reconstruction Operator
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
#            logging.info("SVRTK reconstruction ...")

            subprocess.run([
                "/home/auto-proc-svrtk/scripts/auto-thorax-reconstruction-aide.sh",
                nii_stacks_path,
                operator_workdir
            ])

        # Local testing:
        # create dummy SVR-output.nii.gz file in same location as output from docker-recon-thorax-auto.bash
        if is_local_testing:
            subprocess.run(["cp", "/path/to/local/reo-DSVR-output-thorax.nii.gz", operator_workdir])

        logging.info("Completed SVRTK reconstruction ...")

        # Set output path for next operator
        op_output.set(DataPath(operator_workdir, "svrtk_output"))

        logging.info(f"End {self.compute.__name__}")
