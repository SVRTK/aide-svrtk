from aide_sdk.application import AideApplication
from application import FoetalBrainReconstructor

if __name__ == "__main__":
    AideApplication.start(operator=FoetalBrainReconstructor())
