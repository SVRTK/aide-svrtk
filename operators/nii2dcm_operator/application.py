import os, glob, subprocess

from aide_sdk.inference.aideoperator import AideOperator
from aide_sdk.model.operatorcontext import OperatorContext
from aide_sdk.model.resource import Resource
from aide_sdk.utils.file_storage import FileStorage


class Nii2Dcm(AideOperator):

    def process(self, context: OperatorContext):
        file_manager = FileStorage(context)
        dicom_study = context.origin

        dcm_path = dicom_study.file_path  # basically dcm_path should = /mnt/aide_data/DICOM
        nii_path = ''                     # output nii directory in container - conventionally, we use: /home/recon/
        dcm_3d_path = ''                  # path which will contain 3D SVR DICOMs

        # Create single-frame 3D DICOM files using original 2D DICOMs and 3D SVR-output.nii.gz file
        # svr_nii2dcm.py
        # subprocess.run(["svr_make_dicomdir.bash])

        result_3d_dicom = Resource(format="dicom", content_type="result_nii", file_path=nii_path)
        context.add_resource(result_nii)
        return context