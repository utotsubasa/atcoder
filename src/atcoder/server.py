import json
import mimetypes
import os
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# どこから起動しても解答ファイルを見つけられるよう、cwd ではなくリポジトリルートを使う
ROOT = Path(__file__).resolve().parents[2]
WATCH_DIR = Path(__file__).parent
STATIC_DIR = Path(__file__).parent / "static"
TIMEOUT_SEC = 10
EXCLUDED_DIRS = {".git", ".venv", "src", "__pycache__"}

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



def list_solution_tree() -> dict:
    """ローカルの解答ファイルから {コンテスト種別: {コンテスト番号: [問題番号]}} を返す。"""
    tree: dict[str, dict[str, list[str]]] = {}
    for p in sorted(ROOT.glob("*/*/*.py")):
        kind, number = p.parts[-3], p.parts[-2]
        if kind in EXCLUDED_DIRS:
            continue
        tree.setdefault(kind, {}).setdefault(number, []).append(p.stem)
    return tree


def create_solution(file: str) -> dict:
    path = (ROOT / file).resolve()
    if not path.is_relative_to(ROOT) or path.suffix != ".py":
        return {"error": f"作成できないパスです: {file}"}
    if path.exists():
        return {"error": f"既に存在します: {file}"}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(TEMPLATE)
    return {"created": file}


def run_solver(file: str, input_text: str) -> dict:
    path = (ROOT / file).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        return {"error": f"ファイルが見つかりません: {file}"}
    runner = Path(__file__).with_name("runner.py")
    try:
        proc = subprocess.run(
            [sys.executable, str(runner), str(path)],
            input=input_text,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SEC,
        )
    except subprocess.TimeoutExpired:
        return {"error": f"{TIMEOUT_SEC}秒でタイムアウトしました"}
    return {"stdout": proc.stdout, "stderr": proc.stderr, "returncode": proc.returncode}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/files":
            self._send_json({"tree": list_solution_tree()})
        else:
            self._serve_static("index.html" if self.path == "/" else self.path)

    def _serve_static(self, name: str) -> None:
        path = (STATIC_DIR / name.lstrip("/")).resolve()
        if not path.is_relative_to(STATIC_DIR) or not path.is_file():
            self._send(404, b"Not Found", "text/plain")
            return
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self._send(200, path.read_bytes(), f"{ctype}; charset=utf-8")

    def do_POST(self) -> None:
        if self.path not in ("/run", "/create"):
            self._send(404, b"Not Found", "text/plain")
            return
        length = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(length))
        except json.JSONDecodeError:
            self._send_json({"error": "リクエストボディが不正です"})
            return
        file = body.get("file", "")
        if self.path == "/run":
            self._send_json(run_solver(file, body.get("input", "")))
        else:
            self._send_json(create_solution(file))

    def _send_json(self, payload: dict) -> None:
        self._send(200, json.dumps(payload).encode(), "application/json")

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_) -> None:
        pass


def _watch_and_restart() -> None:
    def snapshot() -> dict[Path, float]:
        return {p: p.stat().st_mtime for p in WATCH_DIR.glob("*.py")}

    before = snapshot()
    while True:
        time.sleep(1)
        if snapshot() != before:
            print("アプリの変更を検知したため再起動します", flush=True)
            os.execv(sys.executable, [sys.executable, "-m", "atcoder", *sys.argv[1:]])


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    threading.Thread(target=_watch_and_restart, daemon=True).start()
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"http://localhost:{port} で起動しました (Ctrl+C で停止)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
