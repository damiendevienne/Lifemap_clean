#!/bin/sh

(cd /tmp/ ; wget http://www-eu.apache.org/dist/lucene/solr/8.3.1/solr-8.3.1.tgz)
(cd /tmp/ ; tar xzf solr-8.3.1.tgz solr-8.3.1/bin/install_solr_service.sh --strip-components=2)
(cd /tmp/ ; sudo bash ./install_solr_service.sh solr-8.3.1.tgz -n)

sudo service solr start
sudo su - solr -c "/opt/solr/bin/solr create -c addi -n data_driven_schema_configs"
sudo su - solr -c "/opt/solr/bin/solr create -c taxo -n data_driven_schema_configs"
sudo cp conf/solrconfig.xml /var/solr/data/taxo/conf/
sudo cp conf/schema.xml /var/solr/data/taxo/conf/
sudo rm /var/solr/data/taxo/conf/managed-schema

sudo service solr restart


##CONFIGURE SERVER
#edit /etc/apache2/envvars to read server_adress from external file as an environment variable
sudo echo -e ". /etc/lifemap_envir\n" >> /etc/apache2/envvars
sudo ./update_server.sh

##COPY LIFEMAP CODE TO DEDICATED FOLDER
sudo cp -r tree/* /usr/local/lifemap/



