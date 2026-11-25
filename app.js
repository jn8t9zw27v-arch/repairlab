'use strict';
const C=window.RepairCore,$=id=>document.getElementById(id);
let session=C.create();
function bubble(text,role='system'){const p=document.createElement('div');p.className='message '+role;const name=document.createElement('span');name.className='speaker';name.textContent=role==='user'?'YOU':'ASSISTANT';p.append(name,document.createTextNode(text));$('messages').append(p);$('messages').scrollTop=$('messages').scrollHeight;}
function button(text,fn,cls=''){const b=document.createElement('button');b.type='button';b.textContent=text;b.className=cls;b.onclick=fn;return b;}
function act(fn){bubble(fn(session));render();}
function render(){
 $('records').replaceChildren();
 for(const r of session.records){const card=document.createElement('article');card.className='record '+r.status;const h=document.createElement('h3');h.textContent=r.service;const date=document.createElement('p');date.textContent=`${r.day} · ${r.date}`;const time=document.createElement('p');time.textContent=r.time;const meta=document.createElement('div');meta.className='meta';const id=document.createElement('span');id.textContent=r.id;const status=document.createElement('span');status.className='status-'+r.status;status.textContent=r.status==='active'?'Active':'Cancelled';meta.append(id,status);card.append(h,date,time,meta);$('records').append(card);}
 $('active-count').textContent=session.records.filter(r=>r.status==='active').length+' active';
 $('state').textContent={idle:'Ready',repair:'Clarification needed',preview:'Awaiting confirmation',done:'Completed'}[session.phase];
 $('actions').replaceChildren();
 if(session.phase==='repair'&&session.candidates.length){for(const id of session.candidates){const r=session.records.find(r=>r.id===id);$('actions').append(button(`${r.service} · ${r.day} ${r.time}`,()=>{bubble(`I mean ${r.service} (${id}).`,'user');act(s=>C.choose(s,id));},'candidate'));}$('actions').append(button('None of these — describe another appointment',()=>act(C.reject),'reject'));}
 if(session.phase==='preview'){$('actions').append(button('Confirm cancellation',()=>act(C.confirm)),button('Go back and correct',()=>act(C.back),'quiet'));}
 if(session.lastAction)$('actions').append(button('Undo last cancellation',()=>act(C.undo),'quiet'));
 $('request').disabled=session.phase==='preview';$('request').placeholder=session.phase==='preview'?'Review the proposed cancellation above':'For example: Cancel my appointment';
 $('events').replaceChildren();for(const e of session.events){const li=document.createElement('li');li.textContent=e.type+': '+(typeof e.detail==='string'?e.detail:JSON.stringify(e.detail));$('events').append(li);}$('event-count').textContent=`(${session.events.length})`;
}
function reset(){session=C.create(document.querySelector('input[name=strategy]:checked').value,Number($('coverage').value));$('messages').replaceChildren();bubble('I can help cancel a fictional appointment. Tell me which one, or try an ambiguous request. I will show my interpretation before changing any record.');render();}
function submit(text){if(!text.trim())return;bubble(text,'user');act(s=>C.input(s,text));$('request').value='';$('request').focus();}
$('request-form').onsubmit=e=>{e.preventDefault();submit($('request').value);};
$('reset').onclick=reset;$('stop').onclick=()=>act(C.stop);
for(const e of document.querySelectorAll('input[name=strategy]'))e.onchange=reset;
$('coverage').onchange=reset;
for(const e of document.querySelectorAll('[data-request]'))e.onclick=()=>submit(e.dataset.request);
$('omitted').onclick=()=>{document.querySelector('input[value=options]').checked=true;$('coverage').value='2';reset();bubble('Omission demo: imagine you intend to cancel Friday physiotherapy. The first suggestion list will deliberately omit it. Use “None of these” to repair.');submit('Cancel my appointment');};
$('export').onclick=()=>{const payload={prototype:'RepairLab',interpretation:'deterministic rules',strategy:session.strategy,candidateLimit:session.limit,events:session.events,records:session.records};const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='repairlab-session.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
reset();
