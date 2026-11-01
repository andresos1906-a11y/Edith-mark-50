[app]
title = EDITH VISION V2
package.name = edithvisionv2
package.domain = com.stark.edith
source.dir = .
version = 51.0
requirements = python3,kivy==2.3.0,plyer,pyjnius
orientation = portrait
[buildozer]
log_level = 2
[app:android]
android.permissions = INTERNET,RECORD_AUDIO,READ_CONTACTS,QUERY_ALL_PACKAGES
android.api = 33
android.minapi = 21
android.build_tools_version = 33.0.2
android.ndk = 25b
android.accept_sdk_license_agreements = True
p4a.branch = v2024.01.21
p4a.bootstrap = sdl2
# icon.filename = ./icon.png
