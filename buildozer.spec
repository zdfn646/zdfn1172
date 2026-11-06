[app]
# 应用显示名称
title = 曲线行驶
# 包名（只能用小写字母和数字）
package.name = quxian
# 域名
package.domain = com.mycompany

# 源代码目录
source.dir = .
# 包含的文件类型
source.include_exts = py,png,jpg,kv,atlas

# 版本号
version = 1.0.0

# 依赖项（Kivy 必须包含 python3,kivy）
requirements = python3,kivy

# 强制横屏
orientation = landscape
# 强制全屏
fullscreen = 1

# 安卓权限（虽然目前没用到网络，但加上去没坏处）
android.permissions = INTERNET
