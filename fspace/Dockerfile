FROM alpine
WORKDIR /app
RUN apk add git build-base
RUN git clone https://github.com/Mandrew0822/fspace && cd fspace
WORKDIR /app/fspace
RUN chmod +x install.sh && ./install.sh
ENTRYPOINT fspace
#ENTRYPOINT /app/fspace/install.sh
# Install base packages
#RUN apt update && apt upgrade -y
#RUN apt-get install -y git ffmpeg espeak-ng espeak
# Install MimicMania
#ENV install_dir=/var/tmp/mimicmania
#RUN git clone https://github.com/everydaycodings/mimicmania $install_dir && ls $install_dir
#WORKDIR $install_dir
#RUN pip install requests tqdm
#RUN pip install -r requirements.txt
# Below step is 6 GB so only do this for caching purposes
#RUN python setup.py
#RUN pip install -r requirements
#ENTRYPOINT ["streamlit", "run", "app.py"]
# Running just the binary, no config
#ENTRYPOINT ["sh", "-c", "$install_dir/seashells-server"]
