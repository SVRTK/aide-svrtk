import copy
import os

from aide_sdk.inference.aideoperator import AideOperator
from aide_sdk.model.dicom_image import DicomImage
from aide_sdk.model.dicom_series import DicomSeries
from aide_sdk.model.operatorcontext import OperatorContext
from aide_sdk.model.resource import Resource
from aide_sdk.utils.file_storage import FileStorage
from reportlab.pdfgen.canvas import Canvas


class Dcm2Nii(AideOperator):

    def process(self, context: OperatorContext):
        # origin_dicom = context.origin
        #
        # result = my_cool_stuff(origin_dicom)  # Your magic goes here
        #
        # file_manager = FileStorage(context)
        # path = file_manager.save_dicom("my_results", result)
        #
        # result_dicom = Resource(format="dicom", content_type="result", file_path=path)
        # context.add_resource(result_dicom)
        # return context

        file_manager = FileStorage(context)

        # load
        dcmImageFile = r'/mnt/aide_data/DICOM/IM_0001'
        dcmImage = DicomImage(dcmImageFile)
        dcmData = dcmImage.load_dataset()

        print(dcmImageFile)
        print(dcmData.pixel_array.shape)

        canvas = Canvas('report.pdf')
        canvas.drawString(300, 300, dcmImageFile)
        canvas_pdf_data = canvas.getpdfdata()
        file_path = file_manager.save_file(canvas_pdf_data, 'report.pdf')
        context.add_resource(Resource(format='pdf', content_type='pixel_mean', file_path=file_path))
        return context