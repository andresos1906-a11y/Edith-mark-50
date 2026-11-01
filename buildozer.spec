[app]

# (str) Title of your application
title = AURA IA

# (str) Package name
package.name = auraia

# (str) Package domain (needed for android packaging)
package.domain = com.markmetalabs.auraia

# (list) Source files to include
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt

# (str) Application version
version = 0.1

# (list) Application requirements
# (edge-tts y google-generativeai removidos para evitar errores de compilación en p4a)
requirements = python3,kivy,plyer,requests,certifi,urllib3,idna,charset_normalizer,openssl

# (str) Supported orientations
orientation = portrait

# (int) Fullscreen (1 = fullscreen, 0 = not fullscreen)
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,RECORD_AUDIO

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android build tools version
android.build_tools_version = 33.0.2

android.accept_sdk_license_ = True

# (str) Bootstrap to use for p4a
p4a.bootstrap = sdl2

# (str) Branch to use for p4a
p4a.branch = master


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2
