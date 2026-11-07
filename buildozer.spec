[app]
title = 曲线行驶
package.name = quxian
package.domain = com.mycompany
# 关键的一行：告诉 Buildozer 源码在当前目录
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy
orientation = landscape
fullscreen = 1

# Android 配置
android.accept_sdk_license = True
android.api = 33
android.minapi = 24
android.ndk = 25b
