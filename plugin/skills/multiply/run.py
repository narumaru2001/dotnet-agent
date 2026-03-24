import json
import sys
import os

# 共通ランタイムを読み込み
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
from runtime_init import init_runtime  # type: ignore[import-not-found]

init_runtime("SampleLib")
from SampleLib import Calculator  # type: ignore[import-not-found]


def main():
    params = json.loads(sys.argv[1])
    a = int(params["a"])
    b = int(params["b"])

    calc = Calculator()
    result = calc.Multiply(a, b)

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
