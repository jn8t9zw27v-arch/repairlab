(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.RepairCore=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
 'use strict';
 const seed=[
  {id:'A101',service:'Dental check',day:'Tuesday',date:'2026-12-01',time:'09:30',aliases:['dental','dentist','teeth','tooth','tuesday','december 1','1 december'],status:'active'},
  {id:'A102',service:'Eye appointment',day:'Thursday',date:'2026-12-03',time:'14:00',aliases:['eye','optician','thursday','december 3','3 december'],status:'active'},
  {id:'A103',service:'Physiotherapy',day:'Friday',date:'2026-12-04',time:'11:15',aliases:['physio','physiotherapy','friday','december 4','4 december'],status:'active'}
 ];
 function create(strategy='options',limit=3){return {strategy,limit,records:JSON.parse(JSON.stringify(seed)),phase:'idle',pending:null,candidates:[],lastAction:null,events:[]};}
 function log(s,type,detail){s.events.push({step:s.events.length+1,type,detail});}
 function say(s,text){log(s,'response',text);return text;}
 function preview(s,r){s.phase='preview';s.pending=r.id;s.candidates=[];log(s,'preview',r.id);return say(s,`I understood: cancel ${r.service}, ${r.day} ${r.date} at ${r.time} (${r.id}). Nothing has changed. Confirm below, or go back to correct it.`);}
 function input(s,raw){
  const t=String(raw).trim().toLowerCase();log(s,'input',String(raw));
  if(!t)return say(s,'Please enter a request.');
  if(s.phase==='preview')return say(s,'A cancellation is awaiting review. Go back to correct it, confirm it, or stop the request.');
  if(s.phase==='done')s.phase='idle';
  if(/\b(book|reschedule|move|email|send|pay)\b/.test(t))return say(s,'This prototype only cancels fictional appointments. Booking, rescheduling and external actions are not available. Your records have not changed.');
  const active=s.records.filter(r=>r.status==='active');
  const allMatches=s.records.filter(r=>t.includes(r.id.toLowerCase())||t.includes(r.date)||r.aliases.some(a=>new RegExp('\\b'+a+'\\b').test(t)));
  const matches=allMatches.filter(r=>r.status==='active');
  if(matches.length===1)return preview(s,matches[0]);
  if(allMatches.length&&matches.length===0)return say(s,'That appointment is already cancelled. You can undo the most recent cancellation if it is the one you need.');
  if(!active.length)return say(s,'There are no active appointments to cancel.');
  if(/\b(monday|wednesday|saturday|sunday|surgery|cardiology|hospital)\b/.test(t))return say(s,'I cannot match that description to an active record. Please use a service, date or appointment ID from the schedule. Nothing has changed.');
  if(!/\b(cancel|appointment|booking)\b/.test(t)&&s.phase!=='repair')return say(s,'I can help cancel a fictional appointment. Try “Cancel my appointment” or name its service, date or ID.');
  if(active.length===1)return preview(s,active[0]);
  s.phase='repair';s.pending=null;
  if(s.strategy==='repeat'){s.candidates=[];return say(s,'I did not understand which appointment you mean. Please say your request again.');}
  if(s.strategy==='targeted'){s.candidates=[];return say(s,'Which appointment do you want to cancel? Please give its service, date or ID.');}
  const source=matches.length>1?matches:active;
  s.candidates=source.slice(0,s.limit).map(r=>r.id);
  return say(s,`I found more than one possible appointment. Select the one you mean, or choose “None of these” and describe it. Showing ${s.candidates.length} of ${source.length} possible records.`);
 }
 function choose(s,id){
  log(s,'choose',id);
  if(s.phase!=='repair'||!s.candidates.includes(id))return say(s,'That is not a current candidate. Please describe the appointment instead.');
  const r=s.records.find(x=>x.id===id&&x.status==='active');
  if(!r)return say(s,'This record is no longer active. Please start again.');
  return preview(s,r);
 }
 function reject(s){log(s,'reject_candidates',s.candidates.slice());s.candidates=[];s.pending=null;s.phase='repair';return say(s,'None of these matches your intention. Please give the service, date or ID you meant. You do not have to choose a listed option.');}
 function back(s){log(s,'correct',s.pending);s.pending=null;s.candidates=[];s.phase='repair';return say(s,'The proposed cancellation was discarded. Which service, date or ID did you mean? Nothing has changed.');}
 function stop(s){log(s,'stop',s.pending);s.pending=null;s.candidates=[];s.phase='idle';return say(s,'Request stopped. No pending cancellation was applied.');}
 function confirm(s){
  if(s.phase!=='preview'||!s.pending)return say(s,'There is no cancellation ready to confirm.');
  const r=s.records.find(x=>x.id===s.pending&&x.status==='active');
  if(!r){s.phase='idle';s.pending=null;return say(s,'The record changed. Please identify the appointment again.');}
  r.status='cancelled';s.lastAction=r.id;s.pending=null;s.phase='done';log(s,'cancelled',r.id);
  return say(s,`Cancelled ${r.service} (${r.id}) in this local simulation only. No real provider was contacted. You can undo this change.`);
 }
 function undo(s){
  const r=s.records.find(x=>x.id===s.lastAction&&x.status==='cancelled');
  if(!r)return say(s,'There is no recent cancellation to undo.');
  r.status='active';s.lastAction=null;s.pending=null;s.candidates=[];s.phase='idle';log(s,'undo',r.id);
  return say(s,`Restored ${r.service} (${r.id}). It is active again in the local simulation.`);
 }
 return {seed,create,input,choose,reject,back,stop,confirm,undo};
});
