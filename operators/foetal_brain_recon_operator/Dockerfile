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

## Install MIRTK/SVRTK
RUN git clone https://github.com/SVRTK/MIRTK.git
RUN mkdir -p /home/MIRTK/Packages/SVRTK
RUN git clone https://github.com/SVRTK/SVRTK.git /home/MIRTK/Packages/SVRTK
RUN mkdir -p /home/MIRTK/build \
	&& cd /home/MIRTK/build \
	&& cmake -D WITH_TBB="ON" -D MODULE_SVRTK="ON" .. \
	&& make -j

ENV PATH="$PATH:/home/MIRTK/build/bin:/home/MIRTK/build/lib/tools"

## Setup 3D UNet models
RUN git clone https://github.com/SVRTK/Segmentation_FetalMRI.git /home/Segmentation_FetalMRI
RUN git checkout -b dev 76f8fb9f8d4503943c98bb43f8bb3e6f122b2926

#COPY requirements.txt requirements.txt
#RUN pip install -r requirements.txt
#
#COPY main.py main.py
#COPY application.py application.py
#COPY manifest.json manifest.json
#
#CMD ["python", "main.py"]