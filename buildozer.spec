[app]
title = quxian
package.name = quxian
package.domain = com.mycompany
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy
orientation = landscape
fullscreen = 1

# 使用清华源加速 Python 依赖包下载
pypi_mirror = https://pypi.tuna.tsinghua.edu.cn/simple

android.accept_sdk_license = True
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
