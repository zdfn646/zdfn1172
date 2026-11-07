[app]
title = 曲线行驶
package.name = quxian
package.domain = com.mycompany
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy
orientation = landscape
fullscreen = 1

# 关键修复：指定稳定的 NDK 和 SDK 版本，并自动同意协议
android.accept_sdk_license = True
android.ndk = 25b
android.sdk = 33
