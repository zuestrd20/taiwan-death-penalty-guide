(function(root){
'use strict';
function normalizeRange(start,end){const a=Math.max(1996,Math.min(2025,Number(start)));const b=Math.max(1996,Math.min(2025,Number(end)));return a<=b?[a,b]:[b,a];}
function filterAnnual(rows,start,end){const [a,b]=normalizeRange(start,end);return rows.filter(r=>r.period_type==='full_year'&&r.year>=a&&r.year<=b);}
function summarize(rows){return {total:rows.reduce((s,r)=>s+r.executions,0),years:rows.length,average:rows.length?rows.reduce((s,r)=>s+r.executions,0)/rows.length:null};}
function filterGlobal(rows,mode){return rows.filter(r=>mode==='all'||(mode==='unknown'?r.numeric_recorded===null:r.numeric_recorded!==null));}
function searchMatch(text,query){return query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean).every(q=>text.toLocaleLowerCase().includes(q));}
function periodSegments(periods,start,end){const min=Date.UTC(start,0,1),max=Date.UTC(end+1,0,1),span=max-min;return periods.map(p=>{const a=Math.max(min,Date.parse(p.observed_start_inclusive)),b=Math.min(max,Date.parse(p.observed_end_exclusive));return {...p,left:(a-min)/span*100,width:(b-a)/span*100};}).filter(p=>p.width>0);}
const api={normalizeRange,filterAnnual,summarize,filterGlobal,searchMatch,periodSegments};if(typeof module!=='undefined'&&module.exports)module.exports=api;root.ResearchLogic=api;
})(typeof window==='undefined'?globalThis:window);
