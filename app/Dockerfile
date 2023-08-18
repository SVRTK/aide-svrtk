FROM fetalsvrtk/aide:map-test AS build

# Add dcm2niix to MAP
WORKDIR /bin

RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y \
	git build-essential cmake pigz

RUN git clone https://github.com/rordenlab/dcm2niix.git --branch master --single-branch \
	&& cd dcm2niix \
	&& mkdir build && cd build \
	&& cmake .. \
	&& make

ENV PATH="$PATH:/bin/dcm2niix/build/bin"

WORKDIR /var/monai


# Add SVRTK to MAP

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

WORKDIR /var/monai


# Add 3D UNet model weights & execution script

WORKDIR /home

# Setup 3D UNet models
RUN git clone https://github.com/SVRTK/Segmentation_FetalMRI.git --branch svrtk-docker-gpu-0.10 --single-branch /home/Segmentation_FetalMRI

RUN wget https://gin.g-node.org/SVRTK/fetal_mri_network_weights/raw/master/checkpoints-brain-loc-2-labels/latest.ckpt -P /home/Segmentation_FetalMRI/trained-models/checkpoints-brain-loc-labels \
    && wget https://gin.g-node.org/SVRTK/fetal_mri_network_weights/raw/master/checkpoints-brain-loc-2-labels-cropped/latest.ckpt -P /home/Segmentation_FetalMRI/trained-models/checkpoints-brain-loc-labels-cropped \
    && wget https://gin.g-node.org/SVRTK/fetal_mri_network_weights/raw/master/checkpoints-brain-reo-5-labels/latest.ckpt -P /home/Segmentation_FetalMRI/trained-models/checkpoints-brain-reorientation \
    && wget https://gin.g-node.org/SVRTK/fetal_mri_network_weights/raw/master/checkpoints-brain-reo-5-labels-raw-stacks/latest.ckpt -P /home/Segmentation_FetalMRI/trained-models/checkpoints-brain-reorientation-stacks

# Install Python packages
RUN python -m pip install -r /home/Segmentation_FetalMRI/requirements.txt

# Bugfix: without below, cannot import torch within Python
# Error: OSError: /opt/hpcx/ompi/lib/libmpi.so.40: undefined symbol: opal_hwloc201_hwloc_get_type_depth
# Fix: https://forums.developer.nvidia.com/t/issues-building-docker-image-from-ngc-container-nvcr-io-nvidia-pytorch-22-py3/209034/5
ENV PATH="${PATH}:/opt/hpcx/ompi/bin"
ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/opt/hpcx/ompi/lib"

COPY operators/docker-recon-brain-auto.bash /home/scripts/docker-recon-brain-auto.bash
RUN mkdir -p /home/recon \
    && mkdir -p /home/output \
    && chmod +x /home/scripts/*

WORKDIR /var/monai
