%{?!python3_pkgversion:%global python3_pkgversion 3}

# OpenSUSE uses alternative Go based tool:
# https://github.com/mikefarah/yq

%global srcname yq
%global srcforge https://github.com/kislyuk/yq

Name:           python-yq
Version:        3.2.3
Release:        %autorelease
Summary:        Command-line YAML/XML processor - jq wrapper for YAML/XML documents
License:        Apache-2.0
URL:            https://pypi.org/project/yq/
VCS:            git:%{srcforge}
Source0:        %pypi_source

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  jq

%description
%{summary}.


%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

Requires:       jq

%description -n python%{python3_pkgversion}-%{srcname}
%{summary}.


%prep
%autosetup -p1 -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{srcname}


%check
# python3 setup.py test is failing. Run test directly.
%{python3} test/test.py


%files -n  python%{python3_pkgversion}-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst
%{_bindir}/%{srcname}
%{_bindir}/tomlq
%{_bindir}/xq


%changelog
%autochangelog
