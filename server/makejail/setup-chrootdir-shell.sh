#!/bin/sh

# Given a (non-existant) directory
# creates a chroot environment so users can login
# and have limited movements

# (c) 2002 Javier Fernandez-Sanguino Peña <jfs@computer.org>

[ -z "$1" ] && {
	echo "Usage $0 directory username"
	exit 1
}
id=`/usr/bin/id -u`

[ "$id" -gt 0 ] && 
	echo "WARNING: Needs to be run as root (for mknod to work)"

dir=$1
user=$2

if [  -e "$dir" ]; then
	echo "WARNING: $dir exists. Sure you're not overwriting anything?"
	#exit 1
else
	/bin/mkdir -p $dir
fi

curdir=`/bin/pwd`

# Create Directory Tree
cd $dir
for i in etc bin dev lib home; do 
	/bin/mkdir -p $i 
done
cp -R /etc/skel/ home/$user

# Procedure:
# Copy for files and just copy symbolic links.
# Hard link could also be used if the files
# and chroot are on the same device. Replace cp with ln.

# Bin directory (minimal set of binaries)
for cmd in ls pwd true false rbash bash ; do
	if [ -f /bin/$cmd -a ! -L /bin/$cmd ] ; then
		/bin/cp /bin/$cmd bin/
	fi
	if [ -L /bin/$cmd ] ; then
		cp -a /bin/$cmd lib/
	fi
done

# Libraries (for previous binaries)
for lib in \
	/lib/libnss_files* \
	/lib/libattr* \
	/lib/librt* \
	/lib/libacl* \
	/lib/libncurses* \
	/lib/ld* \
	/lib/libc.* \
	/lib/libc-* \
	/lib/libdl* \
	/lib/librt* \
	/lib/ncurse* \
	/lib/libpthread* \
	; do
	if [ -f $lib -a ! -L $lib ] ; then
		/bin/cp $lib lib/
	fi
	if [ -L "$lib" ] ; then
		cp -a $lib lib/
	fi
done

# Config Files (etc)
grep "root:\|$user" /etc/passwd > etc/passwd
grep "root:\|$user" /etc/group > etc/group

# Devices
cd dev
# We need as many tty's as consoles
/bin/mknod -m 644 tty1 c 4 1
/bin/mknod -m 644 tty2 c 4 2
/bin/mknod -m 644 tty3 c 4 3
/bin/mknod -m 644 tty4 c 4 4
/bin/mknod -m 644 tty5 c 4 5
/bin/mknod -m 644 tty6 c 4 6
# Some special nodes, just for fun
/bin/mknod -m 444 urandom c 1 9
/bin/mknod -m 666 zero c 1 5
/bin/mknod -m 666 null c 1 3
# Warning: since we do not have the /dev/log socket the
# 'debug' option of the PAM module will not work once chrooted

# Finish and get back were we started
cd $curdir

# Set permissions
chown -R root:root $dir
chown -R $user:$user $dir/home/$user

exit 0
