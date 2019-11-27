#! /bin/sh

##COPY CORRECT HTTP TO /VAR/WWW/HTML AND UPDATE HTML FILE
if [ $html_version=="NCBI" ]; then
        sudo cp -r html/HTTP-NCBI/* /var/www/html
        sudo sed -i s/"lifemap.univ-lyon1.fr"/$server/g /var/www/html/index.html
else 
        sudo cp -r html/HTTP-MAIN/* /var/www/html
        sudo sed -i s/"lifemap.univ-lyon1.fr"/$server/g /var/www/html/explore.html
fi


