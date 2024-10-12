%undefine _debugsource_packages

Name:		python-pydantic-core
Version:	2.24.1
Release:	1
Source0:	https://files.pythonhosted.org/packages/source/p/pydantic-core/pydantic_core-%{version}.tar.gz
# To hell with ****ing rust!
Source1:	vendor.tar.xz
Summary:	Core functionality for Pydantic validation and serialization
URL:		https://pypi.org/project/pydantic-core/
License:	MIT
Group:		Development/Python
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(maturin)
BuildRequires:	rust

%description
Core functionality for Pydantic validation and serialization

%prep
%autosetup -p1 -n pydantic_core-%{version} -a1
cat >>.cargo/config.toml <<'EOF'

[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
%py_build

%install
%py_install

%files
%{python_sitearch}/_pydantic_core
%{python_sitearch}/pydantic_core-*.*-info