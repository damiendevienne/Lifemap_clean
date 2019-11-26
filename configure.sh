#! /bin/sh

##CONFIG  VARIABLES
html_version="NCBI" #can also be "MAIN"
lang="en" #can also be "fr"
server="134.158.247.35"

##UPDATE AND INSTALL REQUIRED PACKAGES
sudo apt-get --yes update
sudo apt-get --yes upgrade
sudo apt-get --yes install libboost-all-dev git-core tar unzip wget bzip2 build-essential autoconf libtool 
sudo apt-get --yes install libxml2-dev libgeos-dev libgeos++-dev libpq-dev libbz2-dev libproj-dev munin-node munin 
sudo apt-get --yes install libprotobuf-c0-dev protobuf-c-compiler libfreetype6-dev libpng-dev libtiff5-dev libicu-dev libgdal-dev libcairo-dev 
sudo apt-get --yes install libcairomm-1.0-dev apache2 apache2-dev libagg-dev liblua5.2-dev ttf-unifont lua5.1 liblua5.1-dev libgeotiff-epsg node-carto
sudo apt-get --yes install postgresql postgresql-contrib postgis postgresql-10-postgis-2.4
sudo apt-get --yes install gdal-bin libgdal-dev libmapnik-dev mapnik-utils python-mapnik
sudo apt-get --yes install python-numpy python-qt4 python-lxml python-six python-pip

##CONFIGURE POSTGRESQL/POSTGIS USER AND DATABASE
sudo -u postgres psql -c "DROP DATABASE IF EXISTS tree;"
sudo -u postgres psql -c "DROP USER IF EXISTS lm;"
sudo -u postgres psql -c "CREATE USER lm WITH PASSWORD 'gvC5b78Ch9nDePjF';"
sudo -u postgres psql -c "CREATE DATABASE tree OWNER lm ENCODING UTF8;"
sudo -u postgres psql -d tree -c "CREATE EXTENSION postgis;"
sudo -u postgres psql -d tree -c "ALTER TABLE geometry_columns OWNER TO lm;"
sudo -u postgres psql -d tree -c "ALTER TABLE spatial_ref_sys OWNER TO lm;" 
##copy pgpass locally 
cp conf/.pgpass ~/.pgpass
sudo chmod 0600 ~/.pgpass

##CREATE LIFEMAP FOLDERS AND COPY CONF FILES
sudo mkdir /usr/share/fonts/lifemap
sudo mkdir /usr/lifemap/
sudo cp -r fonts/ /usr/lifemap/
sudo cp -r style/ /usr/lifemap/


##INSTALL MOD TILE and RENDERD
git clone git://github.com/damiendevienne/mod_tile_deepzoom.git /opt/mod_tile
(cd /opt/mod_tile/ ; ./autogen.sh)
(cd /opt/mod_tile/ ; ./configure)
(cd /opt/mod_tile/ ; make)
(cd /opt/mod_tile/ ; sudo make install)
(cd /opt/mod_tile/ ; sudo make install-mod_tile)
sudo ldconfig
sudo mkdir /var/lib/mod_tile
sudo mkdir /var/run/renderd
sudo cp conf/mod_tile.conf /etc/apache2/conf-available/mod_tile.conf
sudo a2enconf mod_tile
sudo cp conf/renderd.conf /etc/ ## a faire avant de relancer apache2

##CONFIGURE APACHE
sudo service apache2 reload
sudo cp conf/000-default.conf /etc/apache2/sites-available/ #replace apache config file 
sudo a2enmod proxy http_proxy
sudo service apache2 restart
sudo sed -i s/"lifemap.univ-lyon1.fr"/$server/g /etc/apache2/sites-available/000-default.conf

##INSTALL ETE (TREE MANIPULATION) AND DEPENDENCIES 
python2.7 -m pip install --upgrade psycopg2-binary
python2.7 -m pip install --upgrade ete3

##COPY CORRECT HTTP TO /VAR/WWW/HTML AND UPDATE HTML FILE
if [ $html_version=="NCBI" ]; then
	sudo cp -r html/HTTP-NCBI/* /var/www/html
	sudo sed -i s/"lifemap.univ-lyon1.fr"/$server/g /var/www/html/index.html
else 
	sudo cp -r html/HTTP-MAIN/* /var/www/html
	sudo sed -i s/"lifemap.univ-lyon1.fr"/$server/g /var/www/html/explore.html
fi


##INSTALL AND CONFIGURE SOLR
sudo apt-get --yes install default-jre default-jdk
wget http://www-eu.apache.org/dist/lucene/solr/8.3.0/solr-8.3.0.tgz
tar xzf solr-8.3.0.tgz solr-8.3.0/bin/install_solr_service.sh --strip-components=2
sudo bash ./install_solr_service.sh solr-8.3.0.tgz
sudo su - solr -c "/opt/solr/bin/solr create -c addi -n data_driven_schema_configs"
sudo su - solr -c "/opt/solr/bin/solr create -c taxo -n data_driven_schema_configs"





#cd ~/src
#wget http://mirrors.ircam.fr/pub/apache/lucene/solr/6.6.3/solr-6.6.3.tgz
#tar xvzf solr-6.6.3.tgz
#cd ~/src/solr-6.6.3
#bin/solr start
#bin/solr create -c taxo
#bin/solr create -c addi
#cp ~/src/Lifemap/OTHER/solr-config/schema.taxo.xml ~/src/solr-6.6.3/server/solr/taxo/conf/schema.xml
#cp ~/src/Lifemap/OTHER/solr-config/solrconfig.taxo.xml ~/src/solr-6.6.3/server/solr/taxo/conf/solrconfig.xml
