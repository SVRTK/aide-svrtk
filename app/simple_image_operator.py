# Simple Image Operator

import logging

import monai.deploy.core as md
from monai.deploy.core import DataPath, ExecutionContext, Image, InputContext, IOType, Operator, OutputContext


@md.input("image", DataPath, IOType.DISK)
@md.output("saved_images_folder", DataPath, IOType.DISK)
class SimpleImageOperator(Operator):
    """Simple Image Operator
    """

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):
        from skimage.transform import rotate
        from skimage.io import imsave

        logging.info(f"Begin {self.compute.__name__}")

        # data_in = op_input.get().asnumpy()
        # if not data_in:
        #     raise ValueError("Input image is not found.")
        # data_out = rotate(data_in, angle=180)

        input_image = op_input.get("image")
        if not input_image:
            raise ValueError("Input image is not found.")
        data_out = rotate(input_image, angle=180)

        logging.info(f"Performed rotation inside {self.compute.__name__}")

        op_output_folder_name = DataPath("saved_images_folder")
        op_output.set(op_output_folder_name, "saved_images_folder")
        op_output_folder_path = op_output.get("saved_images_folder").path
        op_output_folder_path.mkdir(parents=True, exist_ok=True)
        print(f"Operator output folder path: {op_output_folder_path}")

        imsave(op_output_folder_path, data_out)

        # output_folder = op_output.get().path
        # output_path = output_folder / "final_output.png"
        # imsave(output_path, data_out)

        logging.info(f"End {self.compute.__name__}")