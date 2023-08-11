# 3D Fetal Brain MRI reconstruction AIDE app

[AIDE](https://www.aicentre.co.uk/platforms#view1) is an open-source platform for the deployment of AI applications in healthcare settings.

This repo led by Dr Tom Roberts packages automated 3D Fetal Brain MRI reconstruction into a [MONAI Application Package (MAP)](https://github.com/Project-MONAI/monai-deploy) for execution on AIDE.

## Developers

### Testing

```shell
# Setup monai-deploy-sdk venv
python -m venv venv
pip install requirements.txt
source venv/bin/activate

# Test MAP code with Python
# input - 2D multi-stack DICOM files
# output – 3D SVR reconstruction
python app -i input/ -o output/

# Test MAP code via monai-deploy
monai-deploy exec app -i input/ -o output/
```

### Build & Test MAP

Note: currently need two stage process: construct initial MAP, then build on top of this containe

```shell
# Build & push initial MAP
monai-deploy package app --tag fetalsvrtk/aide:map-test -l DEBUG
docker push fetalsvrtk/aide:map-test

# Build on top of MAP & push final MAP
docker build -t fetalsvrtk/aide:map app/
docker push fetalsvrtk/aide:map

# To test MAP
monai-deploy run fetalsvrtk/aide:map input/ output/

# To enter MAP for testing (nb: DGX paths)
docker run -it --rm -v /home/troberts/code/aide-svrtk/input/nii_stacks:/home/recon --entrypoint /bin/bash fetalsvrtk/aide:map
```
