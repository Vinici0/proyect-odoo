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


