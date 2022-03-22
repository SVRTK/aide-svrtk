import os
import glob
import subprocess

from aide_sdk.inference.aideoperator import AideOperator
from aide_sdk.model.operatorcontext import OperatorContext
from aide_sdk.model.resource import Resource
from aide_sdk.utils.file_storage import FileStorage


class Dcm2Nii(AideOperator):

    def process(self, context: OperatorContext):
        file_manager = FileStorage(context)
        dicom_study = context.origin

        dcm_path = dicom_study.file_path
        # dcm_path = r'/Users/tr17/code/aide-svrtk/test_env/dcm_2d_dir'
        nii_path = os.path.join(file_manager.mount_point, file_manager.write_location, 'nii_stacks')
        os.mkdir(nii_path)

        subprocess.run(["dcm2niix", "-z", "y", "-o", nii_path, "-f", "stack-%s", dcm_path])

        # Delete superfluous .json files
        json_files = glob.glob(nii_path + "/*.json")
        for json_file in json_files:
            os.remove(json_file)

        result_nii_stacks = Resource(format="nifti", content_type="nii_stacks", file_path=nii_path)
        context.add_resource(result_nii_stacks)
        return context
