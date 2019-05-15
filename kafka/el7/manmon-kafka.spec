%define kafka_scala_ver 2.12
%define services "manmon-auth manmon-pkg manmon-mib manmon-web manmon-uploader"
Summary: Manmon Kafka
Name: manmon-kafka
Version: 2.2.0
Release: 1
License: GPLv3
URL: http://manmon.net
Group: System
Packager: Tomi Malkki
Requires: java-1.8.0-openjdk-headless
Source0: http://www.nic.funet.fi/pub/mirrors/apache.org/kafka/%{version}/kafka_%{kafka_scala_ver}-%{version}.tgz
Source1: https://raw.githubusercontent.com/manmon-net/manmon-rpm-dev/master/rpm/el7/server.properties
Source2: https://raw.githubusercontent.com/manmon-net/manmon-rpm-dev/master/rpm/el7/zookeeper.properties
Source3: https://raw.githubusercontent.com/manmon-net/manmon-rpm-dev/master/rpm/el7/manmon-zookeeper.service
Source4: https://raw.githubusercontent.com/manmon-net/manmon-rpm-dev/master/rpm/el7/manmon-kafka.service
BuildRoot: ~/rpmbuild/

%description
Manmon suite Kafka

%install
mkdir -p ~/rpmbuild/BUILDROOT/%{name}-%{version}-%{release}.x86_64/home/manmon-kafka/
cd ~/rpmbuild/BUILDROOT/%{name}-%{version}-%{release}.x86_64/home/manmon-kafka/
tar xzf %{SOURCE0}
ln -s /home/manmon-kafka/kafka_%{kafka_scala_ver}-%{version}/ kafka
rm -f ~/rpmbuild/BUILDROOT/%{name}-%{version}-%{release}.x86_64/home/manmon-kafka/kafka_%{kafka_scala_ver}-%{version}/config/server.properties
cp -p %{SOURCE1} ~/rpmbuild/BUILDROOT/%{name}-%{version}-%{release}.x86_64/home/manmon-kafka/kafka_%{kafka_scala_ver}-%{version}/config/server.properties
rm -f ~/rpmbuild/BUILDROOT/%{name}-%{version}-%{release}.x86_64/home/manmon-kafka/kafka_%{kafka_scala_ver}-%{version}/config/zookeeper.properties
cp -p %{SOURCE2} ~/rpmbuild/BUILDROOT/%{name}-%{version}-%{release}.x86_64/home/manmon-kafka/kafka_%{kafka_scala_ver}-%{version}/config/zookeeper.properties
mkdir -p ~/rpmbuild/BUILDROOT/%{name}-%{version}-%{release}.x86_64/usr/lib/systemd/system
cp -p %{SOURCE3} ~/rpmbuild/BUILDROOT/%{name}-%{version}-%{release}.x86_64/usr/lib/systemd/system/
cp -p %{SOURCE4} ~/rpmbuild/BUILDROOT/%{name}-%{version}-%{release}.x86_64/usr/lib/systemd/system/

%pre
if ! id -u 'manmon-kafka' > /dev/null 2>&1; then
  adduser -m manmon-kafka
fi
if [ "$1" -eq 2 ]
then
  if systemctl -q is-active manmon-kafka
  then
    systemctl -q stop manmon-kafka
    sleep 3
  fi
  if systemctl -q is-active manmon-zookeeper
  then
    systemctl -q stop manmon-zookeeper
  fi
fi

%post
if [ `grep -c "manmon-kafka$" /etc/hosts` -eq 0 ]
then
  echo "127.0.0.1 manmon-kafka" >> /etc/hosts
fi
if [ `grep -c "manmon-zookeeper$" /etc/hosts` -eq 0 ]
then
  echo "127.0.0.1 manmon-zookeeper" >> /etc/hosts
fi
systemctl -q daemon-reload
systemctl -q enable manmon-kafka
systemctl -q enable manmon-zookeeper
systemctl -q start manmon-zookeeper
sleep 3
systemctl -q start manmon-kafka

%preun
if [ "$1" -eq 0 ]
then
  if systemctl -q is-active manmon-kafka
  then
    systemctl -q stop manmon-kafka
    sleep 3
  fi
  if systemctl -q is-active manmon-zookeeper
  then
    systemctl -q stop manmon-zookeeper
  fi
fi



%clean
rm -rf %{buildroot} 

%files
/home/manmon-kafka/kafka
/home/manmon-kafka/kafka_%{kafka_scala_ver}-%{version}
/usr/lib/systemd/system/
