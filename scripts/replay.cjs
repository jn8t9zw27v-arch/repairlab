const fs=require('node:fs');const path=require('node:path');const C=require('../core.js');
const out=path.join(__dirname,'../evidence');fs.mkdirSync(out,{recursive:true});
const cases=[];
function record(name,strategy,limit,steps){const s=C.create(strategy,limit);const frames=[];for(const [action,arg] of steps){const response=arg===undefined?C[action](s):C[action](s,arg);frames.push({action,input:arg??null,response,phase:s.phase,pending:s.pending,candidates:s.candidates.slice(),records:s.records.map(({id,status})=>({id,status}))});}cases.push({name,strategy,limit,frames,events:s.events});}
record('correct candidate','options',3,[['input','Cancel my appointment'],['choose','A101'],['confirm'],['undo']]);
record('omitted intention','options',2,[['input','Cancel my appointment'],['reject'],['input','Friday'],['confirm']]);
record('correct before acting','options',3,[['input','Cancel dental'],['back'],['input','eye'],['confirm']]);
record('general repetition','repeat',3,[['input','Cancel my appointment'],['input','Cancel my appointment'],['input','Friday'],['stop']]);
record('targeted question','targeted',3,[['input','Cancel my appointment'],['input','Friday'],['stop']]);
fs.writeFileSync(path.join(out,'scenario-replays.json'),JSON.stringify({type:'deterministic functional replay, not participant data',cases},null,2));console.log('Wrote five reproducible scenario traces.');
