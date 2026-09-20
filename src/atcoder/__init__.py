import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

TEMPLATE = '''class Solver:
    def input(self):
        pass

    def solve(self):
        pass

    def output(self):
        pass


if __name__ == "__main__":
    s = Solver()
    s.input()
    s.solve()
    s.output()
'''


def main() -> None:
    if len(sys.argv) != 4:
        print("使い方: atcoder <コンテスト種別> <コンテスト番号> <問題番号>", file=sys.stderr)
        print("例:     atcoder abc 476 b", file=sys.stderr)
        sys.exit(2)
    kind, number, prob = sys.argv[1:]
    path = ROOT / kind / number / f"{prob}.py"
    rel = path.relative_to(ROOT)
    if path.exists():
        print(f"既に存在します: {rel}", file=sys.stderr)
        sys.exit(1)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(TEMPLATE)
    print(f"作成しました: {rel}")
