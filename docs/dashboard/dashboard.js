// Autor: Carlos Adriano | Data: 25/11/2026
// Snapshot dos indicadores consolidados do RUN-FULL01.
const data=[['P01','Baseline',98.45,97.56,0,2.71,3],['P02','Role',98.95,98.67,3.33,9.01,0],['P03','Estruturado',97.48,97.44,3.33,2.77,0],['P04','Few-shot',97.67,98.33,3.33,8.62,0],['P05','Restrições',98.39,99.33,1.11,2.83,3]];
const fmt=n=>n.toLocaleString('pt-BR',{minimumFractionDigits:2,maximumFractionDigits:2});
const el=id=>document.getElementById(id);
const metrics={sgd:[2,100,'Score global de desempenho','Escala de 0 a 100 pontos'],consistency:[3,100,'Consistência','Percentual de equivalência'],hallucination:[4,5,'Taxa de alucinação','Menor é melhor · escala de 0 a 5%'],p95:[5,10,'Latência P95','Menor é melhor · segundos']};
// Descrição: Atualiza gráfico conforme o indicador selecionado.
function render(){const [i,max,title,note]=metrics[el('metric').value];el('charttitle').textContent=title;el('chartnote').textContent=note;el('bars').innerHTML=data.map(d=>'<div class="barrow"><span>'+d[0]+' '+d[1]+'</span><div class="track"><i style="width:'+d[i]/max*100+'%"></i></div><b>'+fmt(d[i])+'</b></div>').join('')}
el('metric').addEventListener('change',render);render();
el('rows').innerHTML=data.map(d=>'<tr><td><b>'+d[0]+'</b> · '+d[1]+'</td><td>'+fmt(d[2])+'</td><td>'+fmt(d[3])+'%</td><td>'+fmt(d[4])+'%</td><td>'+fmt(d[5])+' s</td><td>Inconclusivo</td></tr>').join('');
el('finance').innerHTML=data.map(d=>'<div class="barrow"><span>'+d[0]+'</span><div class="cells">'+Array.from({length:3},(_,i)=>'<i class="'+(i<d[6]?'':'bad')+'">'+(i<d[6]?'✓':'×')+'</i>').join('')+'</div><b>'+d[6]+'/3</b></div>').join('');
el('theme').addEventListener('click',()=>document.body.classList.toggle('dark'));
const line=(x,y,x2,y2,stroke='currentColor',extra='')=>'<line x1="'+x+'" y1="'+y+'" x2="'+x2+'" y2="'+y2+'" stroke="'+stroke+'" '+extra+'/>';
const txt=(x,y,t,extra='')=>'<text x="'+x+'" y="'+y+'" fill="currentColor" font-size="11" '+extra+'>'+t+'</text>';
const sx=v=>42+v/4*260,sy=v=>190-(v-97)/3*150;
el('scatter').innerHTML=[97,98,99,100].map(v=>line(42,sy(v),302,sy(v),'currentColor','opacity=".13"')+txt(8,sy(v)+4,v+'%')).join('')+[0,1,2,3,4].map(v=>txt(sx(v),208,v+'%','text-anchor="middle"')).join('')+data.map((d,i)=>'<circle cx="'+sx(d[4])+'" cy="'+sy(d[3])+'" r="6" fill="#16877e"/>'+txt(sx(d[4])+(i===3?-27:8),sy(d[3])-8,d[0])).join('')+txt(170,231,'Taxa de alucinação','text-anchor="middle"');
const ci=[['P02',.50,-.66,1.69],['P03',-.98,-2.90,.62],['P04',-.79,-2.11,.37],['P05',-.07,-1.62,1.22]],fx=v=>90+(v+3)*100;
el('forest').innerHTML=[-3,-2,-1,0,1,2].map(v=>line(fx(v),15,fx(v),190,'currentColor',v===0?'stroke-dasharray="4 4" opacity=".7"':'opacity=".12"')+txt(fx(v),215,v,'text-anchor="middle"')).join('')+ci.map((d,i)=>{const y=35+i*44;return txt(20,y+4,d[0])+line(fx(d[2]),y,fx(d[3]),y,'#16877e','stroke-width="4"')+'<circle cx="'+fx(d[1])+'" cy="'+y+'" r="6" fill="#16877e"/>'}).join('');
