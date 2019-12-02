#! /bin/sh

usage="$(basename "$0") [-h] [-s server_address] -- update apache2 and Lifemap html scripts with specific server asdress. 

where:
    -h  show this help text
    -s  server to use. (default: ip adress of the machine on the web)"

server="default.default"
while getopts ':hs:' option; do
  case "$option" in
    h) echo "$usage"
       exit
       ;;
    s) server=$OPTARG
       ;;
    :) printf "missing argument for -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
   \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
  esac
done
shift $((OPTIND - 1))


#html_version="NCBI" #can also be "MAIN"
#lang="en" #can also be "fr"
#server="default.default" ##IP address of domain. without http. If not specified, IP adress is retrieved from with command ifconfig.me 

if [ $server=="default.default" ]; then
        echo "Getting IP adress of machine..."
	server=$(curl ifconfig.me)
fi
echo "Exporting server address to /etc/lifemap_envir"
sudo echo "export SERVER_ADDRESS="$server > /etc/lifemap_envir
echo "Restarting apache"
sudo service apache2 restart

##COPY CORRECT HTTP TO /VAR/WWW/HTML AND UPDATE HTML FILE with server name
if [ $html_version=="NCBI" ]; then
        sudo cp -r html/HTTP-NCBI/* /var/www/html
        sudo sed -i s/"lifemap.univ-lyon1.fr"/$server/g /var/www/html/index.html
else 
        sudo cp -r html/HTTP-MAIN/* /var/www/html
        sudo sed -i s/"lifemap.univ-lyon1.fr"/$server/g /var/www/html/explore.html
fi


