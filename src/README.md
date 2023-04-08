>>> import locale
>>> locale.getdefaultlocale()
('es_ES', 'UTF-8')

python3 -m pip install tzlocal
>>> from tzlocal import get_localzone_name
>>> get_localzone_name()
'Europe/Madrid'
