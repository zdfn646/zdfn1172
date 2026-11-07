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

# 锁定版本与路径，防止报错
android.accept_sdk_license = True
android.ndk = 25b
android.sdk = 33

# 核心修改：直接使用 GitHub 环境自带的 SDK 和 NDK，省去半小时下载时间
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.1.8937393
