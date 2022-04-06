FROM python:3.10.3 as environment

RUN apt update && apt install -y ffmpeg libsm6 libxext6 libgdal-dev=3.2.2+dfsg-2+deb11u1
ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal
ENV QT_QPA_PLATFORM offscreen
COPY requirements.txt .
RUN xargs -n 1 pip install < requirements.txt

CMD ['/bin/bash']

FROM environment as test

WORKDIR /app
COPY . .
# Add data
RUN gdown --folder "https://drive.google.com/drive/folders/1Ey2Gqbc6ZLqrLN8X1DMXFGKI48vYWFrJ"
RUN python -m unittest test/*
