%define dnet_major 1
%define dnet_version %{dnet_major}.2
%define dap_major 2
%define dap_version %{dap_major}.23
%define dnprogs_version %{dap_version}
Summary:	DECnet tools and libraries
Summary(pl.UTF-8):	Narzędzia i biblioteki DECnet
Name:		dnprogs
Version:	%{dnprogs_version}
Release:	0.1
License:	GPL
Group:		Networking/Utilities
Source0:	http://downloads.sourceforge.net/linux-decnet/%{name}-%{version}.tar.gz
# Source0-md5:	666e1479f60f7f0fe3bf8da3abab98bd
URL:		http://linux-decnet.sourceforge.net/
Requires(post,preun):	/sbin/chkconfig
Requires(post):	/sbin/ldconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rc-scripts
ExclusiveOS:	Linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DECnet programs for Linux.

These tools are the application layer interface for DECnet on Linux
systems. They provide file/terminal access facilities between OpenVMS
and Linux and remote execution of commands.

To use them you will need to have DECnet built into your kernel. See
<http://linux.dreamtime.org/decnet/> to get the kernel patch and
instructions on how to apply it.

%description -l pl.UTF-8
Programy DECnet dla Linuksa.

Narzędzia te stanowią interfejs warstwy aplikacji dla DECnetu na
systemach linuksowych. Zawierają elementy zapewniające dostęp
terminalowy i plikowy między OpenVMS-em a Linuksem oraz zdalne
wykonywanie poleceń.

Aby ich użyć trzeba mieć wbudowaną w jądro obsługę DECnetu. Łatę oraz
instrukcje dotyczące jej instalacji można znaleźć na stronie:
<http://linux.dreamtime.org/decnet/>.

%package libs
Summary:	DECnet shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone DECnet
Group:		Libraries

%description libs
DECnet shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone DECnet.

%package devel
Summary:	Header files for DECnet libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek DECnet
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for DECnet libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek DECnet.

%package static
Summary:	Static DECnet libraries
Summary(pl.UTF-8):	Statyczne biblioteki DECnet
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static DECnet libraries.

%description static -l pl.UTF-8
Statyczne biblioteki DECnet.

%prep
%setup -q

find . -type f -name '*~' -print0 | xargs -0 rm -f

%build
%{__make} \
	DFLAGS="%{rpmcflags}" \
	LIBCRYPT=-lcrypt \
	SHADOWDEFS=-DSHADOW_PWD \
	prefix=%{_prefix} \
	libprefix=%{_prefix} \
	sysconfprefix=

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/rc.d/{init,rc{0,1,2,3,4,5,6}}.d,%{_lib},sbin}
%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	libprefix=$RPM_BUILD_ROOT%{_prefix} \
	sysconfprefix=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libdnet.so
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libdnet.so.%{dnet_major}
mv -f $RPM_BUILD_ROOT%{_libdir}/libdnet.so.%{dnet_version} \
	$RPM_BUILD_ROOT/%{_lib}
ln -sf libdnet.so.%{dnet_version} \
	$RPM_BUILD_ROOT/%{_lib}/libdnet.so.%{dnet_major}
ln -sf /%{_lib}/libdnet.so.%{dnet_major} \
	$RPM_BUILD_ROOT%{_libdir}/libdnet.so

mv -f $RPM_BUILD_ROOT%{_sbindir}/startnet $RPM_BUILD_ROOT/sbin/startnet

touch $RPM_BUILD_ROOT%{_sysconfdir}/decnet.proxy

install scripts/decnet.sh $RPM_BUILD_ROOT/etc/rc.d/init.d/decnet

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add decnet

%postun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del decnet
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Documentation/* README NEWS dnprogs.lsm
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/decnet.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/decnet.proxy
%attr(754,root,root) /etc/rc.d/init.d/decnet
%attr(755,root,root) /sbin/startnet
%attr(755,root,root) %{_bindir}/dncopy
%attr(755,root,root) %{_bindir}/dndel
%attr(755,root,root) %{_bindir}/dndir
%attr(755,root,root) %{_bindir}/dnping
%attr(755,root,root) %{_bindir}/dnprint
%attr(755,root,root) %{_bindir}/dnsubmit
%attr(755,root,root) %{_bindir}/dntask
%attr(755,root,root) %{_bindir}/dntype
%attr(755,root,root) %{_bindir}/phone
%attr(755,root,root) %{_bindir}/sethost
%attr(755,root,root) %{_sbindir}/ctermd
%attr(755,root,root) %{_sbindir}/dnmirror
%attr(755,root,root) %{_sbindir}/fal
%attr(755,root,root) %{_sbindir}/phoned
%attr(755,root,root) %{_sbindir}/sendvmsmail
%attr(755,root,root) %{_sbindir}/vmsmaild
%{_mandir}/man1/ctermd.1*
%{_mandir}/man1/dncopy.1*
%{_mandir}/man1/dndel.1*
%{_mandir}/man1/dndir.1*
%{_mandir}/man1/dnmirror.1*
#%%{_mandir}/man1/dnmount.1*
%{_mandir}/man1/dnping.1*
%{_mandir}/man1/dnprint.1*
%{_mandir}/man1/dnsubmit.1*
%{_mandir}/man1/dntask.1*
%{_mandir}/man1/dntype.1*
%{_mandir}/man1/phone.1*
%{_mandir}/man1/sethost.1*
%{_mandir}/man1/startnet.1*
%{_mandir}/man3/setnodeent.3*
%{_mandir}/man5/decnet.conf.5*
%{_mandir}/man5/decnet.proxy.5*
%{_mandir}/man8/fal.8*
%{_mandir}/man8/phoned.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdap.so.%{dap_major}
%attr(755,root,root) %{_libdir}/libdap.so.%{dap_version}
%attr(755,root,root) /lib/libdnet.so.%{dnet_version}
%attr(755,root,root) /lib/libdnet.so.%{dnet_major}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdap.so
%attr(755,root,root) %{_libdir}/libdnet.so
%{_includedir}/netdnet
%{_mandir}/man3/dnet_addr.3*
%{_mandir}/man3/dnet_conn.3*
%{_mandir}/man3/dnet_htoa.3*
%{_mandir}/man3/dnet_ntoa.3*
%{_mandir}/man3/getnodeadd.3*
%{_mandir}/man3/getnodebyaddr.3*
%{_mandir}/man3/getnodebyname.3*
%{_mandir}/man3/libdnet.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libdnet.a
%{_libdir}/libdap.a
