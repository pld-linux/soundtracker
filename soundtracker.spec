#
# Conditional build:
# _without_gnome - without gnome support
# _without_esound - without esd support
#
Summary:	Soundtracker - Music editor in format xm/mod
Summary(pl):	Soundtracker - Program do komponowania muzyki w formatach xm/mod
Name:		soundtracker
%define	ver	0.6
%define	subver	6
Version:	%{ver}.%{subver}
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	ftp://ftp.soundtracker.org/pub/soundtracker/v%{ver}/%{name}-%{version}.tar.gz
Patch0:		%{name}-no_chmod.patch
Patch1:		%{name}-acfix.patch
Patch2:		%{name}-am_fix.patch
URL:		http://www.soundtracker.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	audiofile-devel >= 0.1.5
%{?!_without_esound:BuildRequires:	esound-devel >= 0.2.8}
BuildRequires:	gettext-devel
%{?!_without_gnome:BuildRequires:	gnome-libs-devel}
BuildRequires:	gtk+-devel >= 1.2.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
SoundTracker is a pattern-oriented music editor (similar to the DOS
program 'FastTracker'). Samples are lined up on tracks and patterns
which are then arranged to a song. Supported module formats are XM and
MOD; the player code is the one from OpenCP. A basic sample recorder
and editor is also included.

%description -l pl
SoundTracker jest edytorem plików muzycznych podobnym do znanego spod
DOS programu FastTracker. Obs³uguje formaty XM i MOD.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2

%build
rm -f missing
%{__gettextize}
aclocal
%{__autoconf}
%{__automake}
%configure \
	%{?_without_esound:--disable-esd} \
	%{?_without_gnome:--disable-gnome} \
	%{!?_with_asm:--disable-asm}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	utildir=%{_applnkdir}/Multimedia

install soundtracker.desktop $RPM_BUILD_ROOT%{_applnkdir}/Multimedia

%find_lang %{name} %{!?_without_gnome:--with-gnome}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS FAQ NEWS TODO README ChangeLog doc/x[im].txt
%attr(755,root,root) %{_bindir}/*
%{_datadir}/soundtracker
%{_applnkdir}/*/*
