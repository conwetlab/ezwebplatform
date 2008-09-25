#!/bin/sh
# since reprepro 0.8 this is no longer needed, as it can
# create .bz2 files on its own (when compiled with libbz2-dev
# present). It's still here for reference how to such a filter works.

# Copy this script to your conf/ dir as bzip2.sh, make it executable
# and add to some definition in conf/distributions
# DscIndices: Sources Release . .gz bzip2.sh
# DebIndices: Packages Release . .gz bzip2.sh
# UDebIndices: Packages . .gz bzip2.sh
# and you have .bz2'd Packages and Sources.
# (alternatively, if you are very brave, put the full path to this file in there)

DIROFDIST="$1"
NEWNAME="$2"
OLDNAME="$3"
# this can be old($3 exists), new($2 exists) or change (both):
STATUS="$4"
BASENAME="`basename "$OLDNAME"`"

# with reprepro <= 0.7 this could also be Packages.gz or Sources.gz,
# but now only the uncompressed name is given. (even if not generated)
if [ "xPackages" = "x$BASENAME" ] || [ "xSources" = "x$BASENAME" ] ; then
	if [ "x$STATUS" == "xold" ] ; then
		if [ -f "$DIROFDIST/$OLDNAME.bz2" ] ; then
			echo "$OLDNAME.bz2" >&3
		else
			bzip2 -c -- "$DIROFDIST/$OLDNAME" >"$DIROFDIST/$OLDNAME.bz2.new" 3>/dev/null
			echo "$OLDNAME.bz2.new" >&3
		fi
	else
		bzip2 -c -- "$DIROFDIST/$NEWNAME" >"$DIROFDIST/$OLDNAME.bz2.new" 3>/dev/null
		echo "$OLDNAME.bz2.new" >&3
	fi
fi
