import json
import sys
import os

# 共通ランタイムを読み込み
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
from runtime_init import init_runtime  # type: ignore[import-not-found]

init_runtime("SampleLib")
from SampleLib import Greeter  # type: ignore[import-not-found]


def main():
    params = json.loads(sys.argv[1])
    name = params["name"]

    greeter = Greeter()
    result = greeter.Hello(name)

    print(json.dumps({"result": result}, ensure_ascii=False))


if __name__ == "__main__":
    main()
