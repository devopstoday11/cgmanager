#
# cgmanager: cgroup manager daemon
#
# Copyright (C) 2013 Oracle
#
# Authors:
# Dwight Engen <dwight.engen@oracle.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

Name: cgmanager
Version: 0.36
Release: 1%{?dist}
URL: http://cgmanager.linuxcontainers.org
Source: http://cgmanager.linuxcontainers.org/downloads/%{name}-%{version}.tar.gz
Summary: Linux cgroup manager
Group: Applications/System
License: LGPLv2+
BuildRoot: %{_tmppath}/%{name}-%{version}-build
Requires: dbus libnih
BuildRequires: libnih-devel dbus-devel help2man

%description
CGManager is a central privileged daemon that manages all your cgroups for
you through a simple DBus API.  It's designed to work with nested LXC
containers as well as accepting unprivileged requests including resolving
user namespaces UIDs/GIDs.

%package	libs
Summary:	Shared library files for %{name}
Group:		System Environment/Libraries
%description	libs
The %{name}-libs package contains libraries for running %{name} applications.

%package	devel
Summary:	Development library for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}, pkgconfig
%description	devel
The %{name}-devel package contains header files and library needed for
development with %{name}.

%prep
%setup -q -n %{name}-%{version}
%build
PATH=$PATH:/usr/sbin:/sbin %configure $args
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find %{buildroot} -type f -name '*.la' -exec rm -f {} ';'

%clean
rm -rf %{buildroot}

%post
%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man8/*
%{_datadir}/%{name}/*

%files libs
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%changelog
* Mon Mar 24 2014 Dwight Engen <dwight.engen@oracle.com> - 0.23
remove libnih-dbus Requires since there is no such package, libnih is sufficient

* Mon Mar 24 2014 Dwight Engen <dwight.engen@oracle.com> - 0.22
add cgm script

* Tue Feb 04 2014 Dwight Engen <dwight.engen@oracle.com> - 0.19
- created
