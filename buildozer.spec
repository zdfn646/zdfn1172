[app]
# 应用显示名称
title = 曲线行驶
# 应用包名 (全小写)
package.name = quxian
# 应用域名 (通常公司或个人域名的反写)
package.domain = com.mycompany

# 包含的源代码和资源文件扩展名
source.include_exts = py,png,jpg,kv,atlas

# 应用版本
version = 1.0.0

# ★ 核心依赖：必须包含 python3 和 kivy，这是打包成功的基础[reference:1]
requirements = python3,kivy

# ★ 权限配置：根据你的App需求按需添加，例如：
# android.permissions = INTERNET, CAMERA
# 你的App如果是离线单机，可以不写或留空

# ★ 屏幕方向：强制横屏
orientation = landscape

# ★ 全屏设置：1 表示全屏
fullscreen = 1

# --- 以下为 Android 平台推荐配置，有助于避免常见错误 ---
# 接受SDK许可
android.accept_sdk_license = True
# 目标 Android API 版本 (Android 13)[reference:3][reference:4]
android.api = 33
# 最低支持的 Android API 版本 (Android 7.0)
android.minapi = 24
# 指定 NDK 版本，锁定 25b 通常更稳定[reference:5][reference:6]
android.ndk = 25b
