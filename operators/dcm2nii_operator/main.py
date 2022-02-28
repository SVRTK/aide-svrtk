from aide_sdk.application import AideApplication
from application import Dcm2Nii

if __name__ == "__main__":
    AideApplication.start(operator=Dcm2Nii())
