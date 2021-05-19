FROM python
RUN git clone https://github.com/sepandhaghighi/penney.git
RUN cd penney && pip install -r requirements.txt && python setup.py install
ENTRYPOINT ["python","-m","penney"]
