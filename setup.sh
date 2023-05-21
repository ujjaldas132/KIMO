sudo apt install python3.10-venv libffi-dev libnacl-dev
sudo apt-get install python3.10-dev default-libmysqlclient-dev build-essential


sudo python3.10 -m venv venv
sudo chown -R $userName:$userName venv

source ./venv/bin/activate


./venv/bin/pip3.10 install -r requirements.txt