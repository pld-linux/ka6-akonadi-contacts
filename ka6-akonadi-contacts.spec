#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.08.1
%define		qtver		5.15.2
%define		kaname		akonadi-contacts
Summary:	Akonadi Contacts
Name:		ka6-%{kaname}
Version:	24.08.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	04128272ed93c3b9d3409a00fe9ffe2b
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6Test-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	gpgme-qt6-devel
BuildRequires:	ka6-akonadi-devel >= %{kdeappsver}
BuildRequires:	ka6-grantleetheme-devel >= %{kdeappsver}
BuildRequires:	ka6-kmime-devel >= %{kdeappsver}
BuildRequires:	ka6-libkleo-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= 5.51.0
BuildRequires:	kf6-kcmutils-devel >= 5.87.0
BuildRequires:	kf6-kcodecs-devel >= 5.51.0
BuildRequires:	kf6-kcompletion-devel >= 5.51.0
BuildRequires:	kf6-kcontacts-devel >= 5.65.0
BuildRequires:	kf6-kdbusaddons-devel >= 5.51.0
BuildRequires:	kf6-ki18n-devel >= 5.51.0
BuildRequires:	kf6-kiconthemes-devel >= 5.51.0
BuildRequires:	kf6-kio-devel >= 5.51.0
BuildRequires:	kf6-kitemmodels-devel >= 5.87.0
BuildRequires:	kf6-ktextwidgets-devel >= 5.51.0
BuildRequires:	kf6-prison-devel >= 5.51.0
BuildRequires:	ninja
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Akonadi Contacts is a library that effectively bridges the
type-agnostic API of the Akonadi client libraries and the
domain-specific KContacts library. It provides jobs, models and other
helpers to make working with contacts and addressbooks through Akonadi
easier.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt6/plugins/akonadi_serializer_addressee.so
%attr(755,root,root) %{_libdir}/qt6/plugins/akonadi_serializer_contactgroup.so
%{_datadir}/akonadi/plugins/serializer/akonadi_serializer_addressee.desktop
%{_datadir}/akonadi/plugins/serializer/akonadi_serializer_contactgroup.desktop
%attr(755,root,root) %{_libdir}/libKPim6AkonadiContactCore.so.*.*
%ghost %{_libdir}/libKPim6AkonadiContactCore.so.6
%attr(755,root,root) %{_libdir}/libKPim6AkonadiContactWidgets.so.*.*
%ghost %{_libdir}/libKPim6AkonadiContactWidgets.so.6
%{_datadir}/kf6/akonadi/contact/data/zone.tab
%{_datadir}/kf6/akonadi/contact/pics/world.jpg
%{_datadir}/qlogging-categories6/akonadi-contacts.categories
%{_datadir}/qlogging-categories6/akonadi-contacts.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KPim6/AkonadiContactCore
%{_includedir}/KPim6/AkonadiContactWidgets
%{_libdir}/cmake/KPim6AkonadiContactCore
%{_libdir}/cmake/KPim6AkonadiContactWidgets
%{_libdir}/libKPim6AkonadiContactCore.so
%{_libdir}/libKPim6AkonadiContactWidgets.so
