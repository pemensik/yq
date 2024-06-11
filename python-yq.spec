# OpenSUSE uses alternative Go based tool:
# https://github.com/mikefarah/yq

%global srcname yq
%global srcforge https://github.com/kislyuk/yq

Name:           python-yq
Version:        3.4.3
Release:        %autorelease
Summary:        Command-line YAML/XML processor - jq wrapper for YAML/XML documents
License:        Apache-2.0
URL:            https://pypi.org/project/yq/
VCS:            git:%{srcforge}
Source0:        %pypi_source

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  jq

%global _description %{expand:
Lightweight and portable command-line YAML, JSON and XML processor.
yq uses jq like syntax but works with yaml files as well as json, xml,
properties, csv and tsv. It doesn't yet support everything jq does - but it
does support the most common operations and functions, and more is being
added continuously.}

%description
%{_description}


%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

Requires:       jq

%description -n python3-%{srcname}
%{_description}


%prep
%autosetup -p1 -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{srcname}

# xq tool is already taken
# Already packaged separately in https://github.com/sibprogrammer/xq
mv %{buildroot}%{_bindir}/{xq,xqp}


%check
# python3 setup.py test is failing. Run test directly.
%{python3} test/test.py


%files -n  python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst
%{_bindir}/%{srcname}
%{_bindir}/tomlq
%{_bindir}/xqp


%changelog
%autochangelog
