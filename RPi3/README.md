# Raspberry Pi 3 Software Preparation

Download the latest version of Raspbian

```shell
wget https://downloads.raspberrypi.org/raspbian_lite_latest
unzip YYYY-MM-DD-raspbian-strecth-lite.zip
```

This then needs to be copied to a uSD card for use.  Determine the Device to be used and replace X with the number

```shell
sudo dd if=rasbian.img of=/dev/sdX bs=2M status=progress && sync
```

Connect monitor and keyboard and boot

* User = pi 
* Password=raspberry 

```shell
sudo raspi-config
``` 
* expand fs
*	set hostname ML_XX
* Booting Options
  *	boot option - console
* localisation
  * en.AU_UTF-8
	*	timezone - au – syd
* Wi-Fi
  * au
* interface
	*	enable ssh
* Advanced
	*	memory split 16

```shell
sudo reboot
```

* User = pi 
* Password = raspberry 

Now setup a local user and del user 'pi'

```shell
sudo adduser bloggs
```
Enable this user to sudo

```shell
sudo visudo
```
Add this at the bottom

bloggs	ALL=(ALL:ALL)ALL

Then save and exit

```shell
sudo apt update && sudo apt upgrade sudo deluser pi && sudo rm -r /home/pi
```
```shell
sudo reboot
```
Now remote connections can be initinlised, so you can disconnenct display and keyboard and use another computer to connect via SSH

```shell
ssh blogs@192.168.20.XX 
```

```shell
sudo
apt install python3 python3-pip python3-dev python3-scipy autoconf automake libtool curl make g++ unzip build-essential ntpdate
```

To set a static IP address use the following commands

```shell
sudo nanao /etc/dhcpcd.conf
```
Static IP Address Setup to be entered

interface eth0

static ip_address=192.168.20.XX/24 

static routers=192.168.20.YY

static domain_name_servers=192.168.20.YY

To disable wifi enter the following

```shell
sudo nanao /config.txt
```
Add the following two lines then save and exit

dtoverlay=pi3-disable-wifi

dtoverlay=pi3-disable-bt

```shell
sudo reboot
```


```shell
ssh bloggs@192.168.20.XX
```

The version of Tensorflow used was r1. and and available through 

```shell
wget https://github.com/samjabrahams/tensorflow-on-raspberry-pi/releases/download/v1.1.0/tensorflow-1.1.0-cp34-cp34m-linux_armv7l.whl
```

```shell
sudo pip3 install tensorflow-1.1.0-cp34-cp34m-linux_armv7l.whl
sudo pip3 uninstall mock
sudo pip3 install mock
sudo pip3 install matplotlib
```
