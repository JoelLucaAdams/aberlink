#!/bin/bash
#Black        0;30     Dark Gray     1;30
#Red          0;31     Light Red     1;31
#Green        0;32     Light Green   1;32
#Brown/Orange 0;33     Yellow        1;33
#Blue         0;34     Light Blue    1;34
#Purple       0;35     Light Purple  1;35
#Cyan         0;36     Light Cyan    1;36
#Light Gray   0;37     White         1;37

BLACK='\e[0;30m'
RED='\e[0;31m'
GREEN='\e[0;32m'
YELLOW='\e[0;33m'
BLUE='\e[0;34m'
PURPLE='\e[0;35m'
CYAN='\e[0;36m'
LGREY='\e[0;37m'
DGREY='\e[1;30m'
LRED='\e[1;31m'
LGREEN='\e[1;32m'
LYELLOW='\e[1;33m'
LBLUE='\e[1;34m'
LPURPLE='\e[1;35m'
LCYAN='\e[1;36m'
WHITE='\e[1;37m'
NC='\e[0m' # No Color


header="
    _    _               _     _       _    
   / \  | |__   ___ _ __| |   (_)_ __ | | __
  / _ \ | '_ \ / _ \ '__| |   | | '_ \| |/ /
 / ___ \| |_) |  __/ |  | |___| | | | |   < 
/_/   \_\_.__/ \___|_|  |_____|_|_| |_|_|\_\\"
# lolcat easter egg by Xanthinian
if ! command -v lolcat &> /dev/null
then
    echo "$header"
else
    echo "$header" | lolcat
fi

echo -e "Welcome to the bash setup script for ${YELLOW}AberLink${NC}."
echo -e "The following program has been tested on ${RED}Debian 10 (Buster)${NC}"
echo -e "This script will install or enable the following:
${GREEN}Apache 2.0${NC}
-ssl
-auth_openidc
-wsgi
-rewrite
${GREEN}Python 3.7${NC}
-see Pipfiles for libraries
${GREEN}Pipenv (LATEST VERSION)"${NC}
read -p "Do you want to continue? [Y/n]: " input
if [ -z "$input" ] || [ ${input^^} = "Y" ]; then
    echo "Beginning package installs..."
elif [ $input = "n" ]; then
    echo "bye"
    exit 130
else
    echo "Invalid input, exiting..."
    exit 130
fi

echo -e "Installing ${LGREEN}apache2${NC}..."; sudo apt-get install apache2 -y > /dev/null; 
echo -e "-Enabling apache2 mod ${LPURPLE}ssl${NC}"; sudo a2enmod ssl > /dev/null; 
echo -e "-Enabling apache2 mod ${LPURPLE}wsgi${NC}"; sudo a2enmod wsgi > /dev/null; 
echo -e "-Enabling apache2 mod ${LPURPLE}rewrite${NC}"; sudo a2enmod rewrite > /dev/null; 
echo -e "-Installing apache2 mod ${LPURPLE}auth_openidc${NC}"; sudo apt-get install libapache2-mod-auth-openidc -y > /dev/null; 
echo -e "-Enabling apache2 mod ${LPURPLE}auth_openidc${NC}"; sudo a2enmod auth_openidc > /dev/null;
echo -e "Installing ${LGREEN}pipenv${NC}..."; sudo apt-get install pipenv > /dev/null;
echo "==================================================================="
echo -e "Installing packages required for ${LGREEN}psycopg2${NC}..."; sudo apt-get install libpq-dev python-dev -y > /dev/null;
echo -e "Installing dependencies for ${LGREEN}Discord bot (/src/AberLinkDiscord/)${NC}..."; cd ../src/AberLinkDiscord/; pipenv install; cd ../../config;
echo "==================================================================="
echo -e "Creating virtualenv for ${LGREEN} Django (/src/AberLinkAuthentication)${NC}"...; cd ../src/AberLinkAuthentication; virtualenv venv > /dev/null; source venv/bin/activate > /dev/null; pipenv install; deactivate; cd ../../config;

echo -e "Automatically removing uneeded ${LGREEN}packages${NC}..."; sudo apt-get autoremove > /dev/null;
