import copy, os, subprocess

from aide_sdk.inference.aideoperator import AideOperator
from aide_sdk.model.dicom_image import DicomImage
from aide_sdk.model.dicom_series import DicomSeries
from aide_sdk.model.operatorcontext import OperatorContext
from aide_sdk.model.resource import Resource
from aide_sdk.utils.file_storage import FileStorage


class Dcm2Nii(AideOperator):

    def process(self, context: OperatorContext):
        file_manager = FileStorage(context)
        origin_dicom = context.origin

        dcm_path = context.origin.file_path  # basically dcm_path should = /mnt/aide_data/DICOM
        nii_path = ''                        # somewhere in the container (e.g: /mnt/nifti_data ?)

        subprocess.run(["dcm2niix", "-z", "y", "-o", nii_path, "-f", "%t_%v_%s_%p", dcm_path])

        # not sure what to do here
        # - load the nifti files in variable result_nii and send to Resource below?

        result_nii = Resource(format="nifti", content_type="result_nii", file_path=dcm_path)  # file_path=dcm_path or file_path=nii_path?
        context.add_resource(result_nii)
        return context