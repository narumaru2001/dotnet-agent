import json
import sys
import os

import clr

# DLL のパスを解決
dll_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "..", "bin")
dll_path = os.path.normpath(dll_dir)
sys.path.append(dll_path)
clr.AddReference("SampleLib")  # type: ignore[attr-defined]

from SampleLib import Greeter  # type: ignore[import-not-found]


def main():
    params = json.loads(sys.argv[1])
    name = params["name"]

    greeter = Greeter()
    result = greeter.Hello(name)

    print(json.dumps({"result": result}, ensure_ascii=False))


if __name__ == "__main__":
    main()
