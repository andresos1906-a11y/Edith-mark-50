[app]
title = AURA
package.name = aura
package.domain = org.ecatepec.aura

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

requirements = python3,kivy==2.3.0,pillow,requests,plyer,android

orientation = portrait
fullscreen = 0

# Permisos para los perritos
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 28c
android.accept_sdk_license_agreement = True
android.ant = auto

# Icono - si no tienes, quita esta linea
#icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
