[app]
title = 曲线行驶
package.name = quxian
package.domain = com.mycompany
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# 核心依赖
requirements = python3,kivy

# 屏幕配置
orientation = landscape
fullscreen = 1

# Android 基础配置
android.accept_sdk_license = True
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a

# 让 p4a 强制使用最新稳定分支，避免旧版本 Bug
p4a.branch = develop
