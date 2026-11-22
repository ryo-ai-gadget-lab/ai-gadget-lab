// 15歳のAI・ガジェット研究所 — Phase 1 skeleton
// data/*.json を読み込んで表を描画する。数字はJSONだけを直す。
"use strict";

async function loadJson(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(path + " が読み込めませんでした (" + res.status + ")");
  return res.json();
}

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

function scoreCell(score) {
  if (score === null || score === undefined) return '<td class="score">未採点</td>';
  return '<td class="score">' + score + '点<div class="score-bar"><span style="width:' + score + '%"></span></div></td>';
}

function renderAi(data) {
  const el = document.getElementById("ai-ranking");
  if (!el) return;
  const criteria = (data.criteria || []).map((c) =>
    "<li>" + esc(c.name) + " " + c.weight + "</li>").join("");
  const rows = (data.ranking || []).map((r) =>
    "<tr class=\"" + (r.rank === 1 ? "top1" : "") + "\"><td>" + r.rank + "位</td><td>" +
    esc(r.name) + "</td>" + scoreCell(r.score) + "</tr>").join("");
  const special = data.special_frame
    ? '<div class="special"><h3>' + esc(data.special_frame.name) +
      '<span class="tag">' + esc(data.special_frame.note) + '</span></h3><p>' +
      esc(data.special_frame.score) + '点（特別枠）</p></div>'
    : "";
  el.innerHTML =
    '<p class="note">' + esc(data.note || "") + '</p>' +
    '<ul class="criteria">' + criteria + '</ul>' +
    '<table><thead><tr><th>順位</th><th>AI</th><th>合計</th></tr></thead><tbody>' +
    rows + '</tbody></table>' + special;
}

function renderDevices(data) {
  const el = document.getElementById("device-list");
  if (!el) return;
  const rows = (data.devices || []).map((d) => {
    const spec = d.spec ? "（" + esc(d.spec) + "）" : "";
    return "<tr><td>" + esc(d.name) + spec + "</td>" + scoreCell(d.score) + "<td>" + esc(d.note || "") + "</td></tr>";
  }).join("");
  el.innerHTML =
    '<p class="note">' + esc(data.note || "") + '</p>' +
    '<table><thead><tr><th>機種</th><th>満足度</th><th>備考</th></tr></thead><tbody>' +
    rows + '</tbody></table>';
}

function renderPhones(data) {
  const renderList = (section) => {
    if (!section) return "";
    const rows = (section.ranking || []).map((r) =>
      "<tr class=\"" + (r.rank === 1 ? "top1" : "") + "\"><td>" + r.rank + "位</td><td>" +
      esc(r.name) + "</td><td>" + esc(r.price || "—") + "</td>" + scoreCell(r.score) + "</tr>").join("");
    return "<h3>" + esc(section.title) + "</h3><p class=\"note\">" + esc(section.note || "") + "</p>" +
      '<table><thead><tr><th>順位</th><th>機種</th><th>価格</th><th>合計</th></tr></thead><tbody>' +
      rows + "</tbody></table>";
  };
  const el = document.getElementById("phone-list");
  if (!el) return;
  el.innerHTML =
    '<p class="disclaimer">' + esc(data.note || "") + '</p>' +
    renderList(data.flagship) + renderList(data.cost_performance);
}

function showError(err) {
  document.querySelectorAll("[data-loading]").forEach((el) => {
    el.innerHTML = '<p class="note">データの読み込みに失敗しました。' + esc(err.message) + '</p>';
  });
  console.error(err);
}

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const [ai, devices, phones] = await Promise.all([
      loadJson("data/ai_top10.json"),
      loadJson("data/devices.json"),
      loadJson("data/smartphones.json"),
    ]);
    renderAi(ai);
    renderDevices(devices);
    renderPhones(phones);
  } catch (err) {
    showError(err);
  }
});
