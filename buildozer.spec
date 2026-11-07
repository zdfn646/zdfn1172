[app]
title = 曲线行驶
package.name = quxian
package.domain = com.mycompany
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# ★ 核心修复 1：强制指定 Python 3.10，避开 3.14 的坑
requirements = python3==3.10.12,kivy

orientation = landscape
fullscreen = 1

# 基础配置
android.accept_sdk_license = True
android.api = 33
android.minapi = 24
android.ndk = 25b
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.1.8937393

# ★ 核心修复 2：只编译 arm64-v8a（绝大多数现代手机），防止编译内存溢出和超时
android.archs = arm64-v8a
