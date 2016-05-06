FROM tomdymond/xenial-armv7l
COPY ./98C1A6920E0CE4DC.gpgkey /tmp/98C1A6920E0CE4DC.gpgkey
RUN apt-key add /tmp/98C1A6920E0CE4DC.gpgkey
COPY ./sources.list /etc/apt/sources.list
COPY ./ubuntu-pi-flavour-makers-ubuntu-ppa-xenial.list /etc/apt/sources.list.d/ubuntu-pi-flavour-makers-ubuntu-ppa-xenial.list
RUN apt-get update && apt-get -y install libexiv2-dev python-redis python-yaml python-flask python-pil git vim python-pip python-pyexiv2
RUN pip install piglow requests dropbox sh
RUN git clone https://github.com/tomdymond/pi-python-ricohgr /opt/pi-python-ricohgr
RUN cd /opt/pi-python-ricohgr && git checkout devel && chmod 755 ./bin/gr.py
CMD /opt/pi-python-ricohgr/bin/gr.py
