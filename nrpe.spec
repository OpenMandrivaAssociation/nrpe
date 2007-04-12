Summary:	Host/service/network monitoring agent for Nagios
Name:		nrpe
Version:	2.5.2
Release:	%mkrel 1
License:	GPL
Group:		Networking/Other
URL:		http://sourceforge.net/projects/nagios/
Source0:	http://prdownloads.sourceforge.net/nagios/%{name}-%{version}.tar.bz2
BuildRequires:	openssl-devel
Requires:	nagios-plugins
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The purpose of this addon is to allow you to execute Nagios
plugins on a remote host in as transparent a manner as possible.

Nrpe is a system daemon that will execute various Nagios plugins
locally on behalf of a remote (monitoring) host that uses the
check_nrpe plugin.  Various plugins that can be executed by the
daemon are available at:
http://sourceforge.net/projects/nagiosplug

This package provides the core agent.

%package	plugin
Summary:	Provides nrpe plugin for Nagios
Group:		Networking/Other
Requires:	nagios-plugins

%description	plugin
Nrpe is a system daemon that will execute various Nagios plugins
locally on behalf of a remote (monitoring) host that uses the
check_nrpe plugin.  Various plugins that can be executed by the
daemon are available at:
http://sourceforge.net/projects/nagiosplug

This package provides the nrpe plugin for Nagios-related applications.

%prep
%setup -q

%build

%configure2_5x \
    --with-init-dir=%{_initrddir} \
    --with-nrpe-port=5666 \
    --with-nrpe-user=nagios \
    --with-nrpe-grp=nagios \
    --sbindir=%{_libdir}/nagios/cgi \
    --libexecdir=%{_libdir}/nagios/plugins \
    --datadir=%{_datadir}/nagios \
    --localstatedir=%{_var}/log/nagios \
    --sysconfdir=%{_sysconfdir}/nagios

%make

%install
%{__rm} -rf $RPM_BUILD_ROOT

install -m755 src/check_nrpe -D $RPM_BUILD_ROOT%{_libdir}/nagios/plugins/check_nrpe
install -m755 src/nrpe -D $RPM_BUILD_ROOT%{_bindir}/nrpe
install -m755 init-script -D $RPM_BUILD_ROOT%{_initrddir}/nrpe
install -m644 sample-config/nrpe.cfg -D $RPM_BUILD_ROOT%{_sysconfdir}/nagios/nrpe.cfg

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README LEGAL README.SSL Changelog SECURITY
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/nagios/nrpe.cfg
%attr(0755,root,root) %{_initrddir}/nrpe
%attr(0755,root,root) %{_bindir}/nrpe

%files plugin
%defattr(-,root,root)
%doc README LEGAL README.SSL Changelog SECURITY
%attr(0755,root,root) %{_libdir}/nagios/plugins/check_nrpe

