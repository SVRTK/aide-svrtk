from aide_sdk.application import AideApplication
from application import Nii2Dcm

if __name__ == "__main__":
    AideApplication.start(operator=Nii2Dcm())
