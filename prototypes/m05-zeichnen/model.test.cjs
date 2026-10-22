'use strict';
const {test}=require('node:test'),a=require('node:assert/strict');
const M=require('./model.js');
test('feste Wiederholung erzeugt Treppe und Zeilenspur',()=>{const r=M.run('wiederhole 3 [\nvor rechts vor links\n]');a.equal(r.error,null);a.deepEqual([r.end.x,r.end.y,r.end.dir],[4,4,0]);a.equal(r.end.lines.length,6);a.equal(r.actions[8].iteration,3);a.equal(r.actions[8].line,2);});
test('rechts dreht am Ort und hoch bewegt ohne Linie',()=>{const r=M.run('rechts vor hoch links vor runter vor');a.deepEqual([r.end.x,r.end.y,r.end.dir,r.end.pen],[3,2,0,true]);a.equal(r.end.lines.length,2);a.deepEqual(r.trace[1].lines,[]);});
test('falsche Syntax, Verschachtelung und Überlast werden abgelehnt',()=>{for(const s of ['', 'vor();','wiederhole 0 [vor]','wiederhole 2 []','wiederhole 2 [vor','wiederhole 2 [wiederhole 2 [vor]]','vor ]','wiederhole 9 [vor vor vor vor vor vor vor vor vor vor vor vor vor vor vor vor vor vor vor vor vor vor vor]'])a.throws(()=>M.parse(s));});
test('Rastergrenze stoppt vor ungültiger Bewegung',()=>{const r=M.run('links wiederhole 3 [vor]');a.equal(r.error.step,3);a.deepEqual([r.end.x,r.end.y],[1,0]);a.equal(r.end.lines.length,1);});
test('Neustart deterministisch und Zustände getrennt',()=>{const r=M.run('vor rechts vor');r.end.lines.push([9,9,9,9]);a.equal(r.trace[1].lines.length,1);a.deepEqual(M.run('vor').end.lines,[[1,1,2,1]]);});
test('Protokoll bewahrt Vorversionen ohne Abschneiden',()=>{a.equal(M.appendRecord('alt','neu'),'neu\n\nFrüherer Versuch / eigene Notizen:\nalt');a.throws(()=>M.appendRecord('x'.repeat(9990),'neu'.repeat(20)),/voll/);});
