#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeappsver	25.04.3
# packages version, not cmake config version (which is 6.2.2)
%define		ka_ver		%{version}
%define		kf_ver		6.3.0
%define		qt_ver		6.6.0
%define		kaname		akonadi-contacts
Summary:	Akonadi Contacts
Summary(pl.UTF-8):	Komponent kontaktów dla Akonadi
Name:		ka6-%{kaname}
Version:	25.04.3
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	e04b43dfb0fa92c4f1f6701c039b6486
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qt_ver}
BuildRequires:	Qt6Gui-devel >= %{qt_ver}
BuildRequires:	Qt6Test-devel >= %{qt_ver}
BuildRequires:	Qt6Widgets-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	ka6-akonadi-devel >= %{ka_ver}
BuildRequires:	ka6-grantleetheme-devel >= %{ka_ver}
BuildRequires:	ka6-kmime-devel >= %{ka_ver}
BuildRequires:	kf6-extra-cmake-modules >= %{kf_ver}
BuildRequires:	kf6-kcodecs-devel >= %{kf_ver}
BuildRequires:	kf6-kcolorscheme-devel >= %{kf_ver}
BuildRequires:	kf6-kcompletion-devel >= %{kf_ver}
BuildRequires:	kf6-kcontacts-devel >= %{kf_ver}
BuildRequires:	kf6-kcoreaddons-devel >= %{kf_ver}
BuildRequires:	kf6-ki18n-devel >= %{kf_ver}
BuildRequires:	kf6-kiconthemes-devel >= %{kf_ver}
BuildRequires:	kf6-kio-devel >= %{kf_ver}
BuildRequires:	kf6-kservice-devel >= %{kf_ver}
BuildRequires:	kf6-ktextaddons-devel >= 1.5.4
BuildRequires:	kf6-ktexttemplate-devel
BuildRequires:	kf6-ktextwidgets-devel >= %{kf_ver}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kf_ver}
BuildRequires:	kf6-kxmlgui-devel >= %{kf_ver}
BuildRequires:	kf6-prison-devel >= %{kf_ver}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	qgpgme-qt6-devel
BuildRequires:	qt6-build >= %{qt_ver}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6Core >= %{qt_ver}
Requires:	Qt6Gui >= %{qt_ver}
Requires:	Qt6Widgets >= %{qt_ver}
Requires:	ka6-akonadi >= %{ka_ver}
Requires:	ka6-grantleetheme >= %{ka_ver}
Requires:	ka6-kmime >= %{ka_ver}
Requires:	kf6-kcodecs >= %{kf_ver}
Requires:	kf6-kcolorscheme >= %{kf_ver}
Requires:	kf6-kcompletion >= %{kf_ver}
Requires:	kf6-kcontacts >= %{kf_ver}
Requires:	kf6-kcoreaddons >= %{kf_ver}
Requires:	kf6-ki18n >= %{kf_ver}
Requires:	kf6-kiconthemes >= %{kf_ver}
Requires:	kf6-kio >= %{kf_ver}
Requires:	kf6-ktextaddons >= 1.5.4
Requires:	kf6-ktextwidgets >= %{kf_ver}
Requires:	kf6-kwidgetsaddons >= %{kf_ver}
Requires:	kf6-kxmlgui >= %{kf_ver}
Requires:	kf6-prison >= %{kf_ver}
Obsoletes:	ka5-akonadi-contacts < 24
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Akonadi Contacts is a library that effectively bridges the
type-agnostic API of the Akonadi client libraries and the
domain-specific KContacts library. It provides jobs, models and other
helpers to make working with contacts and addressbooks through Akonadi
easier.

%description -l pl.UTF-8
Akonadi Contacts to biblioteka efektywnie łącząca niezależne od typów
API bibliotek klienckich Akonadi oraz bibliotekę KContacts. Zapewnia
funkcje pomocnicze dla zadań, modeli itp., ułatwiające pracę z
kontaktami i książkami adresowymi poprzez Akonadi.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Widgets-devel >= %{qt_ver}
Requires:	ka6-akonadi-devel >= %{ka_ver}
Requires:	ka6-grantleetheme-devel >= %{ka_ver}
Requires:	kf6-kcontacts-devel >= %{kf_ver}
Obsoletes:	ka5-akonadi-contacts-devel < 24

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

# akonadicontact6 and akonadicontact6-serializer domains
%find_lang %{kaname} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libKPim6AkonadiContactCore.so.*.*.*
%ghost %{_libdir}/libKPim6AkonadiContactCore.so.6
%attr(755,root,root) %{_libdir}/libKPim6AkonadiContactWidgets.so.*.*.*
%ghost %{_libdir}/libKPim6AkonadiContactWidgets.so.6
%attr(755,root,root) %{_libdir}/qt6/plugins/akonadi_serializer_addressee.so
%attr(755,root,root) %{_libdir}/qt6/plugins/akonadi_serializer_contactgroup.so
%{_datadir}/akonadi/plugins/serializer/akonadi_serializer_addressee.desktop
%{_datadir}/akonadi/plugins/serializer/akonadi_serializer_contactgroup.desktop
%{_datadir}/kf6/akonadi/contact
%{_datadir}/qlogging-categories6/akonadi-contacts.categories
%{_datadir}/qlogging-categories6/akonadi-contacts.renamecategories

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKPim6AkonadiContactCore.so
%{_libdir}/libKPim6AkonadiContactWidgets.so
%{_includedir}/KPim6/AkonadiContactCore
%{_includedir}/KPim6/AkonadiContactWidgets
%{_libdir}/cmake/KPim6AkonadiContactCore
%{_libdir}/cmake/KPim6AkonadiContactWidgets
