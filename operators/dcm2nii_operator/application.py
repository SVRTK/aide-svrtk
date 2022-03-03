import subprocess

from aide_sdk.inference.aideoperator import AideOperator
from aide_sdk.model.operatorcontext import OperatorContext
from aide_sdk.model.resource import Resource
from aide_sdk.utils.file_storage import FileStorage


class Dcm2Nii(AideOperator):

    def process(self, context: OperatorContext):
        file_manager = FileStorage(context)
        dicom_study = context.origin

        dcm_path = dicom_study.file_path  # basically dcm_path should = /mnt/aide_data/DICOM
        output_dir = ''                      # output directory in container (e.g: /mnt/nifti_data ?)

        subprocess.run(["dcm2niix", "-z", "y", "-o", output_dir, "-f", "%t_%v_%s_%p", dcm_path])

        result_nii = Resource(format="nifti", content_type="result_nii", file_path=output_dir)
        context.add_resource(result_nii)
        return context