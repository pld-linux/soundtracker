Summary:	Soundtracker - Sekwencer MIDI
Summary(pl):	Soundtracker - MIDI sequencer
Name:		soundtracker
%define	ver	0.5
%define	subver	7
Version:	%{ver}.%{subver}
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Group(pl):	X11/Aplikacje/Multimedia
Source0:	ftp://ftp.soundtracker.org/pub/soundtracker/v%{ver}/%{name}-%{version}.tar.gz
Patch0:		%{name}-no_chmod.patch
URL:		http://www.soundtracker.org
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	gtk+-devel
BuildRequires:	audiofile-devel
# optional
BuildRequires:	esound-devel
BuildRequires:	gnome-libs-devel
ExclusiveArch:	%{ix86}

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description

%description -l pl

%prep
%setup -q
%patch -p1

%build
gettextize --copy --force
CFLAGS="$RPM_OPT_FLAGS"; export CFLAGS
%configure \
	# --disable-esd \
	# --disable-gnome \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	utildir=%{_applnkdir}/Multimedia \

%find_lang %{name} #--with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_applnkdir}/*/*
