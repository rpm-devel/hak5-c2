Summary: Hak5 C2 Panel
Name: hak5-c2
Version: 3.1.2
Release: 1%{?dist}
License: GPLv2
Group: System Environment/Base
URL: http://casjaysdev.com/

Source0: c2
Source1: c2.service
#Source2: c2-apache.conf

%description
Hak5 Control Panel - https://shop.hak5.org/products/c2
Download url - https://downloads.hak5.org/cloudc2/community

%prep
%setup -c -T
wget https://c2.hak5.org/download/community -O %{SOURCE0}

# %build

%install
%{__rm} -rf %{buildroot}
%{__install} -Dpm 0755 %{SOURCE0} %{buildroot}/%{_datarootdir}/%{name}/c2
%{__install} -Dpm 0644 %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service
#%{__install} -Dpm 0644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/httpd/conf.d/%{name}.conf
%{__install} -d %{buildroot}%{_datarootdir}/%{name}
%{__install} -d %{buildroot}%{_bindir}
touch %{buildroot}%{_bindir}/%{name}


%clean
%{__rm} -rf %{buildroot}

%post
echo "#!/bin/sh
%{_datarootdir}/%{name}/c2 -db %{_datarootdir}/%{name}/c2.db -listenport 8092 -sshport 2022 -hostname $(hostname -f) -reverseProxy -reverseProxyPort 443" > %{_bindir}/%{name}
chmod -Rf 755 %{_bindir}/%{name}

/sbin/ldconfig > /dev/null 2>&1
systemctl enable %{name}.service > /dev/null 2>&1
%{_datarootdir}/%{name}/c2 -db %{_datarootdir}/%{name}/c2.db -listenport 8092 -sshport 2022 -hostname $(hostname -f) -reverseProxy -reverseProxyPort 443 > /root/hak5-c2.txt 2>&1&
echo -e "\nRead the /root/hak5-c2.txt file for token \nHak5 C2 is available at http://$(hostname --ip-address):8092\n"

%postun
killall --quiet -s 9 c2 > /dev/null 2>&1
/sbin/ldconfig > /dev/null 2>&1
%systemd_postun_with_restart %{name}.service > /dev/null 2>&1
systemctl reload httpd > /dev/null 2>&1

%preun
killall --quiet -s 9 c2 > /dev/null 2>&1
%systemd_preun %{name}.service > /dev/null 2>&1
systemctl reload httpd > /dev/null 2>&1
mv -f %{_datarootdir}/%{name}/c2.db %{_datarootdir}/%{name}/c2.old

%files
%defattr(-, root, root, 0755)
#%{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_datarootdir}/%{name}/c2
%{_unitdir}/%{name}.service
%{_bindir}/%{name}
%dir %{_datarootdir}/%{name}

%changelog
* Thu Nov 04 2021 CasjaysDev <rpm-devel@casjaysdev.com> - 0.2
- Updated c2 to version 3.1.2

* Thu Dec 13 2018 CasjaysDev <rpm-admin@rpm-devel.casjaysdev.com> - 0.1
- initial release

