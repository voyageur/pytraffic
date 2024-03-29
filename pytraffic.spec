Name: pytraffic
Version: 2.5.4
Release: 3
Summary: Rush Hour game

Group: Amusements/Games
License: GPL
Url: http://alpha.uhasselt.be/Research/Algebra/Members/pytraffic/

Source0: http://alpha.uhasselt.be/Research/Algebra/Members/pytraffic/pytraffic-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python-devel,  SDL_mixer-devel, desktop-file-utils
Requires: pygtk2 >= 2.4, python >= 2.3 


%description
PyTraffic is a Python version of the board game Rush Hour
created by Binary Arts Coporation. The goal is to remove the red
car out of the grid through the slot on the right. To do this you have to
slide the other cars out of the way.

PyTraffic comes with about 19.000 puzzles ranging from intermediate to
expert.

%package themes
Summary: Extra themes for PyTraffic
Group: Amusements/Games
Requires: pytraffic = 2.5.4
%description themes
Extra themes for PyTraffic.


%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{_bindir}/env LIBDIR=%{_libdir} %{__python} setup.py install --root="%{buildroot}" --prefix=%{_prefix}



%post 
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%clean
%{__rm} -rf %{buildroot}

%files themes
%defattr(-,root,root,-)
%doc CHANGELOG AUTHORS COPYING README
%{_datadir}/pytraffic/extra_themes



%files 
%defattr(-,root,root,-)
%doc CHANGELOG AUTHORS COPYING README
%{_datadir}/pytraffic/
%{_bindir}/pytraffic
%{_libdir}/pytraffic
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/pytraffic.png
%exclude %{_datadir}/pytraffic/extra_themes

%changelog
* Fri Jan 27 2006 Michel Van den Bergh <michel.vandenbergh@uhasselt.be> 2.5.4-3
- Do not strip binaries in installer
* Wed Dec 22 2005 Michel Van den Bergh <michel.vandenbergh@uhasselt.be> 2.5.4-2
- Tell setup.py about install directory for libraries
- Make installation of desktop file more straightforward 
- Make spec file compliant with fedora spectemplate
- Added %postun script
* Wed Dec 16 2005 Michel Van den Bergh <michel.vandenbergh@uhasselt.be> 2.5.4-1
- Initial version
