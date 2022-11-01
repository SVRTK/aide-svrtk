# Rotate Image Operator
# Simple operating to practice creating MAP

import logging

import monai.deploy.core as md
from monai.deploy.core import DataPath, ExecutionContext, Image, InputContext, IOType, Operator, OutputContext


@md.input("image", Image, IOType.DISK)
@md.output("saved_images_folder", DataPath, IOType.DISK)
class RotateImageOperator(Operator):
    """Rotate Image Operator
    Simple test operator
    """

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):
        from skimage.transform import rotate
        from skimage.io import imsave
        from numpy import squeeze

        logging.info(f"Begin {self.compute.__name__}")

        input_image = op_input.get("image")
        if not input_image:
            raise ValueError("Input image is not found.")
        data_out = rotate(input_image._data, angle=180, preserve_range=True)

        logging.info(f"Performed rotation inside {self.compute.__name__}")

        op_output_folder_path = op_output.get("saved_images_folder").path
        op_output_folder_path.mkdir(parents=True, exist_ok=True)
        print(f"Operator output folder path: {op_output_folder_path}")

        imsave(op_output_folder_path / "original_image.png", squeeze(input_image._data))
        imsave(op_output_folder_path / "rotated_image.png", squeeze(data_out))

        logging.info(f"End {self.compute.__name__}")