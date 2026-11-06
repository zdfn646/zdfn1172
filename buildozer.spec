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

# 关键配置：强制接受安卓 SDK 协议，并指定 API 版本
android.accept_sdk_license = True
android.api = 31
android.minapi = 21
android.ndk = 23b
