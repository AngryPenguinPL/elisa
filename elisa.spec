Summary:	A powerful media player for Plasma
Name:		elisa
Version:	0.0.81
Release:	1
License:	LGPLv2+
Group:		Sound
Url:		https://github.com/KDE/elisa
Source0:	elisa-0.0.81.tar.gz
# Source1:	elisa-0.0.81_ru.tar.gz
# Disabled Patch0 fixed by upstream
# Patch0:		elisa-desktop.patch
# Disabled Patch1 fided by upstream?
# Patch1:		elisa-0.0.1-cmake.patch
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(KF5Archive)
BuildRequires:	cmake(KF5ConfigWidgets)
BuildRequires:	cmake(KF5CoreAddons)
BuildRequires:	cmake(KF5Crash)
BuildRequires:	cmake(KF5Baloo)
BuildRequires:	cmake(KF5Declarative)
BuildRequires:	cmake(KF5DocTools)
BuildRequires:	cmake(KF5FileMetaData)
BuildRequires:	cmake(KF5I18n)
BuildRequires:	cmake(KF5KCMUtils)
BuildRequires:	cmake(KF5XmlGui)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Multimedia)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Qml)
BuildRequires:	pkgconfig(Qt5Quick)
BuildRequires:	pkgconfig(Qt5QuickWidgets)
BuildRequires:	pkgconfig(Qt5QuickControls2)
BuildRequires:	pkgconfig(Qt5Script)
BuildRequires:	pkgconfig(Qt5Sql)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(Qt5WebSockets)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5X11Extras)
BuildRequires:	pkgconfig(Qt5QuickTest)
Requires:	qt5-qtquickcontrols2

%description
A powerful media player for Plasma.

%files -f %{name}.lang
%{_bindir}/elisa
%{_datadir}/applications/org.kde.elisa.desktop
%{_datadir}/kservices5//kcm_elisa_local_file.desktop
%{_datadir}/kpackage/kcms/kcm_elisa_local_file/
%{_iconsdir}/hicolor/scalable/apps/elisa.svg
%{_iconsdir}/hicolor/*/apps/elisa.png
%{_datadir}/metainfo/org.kde.elisa.appdata.xml
%{_qt5_plugindir}/kcms/kcm_elisa_local_file.so

#--------------------------------------------------------------------

%prep
%setup -q

%cmake_kde5

%build
%ninja -C build

%install
%ninja_install -C build

%find_lang %{name} kcm_elisa_local_file %{name}.lang --with-kde --with-html
