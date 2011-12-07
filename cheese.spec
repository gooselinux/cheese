Name:           cheese
Version:        2.28.1
Release:        7%{?dist}
Summary:        Application for taking pictures and movies from a webcam

Group:          Amusements/Graphics
License:        GPLv2+
URL:            http://projects.gnome.org/cheese/
Source0:        http://download.gnome.org/sources/cheese/2.28/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gtk2-devel >= 2.17.3
BuildRequires: libglade2-devel >= 2.6.0
BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel
BuildRequires: gstreamer-devel >= 0.10.16
BuildRequires: gstreamer-plugins-base-devel >= 0.10.12
BuildRequires: gnome-vfs2-devel
BuildRequires: GConf2-devel
BuildRequires: cairo-devel >= 1.2.4
BuildRequires: hal-devel >= 0.5.9
BuildRequires: libgnomeui-devel
BuildRequires: librsvg2-devel >= 2.18.0
BuildRequires: evolution-data-server-devel
BuildRequires: libXxf86vm-devel
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: gnome-doc-utils
BuildRequires: intltool
BuildRequires: gnome-desktop-devel >= 2.25.1

Requires: gstreamer-plugins-good >= 0.10.6-2
Requires(post): GConf2
Requires(pre): GConf2
Requires(preun): GConf2

# http://bugzilla.gnome.org/show_bug.cgi?id=592663
Patch1: trash-menu.patch
# http://bugzilla.gnome.org/show_bug.cgi?id=613287
Patch2: cheese-effects-i18n.patch

# http://bugzilla.gnome.org/614027
Patch3: cheese-dir-prefix.patch

# upstream translations
Patch4: cheese-translations.patch
Patch5: cheese-translations2.patch

# make docs show up in rarian/yelp
Patch6: cheese-doc-category.patch

%description
Cheese is a Photobooth-inspired GNOME application for taking pictures and
videos from a webcam. It can also apply fancy graphical effects.

%prep
%setup -q
%patch1 -p1 -b .trash-menu
%patch2 -p1 -b .effects-i18n
%patch3 -p1 -b .dir-prefix
%patch4 -p1 -b .translations
%patch5 -p2 -b .translations2
%patch6 -p1 -b .doc-category

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

desktop-file-install --delete-original --vendor="" 	\
 	--dir=$RPM_BUILD_ROOT%{_datadir}/applications 	\
	--add-category X-AudioVideoImport		\
	$RPM_BUILD_ROOT%{_datadir}/applications/cheese.desktop

# save space by linking identical images in translated docs
helpdir=$RPM_BUILD_ROOT%{_datadir}/gnome/help/%{name}
for f in $helpdir/C/figures/*.jpg; do
  b="$(basename $f)"
  for d in $helpdir/*; do
    if [ -d "$d" -a "$d" != "$helpdir/C" ]; then
      g="$d/figures/$b"
      if [ -f "$g" ]; then
        if cmp -s $f $g; then
          rm "$g"; ln -s "../../C/figures/$b" "$g"
        fi
      fi
    fi
  done
done

%find_lang %{name} --with-gnome


%clean
rm -rf $RPM_BUILD_ROOT


%pre
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/cheese.schemas > /dev/null || :
fi


%preun
if [ "$1" -gt 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/cheese.schemas > /dev/null || :
fi


%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/cheese.schemas > /dev/null || :


%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_bindir}/cheese
%{_datadir}/applications/cheese.desktop
%{_datadir}/cheese
%{_datadir}/icons/hicolor/*/apps/cheese.png
%{_datadir}/icons/hicolor/scalable/apps/cheese.svg
%{_sysconfdir}/gconf/schemas/cheese.schemas
%{_libexecdir}/cheese
%{_datadir}/dbus-1/services/org.gnome.Cheese.service

%changelog
* Tue Aug 10 2010 Matthias Clasen <mclasen@redhat.com> 2.28.1-7
- More translation updates
Resolves: #576068

* Thu Aug  5 2010 Matthias Clasen <mclasen@redhat.com> 2.28.1-6
- Update translations from upstream
Resolves: #576068

* Mon May  3 2010 Matthias Clasen <mclasen@redhat.com> 2.28.1-5
- Make docs show up in yelp
Resolves: #588523

* Mon May  3 2010 Matthias Clasen <mclasen@redhat.com> 2.28.1-4
- Update translations
Resolves: #576068

* Fri Mar 26 2010 Ray Strode <rstrode@redhat.com> 2.28.1-3
- Support relocatable .gnome2
Resolves: #577287

* Fri Mar 19 2010 Matthias Clasen <mclasen@redhat.com> 2.28.1-2
- Fix text rendering issues on the effects tab

* Mon Oct 19 2009 Matthias Clasen  <mclasen@redhat.com> 2.28.1-1
- Update to 2.28.1

* Tue Sep 29 2009 Matthias Clasen  <mclasen@redhat.com> 2.28.0.1-1
- Update to 2.28.0.1

* Sun Sep 27 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> 2.28.0-2
- Update desktop file according to F-12 FedoraStudio feature

* Mon Sep 21 2009 Matthias Clasen  <mclasen@redhat.com> 2.28.0-1
- Update to 2.28.0

* Mon Sep  7 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.92-1
- Update to 2.27.92

* Mon Aug 24 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.91-1
- Update to 2.27.91

* Sat Aug 22 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.90-3
- Update sensitivity of menu items

* Fri Aug 14 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.90-2
- Fix schemas file syntax

* Tue Aug 11 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.90-1
- Update to 2.27.90

* Tue Jul 28 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.5-1
- Update to 2.27.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.4-1
- Update to 2.27.4

* Tue Jun 16 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.3-1
- Update to 2.27.3

* Sun May 31 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.2-1
- Update to 2.27.2

* Fri May 15 2009 Matthias Clasen  <mclasen@redhat.com> 2.27.1-1
- Update to 2.27.1

* Mon Mar 16 2009 Matthias Clasen  <mclasen@redhat.com> 2.26.0-1
- Update to 2.26.0

* Mon Mar  2 2009 Matthias Clasen  <mclasen@redhat.com> 2.25.92-1
- Update to 2.25.92

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen  <mclasen@redhat.com> 2.25.91-1
- Update to 2.25.91

* Tue Feb  3 2009 Matthias Clasen  <mclasen@redhat.com> 2.25.90-1
- Update to 2.25.90

* Tue Jan  6 2009 Matthias Clasen  <mclasen@redhat.com> 2.25.4-1
- Update to 2.25.4

* Wed Dec 17 2008 Matthias Clasen  <mclasen@redhat.com> 2.25.3-1
- Update to 2.25.3

* Wed Dec  3 2008 Matthias Clasen  <mclasen@redhat.com> 2.25.2-1
- Update to 2.25.2

* Thu Nov 21 2008 Matthias Clasen  <mclasen@redhat.com> 2.25.1-4
- Better URL

* Thu Nov 13 2008 Matthias Clasen  <mclasen@redhat.com> 2.25.1-3
- Update to 2.25.1

* Sun Nov  9 2008 Hans de Goede <hdegoede@redhat.com> 2.24.1-2
- Fix cams which only support 1 resolution not working (rh470698, gnome560032)

* Mon Oct 20 2008 Matthias Clasen  <mclasen@redhat.com> 2.24.1-1
- Update to 2.24.1

* Wed Oct  8 2008 Matthias Clasen  <mclasen@redhat.com> 2.24.0-2
- Save space

* Mon Sep 22 2008 Matthias Clasen  <mclasen@redhat.com> 2.24.0-1
- Update to 2.24.0

* Tue Sep  9 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.92-3
- Update to 2.23.92
- Drop upstreamed patches

* Wed Sep  3 2008 Hans de Goede <hdegoede@redhat.com> 2.23.91-2
- Fix use with multiple v4l devices (rh 460956, gnome 546868, gnome 547144)

* Tue Sep  2 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.91-1
- Update to 2.23.91

* Fri Aug 22 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.90-1
- Update to 2.23.90

* Tue Aug  5 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.6-1
- Update to 2.23.6

* Tue Jul 22 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.5-1
- Update to 2.23.5

* Wed Jun 18 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.4-1
- Update to 2.23.4

* Tue Jun  3 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.3-1
- Update to 2.23.3

* Tue May 13 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.2-1
- Update to 2.23.2

* Fri Apr 25 2008 Matthias Clasen  <mclasen@redhat.com> 2.23.1-1
- Update to 2.23.1

* Tue Apr 22 2008 Matthias Clasen  <mclasen@redhat.com> 2.22.1-2
- Fix an invalid free

* Mon Apr  7 2008 Matthias Clasen  <mclasen@redhat.com> 2.22.1-1
- Update to 2.22.1

* Mon Mar 10 2008 Matthias Clasen  <mclasen@redhat.com> 2.22.0-1
- Update to 2.22.0

* Tue Feb 26 2008  Matthias Clasen  <mclasen@redhat.com> 2.21.92-1
- Update to 2.21.92

* Fri Feb 15 2008  Matthias Clasen  <mclasen@redhat.com> 2.21.91-3
- Fix a locking problem that causes the UI to freeze

* Fri Feb  8 2008  Matthias Clasen  <mclasen@redhat.com> 2.21.91-2
- Rebuild for gcc 4.3

* Tue Jan 29 2008  Matthias Clasen  <mclasen@redhat.com> 2.21.91-1
- Update to 2.21.91

* Mon Jan 14 2008  Matthias Clasen  <mclasen@redhat.com> 2.21.5-1
- Update to 2.21.5

* Mon Dec 24 2007  Matthias Clasen  <mclasen@redhat.com> 0.3.0-1
- Update to 0.3.0

* Fri Sep  7 2007  Matthias Clasen  <mclasen@redhat.com> 0.2.4-2
- package review feedback

* Thu Sep  6 2007  Matthias Clasen  <mclasen@redhat.com> 0.2.4-1
- Initial packages
