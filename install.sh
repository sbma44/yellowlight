sudo apt-get update -y
sudo apt-get install -y supervisor git python-setuptools
sudo mkdir -p /usr/local/etc
sudo pip install -e git+https://github.com/sbma44/nextbus.git#egg=nextbus
sudo git clone git@github.com:sbma44/yellowlight.git /usr/local/etc/yellowlight
sudo pip install -r /usr/local/etc/yellowlight/requirements.txt
sudo cp /usr/local/etc/yellowlight/yellowlight.conf /etc/supervisor/conf.d/yellowlight.conf
sudo /usr/sbin/service restart supervisor