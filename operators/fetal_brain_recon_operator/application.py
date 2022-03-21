import os
import subprocess

from aide_sdk.inference.aideoperator import AideOperator
from aide_sdk.model.operatorcontext import OperatorContext
from aide_sdk.model.resource import Resource
from aide_sdk.utils.file_storage import FileStorage


class FetalBrainReconstructor(AideOperator):

    def process(self, context: OperatorContext):
        file_manager = FileStorage(context)

        nii_stacks_resource = context.get_resources_by_type(format="nifti", content_type="nii_stacks")
        nii_stacks_path = nii_stacks_resource.file_path     # Folder because added as folder in previous app
        nii_3d_path = os.path.join(file_manager.mount_point, file_manager.write_location, 'nii_3d')

        subprocess.run(["/home/scripts/docker-recon-brain-auto.bash", nii_stacks_path, "-1", "-1"])

        result_nii_3d = Resource(format="nifti", content_type="nii_3d", file_path=nii_3d_path)
        context.add_resource(result_nii_3d)
        return context
