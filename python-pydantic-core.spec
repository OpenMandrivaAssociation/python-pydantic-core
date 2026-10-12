%undefine _debugsource_packages
%define module pydantic-core
%define oname pydantic_core

# NOTE update python-pydantic AFTER updating this package, both packages are
# NOTE version matched/dependant, but python-pydantic requires this package to exist in
# NOTE the package repositories first in order to pass build tests.

Name:		python-pydantic-core
Version:	2.46.4
Release:	2
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

%description
Core functionality for Pydantic validation and serialization

%prep -a
# The crates are already vendored, so this build does not need rust-packaging.
tar -xf %{SOURCE1}
mkdir -p .cargo
cat > .cargo/config.toml << 'EOF'
[net]
offline = true

[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build -p
export CARGO_NET_OFFLINE=true
export RUSTFLAGS="-lpython%{pyver}"
export CARGO_HOME=$PWD/.cargo
cargo tree --workspace --offline --edges no-build,no-dev,no-proc-macro \
	--prefix none --format '{l}: {p}' \
	| sed -e "s: ($(pwd)[^)]*)::g" -e 's: / :/:g' -e 's:/: OR :g' \
	| sort -u > LICENSES.dependencies

%files
%license LICENSE LICENSES.dependencies
%{python_sitearch}/%{oname}
%{python_sitearch}/%{oname}-%{version}.dist-info
