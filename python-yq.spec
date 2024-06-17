# Fedora and OpenSUSE has alternative Go based tool (rhbz#2276522):
# https://github.com/mikefarah/yq

%global srcname yq
%global srcforge https://github.com/kislyuk/yq

Name:           python-yq
Version:        3.4.3
Release:        %autorelease
Summary:        Command-line YAML/XML/TOML processor - jq wrapper
License:        Apache-2.0
URL:            https://pypi.org/project/yq/
VCS:            git:%{srcforge}
Source0:        %{pypi_source yq}

Patch1:         yq-tomlkit-f39.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  jq
%if 0%{?fedora} && 0%{?fedora} <= 39
BuildRequires:  sed
%endif


%global _description %{expand:
jq wrapper for YAML, XML, TOML documents.

yq takes YAML input, converts it to JSON, and pipes it to jq. By
default, no conversion of jq output is done. yq also supports XML,
which transcodes XML to JSON using xmltodict and pipes it to jq.
yq supports TOML as well, which uses the tomlkit library to
transcode TOML to JSON, then pipes it to jq.}

%description
%{_description}


%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

Requires:       jq
Recommends:     python3-%{srcname}-alt

%description -n python3-%{srcname}
%{_description}

Provides yqp, xqp and tomlq commands and python yq module.

%package -n python3-%{srcname}-alt
Summary:          %{summary}

Requires:         python3-%{srcname} = %{version}-%{release}
Requires(post):   %{_sbindir}/alternatives
Requires(postun): %{_sbindir}/alternatives
# Until Go yq provides alternatives, conflict with that package
Conflicts:        yq

%description -n python3-%{srcname}-alt
%{_description}

Alternative wrapper providing yq binary via alternatives.


%prep
%autosetup -p1 -n %{srcname}-%{version} -N

%if 0%{?fedora} && 0%{?fedora} <= 39
# version_file is not supported in setuptools-scm 7.1.0
sed -e 's/^version_file/#write_to/' -i pyproject.toml
%autopatch -M 1 -p1
%endif

%autopatch -m 2 -p1

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{srcname}

# xq command is already taken
# Already packaged separately in xq package
# https://github.com/sibprogrammer/xq = https://src.fedoraproject.org/rpms/xq
mv %{buildroot}%{_bindir}/{xq,xqp}
# yq conflicts with Go project
# https://github.com/mikefarah/yq = https://src.fedoraproject.org/rpms/yq
mv %{buildroot}%{_bindir}/{yq,yqp}

touch %{buildroot}%{_bindir}/yq


%check
# python3 setup.py test is failing. Run test directly.
%{python3} test/test.py

%postun -n python3-%{srcname}-alt
if [ $1 -eq 0 ] ; then
  %{_sbindir}/alternatives --remove yq %{_bindir}/yqp
fi

%post -n python3-%{srcname}-alt
%{_sbindir}/alternatives --install %{_bindir}/yq \
  yq %{_bindir}/yqp 10


%files -n  python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst
%{_bindir}/yqp
%{_bindir}/tomlq
%{_bindir}/xqp


%files -n python3-%{srcname}-alt
%ghost %{_bindir}/yq


%changelog
%autochangelog
