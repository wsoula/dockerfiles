FROM python
ENV version=0.4
WORKDIR /var/tmp/nafas/nafas-${version}
RUN cd ../ && curl -Lo nafas-${version}.zip https://github.com/sepandhaghighi/nafas/archive/v${version}.zip && unzip nafas-${version}.zip
RUN pip install -r requirements.txt
RUN python3 setup.py install
ENTRYPOINT ["python3","-m","nafas"]
