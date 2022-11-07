# DICOM to NIfTI conversion operator
# TODO: use MONAI Image class – for now, use dcm2niix as way of testing third-party software and MAPs

import logging
import os, glob, subprocess

import monai.deploy.core as md
from monai.deploy.core import DataPath, ExecutionContext, Image, InputContext, IOType, Operator, OutputContext


@md.input("image", Image, IOType.DISK)
@md.output("saved_images_folder", DataPath, IOType.DISK)
class Dcm2NiiOperator(Operator):
    """
    DICOM to NIfTI Operator
    """

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):

        logging.info(f"Begin {self.compute.__name__}")

        # TODO: add in access to input_folder

        input_image = op_input.get("image")
        if not input_image:
            raise ValueError("Input image is not found.")
        data_out = rotate(input_image._data, angle=180, preserve_range=True)

        op_output_folder_path = op_output.get("saved_images_folder").path
        op_output_folder_path.mkdir(parents=True, exist_ok=True)
        print(f"Operator output folder path: {op_output_folder_path}")

        subprocess.run(["dcm2niix", "-z", "y", "-o", input_path, "-f", "stack-%s", op_output_folder_path])

        logging.info(f"Performed dcm2niix conversion inside {self.compute.__name__}")

        logging.info(f"End {self.compute.__name__}")