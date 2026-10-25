'use strict';
const $ = (id) => document.getElementById(id);
const files = {entries:'./data/entries.json', sources:'./data/sources.json',updates:'./data/updates.json'};
let entries=[],sources=[],updates=[],category='Tất cả';
const text = (s) => String(s ?? '');
const el = (tag, cls, content) => {const node=document.createElement(tag);if(cls)node.className=cls;if(content!==undefined)node.textContent=text(content);return node;};
const LEVELS={A:'A · Chính thức',B:'B · Có cơ sở',C:'C · Chưa xác nhận'};
function entryCard(item){
 const card=el('article','entry'),top=el('div','entry-top');top.append(el('span','kind',item.category));
 const badge=el('span','level level-'+text(item.level).toLowerCase(),LEVELS[item.level]||'Cần kiểm tra');top.append(badge);card.append(top);
 card.append(el('h3','',item.hv||item.en||'Chưa đặt tên'));
 card.append(el('div','aliases',[item.zh,item.en].filter(Boolean).join('  ·  ')));
 card.append(el('p','',item.description));
 const src=el('div','sources-line');const link=el('a','','Xem nguồn và kiểm chứng ↗');link.href=item.source_url||'#';link.target='_blank';link.rel='noopener noreferrer';src.append(link);card.append(src);return card;
}
function renderEntries(){
 const q=$('query').value.trim().toLocaleLowerCase('vi');const items=entries.filter(e=> (category==='Tất cả'||e.category===category)&&[e.hv,e.zh,e.en,e.description].join(' ').toLocaleLowerCase('vi').includes(q));
 const library=$('library');library.replaceChildren(...items.map(entryCard));$('empty').hidden=items.length>0;$('result-count').textContent=`${items.length} mục`;
}
function makeFilters(){const cats=['Tất cả',...new Set(entries.map(e=>e.category))];const parent=$('filters');for(const c of cats){const b=el('button','',c);b.type='button';b.setAttribute('aria-pressed',String(c===category));b.addEventListener('click',()=>{category=c;for(const n of parent.children)n.setAttribute('aria-pressed',String(n.textContent===c));renderEntries()});parent.append(b)}}
function renderSources(){const frag=[];for(const s of sources){const item=el('article','');item.append(el('strong','',s.name+' · '+s.type));item.append(el('p','',s.note));const a=el('a','','Mở nguồn ↗');a.href=s.url;a.rel='noopener noreferrer';a.target='_blank';item.append(a);frag.push(item)}$('sources').replaceChildren(...frag)}
function renderUpdates(){const frag=[];for(const u of [...updates].reverse()){const box=el('article','');box.append(el('strong','',u.title||'Nguồn thay đổi'));box.append(el('p','',`Phát hiện: ${u.detected_at||'không rõ'} · ${u.status||'Chờ biên tập'}`));const a=el('a','','Đọc nội dung tại nguồn ↗');a.href=u.url;a.rel='noopener noreferrer';a.target='_blank';box.append(a);frag.push(box)}if(!frag.length){const n=el('article','');n.append(el('strong','','Chưa có thay đổi được ghi nhận'));n.append(el('p','','Trình theo dõi sẽ tạo lịch sử sau khi GitHub Actions hoạt động. Lần chạy đầu tiên chỉ lưu mốc để so sánh.'));frag.push(n)}$('updates').replaceChildren(...frag)}
function showSection(){const hash=location.hash.replace('#','')||'tong-quan';const valid=['tong-quan','thu-vien','cap-nhat','nguon','bien-tap'];const selected=valid.includes(hash)?hash:'tong-quan';for(const id of valid)$(id).hidden=id!==selected;for(const link of document.querySelectorAll('[data-nav]'))link.classList.toggle('active',link.dataset.nav===selected)}
async function readJson(path){const resp=await fetch(path,{cache:'no-store'});if(!resp.ok)throw new Error(path+' '+resp.status);return await resp.json()}
(async function init(){try{[entries,sources,updates]=await Promise.all([readJson(files.entries),readJson(files.sources),readJson(files.updates)]);$('stat-entries').textContent=entries.length;$('stat-sources').textContent=sources.length;$('stat-updates').textContent=updates.length;$('featured').replaceChildren(...entries.slice(0,4).map(entryCard));makeFilters();renderEntries();renderSources();renderUpdates();$('query').addEventListener('input',renderEntries)}catch(e){console.error(e);$('featured').append(el('p','empty','Không tải được dữ liệu. Hãy mở website qua GitHub Pages, không mở trực tiếp file index.html.'))}showSection();window.addEventListener('hashchange',showSection)})();
