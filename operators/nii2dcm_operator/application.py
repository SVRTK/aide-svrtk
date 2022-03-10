import os

from aide_sdk.inference.aideoperator import AideOperator
from aide_sdk.model.operatorcontext import OperatorContext
from aide_sdk.model.resource import Resource
from aide_sdk.utils.file_storage import FileStorage


class Nii2Dcm(AideOperator):

    def process(self, context: OperatorContext):
        file_manager = FileStorage(context)

        dicom_study = context.origin
        dcm_stacks_path = dicom_study.file_path

        nii_3d_resource = next(context.get_resources_by_type(format='nifti', content_type='nii_3d'))
        nii_3d_path = nii_3d_resource.file_path  # folder because added as folder in previous app

        dcm_3d_path = os.path.join(file_manager.mount_point, file_manager.write_location, 'dcm_3d')

        # create 3D dicom
        # TODO:
        #  - adjust svr_nii2dcm.py to use AIDE-SDK dicom creator
        #  - make svr_nii2dcm.py function to take inputs: (dcm_stacks_path, nii_3d_path, dcm_3d_path)

        result_dcm_3d = Resource(format="dicom", content_type="result", file_path=dcm_3d_path)
        context.add_resource(result_dcm_3d)
        return context
