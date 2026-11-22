// 中古スマホ判断シミュレーター（フェーズ2・暫定版）
// データ源：data/smartphones.json のみ。価格・仕様は推測で作らない。
// 価格が確認済みの機種は Xiaomi 13T（中古29,800円〜）だけ。
// コスパ版は「7万円以下」、フラッグシップ版は「10万円以上」という
// カテゴリ定義だけが分かっている。個別の価格・ストレージ・FeliCa・
// バッテリーの仕様は smartphones.json に入っていないため、
// 暫定版ではその3条件で絞り込みはしない（結果に明記する）。
// povo対応は条件に含めない。
"use strict";

let phoneData = null;

async function loadPhones() {
  const res = await fetch("data/smartphones.json");
  if (!res.ok) throw new Error("smartphones.json が読み込めませんでした");
  phoneData = await res.json();
}

function esc(s) {
  return String(s).replace(/[&<>\"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

function runSimulator() {
  const out = document.getElementById("sim-result");
  if (!out) return;
  if (!phoneData) {
    out.innerHTML = '<p class="note">データを読み込み中です。もう一度押してください。</p>';
    return;
  }
  const budget = Number(document.getElementById("sim-budget").value);
  const storage = document.getElementById("sim-storage").value;
  const felica = document.getElementById("sim-felica").value;
  const battery = document.getElementById("sim-battery").value;

  const cost = phoneData.cost_performance.ranking;
  const flagship = phoneData.flagship.ranking;
  let picks = [];
  let head = "";

  if (budget < 29800) {
    head = "<p><strong>該当する機種はありません。</strong></p>" +
      "<p>価格が確認できている一番安い機種は Xiaomi 13T（中古29,800円〜）で、" +
      "予算 " + budget.toLocaleString() + "円では買えません。" +
      "お小遣い3,000円/月なら約10ヶ月分です。貯めてから買うのが現実的です。</p>";
  } else if (budget < 60000) {
    picks = cost.filter((r) => r.name === "Xiaomi 13T");
    head = "<p><strong>予算内で価格が確認できている機種：</strong></p>";
  } else if (budget < 100000) {
    picks = cost;
    head = "<p><strong>コスパ版TOP5（7万円以下のカテゴリ）が候補です。</strong></p>" +
      "<p class=\"note\">ただし個別の価格が確認できているのは Xiaomi 13T（中古29,800円〜）だけで、" +
      "ほかの4機種の価格は未確認です。買う前に中古価格を必ず確認してください。</p>";
  } else {
    picks = flagship.concat(cost);
    head = "<p><strong>フラッグシップ版TOP5（10万円以上のカテゴリ）とコスパ版TOP5の両方が候補です。</strong></p>" +
      "<p class=\"note\">フラッグシップ版は10万円以上なので、学生のお小遣いでは買えません。" +
      "「魅力的。だけど学生には買えません」が結論です。</p>";
  }

  let html = head;
  if (picks.length > 0) {
    html += "<table><thead><tr><th>機種</th><th>価格</th><th>合計</th></tr></thead><tbody>" +
      picks.map((r) =>
        "<tr><td>" + esc(r.name) + "</td><td>" + esc(r.price || "価格未確認") +
        "</td><td class=\"score\">" + r.score + "点</td></tr>").join("") +
      "</tbody></table>";
  }

  // 暫定版の正直な注記：仕様データがない3条件では絞り込めていない
  const asked = [];
  if (storage !== "any") asked.push("ストレージ " + storage);
  if (felica === "must") asked.push("FeliCa必須");
  if (battery === "important") asked.push("バッテリー重視");
  html += "<p class=\"note\">以下は本人が持っていない機種の判断記事であり、実体験レビューではありません。</p>";
  if (asked.length > 0) {
    html += "<p class=\"note\">暫定版の注意：あなたが選んだ「" + esc(asked.join("・")) +
      "」は、批評データに仕様が入っていないため絞り込みに使えていません。" +
      "予算と点数だけで選んでいます。仕様で絞り込めるのは正式版の課題です。</p>";
  } else {
    html += "<p class=\"note\">暫定版の注意：ストレージ・FeliCa・バッテリーの仕様は" +
      "批評データに入っていないため、この結果は予算と点数だけで選んでいます。</p>";
  }
  out.innerHTML = html;
}

document.addEventListener("DOMContentLoaded", async () => {
  try {
    await loadPhones();
  } catch (err) {
    const out = document.getElementById("sim-result");
    if (out) out.innerHTML = '<p class="note">データの読み込みに失敗しました。</p>';
    console.error(err);
  }
  const btn = document.getElementById("sim-run");
  if (btn) btn.addEventListener("click", runSimulator);
});
