import json
import sys
import os

import clr

# DLL のパスを解決
dll_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "..", "bin")
dll_path = os.path.normpath(dll_dir)
sys.path.append(dll_path)
clr.AddReference("SampleLib")  # type: ignore[attr-defined]

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
