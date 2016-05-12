FROM tomdymond/xenial-armv7l
COPY ./98C1A6920E0CE4DC.gpgkey /tmp/98C1A6920E0CE4DC.gpgkey
RUN useradd --create-home appuser
COPY ./appuser.sudo /etc/sudoers.d/appuser
COPY ./start.sh /opt/start.sh
COPY ./interfaces /etc/network/interfaces
RUN chmod 755 /opt/start.sh
RUN mkdir /var/log/piricohmoto && chown appuser /var/log/piricohmoto
RUN apt-key add /tmp/98C1A6920E0CE4DC.gpgkey
COPY ./sources.list /etc/apt/sources.list
COPY ./ubuntu-pi-flavour-makers-ubuntu-ppa-xenial.list /etc/apt/sources.list.d/ubuntu-pi-flavour-makers-ubuntu-ppa-xenial.list
RUN apt-get update && apt-get -y install --no-install-recommends \
  supervisor \
  git vim less \
  python-redis python-yaml python-flask python-pil python-pip python-pyexiv2 python-gps python-smbus python-setuptools \
  redis-server gpsd-clients nginx wireless-tools wpasupplicant net-tools ifupdown isc-dhcp-client \
  && rm -rf /var/cache/apt
RUN pip install --upgrade pip
RUN pip install piglow requests dropbox sh ipython

COPY ./etc/supervisor/piricohmotoServiceMain /etc/supervisor/conf.d/piricohmotoServiceMain.conf
COPY ./etc/supervisor/piricohmotoServiceLogger /etc/supervisor/conf.d/piricohmotoServiceLogger.conf
COPY ./etc/supervisor/piricohmotoServiceNotifier /etc/supervisor/conf.d/piricohmotoServiceNotifier.conf

RUN git clone https://github.com/tomdymond/pi-python-ricohgr /opt/pi-python-ricohgr
RUN cd /opt/pi-python-ricohgr && git checkout devel && chmod -R 755 ./bin/
CMD /opt/start.sh
