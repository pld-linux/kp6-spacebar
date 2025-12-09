#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeplasmaver	6.5.4
%define		qtver		6.7.0
%define		kpname		spacebar
%define		kf6_ver		6.5.0

Summary:	A SMS/MMS messaging client
Summary(pl.UTF-8):	Program do wysyłania SMSów|MMSów
Name:		kp6-%{kpname}
Version:	6.5.4
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	fb27d91f101784b36d23dd108dc213af
URL:		https://invent.kde.org/plasma-mobile/spacebar
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Sql-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	curl-devel
BuildRequires:	futuresql-qt6-devel
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kf6_ver}
BuildRequires:	kf6-kconfig-devel >= %{kf6_ver}
BuildRequires:	kf6-kcontacts-devel >= %{kf6_ver}
BuildRequires:	kf6-kcoreaddons-devel >= %{kf6_ver}
BuildRequires:	kf6-kcrash-devel >= %{kf6_ver}
BuildRequires:	kf6-kdbusaddons-devel >= %{kf6_ver}
BuildRequires:	kf6-ki18n-devel >= 6.7.0
BuildRequires:	kf6-kio-devel >= %{kf6_ver}
BuildRequires:	kf6-kirigami-addons-devel >= 1.4
BuildRequires:	kf6-kirigami-devel >= %{kf6_ver}
BuildRequires:	kf6-knotifications-devel >= %{kf6_ver}
BuildRequires:	kf6-kpeople-devel >= %{kf6_ver}
BuildRequires:	kf6-kwindowsystem-devel >= %{kf6_ver}
BuildRequires:	kf6-modemmanager-qt-devel >= %{kf6_ver}
BuildRequires:	libphonenumber-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qcoro-qt6-devel
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	kp5-spacebar < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Spacebar is a SMS/MMS messaging client. It allows you to send text
messages, pictures and other files over a cellular network.

%description -l pl.UTF-8
Spacebar jest programem do wysyłania SMSów|MMSów. Pozwala wysyłać
wiadomości tekstowe, zdjęcia i inne pliki przez sieci komórkowe.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}

%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{kpname}.lang
%defattr(644,root,root,755)
/etc/xdg/autostart/org.kde.spacebar.daemon.desktop
%attr(755,root,root) %{_bindir}/spacebar
%attr(755,root,root) %{_bindir}/spacebar-fakeserver
%attr(755,root,root) %{_prefix}/libexec/spacebar-daemon
%{_desktopdir}/org.kde.spacebar.desktop
%{_iconsdir}/hicolor/scalable/apps/org.kde.spacebar.svg
%{_datadir}/knotifications6/spacebar.notifyrc
%{_datadir}/metainfo/org.kde.spacebar.appdata.xml
