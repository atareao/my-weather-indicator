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

pwd
KEY=518F68656535CF955D421424F6DE514E0459B75C
PPA="atareao/atareao"
MAIN_DIR=/app
SRCDIR=/app/src
LOCALE=/app/locale
CHANGELOG=/app/debian/changelog
PARENDIR="$(dirname "$MAIN_DIR")"
PYCACHEDIR=$SRCDIR'/__pycache__'
if [ ! -f "${CHANGELOG}" ]
then
    echo "Esto no es para empaquetar"
    return 1
fi
if [[ -d "$PYCACHEDIR" ]]; then
    echo '====================================='
    echo "Removing cache directory: $PYCACHEDIR"
    rm -rf "$PYCACHEDIR"
fi
if [ -d "$LOCALE" ]; then
    echo '====================================='
    echo "Removing locale directory: $LOCALE"
    rm -rf "$LOCALE"
fi
firstline=$(head -n 1 "$CHANGELOG")
app=$(echo "$firstline" | grep -oP "^[^\s]*")
app=${app:l} #lowercase
version=$(echo "$firstline" | grep -oP "\s\(\K[^\)]*")
#
echo '=========================='
echo 'Building debian package...'
debuild --no-tgz-check -S -sa -d -k"$KEY"
package="${PARENDIR}/${app}_${version}_source.changes"
if [ -f "$package" ]; then
    echo '==========================='
    echo "Uploading debian package..."
    dput ppa:"$PPA" "${PARENDIR}/${app}_${version}_source.changes"
else
    echo "Error: package not build"
fi
rm "${PARENDIR}/${app}_${version}*"
