%undefine _debugsource_packages
%define module pydantic-core
%define oname pydantic_core

# NOTE update python-pydantic AFTER updating this package, both packages are
# NOTE version matched/dependant, but python-pydantic requires this package to exist in
# NOTE the package repositories first in order to pass build tests.

Name:		python-pydantic-core
Version:	2.46.4
Release:	1
Summary:	Core functionality for Pydantic validation and serialization
License:	MIT
Group:		Development/Python
URL:		https://pypi.org/project/pydantic-core
Source0:	https://files.pythonhosted.org/packages/source/p/%{module}/%{oname}-%{version}.tar.gz
Source1:	%{oname}-%{version}-vendor.tar.xz

BuildSystem:	python
BuildRequires:	cargo
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(maturin)
BuildRequires:	python%{pyver}dist(typing-extensions)
BuildRequires:	rust-packaging

%description
Core functionality for Pydantic validation and serialization

%prep -a
# Extract vendored crate tarball
tar xf %{S:1}
# Prep vendored crates
%cargo_prep -v vendor/
# create .cargo/config file from vendoring output
cat >>.cargo/config <<EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build -p
export RUSTFLAGS="-lpython%{pyver}"

%build -a
export CARGO_HOME=$PWD/.cargo
# sort out crate licenses
%cargo_license_summary
%{cargo_license} > LICENSES.dependencies

%files
%license LICENSE LICENSES.dependencies
%{python_sitearch}/%{oname}
%{python_sitearch}/%{oname}-%{version}.dist-info
