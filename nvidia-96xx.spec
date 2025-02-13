# I love OpenSource :-(
%define xconfigversion	96.43.20

# the highest supported videodrv abi
%define videodrv_abi    12

%define priority	9600

# pkg0: plain archive
# pkg1: + precompiled modules
# pkg2: + 32bit compatibility libraries
%define pkgname32	NVIDIA-Linux-x86-%{version}-pkg0
%define pkgname64	NVIDIA-Linux-x86_64-%{version}-pkg2

%define drivername		nvidia96xx
%define driverpkgname		x11-driver-video-nvidia96xx
%define modulename		%{drivername}
%define xorg_libdir		%{_libdir}/xorg
%define xorg_extra_modules	%{_libdir}/xorg/extra-modules
%define nvidia_driversdir	%{_libdir}/%{drivername}/xorg
%define nvidia_extensionsdir	%{_libdir}/%{drivername}/xorg
%define nvidia_modulesdir	%{_libdir}/%{drivername}/xorg
%define nvidia_libdir		%{_libdir}/%{drivername}
%define nvidia_libdir32		%{_prefix}/lib/%{drivername}
%define nvidia_bindir		%{nvidia_libdir}/bin
%define nvidia_deskdir		%{_datadir}/%{drivername}
%define nvidia_xvmcconfdir	%{_sysconfdir}/%{drivername}
%define nvidia_xinitdir         %{_sysconfdir}/%{drivername}
%define ld_so_conf_dir		%{_sysconfdir}/%{drivername}
%define ld_so_conf_file		ld.so.conf

%if %{mdkversion} <= 200910
%define nvidia_driversdir	%{xorg_libdir}/modules/drivers/%{drivername}
%endif

%if %{mdkversion} <= 200900
%define nvidia_extensionsdir	%{xorg_libdir}/modules/extensions/%{drivername}
%define nvidia_modulesdir       %{xorg_libdir}/modules
%endif

%if %{mdkversion} <= 200710
%define driverpkgname		%{drivername}
%endif

%if %{mdkversion} <= 200700
%define drivername		nvidia
%define ld_so_conf_dir		%{_sysconfdir}/ld.so.conf.d/GL
%define ld_so_conf_file		%{drivername}.conf
%endif

%if %{mdkversion} <= 200600
%define xorg_libdir		%{_prefix}/X11R6/%{_lib}
%define ld_so_conf_dir		%{_sysconfdir}/ld.so.conf.d
%define nvidia_driversdir	%{xorg_libdir}/modules/drivers
%define nvidia_bindir		%{_bindir}
%define nvidia_xvmcconfdir	%{_sysconfdir}/X11
%define nvidia_deskdir		%{_datadir}/applications
%define nvidia_xinitdir		%{_sysconfdir}/X11/xinit.d
%endif

%define biarches x86_64
%ifarch %{ix86}
%define nsource %{SOURCE0}
%define pkgname %{pkgname32}
%endif
%ifarch x86_64
%define nsource %{SOURCE1}
%define pkgname %{pkgname64}
%endif

# Other packages should not require any NVIDIA libraries, and this package
# should not be pulled in when libGL.so.1 is required
%if %{_use_internal_dependency_generator}
%define __noautoprov '\\.so|libGL\\.so\\.1(.*)|devel\\(libGL(.*)'
%define common_requires_exceptions libGLcore\\.so|libnvidia.*\\.so
%else
%define _provides_exceptions \\.so
%define common_requires_exceptions libGLcore\\.so\\|libnvidia.*\\.so
%endif

%ifarch %{biarches}
# (anssi) Allow installing of 64-bit package if the runtime dependencies
# of 32-bit libraries are not satisfied. If a 32-bit package that requires
# libGL.so.1 is installed, the 32-bit mesa libs are pulled in and that will
# pull the dependencies of 32-bit nvidia libraries in as well.
%if %{_use_internal_dependency_generator}
%define __noautoreq '%{common_requires_exceptions}|lib.*so\\.[^(]+(\\([^)]+\\))?$'
%else
%define __noautoreq %{common_requires_exceptions}\\|lib.*so\\.[^(]\\+\\(([^)]\\+)\\)\\?$
%endif
%else
%if %{_use_internal_dependency_generator}
%define __noautoreq '%{common_requires_exceptions}'
%else
%define __noautoreq %{common_requires_exceptions}
%endif
%endif

Summary:	NVIDIA proprietary X.org driver and libraries for most GF2/3/4 class cards
Name:		nvidia-96xx
Version:	96.43.23
Release:	2
Source0:	ftp://download.nvidia.com/XFree86/Linux-x86/%{version}/%{pkgname32}.run
Source1:	ftp://download.nvidia.com/XFree86/Linux-x86_64/%{version}/%{pkgname64}.run
# GPLv2 source code; see also http://cgit.freedesktop.org/~aplattner/
Source2:	ftp://download.nvidia.com/XFree86/nvidia-settings/nvidia-settings-%{xconfigversion}.tar.gz
Source3:	ftp://download.nvidia.com/XFree86/nvidia-xconfig/nvidia-xconfig-%{xconfigversion}.tar.gz
# -Werror=format-string
Patch0:		nvidia-settings-format-string.patch
# https://qa.mandriva.com/show_bug.cgi?id=39921
Patch1:		nvidia-settings-enable-dyntwinview-mdv.patch
# --as-needed + --no-undefined
Patch2:		nvidia-xconfig-ldflags-order.patch
# Understand Disable keyword in xorg.conf, from upstream 190.40:
Patch4:		nvidia-xf86config-parser-add-disable-keyword.patch
# (tpg) in 2010.1+ X_XF86VidModeGetGammaRampSize is in xf86vmproto.h and not in xf86vmode.h
Patch5:		nvidia-settings-1.0-missing-header.patch
Patch6:		nvidia-96xx-96.43.20-link-against-libdl.patch
Patch7:		nvidia-96xx-96.43.20-dont-check-patchlevel-and-sublevel.patch
License:	Freeware
URL:		https://www.nvidia.com/object/unix.html
Group: 		System/Kernel and hardware
ExclusiveArch:	%{ix86} x86_64
BuildRequires:	imagemagick
BuildRequires:  pkgconfig(gtk+-x11-2.0)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(gl)
%if %{mdkversion} >= 200700
BuildRequires:	pkgconfig(xv)
%endif
%if "%{driverpkgname}" == "nvidia"
# old nvidia package had different versioning
Epoch:		1
%endif

%description
Source package of the 96xx legacy NVIDIA proprietary driver series.
Binary packages are named x11-driver-video-nvidia96xx on Mandriva
Linux 2008 and later, nvidia96xx on 2007.1, and nvidia on 2007.0 and
earlier.

%package -n %{driverpkgname}
Summary:	NVIDIA proprietary X.org driver and libraries for most GF2/3/4 class cards
Group:		System/Kernel and hardware
%if %{mdkversion} >= 200700
Requires(post): update-alternatives >= 1.9.0
Requires(postun): update-alternatives >= 1.9.0
%endif
%if %{mdkversion} >= 200800
Conflicts:	harddrake < 10.4.163
Conflicts:	drakx-kbd-mouse-x11 < 0.21
Conflicts:	x11-server-common < 1.3.0.0-17
Suggests:	%{drivername}-doc-html
%endif
%if %{mdkversion} >= 200810
Requires:       kmod(%{modulename}) = %{version}
%endif
%if %{mdkversion} >= 200910
Conflicts:	x11-server-common < 1.6.0-11
%endif
Provides:	NVIDIA_GLX
%if %{mdkversion} >= 200800
Obsoletes:	nvidia96xx < %{version}-%{release}
Provides:	nvidia96xx = %{version}-%{release}
%endif
%if %{mdkversion} <= 200600
Conflicts:	nvidia_legacy
%endif
# Conflict with the next videodrv ABI break.
# The NVIDIA driver supports the previous ABI versions as well and therefore
# a strict version-specific requirement would not be enough.
### This is problematic as it can cause removal of xserver instead (Anssi 04/2011)
###Conflicts:  xserver-abi(videodrv-%(echo $((%{videodrv_abi} + 1))))

%description -n %{driverpkgname}
NVIDIA proprietary X.org graphics driver, related libraries and
configuration tools for most NVIDIA GeForce2/3/4 class video cards.

NOTE: You should use XFdrake to configure your NVIDIA card. The
correct packages will be automatically installed and configured.

If you do not want to use XFdrake, see README.manual-setup.

This NVIDIA driver should be used with GeForce 3, GeForce4 and
GeForce 2 MX cards.

%package -n dkms-%{drivername}
Summary:	NVIDIA kernel module for most GF2/3/4 class cards
Group:		System/Kernel and hardware
Requires:	dkms
Requires(post):	dkms
Requires(preun): dkms
Requires:	%{driverpkgname} = %{version}
%if %{mdkversion} <= 200600
Conflicts:	dkms-nvidia_legacy
%endif

%description -n dkms-%{drivername}
NVIDIA kernel module for most NVIDIA GeForce2/3/4 class video cards.
This is to be used with the %{name} package.

%package -n %{drivername}-devel
Summary:	NVIDIA static XVMC library and headers for most GF2/3/4 cards
Group:		Development/C
Requires:	%{driverpkgname} = %{version}-%{release}
%if %{mdkversion} <= 200700
Conflicts:	nvidia-devel
%endif
%if %{mdkversion} <= 200600
Conflicts:	nvidia_legacy-devel
%endif

%description -n %{drivername}-devel
NVIDIA XvMC static development library and OpenGL headers for most
NVIDIA GeForce2/3/4 class video cards. This package is not required
for normal use.

%package -n %{drivername}-doc-html
Summary:	NVIDIA html documentation (%{drivername})
Group:		System/Kernel and hardware
Requires:	%{driverpkgname} = %{version}-%{release}

%description -n %{drivername}-doc-html
HTML version of the README.txt file provided in package
%{driverpkgname}.

%prep
%setup -q -c -T -a 2 -a 3
sh %{nsource} --extract-only
%patch0 -p0
%patch1 -p0
%patch2 -p0

cd nvidia-settings-1.0
%patch4 -p1
%patch5 -p1
cd ..
cd nvidia-xconfig-1.0
%patch4 -p2
cd ..
%patch6 -p1 -b .libdl~
pushd %{pkgname}
%patch7 -p2 -b .3x~
popd

rm -rf %{pkgname}/usr/src/nv/precompiled

cat > README.install.urpmi <<EOF
This driver is for GeForce 3, GeForce 4 and GeForce 2 MX cards.

Use XFdrake to configure X to use the correct NVIDIA driver. Any needed
packages will be automatically installed if not already present.
1. Run XFdrake as root.
2. Go to the Graphics Card list.
3. Select your card (it is usually already autoselected).
4. Answer any questions asked and then quit.

If you do not want to use XFdrake, see README.manual-setup.
EOF

cat > README.manual-setup <<EOF
This file describes the procedure for the manual installation of this NVIDIA
driver package. You can find the instructions for the recommended automatic
installation in the file 'README.install.urpmi' in this directory.

- Open %{_sysconfdir}/X11/xorg.conf and make the following changes:
  o Change the Driver to "nvidia" in the Device section
  o Make the line below the only 'glx' related line in the Module section:
%if %{mdkversion} >= 200710
      Load "glx"
%if %{mdkversion} >= 200800
  o Remove any 'ModulePath' lines from the Files section
%else
  o Make the lines below the only 'ModulePath' lines in the Files section:
      ModulePath "%{nvidia_extensionsdir}"
      ModulePath "%{xorg_libdir}/modules"
%endif
%else
      Load "%{nvidia_extensionsdir}/libglx.so"
%endif
%if %{mdkversion} >= 200700
- Run "update-alternatives --set gl_conf %{ld_so_conf_dir}/%{ld_so_conf_file}" as root.
- Run "ldconfig -X" as root.
%endif
EOF

mv %{pkgname}/usr/share/doc/html html-doc

# It wants to link Xxf86vm statically (presumably because it is somewhat more
# rare than the other dependencies)
sed -i 's|-Wl,-Bstatic||' nvidia-settings-1.0/Makefile
sed -i 's|-O ||' nvidia-settings-1.0/Makefile
sed -i 's|-O ||' nvidia-xconfig-1.0/Makefile
rm nvidia-settings-1.0/src/*/*.a

%build
mkdir -p bfd
ln -sf $(which ld.bfd) bfd/ld
export PATH="$PWD/bfd:$PATH"

pushd nvidia-settings-1.0
pushd src/libXNVCtrl
#contains Imakefile file which does not seem to work
gcc %{optflags} -c -o NVCtrl.o NVCtrl.c
ar rv libXNVCtrl.a NVCtrl.o
ranlib libXNVCtrl.a
popd
%make CFLAGS="%optflags" LDFLAGS="%{?ldflags}"
popd

pushd nvidia-xconfig-1.0
%make CFLAGS="%optflags %{?ldflags} -IXF86Config-parser"
popd

%install
rm -rf %{buildroot}
cd %{pkgname}/usr

# dkms
install -d -m755 %{buildroot}%{_usrsrc}/%{drivername}-%{version}-%{release}
install -m644 src/nv/* %{buildroot}%{_usrsrc}/%{drivername}-%{version}-%{release}
chmod 0755 %{buildroot}%{_usrsrc}/%{drivername}-%{version}-%{release}/conftest.sh

#install -d -m755 %{buildroot}%{_usrsrc}/%{drivername}-%{version}-%{release}/patches
#install -m644 %{_sourcedir}/some.patch \
#              %{buildroot}%{_usrsrc}/%{drivername}-%{version}-%{release}/patches

cat > %{buildroot}%{_usrsrc}/%{drivername}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_NAME="%{drivername}"
PACKAGE_VERSION="%{version}-%{release}"
BUILT_MODULE_NAME[0]="nvidia"
DEST_MODULE_LOCATION[0]="/kernel/drivers/char/drm"
%if %{mdkversion} >= 200710
DEST_MODULE_NAME[0]="%{modulename}"
%endif
MAKE[0]="make IGNORE_XEN_PRESENCE=1 SYSSRC=\${kernel_source_dir} module"
CLEAN="make -f Makefile.kbuild clean"
AUTOINSTALL="yes"
MAKE[0]="make IGNORE_XEN_PRESENCE=1 SYSSRC=\${kernel_source_dir} module"
EOF

# OpenGL headers
install -d -m755	%{buildroot}%{_includedir}/%{drivername}
cp -a include/*		%{buildroot}%{_includedir}/%{drivername}

# install binaries
install -d -m755	%{buildroot}%{nvidia_bindir}
install -m755 bin/*	%{buildroot}%{nvidia_bindir}
rm %{buildroot}%{nvidia_bindir}/{makeself.sh,mkprecompiled,tls_test,tls_test_dso.so}
install -m755 ../../nvidia-settings-1.0/nvidia-settings %{buildroot}%{nvidia_bindir}
install -m755 ../../nvidia-xconfig-1.0/nvidia-xconfig %{buildroot}%{nvidia_bindir}
%if %{mdkversion} >= 200700
install -d -m755			%{buildroot}%{_bindir}
touch					%{buildroot}%{_bindir}/nvidia-settings
touch					%{buildroot}%{_bindir}/nvidia-xconfig
touch					%{buildroot}%{_bindir}/nvidia-bug-report.sh
# rpmlint:
chmod 0755				%{buildroot}%{_bindir}/*
%endif

# install man pages
install -d -m755		%{buildroot}%{_mandir}/man1
install -m644 share/man/man1/*	%{buildroot}%{_mandir}/man1
rm %{buildroot}%{_mandir}/man1/nvidia-installer.1*
rm %{buildroot}%{_mandir}/man1/nvidia-settings.1*
rm %{buildroot}%{_mandir}/man1/nvidia-xconfig.1*
install -m755 ../../nvidia-settings-1.0/doc/nvidia-settings.1 %{buildroot}%{_mandir}/man1
install -m755 ../../nvidia-xconfig-1.0/nvidia-xconfig.1 %{buildroot}%{_mandir}/man1
# bug #41638 - whatis entries of nvidia man pages appear wrong
gunzip %{buildroot}%{_mandir}/man1/*.gz || :
sed -r -i '/^nvidia\\-[a-z]+ \\- NVIDIA/s,^nvidia\\-,nvidia-,' %{buildroot}%{_mandir}/man1/*.1
%if %{mdkversion} >= 200700
cd %{buildroot}%{_mandir}/man1
rename nvidia alt-%{drivername} *
cd -
touch %{buildroot}%{_mandir}/man1/nvidia-xconfig.1%{_extension}
touch %{buildroot}%{_mandir}/man1/nvidia-settings.1%{_extension}
%endif

# menu entry
%if %{mdkversion} <= 200600
install -d -m755 %{buildroot}/%{_menudir}
cat <<EOF >%{buildroot}/%{_menudir}/%{driverpkgname}
?package(%{driverpkgname}):command="%{nvidia_bindir}/nvidia-settings" \
                  icon=%{drivername}-settings.png \
                  needs="x11" \
                  section="System/Configuration/Hardware" \
                  title="NVIDIA Display Settings" \
                  longtitle="Configure NVIDIA X driver" \
                  xdg="true"
EOF
%endif

install -d -m755 %{buildroot}%{nvidia_deskdir}
cat > %{buildroot}%{nvidia_deskdir}/mandriva-nvidia-settings.desktop <<EOF
[Desktop Entry]
Name=NVIDIA Display Settings
Comment=Configure NVIDIA X driver
Exec=%{_bindir}/nvidia-settings
Icon=%{drivername}-settings
Terminal=false
Type=Application
Categories=GTK;Settings;HardwareSettings;X-MandrivaLinux-System-Configuration;
EOF

install -d -m755	%{buildroot}%{_datadir}/applications
touch			%{buildroot}%{_datadir}/applications/mandriva-nvidia-settings.desktop

# icons
install -d -m755 %{buildroot}/%{_miconsdir} %{buildroot}/%{_iconsdir} %{buildroot}/%{_liconsdir}
convert share/pixmaps/nvidia-settings.png -resize 16x16 %{buildroot}/%{_miconsdir}/%{drivername}-settings.png
convert share/pixmaps/nvidia-settings.png -resize 32x32 %{buildroot}/%{_iconsdir}/%{drivername}-settings.png
convert share/pixmaps/nvidia-settings.png -resize 48x48 %{buildroot}/%{_liconsdir}/%{drivername}-settings.png

# install libraries
install -d -m755						%{buildroot}%{nvidia_libdir}/tls
install -m755 lib/tls/*						%{buildroot}%{nvidia_libdir}/tls
install -m755 lib/*.*						%{buildroot}%{nvidia_libdir}
install -m755 X11R6/lib/*.*					%{buildroot}%{nvidia_libdir}
rm								%{buildroot}%{nvidia_libdir}/*.la
/sbin/ldconfig -n						%{buildroot}%{nvidia_libdir}
%ifarch %{biarches}
install -d -m755						%{buildroot}%{nvidia_libdir32}/tls
install -m755 lib32/tls/*					%{buildroot}%{nvidia_libdir32}/tls
install -m755 lib32/*.*						%{buildroot}%{nvidia_libdir32}
rm								%{buildroot}%{nvidia_libdir32}/*.la
/sbin/ldconfig -n						%{buildroot}%{nvidia_libdir32}
%endif

# create devel symlinks
for file in %{buildroot}%{nvidia_libdir}/*.so.*.* \
%ifarch %{biarches}
	%{buildroot}%{nvidia_libdir32}/*.so.*.* \
%endif
; do
	symlink=${file%%.so*}.so
	[ -e $symlink ] && continue
	# only provide symlinks that the installer does
	grep -q "^$(basename $symlink) " ../.manifest || continue
	ln -s $(basename $file) $symlink
done

# install X.org files
install -d -m755				%{buildroot}%{nvidia_extensionsdir}
install -m755 X11R6/lib/modules/extensions/*	%{buildroot}%{nvidia_extensionsdir}
ln -s libglx.so.%{version}			%{buildroot}%{nvidia_extensionsdir}/libglx.so
install -d -m755				%{buildroot}%{nvidia_driversdir}
install -m755 X11R6/lib/modules/drivers/*	%{buildroot}%{nvidia_driversdir}

%if %{mdkversion} >= 200700 && %{mdkversion} <= 200910
touch %{buildroot}%{xorg_libdir}/modules/drivers/nvidia_drv.so
%endif
%if %{mdkversion} >= 200800 && %{mdkversion} <= 200900
touch %{buildroot}%{xorg_libdir}/modules/extensions/libglx.so
%endif

# ld.so.conf
install -d -m755		%{buildroot}%{ld_so_conf_dir}
echo "%{nvidia_libdir}" >	%{buildroot}%{ld_so_conf_dir}/%{ld_so_conf_file}
%ifarch %{biarches}
echo "%{nvidia_libdir32}" >>	%{buildroot}%{ld_so_conf_dir}/%{ld_so_conf_file}
%endif
%if %{mdkversion} >= 200700
install -d -m755		%{buildroot}%{_sysconfdir}/ld.so.conf.d
touch				%{buildroot}%{_sysconfdir}/ld.so.conf.d/GL.conf
%endif

# modprobe.conf
%if %{mdkversion} >= 200710
install -d -m755			%{buildroot}%{_sysconfdir}/modprobe.d
touch					%{buildroot}%{_sysconfdir}/modprobe.d/display-driver.conf
echo "install nvidia /sbin/modprobe %{modulename} \$CMDLINE_OPTS" > %{buildroot}%{_sysconfdir}/%{drivername}/modprobe.conf
%endif

%if %{mdkversion} < 201100
# modprobe.preload.d
# This is here because sometimes (one case reported by Christophe Fergeau on 04/2010)
# starting X server fails if the driver module is not already loaded.
# This is fixed by the reworked kms-dkms-plymouth-drakx-initrd system in 2011.0.
install -d -m755			%{buildroot}%{_sysconfdir}/modprobe.preload.d
touch					%{buildroot}%{_sysconfdir}/modprobe.preload.d/display-driver
echo "%{modulename}"			>  %{buildroot}%{_sysconfdir}/%{drivername}/modprobe.preload
%endif

# XvMCConfig
install -d -m755 %{buildroot}%{nvidia_xvmcconfdir}
echo "libXvMCNVIDIA_dynamic.so.1" > %{buildroot}%{nvidia_xvmcconfdir}/XvMCConfig

# xinit script
install -d -m755 %{buildroot}%{nvidia_xinitdir}
cat > %{buildroot}%{nvidia_xinitdir}/nvidia-settings.xinit <<EOF
# to be sourced
#
# Do not modify this file; the changes will be overwritten.
# If you want to disable automatic configuration loading, create
# /etc/sysconfig/nvidia-settings with this line: LOAD_NVIDIA_SETTINGS="no"
#
LOAD_NVIDIA_SETTINGS="yes"
[ -f %{_sysconfdir}/sysconfig/nvidia-settings ] && . %{_sysconfdir}/sysconfig/nvidia-settings
[ "\$LOAD_NVIDIA_SETTINGS" = "yes" ] && %{_bindir}/nvidia-settings --load-config-only
EOF
chmod 0755 %{buildroot}%{nvidia_xinitdir}/nvidia-settings.xinit
%if %{mdkversion} >= 200700
install -d -m755 %{buildroot}%{_sysconfdir}/X11/xinit.d
touch %{buildroot}%{_sysconfdir}/X11/xinit.d/nvidia-settings.xinit
%endif

# don't strip files
export EXCLUDE_FROM_STRIP="$(find %{buildroot} -type f \! -name nvidia-settings \! -name nvidia-xconfig)"

%post -n %{driverpkgname}
%if %{mdkversion} >= 200710
# XFdrake used to generate an nvidia.conf file
[ -L %{_sysconfdir}/modprobe.d/nvidia.conf ] || rm -f %{_sysconfdir}/modprobe.d/nvidia.conf
%endif

%if %{mdkversion} >= 200700
%define compat_ext %([ "%{_extension}" == ".bz2" ] || echo %{_extension})
%{_sbindir}/update-alternatives \
	--install %{_sysconfdir}/ld.so.conf.d/GL.conf gl_conf %{ld_so_conf_dir}/%{ld_so_conf_file} %{priority} \
	--slave %{_mandir}/man1/nvidia-settings.1%{_extension} man_nvidiasettings%{compat_ext} %{_mandir}/man1/alt-%{drivername}-settings.1%{_extension} \
	--slave %{_mandir}/man1/nvidia-xconfig.1%{_extension} man_nvidiaxconfig%{compat_ext} %{_mandir}/man1/alt-%{drivername}-xconfig.1%{_extension} \
	--slave %{_datadir}/applications/mandriva-nvidia-settings.desktop nvidia_desktop %{nvidia_deskdir}/mandriva-nvidia-settings.desktop \
	--slave %{_bindir}/nvidia-settings nvidia_settings %{nvidia_bindir}/nvidia-settings \
	--slave %{_bindir}/nvidia-xconfig nvidia_xconfig %{nvidia_bindir}/nvidia-xconfig \
	--slave %{_bindir}/nvidia-bug-report.sh nvidia_bug_report %{nvidia_bindir}/nvidia-bug-report.sh \
	--slave %{_sysconfdir}/X11/XvMCConfig xvmcconfig %{nvidia_xvmcconfdir}/XvMCConfig \
	--slave %{_sysconfdir}/X11/xinit.d/nvidia-settings.xinit nvidia-settings.xinit %{nvidia_xinitdir}/nvidia-settings.xinit \
%if %{mdkversion} <= 200910
	--slave %{_libdir}/xorg/modules/drivers/nvidia_drv.so nvidia_drv %{_libdir}/xorg/modules/drivers/%{drivername}/nvidia_drv.so \
%endif
%if %{mdkversion} >= 200710
	--slave %{_sysconfdir}/modprobe.d/display-driver.conf display-driver.conf %{_sysconfdir}/%{drivername}/modprobe.conf \
%if %{mdkversion} < 201100
	--slave %{_sysconfdir}/modprobe.preload.d/display-driver display-driver.preload %{_sysconfdir}/%{drivername}/modprobe.preload \
%endif
%endif
%if %{mdkversion} >= 200910
	--slave %{xorg_extra_modules} xorg_extra_modules %{nvidia_extensionsdir} \
%else
%if %{mdkversion} >= 200800
	--slave %{_libdir}/xorg/modules/extensions/libglx.so libglx %{nvidia_extensionsdir}/libglx.so \
%endif
%if %{mdkversion} >= 200900
	--slave %{_libdir}/xorg/modules/extensions/libdri.so libdri.so %{_libdir}/xorg/modules/extensions/standard/libdri.so
%endif
%endif
# empty line so that /sbin/ldconfig is not passed to update-alternatives
%endif
# explicit /sbin/ldconfig due to alternatives
/sbin/ldconfig -X

%if %{mdkversion} < 200900
%update_menus
%endif

%postun -n %{driverpkgname}
%if %{mdkversion} >= 200700
if [ ! -f %{ld_so_conf_dir}/%{ld_so_conf_file} ]; then
  %{_sbindir}/update-alternatives --remove gl_conf %{ld_so_conf_dir}/%{ld_so_conf_file}
fi
%endif
# explicit /sbin/ldconfig due to alternatives
/sbin/ldconfig -X

%if %{mdkversion} < 200900
%clean_menus
%endif

%post -n dkms-%{drivername}
/usr/sbin/dkms --rpm_safe_upgrade add -m %{drivername} -v %{version}-%{release} && 
/usr/sbin/dkms --rpm_safe_upgrade build -m %{drivername} -v %{version}-%{release} &&
/usr/sbin/dkms --rpm_safe_upgrade install -m %{drivername} -v %{version}-%{release} --force

# rmmod any old driver if present and not in use (e.g. by X)
rmmod nvidia > /dev/null 2>&1 || true

%preun -n dkms-%{drivername}
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{drivername} -v %{version}-%{release} --all

# rmmod any old driver if present and not in use (e.g. by X)
rmmod nvidia > /dev/null 2>&1 || true

%clean
rm -rf %{buildroot}

%files -n %{driverpkgname}
%defattr(-,root,root)

%doc README.install.urpmi README.manual-setup
%doc %{pkgname}/usr/share/doc/*
%doc %{pkgname}/LICENSE

# ld.so.conf, modprobe.conf, xvmcconfig, xinit
%if %{mdkversion} >= 200710
# 2007.1+
%ghost %{_sysconfdir}/ld.so.conf.d/GL.conf
%ghost %{_sysconfdir}/X11/xinit.d/nvidia-settings.xinit
%ghost %{_sysconfdir}/modprobe.d/display-driver.conf
%if %{mdkversion} < 201100
%ghost %{_sysconfdir}/modprobe.preload.d/display-driver
%endif
%dir %{_sysconfdir}/%{drivername}
%{_sysconfdir}/%{drivername}/modprobe.conf
%if %{mdkversion} < 201100
%{_sysconfdir}/%{drivername}/modprobe.preload
%endif
%{_sysconfdir}/%{drivername}/ld.so.conf
%{_sysconfdir}/%{drivername}/XvMCConfig
%{_sysconfdir}/%{drivername}/nvidia-settings.xinit
%else
%if %{mdkversion} >= 200700
# 2007.0
%ghost %{_sysconfdir}/ld.so.conf.d/GL.conf
%ghost %{_sysconfdir}/X11/xinit.d/nvidia-settings.xinit
%dir %{_sysconfdir}/ld.so.conf.d/GL
%dir %{_sysconfdir}/%{drivername}
%{_sysconfdir}/ld.so.conf.d/GL/%{drivername}.conf
%{_sysconfdir}/%{drivername}/XvMCConfig
%{_sysconfdir}/%{drivername}/nvidia-settings.xinit
%else
# 2006.0
%config(noreplace) %{_sysconfdir}/X11/XvMCConfig
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{drivername}.conf
%{_sysconfdir}/X11/xinit.d/nvidia-settings.xinit
%endif
%endif

%if %{mdkversion} >= 200700
%ghost %{_bindir}/nvidia-settings
%ghost %{_bindir}/nvidia-xconfig
%ghost %{_bindir}/nvidia-bug-report.sh
%dir %{nvidia_bindir}
%endif
%{nvidia_bindir}/nvidia-settings
%{nvidia_bindir}/nvidia-xconfig
%{nvidia_bindir}/nvidia-bug-report.sh

%if %{mdkversion} >= 200700
%ghost %{_mandir}/man1/nvidia-xconfig.1%{_extension}
%ghost %{_mandir}/man1/nvidia-settings.1%{_extension}
%{_mandir}/man1/alt-%{drivername}-xconfig.1*
%{_mandir}/man1/alt-%{drivername}-settings.1*
%else
%{_mandir}/man1/nvidia-xconfig.1*
%{_mandir}/man1/nvidia-settings.1*
%endif

%if %{mdkversion} >= 200700
%ghost %{_datadir}/applications/mandriva-nvidia-settings.desktop
%dir %{nvidia_deskdir}
%else
%{_menudir}/%{driverpkgname}
%endif
%{nvidia_deskdir}/mandriva-nvidia-settings.desktop

%{_miconsdir}/%{drivername}-settings.png
%{_iconsdir}/%{drivername}-settings.png
%{_liconsdir}/%{drivername}-settings.png

%dir %{nvidia_libdir}
%dir %{nvidia_libdir}/tls
%{nvidia_libdir}/libGL.so.1
%{nvidia_libdir}/libGL.so.%{version}
%{nvidia_libdir}/libGLcore.so.1
%{nvidia_libdir}/libGLcore.so.%{version}
%{nvidia_libdir}/libXvMCNVIDIA_dynamic.so.1
%{nvidia_libdir}/libXvMCNVIDIA.so.%{version}
%{nvidia_libdir}/libnvidia-cfg.so.1
%{nvidia_libdir}/libnvidia-cfg.so.%{version}
%{nvidia_libdir}/libnvidia-tls.so.1
%{nvidia_libdir}/libnvidia-tls.so.%{version}
%{nvidia_libdir}/tls/libnvidia-tls.so.1
%{nvidia_libdir}/tls/libnvidia-tls.so.%{version}
%ifarch %{biarches}
%dir %{nvidia_libdir32}
%dir %{nvidia_libdir32}/tls
%{nvidia_libdir32}/libGL.so.1
%{nvidia_libdir32}/libGL.so.%{version}
%{nvidia_libdir32}/libGLcore.so.1
%{nvidia_libdir32}/libGLcore.so.%{version}
%{nvidia_libdir32}/libnvidia-tls.so.1
%{nvidia_libdir32}/libnvidia-tls.so.%{version}
%{nvidia_libdir32}/tls/libnvidia-tls.so.1
%{nvidia_libdir32}/tls/libnvidia-tls.so.%{version}
%endif

%if %{mdkversion} >= 200910
# 2009.1+ (/usr/lib/drivername/xorg)
%dir %{nvidia_modulesdir}
%endif

%if %{mdkversion} <= 200900
%dir %{nvidia_extensionsdir}
%endif
%{nvidia_extensionsdir}/libglx.so.%{version}
%{nvidia_extensionsdir}/libglx.so
%if %{mdkversion} >= 200800 && %{mdkversion} <= 200900
%ghost %{xorg_libdir}/modules/extensions/libglx.so
%endif

%if %{mdkversion} >= 200700 && %{mdkversion} <= 200910
%dir %{nvidia_driversdir}
%ghost %{xorg_libdir}/modules/drivers/nvidia_drv.so
%endif
%{nvidia_driversdir}/nvidia_drv.so

%files -n %{drivername}-devel
%defattr(-,root,root)
%{_includedir}/%{drivername}
%{nvidia_libdir}/libXvMCNVIDIA.a
%{nvidia_libdir}/libGL.so
%{nvidia_libdir}/libnvidia-cfg.so
%ifarch %{biarches}
%{nvidia_libdir32}/libGL.so
%endif

%files -n dkms-%{drivername}
%defattr(-,root,root)
%doc %{pkgname}/LICENSE
%{_usrsrc}/%{drivername}-%{version}-%{release}

%files -n %{drivername}-doc-html
%defattr(-,root,root)
%doc html-doc/*
