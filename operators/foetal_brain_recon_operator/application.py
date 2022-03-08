import subprocess

from aide_sdk.inference.aideoperator import AideOperator
from aide_sdk.model.operatorcontext import OperatorContext
from aide_sdk.model.resource import Resource
from aide_sdk.utils.file_storage import FileStorage


class FoetalBrainReconstructor(AideOperator):

    def process(self, context: OperatorContext):
        file_manager = FileStorage(context)

        # same nii_path as previous operator
        nii_path = ''

        subprocess.run(["/home/scripts/docker-recon-brain-auto.bash", nii_path, "1", "-1"])

        # At this point, nii_path will contain multiple files
        # Important result file = SVR-output.nii.gz
        # TBC – Either:
        # 1) SVR-output.nii.gz needs to be passed to next operator
        # OR:
        # 2) We pass nii_path folder again to next operator so can access all files within.

        result_nii = Resource(format="nifti", content_type="result_nii", file_path=nii_path)
        context.add_resource(result_nii)
        return context