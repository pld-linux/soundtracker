# TODO:
# - gtk+2 (there was initial port of soundtracker 0.6.7)
# - jack support (needs update to current API, at least two functions disappeared)
#
# Conditional build:
%bcond_without	alsa	# without ALSA support
%bcond_without	esd	# without EsounD support
%bcond_with	jack	# JACK support (requires update for current JACK API)
%bcond_with	gnome	# GNOME 1.x-based GUI instead of plain GTK+1
#
%if !%{with alsa}
%undefine	with_jack
%endif
Summary:	Soundtracker - music editor for xm/mod formats
Summary(pl.UTF-8):	Soundtracker - program do komponowania muzyki w formatach xm/mod
Name:		soundtracker
Version:	0.6.8
Release:	1
License:	GPL
Group:		X11/Applications/Sound
Source0:	http://www.soundtracker.org/dl/v0.6/%{name}-%{version}.tar.gz
# Source0-md5:	1e5a2ef689e214933e53f687b3a199bb
Patch0:		%{name}-no_chmod.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-locale_names.patch
Patch3:		%{name}-po.patch
URL:		http://www.soundtracker.org/
BuildRequires:	SDL-devel >= 1.2.0
%{?with_alsa:BuildRequires:	alsa-lib-devel >= 0.9.0}
BuildRequires:	audiofile-devel >= 0.1.5
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_esd:BuildRequires:	esound-devel >= 0.2.8}
BuildRequires:	gdk-pixbuf-devel >= 0.8.0
BuildRequires:	gettext-tools
%{?with_gnome:BuildRequires:	gnome-libs-devel}
BuildRequires:	gtk+-devel >= 1.2.2
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel}
BuildRequires:	libsndfile-devel >= 1.0.1
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SoundTracker is a pattern-oriented music editor (similar to the DOS
program 'FastTracker'). Samples are lined up on tracks and patterns
which are then arranged to a song. Supported module formats are XM and
MOD; the player code is the one from OpenCP. A basic sample recorder
and editor is also included.

%description -l pl.UTF-8
SoundTracker jest edytorem plików muzycznych podobnym do znanego spod
DOS programu FastTracker. Sample są rozmieszczane na ścieżkach i
szablonach, które są układane w utwory. Edytor obsługuje formaty XM i
MOD. Kod odtwarzacza pochodzi z OpenCP. Załączony jest prosty edytor
i program do nagrywania sampli.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

mv -f po/{no,nb}.po
rm -f po/stamp-po

%build
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{!?with_alsa:--disable-alsa} \
	%{!?with_esd:--disable-esd} \
	%{!?with_jack:--disable-jack} \
	%{!?with_gnome:--disable-gnome} \
%ifnarch %{ix86}
	--disable-asm
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	utildir=%{_desktopdir}

install soundtracker.desktop $RPM_BUILD_ROOT%{_desktopdir}

%find_lang %{name} %{?with_gnome:--with-gnome}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS FAQ NEWS TODO README ChangeLog doc/x[imp].txt
%attr(755,root,root) %{_bindir}/*
%{_datadir}/soundtracker
%{_desktopdir}/*.desktop
