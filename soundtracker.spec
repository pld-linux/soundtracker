#
# Conditional build:
%bcond_without	alsa	# without ALSA support
%bcond_without	esd	# without EsounD support
%bcond_without	jack	# without JACK support
%bcond_with	gnome	# GNOME 1.x-based GUI instead of plain GTK+1
#
%if %{without alsa}
%undefine	with_jack
%endif
Summary:	Soundtracker - music editor for xm/mod formats
Summary(pl):	Soundtracker - program do komponowania muzyki w formatach xm/mod
Name:		soundtracker
Version:	0.6.7
Release:	4
License:	GPL
Group:		X11/Applications/Sound
Source0:	http://www.soundtracker.org/dl/v0.6/%{name}-%{version}.tar.gz
# Source0-md5:	9a5685e0a79fb10066d29baed652d324
Patch0:		%{name}-no_chmod.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-locale_names.patch
URL:		http://www.soundtracker.org/
%{?with_alsa:BuildRequires:	alsa-lib-devel >= 0.9.0}
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_esd:BuildRequires:	esound-devel >= 0.2.8}
BuildRequires:	gdk-pixbuf-devel >= 0.8.0
BuildRequires:	gettext-devel
%{?with_gnome:BuildRequires:	gnome-libs-devel}
BuildRequires:	gtk+-devel >= 1.2.2
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel}
BuildRequires:	libsndfile-devel >= 1.0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SoundTracker is a pattern-oriented music editor (similar to the DOS
program 'FastTracker'). Samples are lined up on tracks and patterns
which are then arranged to a song. Supported module formats are XM and
MOD; the player code is the one from OpenCP. A basic sample recorder
and editor is also included.

%description -l pl
SoundTracker jest edytorem plików muzycznych podobnym do znanego spod
DOS programu FastTracker. Sample s± rozmieszczane na ¶cie¿kach i
szablonach, które s± uk³adane w utwory. Edytor obs³uguje formaty XM i
MOD. Kod odtwarzacza pochodzi z OpenCP. Za³±czony jest prosty edytor
i program do nagrywania sampli.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

mv -f po/{no,nb}.po

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
%doc AUTHORS FAQ NEWS TODO README ChangeLog doc/x[im].txt
%attr(755,root,root) %{_bindir}/*
%{_datadir}/soundtracker
%{_desktopdir}/*
