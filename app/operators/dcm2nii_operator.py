# DICOM to NIfTI conversion operator

import glob
import logging
import os
from pathlib import Path
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

        input_path = str(op_input.get("input_files").path)

        # input_files = [f for f in input_path.iterdir() if f.is_file()]  # old code if all DICOMs in /input folder
        input_files = parse_recursively_dcm_files(input_path)

        dcm_stacks_path = os.path.join(input_path, 'dcm_stacks')
        if not os.path.exists(dcm_stacks_path):
            os.makedirs(dcm_stacks_path)

        for f in input_files:
            shutil.copy(f, dcm_stacks_path)

        nii_path = os.path.join(input_path, 'nii_processing')
        if not os.path.exists(nii_path):
            os.makedirs(nii_path)
        op_output.set(DataPath(nii_path))

        # Run dcm2niix
        subprocess.run(["dcm2niix", "-z", "y", "-o", nii_path, "-f", "stack-%s", dcm_stacks_path])

        # Delete superfluous .json files
        json_files = glob.glob(nii_path + "/*.json")
        for json_file in json_files:
            os.remove(json_file)

        logging.info(f"Performed dcm2niix conversion inside {self.compute.__name__}")

        logging.info(f"End {self.compute.__name__}")


def parse_recursively_dcm_files(input_path):
    """
    Recursively parse Minio folder structure to extract paths to .dcm files
    Minio file structure:
    /var/monai/input
        StudyUID (folder)
            SeriesUID (folders)
                InstanceUID (files)

    :param input_path:
    :return dcm_paths:
    """

    if not 'dcm' in os.listdir(input_path):
        print('dcm folder not found.')
    else:
        dcm_path = os.path.join(input_path, 'dcm')

    try:
        study_dir = ''.join(os.listdir(dcm_path))
        study_path = os.path.join(dcm_path, study_dir)
    except:
        print('Exception occurred with study_path')

    try:
        series_paths = []
        series_dirs = os.listdir(study_path)
        for sd in series_dirs:
            series_paths.append(os.path.join(study_path, sd))
    except:
        print('Exception occurred with series_paths')

    dcm_files = []
    for sp in series_paths:
        series_files = os.listdir(sp)
        for file in series_files:
            if '.dcm' in Path(file).suffix:
                dcm_files.append(file)

    dcm_paths = [os.path.join(a, b) for a, b in zip(series_paths, dcm_files)]

    return dcm_paths
