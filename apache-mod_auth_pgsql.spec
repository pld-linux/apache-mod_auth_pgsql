%define		mod_name	auth_pgsql
%define 	apxs		/usr/sbin/apxs
Summary:	This is the PostgreSQL authentication module for Apache
Summary(cs):	Z�kladn� autentizace pro WWW server Apache pomoc� PostgreSQL
Summary(da):	Autenticering for webtjeneren Apache fra en PostgreSQL-database
Summary(de):	Authentifizierung f�r den Apache Web-Server, der eine PostgreSQL-Datenbank verwendet
Summary(es):	Autenticaci�n v�a PostgreSQL para Apache
Summary(fr):	Authentification de base pour le serveur Web Apache utilisant une base de donn�es PostgreSQL
Summary(it):	Autenticazione di base per il server web Apache mediante un database PostgreSQL
Summary(ja):	PostgreSQL �ǡ����١�����Ȥä� Apache Web �����С��ؤδ���ǧ��
Summary(nb):	Autentisering for webtjeneren Apache fra en PostgreSQL-database
Summary(pl):	Modu� uwierzytelnienia PostgreSQL dla Apache
Summary(pt_BR):	Autentica��o via PostgreSQL para o Apache
Summary(sv):	Grundl�ggande autenticering till webbservern Apache med en PostgreSQL-databas
Name:		apache-mod_%{mod_name}
Version:	2.0.2
%define	_beta	b1
Release:	0.%{_beta}.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.giuseppetanzilli.it/mod_auth_pgsql2/dist/mod_%{mod_name}-%{version}%{_beta}.tar.gz
# Source0-md5:	8216fde4597c288537ff4fec508a4b41
Source1:	apache-mod_auth_pgsql.conf
Patch0:		apache-mod_auth_pgsql.patch
URL:		http://www.giuseppetanzilli.it/mod_auth_pgsql2/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.52-2
BuildRequires:	postgresql-devel
Requires:	apache(modules-api) = %apache_modules_api
Obsoletes:	mod_auth_pgsql
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using PostgreSQL RDBMS.

%description -l cs
Bal��ek mod_auth_pgsql slou�� pro omezen� p��stupu k dokument�m, kter�
poskytuje WWW server Apache. Jm�na a hesla jsou ulo�ena v datab�zi
PostgreSQL.

%description -l de
Mod_auth_pgsql kann verwendet werden, um den Zugriff auf von einem
Web- Server bediente Dokumente zu beschr�nken, indem es die Felder in
einer Tabelle in einer PostgresQL-Datenbank pr�ft.

%description -l es
Mod_auth_pgsql puede usarse para limitar el acceso a documentos
servidos desde un servidor web verificando datos en una base de datos
PostgreSQL.

%description -l fr
mod_auth_pgsql peut �tre utilis� pour limiter l'acc�s � des documents
servis par un serveur Web en v�rifiant des champs dans une table d'une
base de donn�es PostgresQL.

%description -l it
Mod_auth_pgsql pu� essere usato per limitare l'accesso a documenti
serviti da un server Web controllando i campi di una tabella in un
database PostgresQL.

%description -l ja
Mod_auth_pgsql �ϡ�PostgresQL �ǡ����١����Υơ��֥����Υե�����ɤ�
�����å����뤳�Ȥˤ�äơ�Web �����С����󶡤���ʸ��ؤΥ���������
���¤Ǥ��ޤ���

%description -l pl
To jest modu� uwierzytelnienia dla Apache pozwalaj�cy na
uwierzytelnianie klient�w HTTP z u�yciem bazy danych PostgreSQL.

%description -l pt_BR
Com o mod_auth_pgsql voc� pode fazer autentica��o no Apache usando o
PostgreSQL.

%description -l sv
Mod_auth_pgsql kan anv�ndas f�r att begr�nsa �tkomsten till dokument
servade av en webbserver genom att kontrollera data i en
PostgreSQL-databas.

%prep
%setup -q -n mod_%{mod_name}-%{version}%{_beta}
%patch0 -p1

%build
%{apxs} \
	-I%{_includedir}/postgresql \
	-lpq \
	-c mod_%{mod_name}.c \
	-o mod_%{mod_name}.la

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/httpd.conf/52_mod_auth_pgsql.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc *.html
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_auth_pgsql.conf
%attr(755,root,root) %{_pkglibdir}/*.so
