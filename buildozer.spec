[app]
title = EDITH VISION
package.name = edithvision
package.domain = com.edith.vision

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0
version.regex = __version__ = ['"]([^'"]+)['"]
version.filename = %(source.dir)s/main.py

requirements = python3,kivy,opencv,android,numpy,pillow
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.build_tools_version = 33.0.2
android.accept_sdk_license_agreements = True
android.permissions = CAMERA,RECORD_AUDIO,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.features = android.hardware.camera,android.hardware.camera.autofocus
p4a.branch = master
p4a.bootstrap = sdl2

[buildozer:android]
android.sdk_path = /home/runner/android-sdk
android.ndk_path = /home/runner/android-sdk/ndk/25.1.8937393
