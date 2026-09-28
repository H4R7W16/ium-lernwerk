const areas=[
 {id:'lernstudio',label:'Algorithmen'},
 {id:'medienanalyse',label:'Medienanalyse'},
 {id:'quellenquest',label:'Quellenquest'}
];
function inject(html,active){
 if(!areas.some(area=>area.id===active))throw new Error('Unknown learning area: '+active);
 if(!html.includes('</head>')||!html.includes('<header class="topbar">'))throw new Error('Missing navigation insertion point: '+active);
 const links=areas.map(area=>'<a href="../'+area.id+'/index.html"'+(area.id===active?' aria-current="true"':'')+'>'+area.label+'</a>').join('');
 const nav='<nav class="lw-switcher" aria-label="Lernbereiche"><div class="lw-switcher__inner"><span class="lw-switcher__label">IuM · Klasse 5</span><div class="lw-switcher__links">'+links+'</div></div></nav>';
 return html.replace('</head>','<link rel="stylesheet" href="../prototype-navigation.css"></head>').replace('<header class="topbar">',nav+'<header class="topbar">');
}
module.exports={inject};

