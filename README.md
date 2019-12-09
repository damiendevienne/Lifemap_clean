# Configuration of a server for Lifemap

This repository allows the deployment of Lifemap on a new server (tested on Ubuntu Server 18.04). 
You must to be sudoer to use this pipeline. 
It is a simple 5-steps process: 

1. Clone this repository locally and enter in it

```bash
git clone https://github.com/damiendevienne/Lifemap_clean.git
cd Lifemap_clean
```
2. Execute the configuration script, with sudo

```bash
sudo ./configure.sh
```
3. [optional] Update the server information. This allows apache2 and the Lifemap html script to use the correct server name and port redirections. This script is already exectuted by `configure.sh` thus no need to run it again if the default option is to be used.

```bash
sudo ./update_server.sh
##use -s 'server' to specify a domain or ip adress different from the default one (retrieved with command 'curl ificonfig.me')
```
4. Download and build the tree

```bash
sudo ./make_tree.py --lang EN --simplify TRUE

```
options:
- --lang can be ENglish(the default)  or FRench. French names of clades come from the INPN taxonomic reference (https://inpn.mnhn.fr/programme/referentiel-taxonomique-taxref) version 11.
- --simplify (True or False) specifies whether the NCBI taxonomy should be simplified. Simplification involves removing species with termes like 'unclutured','unidentified','environmental', etc.

5. Choose the version of the Lifemap page that you want (main or ncbi) and copy the corresponding folder as follows
```bash
sudo cp -r html/HTTP-MAIN/* /var/www/html/ ##for 'main' version
##OR
sudo cp -r html/HTTP-NCBI/* /var/www/html/ ##for 'ncbi' version
```


# Change the style of the map or create a new map with a new style (keeping the first one) 
To change the style of the map, simply edit the file /usr/lifemap/style/lifemap_style.xml

To create a new map on the same server with a new style:
- create a new style file in the same directory 
```bash
sudo cp /usr/lifemap/style/lifemap_style.xml /usr/lifemap/style/newstyle.xml
```
- open and edit /etc/renderd.conf and add the following block: 
```
[mystyle]
URI=/lifemap_new/
TILEDIR=/var/lib/mod_tile
XML=/usr/lifemap/style/lifemap_newstyle.xml
HOST=localhost
TILESIZE=256
MINZOOM=0
MAXZOOM=40
```
- restart renderd and apache to take changes into account
```bash
sudo service renderd restart
sudo service apache2 restart
```

- finally change the url of the tiles in the html file used to explore the tree (in /var/www/html):
`.../mod_tile/...` should be replaced (in this example) by `.../lifemap_new/...`

If the file is called index.html this is easily done with sed: 
```bash
sudo su
sed s/'osm_tile'/'lifemap_new'/g index.html > indexnewstyle.html
##visit indenewstyle.html to see the changes.
```







---

If you see bugs, please open an issue or send an email to damien.de-vienne@univ-lyon1.fr

