## To build on CentOS 7 & RHEL 7
wget https://raw.githubusercontent.com/manmon-net/manmon-rpm-dev/master/rpm/el7/manmon-kafka.spec

rpmbuild --undefine=_disable_source_fetch -ba manmon-kafka.spec
