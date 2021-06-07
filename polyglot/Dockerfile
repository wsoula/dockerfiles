FROM python
RUN pip install python-polyglot
#ENTRYPOINT ["polyglot","/tmp/polyglot"]
RUN echo "from polyglot.core import Polyglot" > /tmp/run_polyglot.py
RUN echo "polyglot = Polyglot('/tmp/polyglot')" >> /tmp/run_polyglot.py
RUN echo "polyglot.show(display=True)" >> /tmp/run_polyglot.py
# Below entrypoint will give information on the file passed
#ENTRYPOINT ["polyglot"]
# Below entrypoint will give programming languages in project mounted at /tmp/polyglot
ENTRYPOINT ["python","/tmp/run_polyglot.py"]
