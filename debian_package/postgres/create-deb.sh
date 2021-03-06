#!/bin/bash

usage() {
	echo "Usage:"
	echo -e "\t$0 <version>\n"
}

usage_and_error() {
	echo -e "Error: $1\n"
	usage
  exit -1
}

###
# Check arguments
#
BASE_DIR="$(dirname $0)"

PKG_VERSION="$1"

if [ -z $PKG_VERSION ] ; then
	usage_and_error "missing version argument"
fi

###
# Create directory layout
#
mkdir -p $BASE_DIR/debian/DEBIAN

###
# Copy maintainer files
#
cat $BASE_DIR/debian-control | sed s/"<vnumber>"/$PKG_VERSION/g > $BASE_DIR/debian/DEBIAN/control
cp $BASE_DIR/debian-templates $BASE_DIR/debian/DEBIAN/templates
cp $BASE_DIR/debian-postinst $BASE_DIR/debian/DEBIAN/postinst
cp $BASE_DIR/debian-postrm $BASE_DIR/debian/DEBIAN/postrm

###
# Create the Debian package
#
dpkg-deb --build $BASE_DIR/debian ezweb-platform-postgres_${PKG_VERSION}_all.deb

rm -rf $BASE_DIR/debian
