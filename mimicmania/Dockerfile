FROM python:3.10-bullseye
# Install base packages
RUN apt update && apt upgrade -y
RUN apt-get install -y git ffmpeg espeak-ng espeak
# Install MimicMania
ENV install_dir=/var/tmp/mimicmania
RUN git clone https://github.com/everydaycodings/mimicmania $install_dir && ls $install_dir
WORKDIR $install_dir
#RUN pip install requests tqdm
RUN pip install -r requirements.txt
# Below step is 6 GB so only do this for caching purposes
RUN python setup.py
#RUN pip install -r requirements
ENTRYPOINT ["streamlit", "run", "app.py"]
# Running just the binary, no config
#ENTRYPOINT ["sh", "-c", "$install_dir/seashells-server"]
