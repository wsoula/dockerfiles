FROM python:3.10-bullseye
# Install base packages
RUN apt update && apt upgrade -y
# Install exrex
ENV install_dir=/var/tmp/mimicmania
#RUN git clone https://github.com/asciimoo/exrex $install_dir && ls $install_dir
WORKDIR $install_dir
RUN pip install exrex
# Below step is 6 GB so only do this for caching purposes
#RUN python setup.py
#RUN pip install -r requirements
ENTRYPOINT ["exrex"]
