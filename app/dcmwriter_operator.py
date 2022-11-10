# DICOM Writer operator

import logging
import os, glob, subprocess
from typing import List

import monai.deploy.core as md
from monai.deploy.core import DataPath, ExecutionContext, Image, InputContext, IOType, Operator, OutputContext
from monai.deploy.core.domain.dicom_series_selection import StudySelectedSeries


@md.input("image", Image, IOType.DISK)
@md.input("study_selected_series_list", List[StudySelectedSeries], IOType.IN_MEMORY)
@md.output("dicom_instance", DataPath, IOType.DISK)
@md.env(pip_packages=["pydicom >= 2.3.0", "highdicom >= 0.18.2"])
class DicomWriterOperator(Operator):
    """
    DICOM writer
    """

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):

        logging.info(f"Begin {self.compute.__name__}")

        # Gets the input, prepares the output folder, and then delegates the processing.
        study_selected_series_list = op_input.get("study_selected_series_list")
        if not study_selected_series_list or len(study_selected_series_list) < 1:
            raise ValueError("Missing input, list of 'StudySelectedSeries'.")
        for study_selected_series in study_selected_series_list:
            if not isinstance(study_selected_series, StudySelectedSeries):
                raise ValueError("Element in input is not expected type, 'StudySelectedSeries'.")

        # out_image = op_input.get("out_image")
        # # In case the Image object is not in the input, and input is the seg image file folder path.
        # if not isinstance(out_image, Image):
        #     if isinstance(out_image, DataPath):
        #         out_image, _ = self.select_input_file(out_image.path)
        #     else:
        #         raise ValueError("Input 'out_image' is not Image or DataPath.")
        #
        # output_dir = op_output.get().path
        # output_dir.mkdir(parents=True, exist_ok=True)
        #
        # self.process_images(out_image, study_selected_series_list, output_dir)
        #
        # logging.info(f"End {self.compute.__name__}")