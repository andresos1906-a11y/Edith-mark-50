[app]
title = EDITH VISION
package.name = edithvision
package.domain = com.stark.edith
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 51
requirements = python3,kivy==2.3.0,plyer,pyjnius
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

[app:android]
android.permissions = INTERNET,RECORD_AUDIO
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.build_tools_version = 33.0.2
android.accept_sdk_license_agreements = True
p4a.bootstrap = sdl2
p4a.branch = v2024.01.21
