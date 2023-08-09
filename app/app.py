# AI-driven 3D fetal brain MRI reconstruction using SVRTK constructed as a MONAI Application Package (MAP)
#
# Tom Roberts (tom.roberts@gstt.nhs.uk / t.roberts@kcl.ac.uk)
#

import logging

from monai.deploy.core import Application
from monai.deploy.operators.dicom_data_loader_operator import DICOMDataLoaderOperator
from monai.deploy.operators.dicom_series_selector_operator import DICOMSeriesSelectorOperator

from operators.dcm2nii_operator import Dcm2NiiOperator
from operators.fetal_mri_3d_brain_recon_operator import FetalMri3dBrainOperator
from operators.nii2dcm_operator import NiftiToDicomWriterOperator


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

        loader = DICOMDataLoaderOperator()
        selector = DICOMSeriesSelectorOperator(rules=Rules_Text, all_matched=True)

        # DICOM to NIfTI operator
        dcm2nii_op = Dcm2NiiOperator()

        # Fetal Brain 3D MRI reconstruction operator
        fetal_mri_3d_recon_op = FetalMri3dBrainOperator()

        # DICOM Writer operator
        nii2dcm_op = NiftiToDicomWriterOperator()

        # Operator pipeline
        self.add_flow(loader, selector, {"dicom_study_list": "dicom_study_list"})

        self.add_flow(selector, dcm2nii_op, {"study_selected_series_list": "study_selected_series_list"})
        self.add_flow(dcm2nii_op, fetal_mri_3d_recon_op, {"nii_dataset": "nii_dataset"})

        self.add_flow(dcm2nii_op, nii2dcm_op, {"dcm_input": "dcm_input"})
        self.add_flow(fetal_mri_3d_recon_op, nii2dcm_op, {"svrtk_output": "svrtk_output"})

        logging.info(f"End {self.compose.__name__}")


Rules_Text = """
{
    "selections": [
        {
            "name": "MR Series",
            "conditions": {
                "Modality": "MR"
            }
        }
    ]
}
"""

if __name__ == "__main__":
    FetalMri3dBrainApp(do_run=True)