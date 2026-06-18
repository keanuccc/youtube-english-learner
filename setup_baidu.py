"""
本地运行此脚本完成百度网盘授权，获取 token 用于 Railway 部署。

使用方法:
1. pip install bypy
2. 设置环境变量（百度开发者应用的 App Key / Secret Key）:
   - Windows PowerShell:
     $env:BYPY_APPID = "你的AppID"
     $env:BYPY_APPKEY = "你的AppKey"
     $env:BYPY_SECRETKEY = "你的SecretKey"
   - 或者写入 .env 文件
3. python setup_baidu.py
4. 按提示在浏览器中授权
5. 将输出的 token 设置为 Railway 环境变量 BYPY_TOKEN
"""

import json
import os
import sys
import base64


def main():
    print("=" * 50)
    print("百度网盘授权设置")
    print("=" * 50)
    print()

    # Check if bypy is installed
    try:
        from bypy import ByPy
    except ImportError:
        print("请先安装 bypy: pip install bypy")
        sys.exit(1)

    # Check env vars
    appid = os.getenv("BYPY_APPID")
    appkey = os.getenv("BYPY_APPKEY")
    secretkey = os.getenv("BYPY_SECRETKEY")

    if not all([appid, appkey, secretkey]):
        print("请先设置以下环境变量:")
        print()
        print("  BYPY_APPID     - 百度开发者应用 App ID")
        print("  BYPY_APPKEY    - 百度开发者应用 App Key")
        print("  BYPY_SECRETKEY - 百度开发者应用 Secret Key")
        print()
        print("获取方式: https://developer.baidu.com/ → 创建应用 → 开通 PCS 权限")
        print()
        print("设置方法 (PowerShell):")
        print('  $env:BYPY_APPID = "你的AppID"')
        print('  $env:BYPY_APPKEY = "你的AppKey"')
        print('  $env:BYPY_SECRETKEY = "你的SecretKey"')
        sys.exit(1)

    print(f"App ID: {appid[:8]}...")
    print()

    # Run auth
    print("正在初始化 bypy，将生成授权链接...")
    print()
    bp = ByPy(verbose=1)

    print()
    print("请在浏览器中完成授权，然后回到此窗口。")
    print()

    # After auth, show the token
    token_path = os.path.expanduser("~/.bypy/bypy.json")
    if os.path.exists(token_path):
        with open(token_path, "r") as f:
            token_data = json.load(f)

        # Output as base64 for easy copy-paste into Railway env var
        token_json = json.dumps(token_data)
        token_b64 = base64.b64encode(token_json.encode()).decode()

        print("=" * 50)
        print("授权成功！")
        print("=" * 50)
        print()
        print("请将以下内容设置为 Railway 环境变量 BYPY_TOKEN:")
        print()
        print(token_b64)
        print()
        print("设置方法:")
        print("1. 打开 Railway 项目页面")
        print("2. 点击 Variables 标签")
        print("3. 添加变量: BYPY_TOKEN = 上面的值")
        print("4. 保存后 Railway 会自动重新部署")
        print()
        print(f"Token 文件位置: {token_path}")
    else:
        print("[错误] 授权未完成，请重试。")
        sys.exit(1)


if __name__ == "__main__":
    main()
