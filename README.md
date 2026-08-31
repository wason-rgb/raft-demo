# 极境浮生 · 木筏漂流 Android demo（v0.2）

游戏设定：**随机漂流 + 木筏保持屏幕中央 + 玩家不能决策移动** + 横屏 1920×1080 + 48×32 像素 + Android 8.0+

## 目录结构

```
raft-demo/
├── project.godot                  # Godot 4.2 Mono 工程配置
├── RaftDemo.csproj / .sln         # C# 项目
├── export_presets.cfg             # Android 导出预设（arm64-v8a + minSdk 26）
├── icon.svg                       # 应用图标占位
├── scenes/
│   └── Main.tscn                  # 主场景：背景 + 云 + 水面 + 木筏 + 主角 + 漂浮物
├── scripts/                       # C# 脚本
│   ├── RandomDriftController.cs   # 核心：5-15s 随机换向 + 80-120px/s + 100ms lerp
│   ├── Raft.cs                    # 固定屏幕中心 + 4px sin 呼吸（2.4s 周期）
│   ├── Water.cs                   # 双层视差反向滚动（深水 0.7x + 浪 1.5x）
│   ├── Cloud.cs                   # 0.5x 背景视差 + 出屏回卷
│   └── Debris.cs                  # 1.5x 视差 + 4-12s 随机重生
├── assets/sprites/                # 48×32 像素占位符
│   ├── player.png   (16×32)
│   ├── raft.png     (48×32)
│   ├── water_deep.png (48×32)
│   ├── water_wave.png (48×32)
│   ├── cloud.png    (96×32)
│   └── debris.png   (16×16)
├── .github/workflows/
│   └── android.yml                # GitHub Actions：构建 + 蒲公英上传
├── tools/
│   ├── pgyer_upload.py            # 蒲公英上传脚本
│   └── verify_logic.py            # Python 1:1 业务逻辑复现 + 预览图
├── push.sh                        # 一键推代码触发云端构建
└── DEPLOY.md                      # 老板专用部署文档（5 步出 APK）
```

## 业务逻辑（v0.2 关键参数）

| 脚本 | 职责 | 关键参数 |
|------|------|----------|
| RandomDriftController | 每 5–15s 随机换方向 + 速度浮动 + 100ms 平滑切换 | min_speed=80, max_speed=120 |
| Raft | 固定屏幕中心 (960,540) + 4px 上下呼吸 | bob_amp=4, period=2.4s |
| Water | 双层视差反向滚动 | deep=0.7x, wave=1.5x |
| Cloud | 0.5x 背景视差 + 出屏回卷到对侧 | wrap=200px |
| Debris | 1.5x 视差 + 4-12s 随机重生 | respawn=random(4,12)s |

## 验收对照（老板 8/30 拍板 → 实现位置）

| 老板要求 | 实现位置 |
|----------|----------|
| Android 手机平台 | `export_presets.cfg` (Android arm64-v8a) |
| 最低 Android 8.0 (API 26) | `gradle_build/min_sdk=26` |
| 横屏 1920×1080 | `project.godot` (landscape + stretch) |
| 48×32 像素 | `assets/sprites/*` 全部 48×32 横向 |
| 随机漂流 | `RandomDriftController.cs` |
| 木筏居中 | `Raft.cs` (ScreenCenter=960,540) |
| 玩家不能决策移动 | 无 Player 输入脚本（已删除 v0.1 的 Player.cs） |

## 本地开发（可选，仅程序袁用）

```bash
# 装 Godot 4.2 Mono：https://godotengine.org/download
godot --path . --import   # 首次导入资源
godot --path .            # 打开编辑器，F5 跑
```

## 云端构建（生产路径，老板专用）

```bash
bash push.sh "feat: 改了啥"   # 一键推 GitHub + 触发云端构建 + 蒲公英分发
```

详细看 [DEPLOY.md](DEPLOY.md)

## Python 业务逻辑复现（沙箱验证）

```bash
python tools/verify_logic.py
# 输出 tools/preview_montage.png（4×3 拼图，6 秒内 12 帧状态）
```

## v0.1 → v0.2 改动

| 项 | v0.1 (Win11) | v0.2 (Android) |
|----|--------------|----------------|
| 平台 | Win x86_64 | Android 8.0+ arm64-v8a |
| 屏幕 | 窗口可调 | 1920×1080 横屏 + stretch |
| 玩家 | 方向键移动 | 不能决策移动（已删 Player.cs） |
| 相机 | 跟随主角 | 静态（木筏居中） |
| 漂移 | 5px/s 缓慢自漂 | 5-15s 随机换向 + 80-120px/s |
| 视觉层 | 主角 + 木筏 + 水 | + 云 + 漂浮物 |
| 像素 | 16×16 | 48×32 |

## 9/6 最终交付命名

按 v1.1 8.1.1 命名规范：

`raft_demo_v1.0_android_2026-09-06.apk`
