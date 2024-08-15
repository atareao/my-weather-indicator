#!/usr/bin/env bash
# -*- coding: utf-8 -*-

# Copyright (c) 2021 Lorenzo Carbonell <a.k.a. atareao>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

NEWLINE=$'\n'
TAB=$'\t'

firstline="$(head -1 debian/changelog)"
package=$(echo "$firstline" | grep -oP "^[^\s]*")
package=${package:l} #lowercase
version=$(echo "$firstline" | grep -oP "\s\(\K[^\)]*")

echo "========="
echo $package
echo $version
echo "========="

if [ ! -f debian/changelog ]
then
    echo "I can't find debian/changelog"
    return 1
fi

if [ ! -f po/po.pot ];
then
    touch po/po.pot
fi
find -type f -name "*.py" | xargs xgettext -L Python --from-code=UTF-8 -k_ -kN_ -o po/po.pot
if [ -d locale ];then
    rm -rf locale/
fi
trans=$(ls -1 po/ | wc -l)
if [ $trans -gt 1 ]
then
    for i in po/*.po
    do
        echo "=== $i ==="
        filename=$(basename "$i")
        lang=${filename/.po}
        file_size=`wc -c < $i`
        if [ $file_size -gt 0 ];then
            msgmerge -U $i po/po.pot
        else
            msginit --output-file=$i --input=po/po.pot --locale=$lang
        fi
        sed -i -e 's/charset=ASCII/charset=UTF-8/g' $i
        sed -i -e "s/PACKAGE VERSION/$package - $version/g" $i
        sed -i -e "s/PACKAGE package/$package package/g" $i
        ## Translations
        if [ ! -d locale/$lang ];then
            mkdir -p locale/$lang/LC_MESSAGES
        fi
        echo "=== compile $i ==="
        msgfmt $i -o locale/$lang/LC_MESSAGES/$package.mo
        echo "=== end compile $i ==="
    done
fi
find . -type f -name "*.po~" -delete
find po/ -type f -name "*.po~" -delete

echo "=== creating rules ==="
file="debian/rules"
echo "$file"

if [ -f $file ]
then
    rm $file
fi

echo "== Configuration file =="
echo "$file"
echo "#!/usr/bin/make -f
# Sample debian/rules that uses debhelper.
# This file is public domain software, originally written by Joey Hess.
#
# This version is for packages that are architecture independent.

# Uncomment this to turn on verbose mode.
#export DH_VERBOSE=1

build: build-stamp
build-stamp:
dh_testdir

# Add here commands to compile the package.
# MAKE

touch build-stamp

clean:
dh_testdir
dh_testroot
rm -f build-stamp

# Add here commands to clean up after the build process.
# MAKE clean
# MAKE distclean

dh_clean

install: build
dh_testdir
dh_testroot
dh_prep
dh_installdirs
dh_install
" >> ${file}

trans=$(ls -1 po/ | wc -l)
if [ $trans -gt 1 ]
then
    variable1="${TAB}# Create languages directories"
    variable2=''
    for i in po/*.po
    do
        lang=${i//.po}
        lang=${lang//po\/}
        echo $lang
        #echo '	mkdir -p ${CURDIR}/debian/'$package'/usr/share/locale-langpack/'$lang'/LC_MESSAGES' >> $file
        variable1+="${NEWLINE}${TAB}mkdir -p "'${CURDIR}'"/debian/$package/usr/share/locale-langpack/$lang/LC_MESSAGES"
        variable2+="${NEWLINE}${TAB}msgfmt $i -o "'${CURDIR}'"/debian/$package/usr/share/locale-langpack/$lang/LC_MESSAGES/$package.mo"
    done
    variable1+="${NEWLINE}${TAB}# End create languages directories"
    variable1+="${NEWLINE}${TAB}# Compile languages"
    variable1+=$variable2
    variable1+="${NEWLINE}${TAB}# End comile languages"
fi
echo "${variable1}" >> $file
echo "
# Add here commands to install the package into debian/<packagename>.
# MAKE prefix=

# Build architecture-independent files here.
binary-indep: build install
dh_testdir
dh_testroot
dh_installchangelogs
dh_installdocs
dh_installexamples
# added gconf and icons
#	dh_gconf
dh_icons
#	dh_installmenu
#	dh_installdebconf
#	dh_installlogrotate
#	dh_installemacsen
#	dh_installcatalogs
#	dh_installpam
#	dh_installmime
#	dh_installinit
#	dh_installcron
#	dh_installinfo
#	dh_installwm
#	dh_installudev
#	dh_lintian
#	dh_bugfiles
#	dh_undocumented
dh_installman
dh_link
dh_compress
dh_fixperms
#	dh_perl
#	dh_pysupport
dh_installdeb
dh_gencontrol
dh_md5sums
dh_builddeb

# Build architecture-dependent files here.
binary-arch: build install
# We have nothing to do by default.

binary: binary-indep binary-arch
.PHONY: build clean binary-indep binary-arch binary install
" >> ${file}
chmod 777 $file
if [ -d locale ]
then
    rm -rf locale/
fi
