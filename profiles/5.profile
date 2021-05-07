net none
noroot
novideo
nosound
notv
nou2f
no3d
nodvd
nodbus
nogroups

whitelist /tmp/mysession

blacklist /sys
blacklist /etc/*
#blacklist /proc/*
blacklist /opt
blacklist /root
blacklist /lost+found
noblacklist /run/firejail
blacklist /run/*
blacklist /var
blacklist /vmlinuz
blacklist /vmlinuz.old
#blacklist /usr
blacklist /srv
blacklist /snap
blacklist /media
blacklist /mnt
blacklist /cdrom
blacklist /sbin


private-dev
#private-lib /usr/lib/python3.7, /home/megamind/.local/lib/python3.7
#private-bin /usr/bin/python3.7

private-lib /usr/lib/python3.7,/usr/lib/x86_64-linux-gnu,/usr/lib/libssl.so.1.0.0 
private-bin /usr/bin/python3.7,/bin/bash,/bin/ls,/bin/cat,/usr/bin/vim
env LD_LIBRARY_PATH=/usr/lib/python3.7/:/usr/lib/
#seccomp.keep @default-keep,@basic-io
#seccomp.drop @default-nodebuggers,@privileged,@ipc,@aio,@setuid,@io-event

caps.drop all
disable-mnt
##
##nice -5
##Maximum size of virtual memory for sandbox
#rlimit-as 123456789012
##MAximum cpu time in seconds
#rlimit-cpu 123
##Maximum file size
##rlimit-fsize 1024

private /tmp/mysession/5
