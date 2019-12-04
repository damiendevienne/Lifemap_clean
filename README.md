# Configuration of a server for Lifemap

This repository allows the deployment of Lifemap on a new server (tested on Ubuntu Server 18.04). 
You must to be sudoer to use this pipeline. 
It is a 5-steps process: 

1. clone this repository locally and enter in it

```bash
git clone https://github.com/damiendevienne/Lifemap_clean.git
cd Lifemap_clean
```
2. execute the configuration script, with sudo

```bash
sudo ./configure.sh
```
3. update the server information. This allows apache2 and the Lifemap html script to use the correct server name and port redirections

```bash
sudo ./update_server.sh
##use -s 'server' to specify a domain or ip adress different from the default one (retrieved with command 'curl ificonfig.me')
```
4. Download and build the tree

```bash
sudo ./make_tree.py --lang EN --simplify TRUE
##lang can be FR for french version. simplify tells wether the NCBI tree should be simplified beforehand by removing unidentified species. 
```

---

If you see bugs, please open an issue or send an email to damien.de-vienne@univ-lyon1.fr

