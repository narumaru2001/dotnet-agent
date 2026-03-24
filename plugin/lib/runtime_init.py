"""
共通ランタイム初期化モジュール

pythonnet を使って .NET DLL を読み込む共通処理。
Plugin 配布時はこのモジュール経由で DLL パスを解決する。
"""

import os
import sys

import clr


def init_runtime(dll_name: str = "SampleLib") -> None:
    """DLL をロードして pythonnet で使えるようにする。"""
    # Plugin 配布時の DLL 配置先
    # 実環境では DLL の絶対パスに書き換える
    dll_dir = os.path.join(os.path.dirname(__file__), "..", "..", "bin")
    dll_path = os.path.normpath(dll_dir)

    if dll_path not in sys.path:
        sys.path.append(dll_path)

    clr.AddReference(dll_name)  # type: ignore[attr-defined]
