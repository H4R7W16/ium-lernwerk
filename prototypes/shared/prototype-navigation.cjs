const areas=[
 {id:'lernstudio',label:'Algorithmen',title:'Sauber geplant',description:'Befehle erproben und eigene Abläufe entwickeln.',number:'01'},
 {id:'medienanalyse',label:'Bilder und ihre Wirkung',title:'Ein Bild – zwei Geschichten',description:'Bildausschnitte untersuchen und Beiträge gestalten.',number:'02'},
 {id:'quellenquest',label:'Quellen prüfen',title:'Was wird aus unserer Pausenwiese?',description:'Nachrichten untersuchen und mit Belegen antworten.',number:'03'}
];
function inject(html,active,file='index.html'){
 const area=areas.find(a=>a.id===active);
 if(!area)throw new Error('Unknown learning area: '+active);
 const old=html.match(/<header class="topbar">[\s\S]*?<\/header>/);
 if(!html.includes('</head>')||!old)throw new Error('Missing navigation insertion point: '+active);
 const localTools=(old[0].match(/<button\b[\s\S]*?<\/button>/g)||[]).join('');
 const cards=areas.map(a=>`<a href="../${a.id}/index.html"${a.id===active?' aria-current="true"':''}><span class="lw-topic-number" aria-hidden="true">${a.number}</span><span><strong>${a.label}</strong><span>${a.title}</span><small>${a.description}</small>${a.id===active?'<em>Hier bist du</em>':''}</span></a>`).join('');
 const materials=active==='lernstudio'?'lehrkraft.html':'material.html';
 const page=file.split('/').pop(),supportTarget=page==='index.html'?' target="_blank" rel="noopener"':'',supportMark=page==='index.html'?' <span aria-hidden="true">↗</span>':'';
 const header=`<header class="lw-header"><div class="lw-identity"><span class="lw-brand">Lernwerk<span aria-hidden="true">.</span></span><a class="lw-location" href="index.html"><span>Klasse 5</span><b>${area.label}</b></a></div><nav class="lw-links" aria-label="Lernwerk"><details class="lw-topics" onkeydown="if(event.key==='Escape'){this.open=false;this.querySelector('summary').focus()}"><summary>Themen <span aria-hidden="true">⌄</span></summary><div class="lw-topic-panel"><p class="lw-panel-title">Entdecke das Lernwerk <span>Klasse 5</span></p><div class="lw-topic-list">${cards}</div><p class="lw-panel-note">Wähle ein Thema. Die einzelnen Lernschritte kannst du dort direkt öffnen.</p></div></details><a href="wissen.html"${supportTarget}${page==='wissen.html'?' aria-current="page"':''}>Wissen${supportMark}</a><a href="${materials}"${supportTarget}${page===materials?' aria-current="page"':''}>Unterrichtsmaterial${supportMark}</a>${localTools?'<div class="lw-local-tools" aria-label="Werkzeuge dieser Lerneinheit">'+localTools+'</div>':''}</nav></header>`;
 return html.replace('</head>','<link rel="stylesheet" href="../prototype-navigation.css"></head>').replace(old[0],header);
}
module.exports={inject};
