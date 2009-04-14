#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	up		# don't build UP module
%bcond_without	smp		# don't build SMP module
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif
%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

%ifarch sparc
%undefine	with_smp
%endif

%define		rel		1
%define		pname		r8101
Summary:	Linux driver for the RTL8100E/RTL8101E/RTL8102E-GR/RTL8103E(L)/RTL8102E(L)/RTL8101E/RTL8103T Network Interface Cards
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart sieciowych RTL8100E/RTL8101E/RTL8102E-GR/RTL8103E(L)/RTL8102E(L)/RTL8101E/RTL8103T
Name:		%{pname}%{_alt_kernel}
Version:	1.011.00
Release:	%{rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	%{pname}-%{version}.tar.bz2
Patch0:		%{pname}-2.6.16.patch
URL:		http://www.realtek.com.tw/downloads/downloadsView.aspx?Langid=1&PNid=14&PFid=7&Level=5&Conn=4&DownTypeID=3&GetDown=false
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.14}
BuildRequires:	rpmbuild(macros) >= 1.452
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the RTL8100E/RTL8101E/
RTL8102E-GR/RTL8103E(L)/RTL8102E(L)/RTL8101E/RTL8103T Network Interface
Cards.

%description -l pl.UTF-8
Pakiet zawiera sterownik dla Linuksa do kart sieciowych RTL8100E/
RTL8101E/RTL8102E-GR/RTL8103E(L)/RTL8102E(L)/RTL8101E/RTL8103T.

%package -n kernel%{_alt_kernel}-net-%{pname}
Summary:	Linux driver for the RTL8100E/RTL8101E/RTL8102E-GR/RTL8103E(L)/RTL8102E(L)/RTL8101E/RTL8103T Network Interface Cards
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart sieciowych RTL8100E/RTL8101E/RTL8102E-GR/RTL8103E(L)/RTL8102E(L)/RTL8101E/RTL8103T
Release:	%{rel}@%{_kernel_vermagic}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires:	kernel%{_alt_kernel}(vermagic) = %{_kernel_ver}}

%description -n kernel%{_alt_kernel}-net-%{pname}
Linux driver for the Broadcom's NetXtreme RTL8100E/RTL8101E/
RTL8102E-GR/RTL8103E(L)/RTL8102E(L)/RTL8101E/RTL8103T Network Interface
Cards.

%description -n kernel%{_alt_kernel}-net-%{pname} -l pl.UTF-8
Sterownik dla Linuksa do kart sieciowych RTL8100E/RTL8101E/RTL8102E-GR/
RTL8103E(L)/RTL8102E(L)/RTL8101E/RTL8103T.

%package -n kernel%{_alt_kernel}-smp-net-%{pname}
Summary:	Linux SMP driver for the RTL8100E/RTL8101E/RTL8102E-GR/RTL8103E(L)/RTL8102E(L)/RTL8101E/RTL8103T Network Interface Cards
Summary(pl.UTF-8):	Sterownik dla Linuksa SMP do kart sieciowych RTL8100E/RTL8101E/RTL8102E-GR/RTL8103E(L)/RTL8102E(L)/RTL8101E/RTL8103T
Release:	%{rel}@%{_kernel_vermagic}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires:	kernel%{_alt_kernel}-smp(vermagic) = %{_kernel_ver}}

%description -n kernel%{_alt_kernel}-smp-net-%{pname}
Linux SMP driver for the RTL8100E/RTL8101E/RTL8102E-GR/RTL8103E(L)/
RTL8102E(L)/RTL8101E/RTL8103T Network Interface Cards.

%description -n kernel%{_alt_kernel}-smp-net-%{pname} -l pl.UTF-8
Sterownik dla Linuksa SMP do kart sieciowych RTL8100E/RTL8101E/
RTL8102E-GR/RTL8103E(L)/RTL8102E(L)/RTL8101E/RTL8103T.

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1

%build
%build_kernel_modules -m %{pname} -C src

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -m src/%{pname} -d kernel/drivers/net -n %{pname} -s ""
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-%{pname}
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-%{pname}
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-net-%{pname}
%depmod %{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-net-%{pname}
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc readme
%endif

%if %{with kernel}
%if %{with up} || %{without dist_kernel}
%files -n kernel%{_alt_kernel}-net-%{pname}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/%{pname}*.ko*
/etc/modprobe.d/%{_kernel_ver}/%{pname}.conf
%endif

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-net-%{pname}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/%{pname}*.ko*
/etc/modprobe.d/%{_kernel_ver}smp/%{pname}.conf
%endif
%endif
