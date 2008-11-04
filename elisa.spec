%define debug_package	%{nil}

%define rel	1

%define svn	0
%define pre	0
%if %svn
%define release		%mkrel 0.%svn.%rel
%define distname	%name-%svn.tar.lzma
%define dirname		%name
%else
%if %pre
%define release		%mkrel 0.%pre.%rel
%define distname	%name-%version.%pre.tar.gz
%define dirname		%name-%version.%pre
%else
%define release		%mkrel %rel
%define distname	%name-%version.tar.gz
%define dirname		%name-%version
%endif
%endif

# It's the same for releases, but different for pre-releases: please
# don't remove, even if it seems superfluous - AdamW 2008/03
%define fversion	%{version}

Summary:	Media center written in Python
Name:		elisa
Version:	0.5.17
Release:	%{release}
# For SVN:
# svn co https://code.fluendo.com/elisa/svn/trunk elisa
Source0:	http://elisa.fluendo.com/static/download/elisa/%{distname}
# Make sure some config upgrader widget doesn't enable the auto-updater
# - AdamW 2008/07
Patch0:		elisa-0.5.3-updater.patch
License:	GPLv3 and MIT
Group:		Graphical desktop/Other
URL:		http://elisa.fluendo.com/
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	python
BuildRequires:	python-setuptools
BuildRequires:	python-devel
BuildRequires:	python-twisted
BuildRequires:	ImageMagick
BuildRequires:	desktop-file-utils
BuildRequires:	gstreamer0.10-python
Requires:	elisa-plugins-good = %{version}
Requires:	elisa-plugins-bad = %{version}
Requires:	elisa-core = %{version}
Suggests:	elisa-plugins-ugly = %{version}
Suggests:	gstreamer0.10-libvisual

%description
Elisa is a project to create an open source cross platform media center 
solution. Elisa runs on top of the GStreamer multimedia framework and 
takes full advantage of harware acceleration provided by modern graphic 
cards by using OpenGL APIs. In addition to personal video recorder 
functionality (PVR) and Music Jukebox support, Elisa will also 
interoperate with devices following the DLNA standard like Intel’s ViiV 
systems.

%package core
Summary:	Media center written in Python: core files
Group:		Development/Python
Requires:	pigment-python
Requires:	python-imaging
Requires:	python-twisted
Requires:	python-twisted-web2
Requires:	gnome-python-extras
Requires:	gstreamer0.10-python
Requires:	gstreamer0.10-plugins-base
Requires:	python-sqlite2
Requires:	pyxdg
Requires:	python-setuptools
Suggests:	gstreamer0.10-plugins-good
Suggests:	gstreamer0.10-plugins-bad
Suggests:	python-gpod
Suggests:	python-dbus
# To fix upgrade: thanks fcrozat (#44627) - AdamW 2008/10
Conflicts:	elisa-plugins-good <= 0.3.5

%description core
Elisa is a project to create an open source cross platform media center 
solution. Elisa runs on top of the GStreamer multimedia framework and 
takes full advantage of harware acceleration provided by modern graphic 
cards by using OpenGL APIs. In addition to personal video recorder 
functionality (PVR) and Music Jukebox support, Elisa will also 
interoperate with devices following the DLNA standard like Intel’s ViiV 
systems. This package contains the core Python files for Elisa. It is
split from the binaries for packaging reasons.

%prep
%setup -q -n %{dirname}
%patch0 -p1 -b .updater

# correct mandir
sed -i -e 's,man/man1,share/man/man1,g' setup.py

%build

%install
rm -rf %{buildroot}
python setup.py install --root=%{buildroot} --single-version-externally-managed --compile --optimize=2

# Install some stuff manually because the build process can't.
install -D -m644 data/%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# Generate and install 32x32 and 16x16 icons.
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{32x32,16x16}/apps

convert -scale 32 data/%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 data/%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

# Menu file
rm -f %{buildroot}%{_datadir}/applications/%{name}.desktop
rm -f %{buildroot}%{_datadir}/applications/%{name}-mobile.desktop
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=Elisa Media Center
Comment=Play movies and songs on TV with remote
Exec=%{name} %U
StartupWMClass=%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GNOME;GTK;AudioVideo;Audio;Video;Player;X-MandrivaLinux-CrossDesktop;
X-Osso-Service=com.fluendo.elisa
EOF

#don't want these
rm -rf %{buildroot}%{py_puresitedir}/mswin32
rm -f %{buildroot}%{_datadir}/pixmaps/%{name}.png
rm -f %{buildroot}%{_datadir}/icons/%{name}.png
rm -rf %{buildroot}%{_datadir}/mobile-basic-flash

# as there's three plugins packages that aren't interdependent, best
# let the core package own the plugins dir - AdamW 2008/02
mkdir -p %{buildroot}%{py_puresitedir}/%{name}/plugins

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS FAQ FIRST_RUN NEWS RELEASE TRANSLATORS
%{_bindir}/%{name}
%{_bindir}/%{name}-get
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/%{name}.1*
%{_datadir}/dbus-1/services/*.service

%files core
%defattr(-,root,root)
%{py_puresitedir}/%{name}
%{py_puresitedir}/%{name}_generic_setup.py*
%{py_puresitedir}/%{name}-%{fversion}-py%{pyver}-nspkg.pth
%{py_puresitedir}/%{name}-%{fversion}-py%{pyver}.egg-info

