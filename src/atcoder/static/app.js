const $ = (id) => document.getElementById(id);
const kindEl = $("kind");
const numberEl = $("number");
const problemEl = $("problem");
const inputEl = $("input");
const runEl = $("run");
const spinnerEl = runEl.querySelector(".spinner");

let tree = {}; // ローカルの解答ファイル {kind: {number: [probs]}}

const values = () => ({
  kind: kindEl.value.trim(),
  number: numberEl.value.trim(),
  prob: problemEl.value.trim(),
});

const currentPath = () => {
  const { kind, number, prob } = values();
  return `${kind}/${number}/${prob}.py`;
};

const filled = () => Object.values(values()).every((v) => v !== "");

const exists = () => {
  const { kind, number, prob } = values();
  return tree[kind]?.[number]?.includes(prob) ?? false;
};

const refresh = () => {
  $("path").textContent = filled() ? currentPath() : "コンテスト情報を入力してください";
  $("run-label").textContent = exists() ? "実行" : "テンプレート作成";
  runEl.disabled = !filled();
};

for (const el of [kindEl, numberEl, problemEl]) {
  el.addEventListener("input", refresh);
}

const showResult = (r) => {
  $("result").hidden = false;
  const status = $("status");
  if (r.error != null) {
    status.textContent = "エラー";
    status.className = "badge ng";
    $("stdout").textContent = r.error;
  } else if (r.created != null) {
    status.textContent = "作成";
    status.className = "badge ok";
    $("stdout").textContent =
      `テンプレートを作成しました: ${r.created}\nエディタで実装してから実行してください`;
  } else {
    const ok = r.returncode === 0;
    status.textContent = ok ? "成功" : `終了コード ${r.returncode}`;
    status.className = `badge ${ok ? "ok" : "ng"}`;
    $("stdout").textContent = r.stdout;
  }
  $("stderr-field").hidden = !r.stderr;
  $("stderr").textContent = r.stderr ?? "";
};

const run = async () => {
  if (!filled()) return;
  runEl.disabled = true;
  spinnerEl.hidden = false;
  const creating = !exists();
  try {
    const res = await fetch(creating ? "/create" : "/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ file: currentPath(), input: inputEl.value }),
    });
    const r = await res.json();
    if (creating && r.created != null) {
      const { kind, number, prob } = values();
      ((tree[kind] ??= {})[number] ??= []).push(prob);
    }
    showResult(r);
  } catch (e) {
    showResult({ error: `サーバーに接続できません: ${e.message}` });
  } finally {
    runEl.disabled = false;
    spinnerEl.hidden = true;
    refresh();
  }
};

runEl.addEventListener("click", run);
document.addEventListener("keydown", (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === "Enter" && !runEl.disabled) run();
});

const { tree: t } = await (await fetch("/files")).json();
tree = t;
refresh();
