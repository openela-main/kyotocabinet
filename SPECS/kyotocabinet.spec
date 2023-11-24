Summary:        A straightforward implementation of DBM
Name:           kyotocabinet
Version:        1.2.76
Release:        17%{?dist}
License:        GPLv3
Group:          Applications/Databases
URL:            http://fallabs.com/%{name}/
Source:         http://fallabs.com/%{name}/pkg/%{name}-%{version}.tar.gz
Patch0:         kyotocabinet-1.2.76-cflags.patch
Patch1:         kyotocabinet-1.2.76-8-byte-atomics.patch
Patch2:         kyotocabinet-1.2.76-tr1_hashtable.patch
Patch3:         kyotocabinet-1.2.76-gcc6.patch
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
BuildRequires:  zlib-devel, lzo-devel, xz-devel

%description
Kyoto Cabinet is a library of routines for managing a database. The
database is a simple data file containing records, each is a pair of
a key and a value. Every key and value is serial bytes with variable
length. Both binary data and character string can be used as a key
and a value. Each key must be unique within a database. And there is
neither concept of data tables nor data types. Records are organized
in hash table or B+ tree.

%package libs
Summary:        Libraries for applications using Kyoto Cabinet
Group:          System Environment/Libraries
Provides:       %{name}-lib = %{version}-%{release}
Provides:       %{name}-lib%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-lib < 1.2.76-3

%description libs
The kyotocabinet-libs package provides the essential shared libraries
for any Kyoto Cabinet client program or interface.

%package        devel
Summary:        Development files for Kyoto Cabinet
Group:          Development/Libraries
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}, pkgconfig

%description devel
The kyotocabinet-devel package contains libraries and header files for
developing applications that use Kyoto Cabinet.

%package apidocs
Summary:        API documentation for Kyoto Cabinet library
Group:          Documentation
%if 0%{?fedora}%{?rhel} >= 6
BuildArch:      noarch
%endif
Provides:       %{name}-api-doc = %{version}-%{release}
Obsoletes:      %{name}-api-doc < 1.2.76-3

%description apidocs
The kyotocabinet-apidocs package contains API documentation for developing
applications that use Kyoto Cabinet.

%prep
%setup -q
%patch0 -p1 -b .cflags
%patch1 -p1 -b .8-byte-atomics
%if 0%{?rhel} == 5
%patch2 -p1 -b .tr1_hashtable
%endif
%patch3 -p1 -b .gcc6

%build
%configure --disable-opt --enable-lzo --enable-lzma
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install

# Don't install any static .a file
rm -f $RPM_BUILD_ROOT%{_libdir}/libkyotocabinet.a

# Clean up for later usage in documentation
rm -rf $RPM_BUILD_ROOT%{_defaultdocdir}

%check
# All kcutilmgr compression tests on RHEL 5 (ppc) just cause 99.9% CPU
# usage but do not continue or simply fail. However all the other tests
# including compression ones work as expected. What is the impact here?
%if 0%{?rhel} == 5 && "%{_arch}" == "ppc"
sed -e '/$(RUNENV) $(RUNCMD) .\/kcutilmgr comp /d' -i Makefile
%endif
make check

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc doc/{command.html,common.css,icon16.png}
%{_bindir}/kccachetest
%{_bindir}/kcdirmgr
%{_bindir}/kcdirtest
%{_bindir}/kcforestmgr
%{_bindir}/kcforesttest
%{_bindir}/kcgrasstest
%{_bindir}/kchashmgr
%{_bindir}/kchashtest
%{_bindir}/kclangctest
%{_bindir}/kcpolymgr
%{_bindir}/kcpolytest
%{_bindir}/kcprototest
%{_bindir}/kcstashtest
%{_bindir}/kctreemgr
%{_bindir}/kctreetest
%{_bindir}/kcutilmgr
%{_bindir}/kcutiltest
%{_mandir}/man1/kccachetest.1*
%{_mandir}/man1/kcdirmgr.1*
%{_mandir}/man1/kcdirtest.1*
%{_mandir}/man1/kcforestmgr.1*
%{_mandir}/man1/kcforesttest.1*
%{_mandir}/man1/kcgrasstest.1*
%{_mandir}/man1/kchashmgr.1*
%{_mandir}/man1/kchashtest.1*
%{_mandir}/man1/kclangctest.1*
%{_mandir}/man1/kcpolymgr.1*
%{_mandir}/man1/kcpolytest.1*
%{_mandir}/man1/kcprototest.1*
%{_mandir}/man1/kcstashtest.1*
%{_mandir}/man1/kctreemgr.1*
%{_mandir}/man1/kctreetest.1*
%{_mandir}/man1/kcutilmgr.1*
%{_mandir}/man1/kcutiltest.1*

%files libs
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING FOSSEXCEPTION LINKEXCEPTION
%doc ChangeLog
%{_libdir}/libkyotocabinet.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/kccachedb.h
%{_includedir}/kccommon.h
%{_includedir}/kccompare.h
%{_includedir}/kccompress.h
%{_includedir}/kcdb.h
%{_includedir}/kcdbext.h
%{_includedir}/kcdirdb.h
%{_includedir}/kcfile.h
%if 0%{?rhel} == 5
%{_includedir}/kcfunctional.h
%endif
%{_includedir}/kchashdb.h
%{_includedir}/kclangc.h
%{_includedir}/kcmap.h
%{_includedir}/kcplantdb.h
%{_includedir}/kcpolydb.h
%{_includedir}/kcprotodb.h
%{_includedir}/kcregex.h
%{_includedir}/kcstashdb.h
%{_includedir}/kctextdb.h
%{_includedir}/kcthread.h
%{_includedir}/kcutil.h
%{_libdir}/libkyotocabinet.so
%{_libdir}/pkgconfig/kyotocabinet.pc

%files apidocs
%defattr(-,root,root,-)
%doc COPYING doc/api/* kyotocabinet.idl

%changelog
* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 1.2.76-17
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.76-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.76-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.76-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Feb 12 2017 Robert Scheck <robert@fedoraproject.org> 1.2.76-13
- Replace patch from openSUSE by the Debian one to not only build
  kyotocabinet with GCC >= 6 but also with GCC >= 7 (#1307706 #c15)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.76-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug 14 2016 Robert Scheck <robert@fedoraproject.org> 1.2.76-11
- Added patch from openSUSE to build with GCC >= 6 (#1307706)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.76-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.76-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 03 2015 Kalev Lember <kalevlember@gmail.com> - 1.2.76-8
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.76-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.76-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Nov 17 2013 Robert Scheck <robert@fedoraproject.org> 1.2.76-5
- Corrected wrong dependency of -devel from main to -libs package
- Always enable 8 byte atomics patch e.g. for ppc32 (#1007732 #c5)
- Fixed previously added patch for building under RHEL 5 (#915123)
- Added dependencies to enable lzo and lzma/xz compression support
- Enabled the built-in test suite (with limitations at RHEL 5 ppc)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.76-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 02 2013 Robert Scheck <robert@fedoraproject.org> 1.2.76-3
- Splitted main package into an additional library subpackage
- Added patch and workaround for building under RHEL 5 (#915123)
- Corrected duplicate doc packaging, renamed package to apidocs

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.76-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 12 2013 Robert Scheck <robert@fedoraproject.org> - 1.2.76-1
- Update to 1.2.76 (#760939)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.70-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.70-4
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.70-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 19 2011 Casey Dahlin <cdahlin@redhat.com> - 1.2.70-2
- Prevent -march=native build flag [735822], credit Ville Skyatta
  <ville.skyata@iki.fi>

* Wed Aug 31 2011 Casey Dahlin <cdahlin@redhat.com> - 1.2.70-1
- Update to latest upstream

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 3 2011 Casey Dahlin <cjdahlin@ncsu.edu> - 1.2.31-2
- Correct files list for soname bump

* Mon Jan 3 2011 Casey Dahlin <cdahlin@redhat.com> - 1.2.31-1
- Update to latest upstream

* Mon Dec 13 2010 Casey Dahlin <cdahlin@redhat.com> - 1.2.29-1
- Update to latest upstream

* Fri Dec 10 2010 Casey Dahlin <cdahlin@redhat.com> - 1.2.27-2
- Separate out devel-doc package
- Make sure we own our documentation folder
- Kill rpath

* Wed Dec 8 2010 Casey Dahlin <cdahlin@redhat.com> - 1.2.27-1
- Initial packaging
