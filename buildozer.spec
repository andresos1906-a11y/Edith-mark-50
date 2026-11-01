[app]
title = AURA IA
package.name = auraia
package.domain = com.markmetalabs.auraia

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 0.1

requirements = python3,kivy==2.3.0

orientation = portrait
fullscreen = 0

[app:android]
# Propósito: Asistente con voz, inteligente y hecho en México
android.permissions = INTERNET,RECORD_AUDIO
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license_agreement = True
android.archs = arm64-v8a, armeabi-v7a
p4a.branch = develop
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1
