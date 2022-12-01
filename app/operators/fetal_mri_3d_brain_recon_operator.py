# Perform Fetal MRI 3D Brain reconstruction

import glob
import logging
import os
import subprocess
import shutil

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

        # TODO: improve path code below – very hacky as hard-coded based on:
        #  /input
        #   |- /nii_stacks
        #   |- /nii_3d
        input_dir = os.path.dirname(nii_path)

        # nii_3d_path = os.path.join(input_dir, "nii_3d")
        # if not os.path.exists(nii_3d_path):
        #     os.makedirs(nii_3d_path)
        op_output.set(DataPath(input_dir))  # cludge to avoid op_output not exist error

        op_output_folder_path = op_output.get().path
        op_output_folder_path.mkdir(parents=True, exist_ok=True)

        # Run 3D Fetal Brain MRI reconstruction
        # subprocess.run(["/home/scripts/docker-recon-brain-auto.bash", nii_path, "-1", "-1"])
        subprocess.run(["cp", "/Users/tr17/code/aide-svrtk/test_data/SVR-output.nii.gz", nii_path])

        # TODO: may need to copy output files in nii_stacks_path to nii_3d_path
        # copy nifti files output by previous operator for processing in nii_3d_path directory
        # for nii_stack_filename in glob.glob(nii_stacks_path + '/stack*.nii.gz'):
        #     shutil.copy(nii_stack_filename, nii_3d_path)

        # TODO: remove temporary code below - purely for testing writing to output dir
        #  - or add to logs
        # with open(os.path.join(op_output_folder_path, 'results.txt'), 'w') as f:
        #     f.write('Testing paths:\n')
        #     f.write(f'nii_stacks_path: {nii_stacks_path}\n')
        #     f.write(f'input_dir: {input_dir}\n')
        #     f.write(f'nii_3d_path: {nii_3d_path}\n')
        #     f.write(f'op_output_folder_path: {op_output_folder_path}\n')

        logging.info(f"End {self.compute.__name__}")
