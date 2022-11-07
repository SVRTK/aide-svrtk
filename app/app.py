# AI-derived 3D fetal brain MRI reconstruction with SVRTK – MONAI Application Package (MAP)
#
# Tom Roberts (tom.roberts@gstt.nhs.uk / t.roberts@kcl.ac.uk)

import logging

from rotate_image_operator import RotateImageOperator
from dcm2nii_operator import Dcm2NiiOperator

from monai.deploy.core import Application, resource
from monai.deploy.core.domain import Image
from monai.deploy.core.io_type import IOType
from monai.deploy.operators.dicom_data_loader_operator import DICOMDataLoaderOperator
from monai.deploy.operators.dicom_series_selector_operator import DICOMSeriesSelectorOperator
from monai.deploy.operators.dicom_series_to_volume_operator import DICOMSeriesToVolumeOperator


class FetalMri3dBrainApp(Application):
    """
    Motion-corrected 3D fetal brain MRI Application class
    """

    name = "3d-fetal-brain-mri"
    description = "Motion-corrected 3D fetal brain MRI application."
    version = "0.1.0"

    def compose(self):
        """Operators go in here
        """

        logging.info(f"Begin {self.compose.__name__}")

        # Create the custom operator(s) as well as SDK built-in operator(s).
        study_loader_op = DICOMDataLoaderOperator()
        series_selector_op = DICOMSeriesSelectorOperator()
        series_to_vol_op = DICOMSeriesToVolumeOperator()

        # Rotate image operator
        rotate_image_op = RotateImageOperator()

        # # DICOM to NIfTI operator
        # dcm2nii_op = Dcm2NiiOperator()

        # Create operator processing pipeline
        self.add_flow(study_loader_op, series_selector_op, {"dicom_study_list": "dicom_study_list"})
        self.add_flow(
            series_selector_op, series_to_vol_op, {"study_selected_series_list": "study_selected_series_list"}
        )
        self.add_flow(series_to_vol_op, rotate_image_op, {"image": "image"})
        # self.add_flow(series_to_vol_op, dcm2nii_op, {"image": "image"})

        logging.info(f"End {self.compose.__name__}")


if __name__ == "__main__":
    FetalMri3dBrainApp(do_run=True)