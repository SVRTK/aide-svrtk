# Perform Fetal MRI 3D Brain reconstruction

import logging
import os
import subprocess

import monai.deploy.core as md
from monai.deploy.core import DataPath, ExecutionContext, InputContext, IOType, Operator, OutputContext


@md.input("input_files", DataPath, IOType.DISK)
@md.output("input_files", DataPath, IOType.DISK)
@md.env(pip_packages=["pydicom >= 2.3.0", "highdicom >= 0.18.2"])
class FetalMri3dBrainOperator(Operator):
    """
    Fetal MRI 3D Brain Reconstruction Operator
    """

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):

        logging.info(f"Begin {self.compute.__name__}")

        nii_path = op_input.get("input_files").path

        input_dir = os.path.dirname(nii_path)

        # nii_3d_path = os.path.join(input_dir, "nii_3d")
        # if not os.path.exists(nii_3d_path):
        #     os.makedirs(nii_3d_path)
        op_output.set(DataPath(input_dir))  # cludge to avoid op_output not exist error

        op_output_folder_path = op_output.get().path
        op_output_folder_path.mkdir(parents=True, exist_ok=True)

        # Run 3D Fetal Brain MRI reconstruction
        subprocess.run(["/home/scripts/docker-recon-brain-auto.bash", nii_path, "-1", "-1"])

        logging.info(f"End {self.compute.__name__}")
