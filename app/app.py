# AI-drived 3D fetal brain MRI reconstruction with SVRTK – MONAI Application Package (MAP)
#
# Tom Roberts (tom.roberts@gstt.nhs.uk / t.roberts@kcl.ac.uk)

import logging

class FetalMri3dBrainApp(Application):
    """
    Motion-corrected 3D fetal brain MRI Application class
    """

    name = "3d-fetal-brain-mri"
    description = "Motion-corrected 3D fetal brain MRI application."
    version = "0.1.0"

    def compose(self):
        """Operators go in here
        """


if __name__ == "__main__":
    App(do_run=True)