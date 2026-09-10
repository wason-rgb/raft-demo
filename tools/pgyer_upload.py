#!/usr/bin/env python3
"""蒲公英 (Pgyer) APK 上传脚本

Usage:
  python pgyer_upload.py --file <apk> --api-key <key> [--build-name <name>] [--build-desc <desc>]

API doc: https://www.pgyer.com/doc/api
"""
import argparse
import os
import sys
import requests

PGYER_UPLOAD_URL = "https://www.pgyer.com/apiv2/app/upload"


def upload(file_path: str, api_key: str, build_name: str = "", build_desc: str = "") -> dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"APK not found: {file_path}")

    file_size_mb = os.path.getsize(file_path) / 1024 / 1024
    print(f"[pgyer] 上传: {file_path} ({file_size_mb:.2f} MB)")

    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "application/octet-stream")}
        data = {
            "_api_key": api_key,
            "buildType": "1",          # 1=Android
            "buildInstallType": "1",   # 1=公开安装
                        "buildUpdateDescription": build_desc,
        }
        if build_name:
            data["buildName"] = build_name

        resp = requests.post(PGYER_UPLOAD_URL, files=files, data=data, timeout=300)
        resp.raise_for_status()
        result = resp.json()

    if result.get("code") != 0:
        raise RuntimeError(f"蒲公英上传失败: {result}")

    data = result["data"]
    print(f"[pgyer] ✅ 上传成功: v{data.get('buildVersion', '?')} ({data.get('buildFileSize', '?')})")
    print(f"[pgyer] 应用主页: https://www.pgyer.com/{data.get('buildShortcutUrl', '?')}")
    print(f"[pgyer] 二维码 URL: {data.get('buildQRCodeURL', '?')}")
    return result


def main():
    parser = argparse.ArgumentParser(description="蒲公英 APK 上传工具")
    parser.add_argument("--file", required=True, help="APK 文件路径")
    parser.add_argument("--api-key", required=True, help="蒲公英 _api_key")
    parser.add_argument("--build-name", default="", help="构建名称（蒲公英后台显示）")
    parser.add_argument("--build-desc", default="", help="更新说明")
    args = parser.parse_args()
    upload(args.file, args.api_key, args.build_name, args.build_desc)


if __name__ == "__main__":
    main()
