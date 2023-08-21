<!-- PROJECT HEADING -->
<br />
<p align="center">
<h1 align="center">aide-svrtk</h1>
<p align="center">
  AI-driven, automated <a href="https://github.com/SVRTK/SVRTK">SVR reconstruction</a> packaged as an AIDE Application, based on 
  the open-source <a href="https://github.com/Project-MONAI/monai-deploy/blob/main/guidelines/monai-application-package.md">
  MONAI Application Package (MAP)</a> standard.
  <br />
  <br />
  <a href="https://github.com/SVRTK/aide-svrtk/">View repo</a>
  ·
  <a href="https://github.com/SVRTK/aide-svrtk/issues">Report Bug</a>
  ·
  <a href="https://github.com/SVRTK/aide-svrtk/issues">Request Feature</a>
  <br />
</p>

## Overview

The slice-to-volume reconstruction toolkit ([SVRTK](https://github.com/SVRTK/SVRTK)) is an image-based registration 
framework for reconstruction of 3D volumes from multiple 2D image slices. SVRTK is used extensively for performing 
motion-corrected reconstruction of MRI data. 

Currently, this MAP implements SVRTK for reconstruction of 2D **fetal brain MRI** data into motion-corrected 3D volumes. 
Further MAPs for reconstruction of other fetal organs are in development and coming soon.

[AIDE](https://www.aicentre.co.uk/platforms#view1) is an open-source platform for the deployment of AI applications in 
healthcare settings. This repo, created and led by [Tom Roberts](https://github.com/tomaroberts), packages automated 
3D fetal brain MRI reconstruction into a [MONAI Application Package (MAP)](https://github.com/Project-MONAI/monai-deploy) 
for execution on AIDE, and other platforms compatible with the MAP standard.

## aide-svrtk MAP workflow

The input to the aide-svrtk MAP is multiple 2D DICOM Series, each containing multi-slice 2D MRI data. The output is a 3D
MRI DICOM Series contained the motion-corrected reconstruction.

The aide-svrtk MAP consists of three operators:
1. `dcm2nii_operator.py` – converts the input 2D MRI DICOM Series into NIfTI format required by SVRTK, using 
[dcm2niix](https://github.com/rordenlab/dcm2niix)
2. `fetal_mri_3d_brain_recon_operator.py` – runs automated fetal brain SVRTK reconstruction, in three main steps:
   a. AI-driven brain masking 
   b. Slice-to-volume registration reconstruction
   c. AI-driven brain reorientation
3. `nii2dcm_operator.py` – converts the SVRTK output NIfTI into a 3D DICOM Series, using 
[nii2dcm](https://github.com/tomaroberts/nii2dcm)

## Developers

### Prerequisites
- GPU-enabled machine
- Docker
   - Required for running the MAP

## Setup

1. Download
```shell
git clone https://github.com/SVRTK/aide-svrtk.git
```

2. Setup virtual env
```shell
cd aide-svrtk

python -m venv venv
source venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

3. Create `input` and `output` directories
```shell
mkdir input output
```

## Run MAP source code with MONAI Deploy

1. Ensure Python venv running
2. Copy DICOM Series files to `input/` directory
   - Standard or Enhanced DICOMs

```shell
# input - 2D multi-stack DICOM Series files
# output – 3D SVRTK-reconstructed DICOM Series
monai-deploy exec app -i input/ -o -output/
```

## Build and run as MONAI Application Package (MAP)

1. Ensure Python venv running
2. Ensure Docker running
3. Copy DICOM Series files within `input/` directory

_Important:_ we create an initial MAP `map-init` upon which we build any 3rd-party non-Python software (e.g. dcm2niix). 
The final MAP is called `map`

```shell
# Initial packaging of MAP
monai-deploy package app -t ghcr.io/svrtk/aide-svrtk/map-init:0.1.0 -r requirements.txt -l DEBUG

# Build 3rd-party software on top of MAP
docker build -t ghcr.io/svrtk/aide-svrtk/map:0.1.0 app/

# Test MAP with MONAI Deploy
monai-deploy run ghcr.io/svrtk/aide-svrtk/map:0.1.0 input/ output/

# Push initial MAP and final MAP to GHCR
docker push ghcr.io/svrtk/aide-svrtk/map-init:0.1.0
docker push ghcr.io/svrtk/aide-svrtk/map:0.1.0
```

## Optional

Enter Docker container for testing

```shell
docker run --gpus all -it --rm -v local/path/to/aide-svrtk/input:/var/monai/input/ --entrypoint /bin/bash ghcr.io/svrtk/aide-svrtk/map:0.1.0
```

Run on specified GPU if machine has >1 available

```shell
CUDA_VISIBLE_DEVICES=2 monai-deploy run ghcr.io/svrtk/aide-svrtk/map:0.1.0 input/ output/
```

## Running on AIDE
To run aide-svrtk MAP on AIDE, two files from the `app/workflows` directory are required, namely:
- `fetal-3d-brain-mri.json` – AIDE Clinical Workflow file.
  - Effectively a sequence of tasks run on AIDE
- `fetal-brain-3d-recon-argo-template.yaml` – Argo Workflow Template file.
  - Called by the AIDE Clinical Workflow file. Executes the aide-svrtk MAP using Argo. This is the central task within 
  the AIDE Clinical Workflow file.
