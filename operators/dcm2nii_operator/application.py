import os, glob, subprocess

from aide_sdk.inference.aideoperator import AideOperator
from aide_sdk.model.operatorcontext import OperatorContext
from aide_sdk.model.resource import Resource
from aide_sdk.utils.file_storage import FileStorage


class Dcm2Nii(AideOperator):

    def process(self, context: OperatorContext):
        file_manager = FileStorage(context)
        dicom_study = context.origin

        dcm_path = dicom_study.file_path  # basically dcm_path should = /mnt/aide_data/DICOM
        nii_path = ''                     # output nii directory in container - conventionally, we use: /home/recon/

        subprocess.run(["dcm2niix", "-z", "y", "-o", nii_path, "-f", "stack-%s", dcm_path])

        # Delete superfluous .json files
        json_files = glob.glob(nii_path + "/*.json")
        for json_file in json_files:
            os.remove(json_file)

        result_nii = Resource(format="nifti", content_type="result_nii", file_path=nii_path)
        context.add_resource(result_nii)
        return context