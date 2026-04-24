Summary: Hak5 C2 Panel
Name: hak5-c2
Version: 3.1.2
Release: 1%{?dist}
License: GPLv2
URL: http://casjaysdev.pro/

Source0: c2-%{_arch}
Source1: c2.service
#Source2: c2-apache.conf
#Source3: c2-nginx.conf

%description
Hak5 Control Panel - https://shop.hak5.org/products/c2
Download url - https://downloads.hak5.org/cloudc2/community

%prep
%setup -c -T

# %build

%install
%{__install} -Dpm 0755 %{SOURCE0} %{buildroot}/%{_datarootdir}/%{name}/c2-%BuildArch
%{__install} -Dpm 0644 %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service
#%{__install} -Dpm 0644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/httpd/conf.d/%{name}.conf
%{__install} -d %{buildroot}%{_datarootdir}/%{name}
%{__install} -d %{buildroot}%{_bindir}
touch %{buildroot}%{_bindir}/%{name}

%post
echo "#!/bin/sh
%{_datarootdir}/%{name}/c2-%BuildArch \
-db %{_datarootdir}/%{name}/c2.db \
-listenport 8092 \
-sshport 2022 \
-hostname $(hostname -f) \
-reverseProxy \
-reverseProxyPort 443" \
> %{_bindir}/%{name}
chmod -Rf 755 %{_bindir}/%{name}

/sbin/ldconfig &> /dev/null
systemctl enable %{name}.service &> /dev/null
%{_datarootdir}/%{name}/c2-%BuildArch -db %{_datarootdir}/%{name}/c2.db -listenport 8092 -sshport 2022 \
-hostname $(hostname -f) -reverseProxy -reverseProxyPort 443 &> "$HOME/hak5-c2.txt" &
sleep 10
echo -e '\nThis does require a free license get one at\nhttps://hak5.org/cart/add?id=12992425820273' >> "$HOME/hak5-c2.txt"
echo -e "\nRead the "$HOME/hak5-c2.txt" file for token \nHak5 C2 is available at http://$(hostname -f):8092\n"

%postun
killall --quiet -s 9 c2 c2-%BuildArch &> /dev/null
/sbin/ldconfig > /dev/null 2>&1
%systemd_postun_with_restart %{name}.service &> /dev/null
systemctl reload httpd > /dev/null 2>&1

%preun
killall --quiet -s 9 c2 c2-%BuildArch &> /dev/null
%systemd_preun %{name}.service > /dev/null 2>&1
systemctl reload httpd > /dev/null 2>&1
mv -f %{_datarootdir}/%{name}/c2.db %{_datarootdir}/%{name}/c2.old &>/dev/null || true

%files
#%{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_datarootdir}/%{name}/c2-%BuildArch
%{_unitdir}/%{name}.service
%{_bindir}/%{name}
%dir %{_datarootdir}/%{name}

%changelog
* Fri Apr 24 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 3.1.2-1
- Modernize spec for AlmaLinux 10; remove Group, %clean, %defattr

* Thu Nov 04 2021 CasjaysDev <rpm-devel@casjaysdev.pro> - 0.2
- Updated c2 to version 3.1.2

* Thu Dec 13 2018 CasjaysDev <rpm-devel@casjaysdev.pro> - 0.1
- initial release
