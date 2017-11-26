#!/usr/bin/env python3

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from DistUtilsExtra.command import build_extra
from distutils import cmd
from distutils.command.install_data import install_data as _install_data

import fileinput
import os
import glob
import shlex
import subprocess
import shutil
import polib
import configparser
import codecs

DATA_FILES = [
    ('/opt/extras.ubuntu.com/my-weather-indicator/bin', glob.glob('bin/*')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator',
     glob.glob('src/*.py')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator',
     glob.glob('src/*.js')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator',
     glob.glob('src/*.html')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator',
     glob.glob('src/*.svg')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator',
     ['debian/changelog']),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator\
/logos', glob.glob('data/logos/*.png')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator\
/social', glob.glob('data/social/*.svg')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator\
/images', glob.glob('data/images/*.png')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator\
/images', glob.glob('data/images/*.svg')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator\
/icons', glob.glob('data/icons/*.png')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator\
/wimages', glob.glob('data/wimages/*.png')),
    ('/usr/share/fonts/truetype/encode-sans',
     glob.glob('data/fonts/encode-sans/*.ttf')),
    ('/usr/share/fonts/truetype/mplus-1c',
     glob.glob('data/fonts/mplus-1c/*.ttf')),
    ('/usr/share/fonts/truetype/existence',
     glob.glob('data/fonts/existence/*.ttf')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator/\
skins/aclock', glob.glob('data/skins/aclock/*')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator/\
skins/allinone', glob.glob('data/skins/allinone/*')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator/\
skins/anotherone', glob.glob('data/skins/anotherone/*')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator/\
skins/super', glob.glob('data/skins/super/*')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator/\
skins/full', glob.glob('data/skins/full/*')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator/\
skins/medium', glob.glob('data/skins/medium/*')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator/\
skins/little', glob.glob('data/skins/little/*')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator/\
skins/superclock', glob.glob('data/skins/superclock/*')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator/\
skins/simple', glob.glob('data/skins/simple/*')),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/pixmaps',
     ['data/images/my-weather-indicator.png']),
    ('/opt/extras.ubuntu.com/my-weather-indicator/share/my-weather-indicator',
     ['data/my-weather-indicator-autostart.desktop']),
    ('/usr/share/applications',
     ['data/extras-my-weather-indicator.desktop']),
]

MAIN_DIR = os.getcwd()
DATA_DIR = os.path.join(MAIN_DIR, 'data')
DEBIAN_DIR = os.path.join(MAIN_DIR, 'debian')
LANGUAGES_DIR = os.path.join(MAIN_DIR, 'po')
SRC_DIR = os.path.join(MAIN_DIR, 'src')
TEMPLATE = os.path.join(LANGUAGES_DIR, 'po.pot')
CHANGELOG = os.path.join(DEBIAN_DIR, 'changelog')
f = open(CHANGELOG, 'r')
line = f.readline()
f.close()
pos = line.find('(')
posf = line.find('-', pos)
APP = line[:pos].strip().lower()
VERSION = line[pos + 1:posf].strip()
APPNAME = APP.title()
AUTHOR = 'Lorenzo Carbonell'
AUTHOR_EMAIL = 'lorenzo.carbonell.cerezo@gmail.com'
URL = 'http://www.atareao.es'
LICENSE = 'GNU General Public License (GPL)'
COMPILED_LANGUAGE_FILE = '%s.mo' % APP


def get_entry(filein, msgid):
    try:
        po = polib.pofile(filein)
        print(po.metadata['Content-Type'])
        for entry in po:
            if entry.msgid == msgid:
                return entry.msgstr
    except Exception as e:
        print(filein, e)
    return None


def ejecuta(comando):
    print('Ejecutando... %s' % comando)
    args = shlex.split(comando)
    p = subprocess.Popen(args, bufsize=10000, stdout=subprocess.PIPE)
    valor = p.communicate()[0]
    return valor


def list_src():
    file_txt = os.path.join(MAIN_DIR, 'files.txt')
    f = open(file_txt, 'w')
    for file in glob.glob(os.path.join(SRC_DIR, '*.py')):
        f.write('%s\n' % file)
    for file in glob.glob(os.path.join(MAIN_DIR, '*.desktop.in')):
        f.write('%s\n' % file)
    f.close()
    return file_txt


def list_languages():
    lans = []
    file_txt = os.path.join(LANGUAGES_DIR, 'languages.txt')
    if os.path.exists(file_txt):
        f = open(file_txt, 'r')
        for linea in f.readlines():
            lan = linea[:-1]
            print(lan)
            lans.append(lan)
        f.close()
    for file in glob.glob(os.path.join(LANGUAGES_DIR, '*.po')):
        lan = os.path.splitext(os.path.basename(file))[0]
        if lan not in lans:
            lans.append(lan)
    f = open(file_txt, 'w')
    for lan in lans:
        f.write('%s\n' % lan)
    f.close()
    return file_txt


def update_translations():
    file_txt = os.path.join(LANGUAGES_DIR, 'languages.txt')
    f = open(file_txt, 'r')
    for file in f.readlines():
        lan = file[:-1]
        file = os.path.join(LANGUAGES_DIR, lan + '.po')
        print('############################################################')
        print(lan)
        print('############################################################')
        if os.path.exists(file):
            command = 'msgmerge -U %s %s' % (file, TEMPLATE)
        else:
            command = 'msginit --output-file=%s --input=%s --locale=%s' % (
                file, TEMPLATE, lan)
        print(ejecuta(command))
        edit_language_file(file)
    f.close()


def edit_language_file(file):
    po = polib.pofile(file)
    lang = file.split('/')[-1:][0].split('.')[0]
    po.metadata['Project-Id-Version'] = '%s %s' % (APP, VERSION)
    po.metadata['Report-Msgid-Bugs-To'] = AUTHOR_EMAIL
    po.metadata['Language'] = lang
    po.metadata['Content-Type'] = 'text/plain; charset=UTF-8'
    po.metadata['Content-Transfer-Encoding'] = '8bit'
    po.save()


def update_desktop_file_fp():
    lns = []
    for filein in glob.glob('./po/*.po'):
        ln = os.path.splitext(os.path.split(filein)[1])[0]
        lns.append(ln)
    for filedesktopin in glob.glob('*.desktop.in'):
        desktopfile = configparser.ConfigParser()
        desktopfile.optionxform = str
        desktopfile.readfp(
            codecs.open(filedesktopin, encoding='utf-8', mode='r'))
        if len(lns) > 0:
            for entry in desktopfile.items('Desktop Entry'):
                if entry[0].startswith('_'):
                    for ln in lns:
                        desktopfile.set(
                            'Desktop Entry',
                            '$%s[%s]' % (entry[0][1:], ln),
                            "_('%s')" % entry[1])
        with codecs.open(filedesktopin,
                         encoding='utf-8',
                         mode='w') as outputfile:
            desktopfile.write(outputfile)


def update_desktop_file():
    lns = []
    for filein in glob.glob('./po/*.po'):
        ln = os.path.splitext(os.path.split(filein)[1])[0]
        lns.append(ln)
    for filedesktopin in glob.glob('*.desktop.in'):
        desktopfilename = os.path.splitext(os.path.split(filedesktopin)[1])[0]
        print(desktopfilename)
        fileout = os.path.join(DATA_DIR, desktopfilename)
        print(fileout)
        if os.path.exists(fileout):
            os.remove(fileout)
        fileout = codecs.open('./data/%s' % desktopfilename,
                              encoding='utf-8',
                              mode='w')
        fileout.write('[Desktop Entry]\n')
        #
        desktopfile = configparser.ConfigParser()
        desktopfile.optionxform = str
        desktopfile.readfp(codecs.open('./%s.in' % desktopfilename,
                                       encoding='utf-8',
                                       mode='r'))
        if len(lns) > 0:
            for entry in desktopfile.items('Desktop Entry'):
                if not entry[0].startswith('$'):
                    if entry[0].startswith('_'):
                        fileout.write('%s = %s\n' % (entry[0][1:], entry[1]))
                    else:
                        fileout.write('%s = %s\n' % (entry[0], entry[1]))
            for entry in desktopfile.items('Desktop Entry'):
                if entry[0].startswith('_') and not entry[0].startswith('$'):
                    for ln in lns:
                        filepo = os.path.join(LANGUAGES_DIR, '%s.po' % ln)
                        msgstr = get_entry(filepo, entry[1])
                        print(filepo)
                        if not msgstr or msgstr == '':
                            msgstr = entry[1]

                        print('%s[%s]=%s' % (entry[0][1:], ln, msgstr))
                        fileout.write('%s[%s] = %s\n' % (entry[0][1:],
                                                         ln, msgstr))
        fileout.close()


def remove_security_copies():
    for file in glob.glob(os.path.join(LANGUAGES_DIR, '*.po~')):
        os.remove(file)
    for file in glob.glob(os.path.join(LANGUAGES_DIR, '*.pot.bak')):
        os.remove(file)


def delete_it(file):
    if os.path.exists(file):
        if os.path.isdir(file):
            shutil.rmtree(file)
        else:
            os.remove(file)


def remove_files(dir, ext):
    files = []
    for file in glob.glob(os.path.join(dir, '*')):
        if file is not None and os.path.exists(file):
            if file and os.path.isdir(file):
                morefiles = remove_files(file, ext)
                if morefiles:
                    files.extend(morefiles)
            else:
                files.append(file)
    for file in files:
        if os.path.splitext(file)[1] == ext:
            os.remove(file)


def remove_compiled_files(dir):
    cachedir = os.path.join(dir, '__pycache__')
    if os.path.exists(cachedir):
        shutil.rmtree(cachedir)
    remove_files(dir, '.pyc')


def remove_languages_saved_files(dir):
    remove_files(dir, '.po~')


def babilon():
    print('############################################################')
    print('Parent dir -> %s' % MAIN_DIR)
    print('Languages dir -> %s' % LANGUAGES_DIR)
    print('Source dir -> %s' % SRC_DIR)
    print('############################################################')
    print('Updating Desktop File First Part')
    print('############################################################')
    update_desktop_file_fp()
    print('############################################################')
    print('Updating template')
    print('############################################################')
    files_file = list_src()
    command = 'xgettext --msgid-bugs-address=%s --language=Python\
    --keyword=_ --keyword=N_ --sort-by-file --output=%s --files-from=%s'\
    % (AUTHOR_EMAIL, TEMPLATE, files_file)
    print(ejecuta(command))
    print('Cleaning filepath in teplate')
    print('############################################################')
    with fileinput.FileInput(TEMPLATE, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace("#: " + MAIN_DIR, "#: .."))
    print('############################################################')
    delete_it(files_file)
    print('############################################################')
    print('List languages')
    print('############################################################')
    #
    list_languages()
    #
    print('############################################################')
    print('Updating translations')
    print('############################################################')
    update_translations()
    print('############################################################')
    print('Updating Desktop File')
    print('############################################################')
    update_desktop_file()
    print('############################################################')
    print('Removing security copies')
    print('############################################################')
    remove_security_copies()


class clean_and_compile(cmd.Command):
    description = 'Clean and compile languages'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        remove_compiled_files(SRC_DIR)
        babilon()


class translate(build_extra.build_extra):
    sub_commands = build_extra.build_extra.sub_commands + [(
        'clean_and_compile', None)]

    def run(self):
        build_extra.build_extra.run(self)
        pass


class build_trans(cmd.Command):
    description = 'Compile .po files into .mo files'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        po_dir = os.path.join(os.path.dirname(os.curdir), 'po')
        for path, names, filenames in os.walk(po_dir):
            for f in filenames:
                if f.endswith('.po'):
                    lang = f[:len(f) - 3]
                    src = os.path.join(path, f)
                    dest_path = os.path.join('build', 'locale-langpack',
                                             lang, 'LC_MESSAGES')
                    dest = os.path.join(dest_path, COMPILED_LANGUAGE_FILE)
                    if not os.path.exists(dest_path):
                        os.makedirs(dest_path)
                    if not os.path.exists(dest):
                        print('Compiling %s -> %s' % (src, dest))
                        msgfmt_cmd = 'msgfmt {} -o {}'.format(src, dest)
                        subprocess.call(msgfmt_cmd, shell=True)
                    else:
                        src_mtime = os.stat(src)[8]
                        dest_mtime = os.stat(dest)[8]
                        if src_mtime > dest_mtime:
                            print('Compiling %s -> %s' % (src, dest))
                            msgfmt_cmd = 'msgfmt {} -o {}'.format(src, dest)
                            subprocess.call(msgfmt_cmd, shell=True)


class build(build_extra.build_extra):
    sub_commands = build_extra.build_extra.sub_commands + [('build_trans',
                                                            None)]

    def run(self):
        build_extra.build_extra.run(self)


class install_data(_install_data):
    def run(self):
        for lang in os.listdir('build/locale-langpack/'):
            lang_dir = os.path.join(
                '/opt/extras.ubuntu.com/my-weather-indicator/share',
                'locale-langpack', lang, 'LC_MESSAGES')
            lang_file = os.path.join(
                'build', 'locale-langpack', lang, 'LC_MESSAGES',
                COMPILED_LANGUAGE_FILE)
            self.data_files.append((lang_dir, [lang_file]))
        _install_data.run(self)


setup(name=APP,
      version=VERSION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      license=LICENSE,
      data_files=DATA_FILES,
      cmdclass={'build': build,
                'translate': translate,
                'clean_and_compile': clean_and_compile,
                'build_trans': build_trans,
                'install_data': install_data
                },
      )
