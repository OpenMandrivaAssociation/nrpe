Summary:	Host/service/network monitoring agent for Nagios
Name:		nrpe
Version:	2.12
Release:	%mkrel 5
License:	GPLv2
Group:		System/Servers
URL:		https://sourceforge.net/projects/nagios/
Source0:	http://prdownloads.sourceforge.net/nagios/%{name}-%{version}.tar.gz
Source1:	nrpe.init
Patch0:		nrpe_check_control.diff
Patch1:		nrpe-mdv_conf.diff
BuildRequires:	nagios
BuildRequires:	openssl-devel
BuildRequires:	openssl
BuildRequires:	tcp_wrappers-devel
Requires:	tcp_wrappers
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The purpose of this addon is to allow you to execute Nagios plugins on a remote
host in as transparent a manner as possible.

Nrpe is a system daemon that will execute various Nagios plugins locally on
behalf of a remote (monitoring) host that uses the check_nrpe plugin. Various
plugins that can be executed by the daemon are available at:
http://sourceforge.net/projects/nagiosplug

This package provides the core agent.

%package -n	nagios-check_nrpe
Summary:	NRPE Plugin for Nagios
Group:		Networking/Other
Requires:	nagios-plugins

%description -n	nagios-check_nrpe
Nrpe is a system daemon that will execute various Nagios plugins locally on
behalf of a remote (monitoring) host that uses the check_nrpe plugin. Various
plugins that can be executed by the daemon are available at:
http://sourceforge.net/projects/nagiosplug

This package provides the nrpe plugin for Nagios-related applications.

%prep

%setup -q
%patch0 -p0
%patch1 -p0

cp %{SOURCE1} nrpe.init

%build

%configure2_5x \
    --with-init-dir=%{_initrddir} \
    --with-nrpe-port=5666 \
    --with-nrpe-user=nagios \
    --with-nrpe-group=nagios \
    --with-nagios-user=nagios \
    --with-nagios-group=nagios \
    --bindir=%{_sbindir} \
    --libexecdir=%{_libdir}/nagios/plugins \
    --datadir=%{_datadir}/nagios \
    --localstatedir=/var/spool/nagios \
    --sysconfdir=%{_sysconfdir}/nagios \
    --enable-command-args
%make

gcc %{optflags} -o contrib/nrpe_check_control contrib/nrpe_check_control.c

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/nagios/plugins.d
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_libdir}/nagios/plugins
install -d %{buildroot}/var/run/%{name}

install -m0755 src/check_nrpe %{buildroot}%{_libdir}/nagios/plugins/check_nrpe
install -m0755 contrib/nrpe_check_control %{buildroot}%{_libdir}/nagios/plugins/nrpe_check_control
install -m0755 src/nrpe %{buildroot}%{_sbindir}/nrpe
install -m0755 nrpe.init %{buildroot}%{_initrddir}/nrpe
install -m0644 sample-config/nrpe.cfg %{buildroot}%{_sysconfdir}/nagios/nrpe.cfg

cat > check_nrpe.cfg <<'EOF'
# this command runs a program $ARG1$ with arguments $ARG2$
define command {
	command_name	check_nrpe
	command_line	%{_libdir}/nagios/plugins/check_nrpe -H $HOSTADDRESS$ -c $ARG1$ -a $ARG2$
}

# this command runs a program $ARG1$ with no arguments
define command {
	command_name	check_nrpe_1arg
	command_line	%{_libdir}/nagios/plugins/check_nrpe -H $HOSTADDRESS$ -c $ARG1$
}
EOF
install -m0644 check_nrpe.cfg %{buildroot}%{_sysconfdir}/nagios/plugins.d/check_nrpe.cfg


cat > nrpe_check_control.cfg <<'EOF'
define command {
	command_name	nrpe_check_control
	command_line	%{_libdir}/nagios/plugins/nrpe_check_control $SERVICESTATE$ $SERVICESTATETYPE$ $SERVICEATTEMPT$ "$HOSTNAME$"
}
EOF
install -m0644 nrpe_check_control.cfg %{buildroot}%{_sysconfdir}/nagios/plugins.d/nrpe_check_control.cfg

%pre
%_pre_useradd nagios %{_localstatedir}/log/nagios /bin/sh

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel nagios

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README LEGAL README.SSL Changelog SECURITY docs/NRPE.pdf
%dir %{_sysconfdir}/nagios/
%config(noreplace) %{_sysconfdir}/nagios/nrpe.cfg
%{_initrddir}/nrpe
%{_sbindir}/nrpe
%dir /var/run/%{name}

%files -n nagios-check_nrpe
%defattr(-,root,root)
%doc contrib/README.nrpe_check_control
%config(noreplace) %{_sysconfdir}/nagios/plugins.d/check_nrpe.cfg
%config(noreplace) %{_sysconfdir}/nagios/plugins.d/nrpe_check_control.cfg
%{_libdir}/nagios/plugins/check_nrpe
%{_libdir}/nagios/plugins/nrpe_check_control


%changelog
* Tue Sep 14 2010 Michael Scherer <misc@mandriva.org> 2.12-5mdv2011.0
+ Revision: 578194
- fix License
- fix unowned directory ( as nrpe is likely to be installed when nagios is not there )

* Fri May 14 2010 Guillaume Rousse <guillomovitch@mandriva.org> 2.12-4mdv2010.1
+ Revision: 544796
- add nagios user at installation (fix #59203)
- cleanup
- drop useless %%post, as we now use filetrggiers
- %files section cleanup

* Fri Apr 16 2010 Funda Wang <fwang@mandriva.org> 2.12-3mdv2010.1
+ Revision: 535273
- rebuild

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 2.12-2mdv2010.0
+ Revision: 430183
- rebuild

* Sun Sep 07 2008 Oden Eriksson <oeriksson@mandriva.com> 2.12-1mdv2009.0
+ Revision: 282159
- 2.12

* Fri Aug 08 2008 Thierry Vignaud <tv@mandriva.org> 2.11-4mdv2009.0
+ Revision: 268289
- rebuild early 2009.0 package (before pixel changes)

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - sync initscript with ndo2db one

* Thu May 15 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.11-3mdv2009.0
+ Revision: 207538
- LSB headers in initscript

* Tue Apr 29 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.11-2mdv2009.0
+ Revision: 198954
- enable arguments

* Mon Feb 11 2008 Oden Eriksson <oeriksson@mandriva.com> 2.11-1mdv2008.1
+ Revision: 165295
- 2.11

* Sun Feb 10 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.9-2mdv2008.1
+ Revision: 164896
- no need to enforce a dependency on nagios-plugins, they are tons of nagios checks available in other packages

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Oct 12 2007 Oden Eriksson <oeriksson@mandriva.com> 2.9-1mdv2008.1
+ Revision: 97376
- 2.9

* Fri May 11 2007 Oden Eriksson <oeriksson@mandriva.com> 2.8.1-1mdv2008.0
+ Revision: 26291
- 2.8.1

* Tue Apr 17 2007 Oden Eriksson <oeriksson@mandriva.com> 2.7.1-1mdv2008.0
+ Revision: 13802
- 2.7.1


* Thu Jul 13 2006 Oden Eriksson <oeriksson@mandriva.com> 2.5.2-1mdv2007.0
- 2.5.2

* Wed Nov 30 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0-3mdk
- rebuilt against openssl-0.9.8a

* Fri Sep 10 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.0-2mdk
- fix path to conf file 
- fix requires

* Fri Sep 10 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.0-1mdk
- initial mdk release

