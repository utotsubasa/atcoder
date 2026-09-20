"""指定ファイルの Solver を stdin/stdout で実行するサブプロセス用エントリ。"""

import importlib.util
import sys
from pathlib import Path


def main() -> None:
    path = Path(sys.argv[1])
    spec = importlib.util.spec_from_file_location("solution", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    solver = module.Solver()
    solver.input()
    solver.solve()
    solver.output()


if __name__ == "__main__":
    main()
