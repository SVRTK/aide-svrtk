FROM python:3.9.5

RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y \
	git build-essential cmake pigz

RUN git clone https://github.com/rordenlab/dcm2niix.git --branch master --single-branch \
	&& cd dcm2niix \
	&& mkdir build && cd build \
	&& cmake .. \
	&& make

ENV PATH="$PATH:/dcm2niix/build/bin"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY main.py main.py
COPY application.py application.py
COPY manifest.json manifest.json

CMD ["python", "main.py"]