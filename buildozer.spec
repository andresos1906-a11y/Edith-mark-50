[app]
title = AURA IA
package.name = auraia
package.domain = com.markmetalabs.auraia
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1
requirements = python3,kivy==2.3.0
orientation = portrait

[buildozer]
log_level = 2

[app:android]
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.build_tools_version = 33.0.2
android.accept_sdk_license_agreements = True
p4a.bootstrap = sdl2
