FROM python:3.10.3 as environment

RUN apt update && apt install -y ffmpeg libsm6 libxext6 libgdal-dev=3.2.2+dfsg-2+deb11u1
ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal
ENV QT_QPA_PLATFORM offscreen
COPY requirements.txt .
RUN pip install -r requirements.txt
# Outside of requirements due to problems with setuptools
RUN pip install GDAL==3.2.2

CMD ["/bin/bash"]


FROM environment as make_test

WORKDIR /app
# Add data
RUN mkdir data && wget -O data/data.zip https://urjc-my.sharepoint.com/:u:/g/personal/d_correas_2016_alumnos_urjc_es/EdLVog_IJA5Fq71O8tTwpHYBHql0oVRF0fzYnwnoWck2fQ?download=1
RUN unzip data/data.zip -d data
RUN rm data/data.zip
# Add project
COPY . .
WORKDIR /app/test
RUN python ./*.py


FROM scratch AS test
COPY --from=make_test /app/test/results .


FROM environment as deploy
WORKDIR /app/src
COPY ./src .

ENTRYPOINT [ "python", "Principal.py" ]
