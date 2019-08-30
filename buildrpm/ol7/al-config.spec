Name: al-config
Version: 1.0
Release: 1.0.7%{?dist}
Summary: Configuration tasks for Autonomous Linux Oracle Linux instances running in Oracle Cloud Infrastructure
BuildArch: noarch

Group: Development/Tools
URL: http://cloud.oracle.com/iaas
License: UPL
Vendor: Oracle

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
%attr(755,root,root) %{_prefix}/lib/%{name}/add_cron_job.sh
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
if [ -f /etc/uptrack/uptrack.conf ]; then
    # enable ksplice auto update
    sed -i 's/^\(autoinstall =\).*/\1 yes/' /etc/uptrack/uptrack.conf
    # enable Known-Exploit-Detection
    if ! grep -q 'Known-Exploit-Detection' /etc/uptrack/uptrack.conf; then
        cat >> /etc/uptrack/uptrack.conf <<EOF

[Known-Exploit-Detection]
# Known Exploit Detection is another way Ksplice secures your system.
# Ksplice continues to close down vulnerabilities with zero downtime.
# And now you have the added security of being notified when attempted
# privilege escalation attacks are taken on your system.
enabled = yes
EOF
    fi
fi

# We have AL cron job to do ksplice and yum-cron update, so we don't need ksplice and yum-cron cron jobs
rm -f /etc/cron.d/uptrack /etc/cron.d/ksplice \
      /etc/cron.hourly/0yum-hourly.cron \
      /etc/cron.daily/0yum-daily.cron

# Disable yum-cron default and hourly updates
# we have separate config file /etc/al-config/yum-cron.conf
for conf in /etc/yum/yum-cron.conf /etc/yum/yum-cron-hourly.conf; do
    if [ -f $conf ]; then
        sed -i -e 's/^\(apply_updates =\).*/\1 no/' \
            -e 's/^\(download_updates =\).*/\1 no/' \
            -e 's/^\(update_messages =\).*/\1 no/' \
            $conf
    fi
done

%posttrans
# Create random time cron job on fist boot
mkdir -p %{_sharedstatedir}/cloud/scripts/per-instance
ln -sf  %{_prefix}/lib/%{name}/add_cron_job.sh %{_sharedstatedir}/cloud/scripts/per-instance/al.sh

%preun
rm -f %{_sharedstatedir}/cloud/scripts/per-instance/al.sh

%postun

%changelog
* Wed Jul 17 2019 Frank Deng <frank.deng@oracle.com> - 1.0-1.0.7
- Initial commit.
