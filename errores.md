Paso 1:
solucion, ingresar como super su e ingresar el siguiente comando: 
```
apt install python3.8-venv
```

Paso 2:
```
-c odoo.conf -d datatest -dev=all
```

paso 3:
Creo un nuevo modulo con toda la estructura: 
```
sudo ./odoo-bin scaffold films_crm custom_addons/
```

Paso 4:
No olvidar de dar los permisos a los directorios
```
sudo chmod 777 odoo.conf
chmod -R 777 ./ 
```

/usr/bin/python3.8 /snap/pycharm-professional/359/plugins/python/helpers/virtualenv-20.24.5.pyz --system-site-packages /home/sistemas/Escritorio/odoo/odoo/custom_addons/films_crm/venv

AttributeError: module 'virtualenv.create.via_global_ref.builtin.cpython.mac_os' has no attribute 'CPython2macOsFramework'

Traceback (most recent call last):
  File "/usr/lib/python3.8/runpy.py", line 194, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/usr/lib/python3.8/runpy.py", line 87, in _run_code
    exec(code, run_globals)
  File "/snap/pycharm-professional/359/plugins/python/helpers/virtualenv-20.24.5.pyz/__main__.py", line 163, in <module>
  File "/snap/pycharm-professional/359/plugins/python/helpers/virtualenv-20.24.5.pyz/__main__.py", line 159, in run
  File "/snap/pycharm-professional/359/plugins/python/helpers/virtualenv-20.24.5.pyz/virtualenv/__main__.py", line 18, in run
  File "/snap/pycharm-professional/359/plugins/python/helpers/virtualenv-20.24.5.pyz/virtualenv/run/__init__.py", line 31, in cli_run
  File "/snap/pycharm-professional/359/plugins/python/helpers/virtualenv-20.24.5.pyz/virtualenv/run/__init__.py", line 49, in session_via_cli
  File "/snap/pycharm-professional/359/plugins/python/helpers/virtualenv-20.24.5.pyz/virtualenv/run/__init__.py", line 82, in build_parser
  File "/snap/pycharm-professional/359/plugins/python/helpers/virtualenv-20.24.5.pyz/virtualenv/run/plugin/creators.py", line 24, in __init__
  File "/snap/pycharm-professional/359/plugins/python/helpers/virtualenv-20.24.5.pyz/virtualenv/run/plugin/creators.py", line 31, in for_interpreter
  File "/snap/pycharm-professional/359/plugins/python/helpers/virtualenv-20.24.5.pyz/virtualenv/run/plugin/base.py", line 45, in options
  File "/snap/pycharm-professional/359/plugins/python/helpers/virtualenv-20.24.5.pyz/virtualenv/run/plugin/base.py", line 24, in entry_points_for
  File "/snap/pycharm-professional/359/plugins/python/helpers/virtualenv-20.24.5.pyz/virtualenv/run/plugin/base.py", line 24, in <genexpr>
  File "/usr/lib/python3.8/importlib/metadata.py", line 79, in load
    return functools.reduce(getattr, attrs, module)
AttributeError: module 'virtualenv.create.via_global_ref.builtin.cpython.mac_os' has no attribute 'CPython2macOsFramework'
