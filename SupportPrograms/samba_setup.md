sudo apt update
sudo apt install samba

whereis samba
samba: /usr/sbin/samba /usr/lib/samba /etc/samba /usr/share/samba /usr/share/man/man7/samba.7.gz /usr/share/man/man8/samba.8.gz

sudo nano /etc/samba/smb.conf

[PC19]
comment = Samba-share Documents folder -- Sam 6th Aug, 2020
path = /home/nitta/Documents
read only = no
browsable = yes
available = yes

sudo service smbd restart
sudo ufw allow samba

sudo smbpasswd -a nitta
kinesin

