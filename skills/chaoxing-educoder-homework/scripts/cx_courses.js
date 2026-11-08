#!/usr/bin/env node
// 列出学习通全部课程（courseid / clazzid / cpi / 课程名 / 班级 / 教师）
// 用法: node cx_courses.js [state.json 路径]
// 默认读 C:/Users/18032/chaoxing-helper/state.json，结果写到同目录 mycourses.json + courses_table.json
const fs = require('fs');
const path = require('path');

const HELPER = 'C:/Users/18032/chaoxing-helper';
const statePath = process.argv[2] || path.join(HELPER, 'state.json');
const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));
const cookie = state.cookies.map(c => `${c.name}=${c.value}`).join('; ');
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36';

(async () => {
  const r = await fetch('https://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1', {
    headers: { Cookie: cookie, 'User-Agent': UA, Referer: 'https://i.chaoxing.com/' },
  });
  if (!r.ok) { console.error('HTTP', r.status, '（cookie 过期？跑 login.js）'); process.exit(1); }
  const j = await r.json();
  const rows = (j.channelList || []).map(c => {
    const ct = c.content || {};
    const d = ((ct.course || {}).data || [{}])[0] || {};
    return { course: d.name, classname: ct.name, courseid: d.id, clazzid: c.key || ct.id, cpi: c.cpi || ct.cpi, teacher: d.teacherfactor };
  });
  const outDir = path.dirname(statePath);
  fs.writeFileSync(path.join(outDir, 'mycourses.json'), JSON.stringify(j, null, 1), 'utf8');
  fs.writeFileSync(path.join(outDir, 'courses_table.json'), JSON.stringify(rows, null, 1), 'utf8');
  rows.forEach(r2 => console.log(`${r2.courseid}\t${r2.clazzid}\t${r2.cpi}\t${r2.course}\t${r2.classname}\t${r2.teacher}`));
  console.log(`\n共 ${rows.length} 门课 → ${outDir}\\courses_table.json`);
})();
