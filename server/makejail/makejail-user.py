#Start Afresh
#cleanJailFirst=1

#Directory of the jail, change this, also change it below in forceCopy
chroot="/home/googleshare"

#Make sure it works
testCommandsInsideJail=["/usr/local/bin/googleshare -p8080 -s8443","/bin/bash"]
processNames=["python","bash"]
#testCommandsInsideJail=["/bin/bash"]
#processNames=["bash"]

#Makejails isn't very good at finding library dependencies
forceCopy=[
#Change this to the proper homedir
"/home/googleshare",
#
"/lib/libnss_files*",
"/lib/libattr*",
"/lib/librt*",
"/lib/libacl*",
#"/lib/libncurses*",
"/lib/ld*",
"/lib/libc.*",
"/lib/libc-*",
"/lib/libdl*",
"/lib/librt*",
"/lib/libssl*",
#"/lib/ncurse*",
"/lib/libpthread*",
"/etc/group",
"/etc/passwd",
"/etc/ssl/certs/googlesharing.pem",
"/etc/ssl/private/googlesharing.key",
#You can copy anythink from /dev and it will be set-up properly
#"/dev/tty1",
#"/dev/tty2",
#"/dev/tty3",
#"/dev/tty4",
#"/dev/tty5",
#"/dev/tty6",
"/dev/null",
]

#THe users and groups to keep, change this to the correct user
users=["root","googleshare","nobody"]
groups=["root","googleshare","nogroup"]

#Debian packages to copy into chroot
packages=["python","python-openssl","python-psyco","python-twisted-core","python-twisted-bin","python-twisted-web"]
#Will install package dependencies, can be quite useful
useDepends=1
