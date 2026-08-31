# 部署文档：云端构建 + 蒲公英自动分发

> 适用人员：项目主导人（无需技术背景，按本文 5 步操作即可）

## 1. 注册蒲公英账号（3 分钟）

1. 访问 https://www.pgyer.com → 立即注册
2. 填手机号 + 邮箱 + 密码
3. 登录后右上角 → 账户管理 → **API 信息** → 复制 `_api_key`（一串字符）

## 2. 配置 GitHub Secrets（2 分钟）

1. 打开 https://github.com/wason-rgb/raft-demo/settings/secrets/actions
2. 点 **"New repository secret"**
3. 填：
   - **Name**：`PGYER_API_KEY`
   - **Value**：粘贴上一步复制的 `_api_key`
4. 点 **"Add secret"**

## 3. 推送代码触发第一次构建（1 分钟）

把整个 `raft-demo-v0.2-src.zip` 解压到本地一个目录，然后在该目录下执行：

```bash
bash push.sh "feat: 首次提交，搭好云端构建通道"
```

或者手动：

```bash
git init
git add .
git commit -m "feat: 首次提交"
git branch -M main
git remote add origin https://github.com/wason-rgb/raft-demo.git
git push -u origin main
```

> 第一次推送时可能要求登录 GitHub 账号，按提示输入用户名 + Personal Access Token（不是密码）

## 4. 等待云端构建（8-15 分钟）

1. 访问 https://github.com/wason-rgb/raft-demo/actions
2. 看 **"Build Android APK"** workflow 跑完
3. 失败的话点进去看 log（一般是 JDK 版本或 Godot 模板问题）

## 5. 手机扫码装包

构建成功后蒲公英自动收到 APK：

- 程序袁会在群里贴蒲公英二维码
- 微信扫码 → 浏览器打开 → 下载 APK → 安装（首次需允许"安装未知来源"）

## 后续日常流程

您改完代码（一般是程序袁改了）→ 老板执行 `bash push.sh "改了什么"` → 自动触发：

1. GitHub 云端构建 APK
2. 自动上传蒲公英
3. 老板手机扫码装新版本

**全程无需老板做任何构建操作**。

## 9/6 最终交付命名

按 v1.1 8.1.1 命名规范，最终 APK 命名：

`raft_demo_v1.0_android_2026-09-06.apk`

程序袁会在 9/5 晚上把名字固定下来，9/6 上午触发最后一次构建。

## 故障排查

| 现象 | 原因 | 解决 |
|------|------|------|
| 推送要求密码 | GitHub 早就不支持密码推送了 | 用 Personal Access Token（在 GitHub Settings → Developer settings → Personal access tokens 生成） |
| Actions 跑失败 "JAVA_HOME not set" | 偶发 | 重新 push 一次 |
| Actions 跑失败 "command not found: godot-mono" | barichello/godot-ci 版本问题 | 暂时不管，program-袁 会改 |
| 蒲公英上传失败 "Invalid api key" | API key 配错 | 重新配 Secret |
| APK 装不上 "解析包出现问题" | 安卓版本低于 8.0 | 换 Android 8.0+ 设备 |
| APK 装上闪退 | 包名冲突 | 卸载旧版再装 |

有阻塞点随时 @ 程序袁。
