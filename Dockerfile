FROM python:3.10.3 as environment

RUN apt update && apt install -y ffmpeg libsm6 libxext6 libgdal-dev=3.2.2+dfsg-2+deb11u1
ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal
COPY requirements.txt .
RUN xargs -n 1 pip install < requirements.txt

CMD ['/bin/bash']
