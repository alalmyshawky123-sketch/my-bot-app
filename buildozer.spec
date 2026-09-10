[app]
title = My Phone Control
package.name = phonecontrol
package.domain = org.control
source.include_exts = py,png,jpg,kv,atlas
source.dir = .
version = 1.0
requirements = python3,requests,pyjnius
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0

# الصلاحيات المطلوبة لنظام أندرويد لتنفيذ الأوامر وسحب البيانات
android.permissions = INTERNET,READ_CONTACTS,READ_SMS,ACCESS_FINE_LOCATION,CAMERA,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.sdk = 30
android.ndk = 23b
android.archs = arm64-v8a, armeabi-v7a
