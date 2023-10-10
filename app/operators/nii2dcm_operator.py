# nii2dcm_operator
#
# Convert NIfTI output from SVRTK into a 3D DICOM dataset using nii2dcm
#

import logging
import os
from nii2dcm.run import run_nii2dcm
import pydicom as pyd
from pathlib import Path

import monai.deploy.core as md
from monai.deploy.core import DataPath, ExecutionContext, InputContext, IOType, Operator, OutputContext


@md.input("svrtk_output", DataPath, IOType.DISK)
@md.input("dcm_input", DataPath, IOType.DISK)
@md.output("dicom_3d_files", DataPath, IOType.DISK)
@md.env(pip_packages=["pydicom >= 2.3.0, nii2dcm >= 0.1.1"])
class NiftiToDicomWriterOperator(Operator):
    """
    DicomWriterOperator - converts a NIfTI file to DICOM MR Image dataset using nii2dcm
    """

    @staticmethod
    def determine_first_acquired_series(dcm_files):
        """
        Determine which DICOM Series from those supplied was acquired first and use as reference Series when copying
        pertinent DICOM attributes
        :return: dcm_ref_path – path to DICOM Series to use as reference
        """
        series_numbers = []
        for file in dcm_files[:]:
            try:
                dcm = pyd.dcmread(file)
                if 'MR' in dcm.Modality:
                    series_numbers.append(int(dcm.SeriesNumber))
            except:
                logging.warning(f"File {file} does not appear to be DICOM")
                dcm_files.remove(file)

        series_numbers_list_order = [i[0] for i in sorted(enumerate(series_numbers), key=lambda x: x[1])]

        dcm_ref_path = dcm_files[series_numbers_list_order[0]]

        return dcm_ref_path

    def compute(self, op_input: InputContext, op_output: OutputContext, context: ExecutionContext):

        logging.info(f"Begin {self.compute.__name__}")

        operator_workdir = os.getcwd()

        # final DICOM output path
        dcm_output_path = op_output.get().path

        # SVRTK output
        svrtk_output_filename = 'reo-DSVR-output-thorax.nii.gz'
        svrtk_output_path = op_input.get("svrtk_output").path
        svrtk_nii_path = Path(svrtk_output_path / svrtk_output_filename)
        logging.info(f"SVRTK output NIfTI found: {svrtk_nii_path}")

        # input DICOM files
        dcm_input_path = op_input.get("dcm_input").path
        dcm_files = [f for f in dcm_input_path.iterdir() if f.is_file()]  # TODO: add logic to find specific stack
        for d in dcm_files:
            logging.info(f"Original input DICOM file found: {d}")

        # determine first acquired series to use as reference DICOM dataset (dcm_ref) for metadata transferal
        dcm_ref_path = self.determine_first_acquired_series(dcm_files)
        logging.info(f"DICOM file selected as reference for nii2dcm conversion: {dcm_ref_path}")

        # run nii2dcm
        logging.info("Performing NIFTI to DICOM conversion ...")
        run_nii2dcm(
            svrtk_nii_path,
            dcm_output_path,
            dicom_type='SVR',
            ref_dicom_file=dcm_ref_path,
        )
        logging.info(f"DICOM files written to: {dcm_output_path}")

        logging.info(f"End {self.compute.__name__}")
