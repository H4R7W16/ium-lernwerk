'use strict';
const test=require('node:test'), assert=require('node:assert/strict'), fs=require('node:fs'), path=require('node:path');
const P=require('./snap-project-model.js');
const now='2026-11-06T10:00:00.000Z';
const project=xml=>({format:'snap-project',version:1,filename:'Eigener_Rover.xml',savedAt:now,xml});
test('accepts actual ALG-5 starter and own program with escaped text, comments and scene structure',()=>{
 const real=fs.readFileSync(path.join(__dirname,'../klasse7-programmieren/inhalt/klasse7/programmieren/projekte/ALG-5-Start.xml'),'utf8');
 assert.equal(P.validateProject(project(real)).ok,true);
 assert.equal(P.validateProject(project('<?xml version="1.0"?><project><!-- note --><scenes><scene><stage><notes>A &amp; B &#228; <![CDATA[<work>]]></notes></stage></scene></scenes></project>')).ok,true);
});
test('rejects malformed, entity-bearing, incomplete and non-project XML without claiming program correctness',()=>{
 for(const xml of ['<project><stage></project>','<project><stage/></project><other/>','<project><notes>missing stage</notes></project>','<!DOCTYPE project [<!ENTITY x SYSTEM "file:///secret">]><project><stage/></project>','<project><stage>&unknown;</stage></project>','<project a="1" a="2"><stage/></project>','<project><stage x="bad<value"/></project>','<project><stage>&#0;</stage></project>','<project><stage/></project>junk','<project><notes><stage/></notes></project>'])assert.equal(P.validateProject(project(xml)).ok,false,xml);
});
test('validates filename and UTF-8 project byte limit',()=>{
 assert.equal(P.validateProject({...project('<project><stage/></project>'),filename:'a/../../b.xml'}).ok,false);
 assert.equal(P.validateProject({...project('<project><stage/></project>'),filename:'Rover.json'}).ok,false);
 assert.equal(P.validateProject(project('<project><stage>'+('ä'.repeat(P.MAX_PROJECT_BYTES/2))+'</stage></project>')).ok,false);
});

test('rejects malformed XML declarations and comments that XML parsers reject',()=>{
 for(const xml of ['<?xml bogus="x"?><project><stage/></project>','<?xml version="3.0"?><project><stage/></project>','<project><!--a---><stage/></project>']) assert.equal(P.validateProject(project(xml)).ok,false,xml);
});
test('accepts all shipped Snap project XML and preserves Unicode XML without normalization',()=>{
 const base=path.join(__dirname,'../klasse7-programmieren/inhalt/klasse7/programmieren');
 for(const folder of ['projekte','lehrpersonen']) for(const file of fs.readdirSync(path.join(base,folder)).filter(f=>f.endsWith('.xml'))){const xml=fs.readFileSync(path.join(base,folder,file),'utf8');const result=P.validateProject(project(xml));assert.equal(result.ok,true,file+': '+result.error);assert.equal(result.project.xml,xml);}
 const xml='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><project name="Ärger &amp; Spaß 😀"><stage><notes>é &#x1F680; <![CDATA[<eigene Notiz>]]></notes></stage></project>';
 assert.equal(P.validateProject(project(xml)).project.xml,xml);
 assert.equal(P.validateProject(project('<project><stage>\ud800</stage></project>')).ok,false);
});
