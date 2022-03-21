FROM pytorch/pytorch:1.9.0-cuda11.1-cudnn8-devel

WORKDIR /home

# Install general libraries
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y \
	git wget curl unzip

# Install libraries required by MIRTK and SVRTK
RUN apt-get install -y \
	build-essential \
	cmake \
	cmake-curses-gui \
	libboost-all-dev \
	libeigen3-dev \
	libtbb-dev \
	libfltk1.3-dev

# Install MIRTK/SVRTK
RUN git clone https://github.com/SVRTK/MIRTK.git \
    && mkdir -p /home/MIRTK/Packages/SVRTK
RUN git clone https://github.com/SVRTK/SVRTK.git /home/MIRTK/Packages/SVRTK \
    && mkdir -p /home/MIRTK/build \
	&& cd /home/MIRTK/build \
	&& cmake -D WITH_TBB="ON" -D MODULE_SVRTK="ON" .. \
	&& make -j

ENV PATH="$PATH:/home/MIRTK/build/bin:/home/MIRTK/build/lib/tools"

# Setup 3D UNet models
RUN git clone https://github.com/SVRTK/Segmentation_FetalMRI.git --branch svrtk-docker-gpu-0.10 --single-branch /home/Segmentation_FetalMRI

RUN wget https://gin.g-node.org/SVRTK/fetal_mri_network_weights/raw/master/checkpoints-brain-loc-2-labels/latest.ckpt -P /home/Segmentation_FetalMRI/trained-models/checkpoints-brain-loc-labels \
    && wget https://gin.g-node.org/SVRTK/fetal_mri_network_weights/raw/master/checkpoints-brain-loc-2-labels-cropped/latest.ckpt -P /home/Segmentation_FetalMRI/trained-models/checkpoints-brain-loc-labels-cropped \
    && wget https://gin.g-node.org/SVRTK/fetal_mri_network_weights/raw/master/checkpoints-brain-reo-5-labels/latest.ckpt -P /home/Segmentation_FetalMRI/trained-models/checkpoints-brain-reorientation \
    && wget https://gin.g-node.org/SVRTK/fetal_mri_network_weights/raw/master/checkpoints-brain-reo-5-labels-raw-stacks/latest.ckpt -P /home/Segmentation_FetalMRI/trained-models/checkpoints-brain-reorientation-stacks

# Install Python packages
RUN python -m pip install -r /home/Segmentation_FetalMRI/requirements.txt

COPY docker-recon-brain-auto.bash /home/scripts/docker-recon-brain-auto.bash
RUN mkdir -p /home/recon \
    && mkdir -p /home/output \
    && chmod +x /home/scripts/*

# AIDE SDK files
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY main.py main.py
COPY application.py application.py
COPY manifest.json manifest.json

CMD ["python", "main.py"]
