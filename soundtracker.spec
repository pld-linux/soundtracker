#
# Conditional build:
# bcond_off_gnome - without gnome support
# bcond_off_esound - without esd support
#
Summary:	Soundtracker - Sekwencer MIDI
Summary(pl):	Soundtracker - MIDI sequencer
Name:		soundtracker
%define	ver	0.6
%define	subver	2
Version:	%{ver}.%{subver}
Release:	2
License:	GPL
Group:		X11/Applications/Multimedia
Group(de):	X11/Applikationen/Multimedia
Group(pl):	X11/Aplikacje/Multimedia
Source0:	ftp://ftp.soundtracker.org/pub/soundtracker/v%{ver}/%{name}-%{version}.tar.gz
Patch0:		%{name}-no_chmod.patch
URL:		http://www.soundtracker.org
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	gtk+-devel >= 1.2.2
BuildRequires:	audiofile-devel >= 0.1.5
%{?!bcond_off_esound:BuildRequires:	esound-devel >= 0.2.8}
%{?!bcond_off_gnome:BuildRequires:	gnome-libs-devel}
BuildRequires:	gettext-devel
BuildRequires:	automake
BuildRequires:	autoconf
ExclusiveArch:	%{ix86}

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
SoundTracker is a pattern-oriented music editor (similar to the DOS
program 'FastTracker'). Samples are lined up on tracks and patterns
which are then arranged to a song. Supported module formats are XM and
MOD; the player code is the one from OpenCP. A basic sample recorder
and editor is also included.

%description -l pl
SoundTracker jest edytorem plików muzycznych podobnym do znanego
spod DOS programu FastTracker. Obs³uguje formaty XM i MOD.

%prep
%setup -q
%patch -p1

%build
gettextize --copy --force
aclocal
autoconf
automake -a -c
%configure \
	%{?bcond_off_esound:--disable-esd} \
	%{?bcond_off_gnome:--disable-gnome}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	utildir=%{_applnkdir}/Multimedia

%{?bcond_off_gnome:install soundtracker.desktop $RPM_BUILD_ROOT%{_applnkdir}/Multimedia}

gzip -9nf AUTHORS FAQ NEWS TODO README ChangeLog doc/x[im].txt

%find_lang %{name} %{!?bcond_off_gnome:--with-gnome}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%doc *.gz doc/*.gz
%{_applnkdir}/*/*
