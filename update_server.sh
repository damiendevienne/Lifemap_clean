#! /bin/sh

usage="$(basename "$0") [-h] [-s server_address] -- update apache2 and Lifemap html scripts with specific server asdress. 

where:
    -h  show this help text
    -s  server to use. (default: ip adress of the machine on the web)"

server=""
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

if [ -z "$server" ]; then
        echo "Getting IP adress of machine..."
	server=$(curl ifconfig.me)
fi

#Exporting server address to /etc/lifemap_envir
sudo echo "export SERVER_ADDRESS="$server > /etc/lifemap_envir
sudo service apache2 restart

#Export server adress to jsvascript (needed for html pages)
sudo echo "var ServerAddress=\"$server\"" > /var/www/html/server-address.js


