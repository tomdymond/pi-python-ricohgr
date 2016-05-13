FROM tomdymond/xenial-armv7l
MAINTAINER Tom Dymond

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv 0E0CE4DC

COPY ./etc/apt/sources.list /etc/apt/sources.list

RUN echo "deb http://ppa.launchpad.net/ubuntu-pi-flavour-makers/ppa/ubuntu xenial main" | tee -a /etc/apt/sources.list.d/ubuntu-pi-flavour-makers-ubuntu-ppa-xenial.list

RUN apt-get update && apt-get -y install --no-install-recommends \
  supervisor \
  git vim less curl \
  python-redis python-yaml python-flask python-pil python-pip python-pyexiv2 python-gps python-smbus python-setuptools \
  redis-server gpsd-clients nginx wireless-tools wpasupplicant net-tools ifupdown isc-dhcp-client \
  && rm -rf /var/cache/apt
RUN pip install --upgrade pip
RUN pip install piglow requests dropbox sh ipython

COPY ./interfaces /etc/network/interfaces
RUN useradd --create-home appuser

COPY ./appuser.sudo /etc/sudoers.d/appuser
COPY ./start.sh /opt/start.sh
RUN chmod 755 /opt/start.sh
COPY ./etc/supervisor/piricohmotoServiceMain /etc/supervisor/conf.d/piricohmotoServiceMain.conf
COPY ./etc/supervisor/piricohmotoServiceLogger /etc/supervisor/conf.d/piricohmotoServiceLogger.conf
COPY ./etc/supervisor/piricohmotoServiceNotifier /etc/supervisor/conf.d/piricohmotoServiceNotifier.conf

RUN git clone https://github.com/tomdymond/pi-python-ricohgr /opt/pi-python-ricohgr
RUN cd /opt/pi-python-ricohgr && git checkout devel && chmod -R 755 ./bin/
CMD /opt/start.sh
