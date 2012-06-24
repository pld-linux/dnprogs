Summary:	DECnet tools and libraries
Summary(pl):	Narz�dzia i biblioteki DECnet
Name:		dnprogs

%define dnet_major 1
%define dnet_version %{dnet_major}.2

%define dap_major 1
%define dap_version %{dap_major}.05a

%define dnprogs_version %{dap_version}

Version:	%{dnprogs_version}
Release:	2
License:	GPL
Group:		Networking/Utilities
URL:		http://linux.dreamtime.org/decnet/
Source0:	ftp://ftp.dreamtime.org/pub/decnet/%{name}-%{version}.tar.gz
Patch0:		%{name}-1.05a-make.patch.gz
Patch1:		%{name}-1.05a-rc.patch.gz
ExclusiveOS:	Linux
Prereq:		/sbin/chkconfig
Prereq:		/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DECnet programs for Linux.

These tools are the application layer interface for DECnet on Linux
systems. They provide file/terminal access facilities between OpenVMS
and Linux and remote execution of commands.

To use them you will need to have DECnet built into your kernel. See
http://linux.dreamtime.org/decnet/ to get the kernel patch and
instructions on how to apply it.

%description -l pl
Programy DECnet dla Linuksa. Narz�dzia te stanowi� warstw� interfejsu
aplikacji dla DECnetu na systemach linuksowych. Udost�pniaj� pewne
u�atwienia w dost�pie terminalowym i plikowym mi�dzy OpenVMS-em a
Linuksem oraz zdalnym wykonywaniem polece�. Aby ich u�y� musi si� mie�
wbudowan� w j�do obs�ug� DECnetu. �at� oraz instrukcje dotycz�ce jej
instalacji mo�na uzyska� na stronie:
http://linux.dreamtime.org/decnet/.

%prep
%setup -q
%patch0 -p1 -b .make~
%patch1 -p1 -b .rc~

find . -type f -name '*~' -print0 | xargs -0 rm -f

%build
%{__make} DFLAGS="%{rpmcflags}" LIBCRYPT=-lcrypt SHADOWDEFS=-DSHADOW_PWD \
	prefix=%{_prefix} libprefix=%{_prefix} sysconfprefix=

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT
chmod go= $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{etc/rc.d/{init,rc{0,1,2,3,4,5,6}}.d,lib,sbin}
%{__make} prefix=$RPM_BUILD_ROOT%{_prefix} libprefix=$RPM_BUILD_ROOT%{_prefix} \
	sysconfprefix=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT%{_libdir}/libdnet.so
rm -f $RPM_BUILD_ROOT%{_libdir}/libdnet.so.%{dnet_major}
mv -f $RPM_BUILD_ROOT%{_libdir}/libdnet.so.%{dnet_version} \
	$RPM_BUILD_ROOT/lib/libdnet.so.%{dnet_version}
ln -sf libdnet.so.%{dnet_version} \
	$RPM_BUILD_ROOT/lib/libdnet.so.%{dnet_major}
ln -sf ../../lib/libdnet.so.%{dnet_major} \
	$RPM_BUILD_ROOT%{_libdir}/libdnet.so

mv -f $RPM_BUILD_ROOT%{_sbindir}/startnet $RPM_BUILD_ROOT/sbin/startnet

touch $RPM_BUILD_ROOT%{_sysconfdir}/decnet.proxy

install scripts/decnet.sh $RPM_BUILD_ROOT/etc/rc.d/init.d/decnet

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add decnet
/sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 = 0 ]; then
    /sbin/chkconfig --del decnet
fi

%files
%defattr(644,root,root,755)
%doc Documentation/* README NEWS dnprogs.lsm

%config(noreplace) %{_sysconfdir}/decnet.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/decnet.proxy

%attr(754,root,root) /etc/rc.d/init.d/decnet
%attr(-,root,root) /lib/libdnet.so.%{dnet_major}
%attr(755,root,root) /lib/libdnet.so.%{dnet_version}

%attr(755,root,root) /sbin/startnet

%attr(755,root,root) %{_bindir}/dncopy
%attr(755,root,root) %{_bindir}/dndel
%attr(755,root,root) %{_bindir}/dndir
%attr(755,root,root) %{_bindir}/dnping
%attr(-,root,root) %{_bindir}/dnprint
%attr(755,root,root) %{_bindir}/dnsubmit
%attr(755,root,root) %{_bindir}/dntask
%attr(-,root,root) %{_bindir}/dntype
%attr(755,root,root) %{_bindir}/phone
%attr(755,root,root) %{_bindir}/sethost

%{_includedir}/netdnet

%{_libdir}/libdnet.a
%attr(-,root,root) %{_libdir}/libdnet.so
%{_libdir}/libdap.a
%attr(-,root,root) %{_libdir}/libdap.so
%attr(-,root,root) %{_libdir}/libdap.so.%{dap_major}
%attr(755,root,root) %{_libdir}/libdap.so.%{dap_version}

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

%{_mandir}/man3/dnet_addr.3*
%{_mandir}/man3/dnet_conn.3*
%{_mandir}/man3/dnet_htoa.3*
%{_mandir}/man3/dnet_ntoa.3*
%{_mandir}/man3/getnodeadd.3*
%{_mandir}/man3/getnodebyaddr.3*
%{_mandir}/man3/getnodebyname.3*
%{_mandir}/man3/libdnet.3*
%{_mandir}/man3/setnodeent.3*

%{_mandir}/man5/decnet.conf.5*
%{_mandir}/man5/decnet.proxy.5*

%{_mandir}/man8/fal.8*
%{_mandir}/man8/phoned.8*

%attr(755,root,root) %{_sbindir}/ctermd
%attr(755,root,root) %{_sbindir}/dnmirror
%attr(755,root,root) %{_sbindir}/fal
%attr(755,root,root) %{_sbindir}/phoned
%attr(755,root,root) %{_sbindir}/sendvmsmail
%attr(755,root,root) %{_sbindir}/vmsmaild
