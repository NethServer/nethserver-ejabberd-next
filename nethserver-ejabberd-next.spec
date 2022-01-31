Summary: NethServer ejabberd XMPP server
Name: nethserver-ejabberd-next
Version: 1.8.4
Release: 1%{?dist}
License: GPL
Source0: %{name}-%{version}.tar.gz
# Execute prep-sources to create Source1
Source1: %{name}-ui.tar.gz

BuildArch: noarch
BuildRequires: nethserver-devtools
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires: ejabberd
Requires: nethserver-httpd
Conflicts: nethserver-ejabberd

%description
NethServer configuration of ejabberd XMPP server

%prep
%setup

%build
%{makedocs}
perl createlinks
sed -i 's/_RELEASE_/%{version}/' %{name}.json

%install
(cd root ; find . -depth -print | cpio -dump %{buildroot})

mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
tar xvf %{SOURCE1} -C %{buildroot}/usr/share/cockpit/%{name}/
cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/


%{genfilelist} \
    --file /etc/sudoers.d/50_nsapi_nethserver_ejabberd 'attr(0440,root,root)' \
    %{buildroot} > %{name}-%{version}-%{release}-filelist
mkdir -p %{buildroot}/%{_localstatedir}/log/ejabberd
mkdir -p %{buildroot}/%{_sysconfdir}/ejabberd
mkdir -p %{buildroot}/%{_localstatedir}/lib/ejabberd
mkdir -p %{buildroot}/%{_localstatedir}/lib/nethserver/ejabberd
mkdir -p %{buildroot}/%{_localstatedir}/lib/nethserver/ejabberd/upload

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%doc COPYING
%doc README.rst
%dir %{_nseventsdir}/%{name}-update
%attr(0750,ejabberd,ejabberd) %dir %{_localstatedir}/log/ejabberd
%attr(0750,ejabberd,ejabberd) %dir %{_localstatedir}/lib/ejabberd
%attr(0750,ejabberd,ejabberd) %dir %{_sysconfdir}/ejabberd
%attr(0640,ejabberd,ejabberd) %ghost %{_sysconfdir}/ejabberd/ejabberd.yml
%attr(0640,ejabberd,ejabberd) %{_sysconfdir}/ejabberd/inetrc
%attr(0755,root,root) %{_sysconfdir}/cron.daily/ejabberd-purge-mod_mam-database
%attr(0750,ejabberd,ejabberd) %dir %{_localstatedir}/lib/nethserver/ejabberd
%attr(0750,ejabberd,ejabberd) %dir %{_localstatedir}/lib/nethserver/ejabberd/upload

%post
%systemd_post ejabberd.service

%preun
%systemd_preun ejabberd.service

%postun
%systemd_postun ejabberd.service


%changelog
* Fri Jan 29 2021 Davide Principi <davide.principi@nethesis.it> - 1.8.4-1
- Fix LdapTlsPortOverride db prop name - Bug NethServer/dev#6399

* Wed Jan 27 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.8.3-1
- Ejabberd: Samba AD bind is broken in  mod_shared_roster_ldap - Bug NethServer/dev#6399
- ejabberd: rpm build fail after Fedora31 - Bug NethServer/dev#6400

* Thu Sep 03 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.8.2-1
- Increase max_fsm_queue to new default - NethServer/nethserver-ejabberd#36

* Thu Jul 02 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.8.1-1
- Human readable numbers in Cockpit dashboards - NethServer/dev#6206

* Thu Jun 04 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.8.0-1
- Remove TLS 1.0 and TLS 1.1 - NethServer/dev#6170

* Tue Apr 28 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.7.0-1
- Ejabberd: upgrade to 20.03 - NethServer/dev#6108

* Wed Mar 04 2020 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.6.0-1
- Upgrade Ejabberd to V20.01 - NethServer/dev#6070

* Wed Jan 08 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.2-1
- Cockpit: change package Dashboard page title - NethServer/dev#6004

* Thu Nov 21 2019 Davide Principi <davide.principi@nethesis.it> - 1.5.1-1
- Ejabberd password auth fails with special chars - Bug NethServer/dev#5931

* Tue Oct 01 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.0-1
- Sudoers based authorizations for Cockpit UI - NethServer/dev#5805

* Tue Sep 03 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.1-1
- Cockpit. List correct application version - Nethserver/dev#5819

* Tue Mar 05 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.0-1
- Ejabberd Cockpit UI - NethServer/dev#5719

* Mon Oct 08 2018 Davide Principi <davide.principi@nethesis.it> - 1.3.1-1
- Ejabberd: warning in log with policies 20180621 & 20180330 - Bug NethServer/dev#5601
- Package nethserver-X must subscribe nethserver-sssd-save - NethServer/dev#5600

* Fri Sep 28 2018 Davide Principi <davide.principi@nethesis.it> - 1.3.0-1
- Pre-backup-data event fails if ejabberd is installed but disabled - Bug NethServer/dev#5584
- TLS policy and ejabberd: new policy 2018-10-01 - NethServer/dev#5580

* Tue Aug 28 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.0-1
- Ejabberd: upgrade to 18.06 - NethServer/dev#5537

* Mon May 22 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.5-1
- Default userPrincipalName is not an email address - Bug NethServer/dev#5284
- Set user name as DisplayName

* Mon Mar 06 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.4-1
- Fix access prop - NethServer/dev#5196

* Thu Dec 15 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.3-1
- Enable LDAPs protocol on Active Directory clients - NethServer/dev#5161

* Fri Oct 14 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.2-1
- XMPP over bosh does not work - Bug NethServer/dev#5131

* Thu Jul 21 2016 Davide Principi <davide.principi@nethesis.it> - 1.1.1-1
- Web UI: missing labels - Bug NethServer/dev#5061
- Can't install nethserver-messaging with nethserver-dc - Bug NethServer/dev#5052

* Thu Jul 07 2016 Stefano Fancello <stefano.fancello@nethesis.it> - 1.1.0-1
- First NS7 release

* Tue Sep 29 2015 Davide Principi <davide.principi@nethesis.it> - 1.0.5-1
- Make Italian language pack optional - Enhancement #3265 [NethServer]

* Tue Jul 08 2014 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.4-1.ns6
- DNS SRV record for XMPP protocol - Enhancement #2715
- Fix missing Italian translation - Bug #2706

* Wed Feb 05 2014 Davide Principi <davide.principi@nethesis.it> - 1.0.3-1.ns6
- Move admin user in LDAP DB - Feature #2492 [NethServer]
- Lib: synchronize service status prop and chkconfig - Feature #2067 [NethServer]
- Update all inline help documentation - Task #1780 [NethServer]

* Tue Apr 30 2013 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.2-1.ns6
- Rebuild for automatic package handling. #1870
- Small fixes

* Tue Mar 19 2013 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.1-1
- Add migration code

* Thu Jan 17 2013 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.0-1
- First release
