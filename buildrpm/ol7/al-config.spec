Name: al-config
Version: 1.0
Release: 1.0.25%{?dist}
Summary: Configuration tasks for Autonomous Linux Oracle Linux instances running in Oracle Cloud Infrastructure
BuildArch: noarch

Group: Development/Tools
URL: http://cloud.oracle.com/iaas
License: UPL
Vendor: Oracle America

Source: %{name}-%{version}.tar.gz

Requires: uptrack
Requires: yum-cron
Requires: jq
Requires: openssl
Requires: python-oci-cli
Requires: python-oci-sdk
Requires: policycoreutils
Requires: selinux-policy
Buildrequires: checkpolicy policycoreutils-python

%description
This package contains configuration tasks for Autonomous Linux instances running in Oracle Cloud Infrastructure environment

%prep
%autosetup -p1

%build
### compile the selinux policy module
checkmodule -M -m -o omprog_exploit_detection.mod omprog_exploit_detection.te
semodule_package -o omprog_exploit_detection.pp -m omprog_exploit_detection.mod

%install
rm -rf %{buildroot}/*
cp -a install/*  %{buildroot}
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 0644 omprog_exploit_detection.pp %{buildroot}%{_datadir}/selinux/packages

%files

#/usr/lib
%dir %{_prefix}/lib/%{name}
%attr(644,root,root) %{_prefix}/lib/%{name}/functions
%attr(755,root,root) %{_prefix}/lib/%{name}/pre_config.sh
%attr(755,root,root) %{_prefix}/lib/%{name}/add_cron_job.sh
%attr(755,root,root) %{_prefix}/lib/%{name}/activate_known_exploit_detection.sh
%attr(644,root,root) %{_prefix}/lib/systemd/system/al-config.service
%attr(644,root,root) %{_prefix}/lib/systemd/system-preset/84-al.preset
#/usr/sbin
%attr(755,root,root) %{_sbindir}/al-config
%attr(755,root,root) %{_sbindir}/al-start
%attr(755,root,root) %{_sbindir}/al-update
%attr(755,root,root) %{_sbindir}/al-notify
%attr(755,root,root) %{_sbindir}/al-exploit-alert
#/usr/share
%attr(644,root,root) %{_datadir}/selinux/packages/omprog_exploit_detection.pp
#/etc
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/al.conf
%attr(644,root,root) %{_sysconfdir}/%{name}/yum-cron.conf
%attr(644,root,root) %{_sysconfdir}/logrotate.d/%{name}
%attr(644,root,root) %{_sysconfdir}/rsyslog.d/al-exploit-alert.conf
#/var
%dir %{_sharedstatedir}/%{name}

%license LICENSE

%post
# install or upgrade
%{_prefix}/lib/%{name}/pre_config.sh
%{_sbindir}/semodule -i %{_datadir}/selinux/packages/omprog_exploit_detection.pp
%systemd_post %{name}.service

%preun
# uninstall, not upgrade
if [ $1 -eq 0 ]; then
    rm -f %{_sysconfdir}/cron.d/al-update
    %{_sbindir}/semodule -r omprog_exploit_detection &>/dev/null
fi
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%posttrans

%changelog
* Fri Sep 6 2019 Frank Deng <frank.deng@oracle.com> - 1.0-1.0.25
- Log exploit attempt beforing sending notification

* Fri Sep 6 2019 Frank Deng <frank.deng@oracle.com> - 1.0-1.0.24
- Fix typos in output messages.

* Fri Sep 6 2019 Frank Deng <frank.deng@oracle.com> - 1.0-1.0.23
- Try OCI CLI with instance principal auth if CLI config is not available

* Thu Sep 5 2019 Frank Deng <frank.deng@oracle.com> - 1.0-1.0.22
- Allow to configure api key passphrase from url

* Thu Sep 5 2019 Frank Deng <frank.deng@oracle.com> - 1.0-1.0.21
- Remove compartment parameter
- Move notification topic to oci.conf

* Thu Sep 5 2019 Frank Deng <frank.deng@oracle.com> - 1.0-1.0.20
- Simplify email notification subject

* Wed Sep 4 2019 Frank Deng <frank.deng@oracle.com> - 1.0-1.0.19
- Use uptrack commands if ksplice is not available

* Wed Sep 4 2019 Alex Burmashev <alexander.burmashev@oracle.com> - 1.0-1.0.18
- Add selinux support for notification service, triggered by rsyslog omprog

* Tue Sep 3 2019 Frank Deng <frank.deng@oracle.com> - 1.0-1.0.17
- Add al-config.service to create cron job and activate exploit detection.
- Add al-exploit-alert and rsyslog rule to trigger exploit alert

* Sun Sep 1 2019 Frank Deng <frank.deng@oracle.com> - 1.0-1.0.16
- Use 'ksplice -y all upgrade'

* Sun Sep 1 2019 Frank Deng <frank.deng@oracle.com> - 1.0-1.0.15
- Activate known exploit detection on boot.
- Include detected exploit attemps in notification message.

* Sun Sep 1 2019 Frank Deng <frank.deng@oracle.com> - 1.0-1.0.14
- Initial commit.
