#
# spec file for package 
#
# Copyright (c) specCURRENT_YEAR SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Name:           zlog
Version:        1.2.12
Release:        3.1
License:        LGPL-2.1
Summary:        A high-performance, thread safe, pure C logging library
Url:            http://hardysimpson.github.com/zlog/
Group:          Development/Libraries/C and C++
# current 1.2.8 is latest stable realy...
Source0:        https://github.com/HardySimpson/zlog/archive/%{version}/zlog-%{version}.tar.gz
Patch0:         zlog-1.2.12-autoconf.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  fdupes
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
zlog is a reliable, high-performance, thread safe, flexible, clear-model, pure C logging library.
Actually, in the C world there is NO good logging library for application like logback
in java or log4cxx in c++. printf can work,
but can not be easily redirected or reformat. syslog is slow and is designed for system use.

%package devel
Group:          Development/Libraries/C and C++
Summary:        Library and header files for developing with zlog logging library
Requires:       %name = %version
%description devel
Library and header files for developing with zlog thread safe, pure c logging library


%prep
%setup -q
%patch0 -p1

%build
REF_DATE=$(LANG=C date -r src/version.h +"%%b %%d %%Y")
REF_TIME=$(LANG=C date -r src/version.h +"%%H:%%M:%%S")

find -name "*.c" -exec sed -i -e "s/__DATE__/\"${REF_DATE}\"/g" -e "s/__TIME__/\"${REF_TIME}\"/g" {} \;

sh -x ./autogen.sh
%configure --docdir=%{_defaultdocdir}/%{name} --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%buildroot
# remove libtool library descriptors
find %{buildroot}/%{_libdir} -name "*.la" -exec rm -vf {} ';'
%fdupes -s %{buildroot}/%{_defaultdocdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README COPYING TODO
%{_bindir}/zlog-chk-conf
%{_libdir}/libzlog.so.*
%{_mandir}/man1/zlog-chk-conf.1*

%files devel
%defattr(-,root,root)
%{_libdir}/libzlog.so
%{_includedir}/zlog.h

%changelog
* Thu Sep 26 2013 boris@steki.net
- updated to latest upstream 1.2.12
  - bugfix for avoid segmentation fault if call zlog_init()
    many times
  - static file rule to emulate python's WatchedFileHandler mode
    when used with external log rotation
  - changed licensing LGPL v3 -> LGPL v2.1
* Mon Feb 11 2013 boris@steki.net
- updated to latest upstream 1.2.9
  * fix for thread instance applied
* Mon Feb  4 2013 boris@steki.net
- update to latest upstream version 1.2.8 + bugfixes
  git hash = 1a160f7f072c721e8dd63f3db19c7bbe92d8179c
* Fri Dec 14 2012 boris@steki.net
- initial packaging of zlog with 1.2.7 version
