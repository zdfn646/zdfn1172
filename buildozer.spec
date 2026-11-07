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

# 基础配置
android.accept_sdk_license = True
android.api = 33
android.minapi = 24
android.ndk = 25b

# ★ 绝对强制路径，阻止它自己下载旧版本
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.1.8937393
