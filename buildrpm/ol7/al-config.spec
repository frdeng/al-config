Name: al-config
Version: 1.0
Release: 1.0.15%{?dist}
Summary: Configuration tasks for Autonomous Linux Oracle Linux instances running in Oracle Cloud Infrastructure
BuildArch: noarch

Group: Development/Tools
URL: http://cloud.oracle.com/iaas
License: UPL
Vendor: Oracle America

Source: %{name}-%{version}.tar.gz

Requires: uptrack
Requires: ksplice-tools
Requires: ksplice-known-exploit-detection
Requires: yum-cron
Requires: jq
Requires: python-oci-cli
Requires: python-oci-sdk
Requires: cloud-init

%description
This package contains configuration tasks for Autonomous Linux instances running in Oracle Cloud Infrastructure environment

%prep
%autosetup -p1

%build

%install
rm -rf %{buildroot}/*
cp -a install/*  %{buildroot}

%files

#/usr/lib
%dir %{_prefix}/lib/%{name}
%attr(644,root,root) %{_prefix}/lib/%{name}/functions
%attr(755,root,root) %{_prefix}/lib/%{name}/pre_config.sh
%attr(755,root,root) %{_prefix}/lib/%{name}/add_cron_job.sh
%attr(755,root,root) %{_prefix}/lib/%{name}/activate_known_exploit_detection.sh
#/usr/sbin
%attr(755,root,root) %{_sbindir}/al-config
%attr(755,root,root) %{_sbindir}/al-update
%attr(755,root,root) %{_sbindir}/al-notify
#/etc
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/al.conf
%attr(644,root,root) %{_sysconfdir}/%{name}/yum-cron.conf
%attr(644,root,root) %{_sysconfdir}/logrotate.d/%{name}
#/var
%dir %{_sharedstatedir}/%{name}

%license LICENSE

%post
# install or upgrade
%{_prefix}/lib/%{name}/pre_config.sh

# install
if [ "$1" = 1 ]; then
    # TODO: use systemd service to handle following:
    # We only create random time cron job on fist boot
    mkdir -p %{_sharedstatedir}/cloud/scripts/per-instance
    ln -sf  %{_prefix}/lib/%{name}/add_cron_job.sh \
        %{_sharedstatedir}/cloud/scripts/per-instance/al.sh
    # activate known exploit detecton on each boot
    mkdir -p %{_sharedstatedir}/cloud/scripts/per-boot
    ln -sf %{_prefix/lib/%{name}/activate_known_exploit_detection.sh \
        %{_sharedstatedir}/cloud/scripts/per-boot/al.sh
fi

%posttrans

%preun
# uninstall
if [ "$1" = 0 ]; then
    rm -f %{_sysconfdir}/cron.d/al-update
    rm -f %{_sharedstatedir}/cloud/scripts/per-instance/al.sh \
          %{_sharedstatedir}/cloud/scripts/per-boot/al.sh
fi

%postun

%changelog
* Sun Sep 1 2019 Frank Deng <frank.deng@oracle.com> - 1.0-1.0.15
- Activate known exploit detection on boot.
- Include detected exploit attemps in notification message.

* Sun Sep 1 2019 Frank Deng <frank.deng@oracle.com> - 1.0-1.0.14
- Initial commit.
