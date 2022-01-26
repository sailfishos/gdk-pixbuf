Name:           gdk-pixbuf
Version:        2.42.6
Release:        1
Summary:        An image loading library
License:        LGPLv2+
URL:            http://www.gtk.org
Source0:        gdk-pixbuf-%{version}.tar.xz

BuildRequires:  gettext
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(shared-mime-info)
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  meson
BuildRequires:  pkgconfig(gobject-introspection-1.0) >= 0.9.3

# We also need MIME information at runtime
Requires: shared-mime-info

%description
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
clutter.

%package modules
Summary: Additional image modules for gdk-pixbuf
Requires: %{name} = %{version}-%{release}

%description modules
This package contains the additional modules that are needed to load various
image formats such as ICO and JPEG.

%package devel
Summary: Development files for gdk-pixbuf
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the libraries and header files that are needed
for writing applications that are using gdk-pixbuf.

%package tests
Summary: Tests for the %{name} package
Requires: %{name} = %{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%prep
%setup -q -n %{name}-%{version}/%{name}

%build
%meson -Dbuiltin_loaders=png \
       -Ddocs=false \
       -Dman=false

%global _smp_mflags -j1
%meson_build

%install
%meson_install

touch $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache

(cd $RPM_BUILD_ROOT%{_bindir}
 mv gdk-pixbuf-query-loaders gdk-pixbuf-query-loaders-%{__isa_bits}
)

%find_lang gdk-pixbuf

%transfiletriggerin -- %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache

%transfiletriggerpostun -- %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f gdk-pixbuf.lang
%license COPYING
%doc NEWS
%{_libdir}/libgdk_pixbuf-2.0.so.*
%{_libdir}/girepository-1.0
%dir %{_libdir}/gdk-pixbuf-2.0
%dir %{_libdir}/gdk-pixbuf-2.0/2.10.0
%dir %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
%ghost %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache
%{_bindir}/gdk-pixbuf-query-loaders-%{__isa_bits}
%{_bindir}/gdk-pixbuf-thumbnailer
%{_datadir}/thumbnailers/

%files modules
%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/*.so

%files devel
%dir %{_includedir}/gdk-pixbuf-2.0
%{_includedir}/gdk-pixbuf-2.0/gdk-pixbuf
%{_libdir}/libgdk_pixbuf-2.0.so
%{_libdir}/pkgconfig/gdk-pixbuf-2.0.pc
%{_bindir}/gdk-pixbuf-csource
%{_bindir}/gdk-pixbuf-pixdata
%{_datadir}/gir-1.0

%files tests
%{_libexecdir}/installed-tests
%{_datadir}/installed-tests
