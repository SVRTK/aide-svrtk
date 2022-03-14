from aide_sdk.application import AideApplication
from application import FetalBrainReconstructor

if __name__ == "__main__":
    AideApplication.start(operator=FetalBrainReconstructor())
