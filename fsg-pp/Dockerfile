FROM python
# Install base packages
RUN apt update && apt upgrade -y
WORKDIR /var/tmp/
RUN git clone https://github.com/EngMarchG/fsg-pp
WORKDIR /var/tmp/fsg-pp
# Remove interactive component of installation
RUN sed -i "s/read -p \"Press any key to close the window...\"//g" installation.sh
RUN cat installation.sh
RUN chmod 755 installation.sh && chmod 755 launcher.sh
RUN bash installation.sh
# Required Dependency
RUN apt install -y libgl1
# Make available
#RUN sed -i "s/demo.launch()/demo.launch(listen=True)/g" Fsg_pp.py
RUN sed -i "s/demo.launch()/demo.launch(server_name=\"0.0.0.0\")/g" Fsg_pp.py
ENTRYPOINT ["/var/tmp/fsg-pp/launcher.sh"]
