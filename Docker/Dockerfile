FROM tomdymond/xenial-armv7l
COPY ./98C1A6920E0CE4DC.gpgkey /tmp/98C1A6920E0CE4DC.gpgkey
RUN useradd --create-home appuser
COPY ./appuser.sudo /etc/sudoers.d/appuser
COPY ./start.sh /opt/start.sh
COPY ./interfaces /etc/network/interfaces
RUN chmod 755 /opt/start.sh
RUN apt-key add /tmp/98C1A6920E0CE4DC.gpgkey
COPY ./sources.list /etc/apt/sources.list
COPY ./ubuntu-pi-flavour-makers-ubuntu-ppa-xenial.list /etc/apt/sources.list.d/ubuntu-pi-flavour-makers-ubuntu-ppa-xenial.list
RUN apt-get update && apt-get -y install --no-install-recommends libexiv2-dev python-redis python-yaml python-flask python-pil git vim python-pip python-pyexiv2 monit redis-server gpsd gpsd-clients python-gps python-smbus python-setuptools nginx wireless-tools wpasupplicant net-tools ifupdown isc-dhcp-client && rm -rf /var/cache/apt
RUN pip install piglow requests dropbox sh ipython python-daemon

COPY ./monit/redis /etc/monit/conf-available/redis
COPY ./monit/gpsd /etc/monit/conf-available/gpsd
COPY ./monit/gr /etc/monit/conf-available/gr
COPY ./monit/gpslogger /etc/monit/conf-available/gpslogger

RUN ln -s /etc/monit/conf-available/redis /etc/monit/conf-enabled/redis
RUN ln -s /etc/monit/conf-available/gr /etc/monit/conf-enabled/gr
RUN ln -s /etc/monit/conf-available/gpsd /etc/monit/conf-enabled/gpsd
RUN ln -s /etc/monit/conf-available/gpslogger /etc/monit/conf-enabled/gpslogger

RUN git clone https://github.com/tomdymond/pi-python-ricohgr /opt/pi-python-ricohgr
RUN cd /opt/pi-python-ricohgr && git checkout devel && chmod -R 755 ./bin/
CMD su -m appuser -c /opt/start.sh
