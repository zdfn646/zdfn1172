[app]
title = quxian
package.name = quxian
package.domain = com.mycompany
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# ★ 核心修复：强制锁定稳定版本，拒绝 Python 3.14
requirements = python3==3.10.12,hostpython3==3.10.12,kivy==2.3.0

orientation = landscape
fullscreen = 1

pypi_mirror = https://pypi.tuna.tsinghua.edu.cn/simple

android.accept_sdk_license = True
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
