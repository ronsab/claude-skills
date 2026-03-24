# Canvas Animations Library — לפי תחום עסקי

כל אנימציה היא IIFE עצמאית. החלף `[CANVAS_ID]` לפי ה-id בHTML.
כל canvas צריך: `width:100%;height:100%;display:block` ב-CSS.

---

## אבטחה ומצלמות

### CCTV — מצלמת אבטחה חיה
```javascript
(function() {
  const cv = document.getElementById('[CANVAS_ID]');
  if (!cv) return;
  const ctx = cv.getContext('2d', { willReadFrequently: true });
  function resize() { cv.width = cv.parentElement.clientWidth||400; cv.height = cv.parentElement.clientHeight||150; }
  resize(); window.addEventListener('resize', resize);
  let frame = 0;
  function draw() {
    const w=cv.width, h=cv.height;
    ctx.fillStyle='#030f05'; ctx.fillRect(0,0,w,h);
    for(let y=0;y<h;y+=3){ctx.fillStyle='rgba(0,0,0,0.15)';ctx.fillRect(0,y,w,1);}
    const cx=w/2, cy=h/2;
    ctx.strokeStyle='rgba(0,255,80,0.5)'; ctx.lineWidth=1;
    ctx.strokeRect(cx-40,cy-28,80,56);
    ctx.beginPath();ctx.moveTo(cx-55,cy);ctx.lineTo(cx-42,cy);ctx.stroke();
    ctx.beginPath();ctx.moveTo(cx+42,cy);ctx.lineTo(cx+55,cy);ctx.stroke();
    ctx.beginPath();ctx.moveTo(cx,cy-43);ctx.lineTo(cx,cy-30);ctx.stroke();
    ctx.beginPath();ctx.moveTo(cx,cy+30);ctx.lineTo(cx,cy+43);ctx.stroke();
    const sz=12; ctx.strokeStyle='rgba(0,255,80,0.9)'; ctx.lineWidth=2;
    [[cx-40,cy-28,sz,0,sz,0],[cx+40,cy-28,-sz,0,sz,0],[cx-40,cy+28,sz,0,-sz,0],[cx+40,cy+28,-sz,0,-sz,0]]
      .forEach(([x,y,dx1,dy1,dx2,dy2])=>{
        ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+dx1,y+dy1);ctx.stroke();
        ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+dx2,y+dy2);ctx.stroke();
      });
    const rc=Math.floor(Date.now()/600)%2===0;
    if(rc){ctx.fillStyle='#ff3344';ctx.beginPath();ctx.arc(12,12,4,0,Math.PI*2);ctx.fill();}
    ctx.fillStyle='rgba(0,255,80,0.8)';ctx.font='700 9px Share Tech Mono,monospace';
    ctx.fillText('REC',20,16);
    ctx.textAlign='right';ctx.fillText(new Date().toLocaleTimeString('he-IL'),w-6,16);ctx.textAlign='left';
    ctx.fillStyle='rgba(0,255,80,0.4)';ctx.font='8px Share Tech Mono,monospace';
    ctx.fillText('CAM-01 · LIVE',6,h-7);
    frame++; requestAnimationFrame(draw);
  }
  draw();
})();
```

### RADAR — מערכת אזעקה / סריקה
```javascript
(function() {
  const cv = document.getElementById('[CANVAS_ID]');
  if (!cv) return;
  const ctx = cv.getContext('2d', { willReadFrequently: true });
  function resize() { cv.width = cv.parentElement.clientWidth||400; cv.height = cv.parentElement.clientHeight||150; }
  resize(); window.addEventListener('resize', resize);
  let angle = 0, frame = 0;
  const blips = [];
  function draw() {
    const w=cv.width, h=cv.height;
    const cx=w/2, cy=h/2, r=Math.min(w,h)*0.42;
    ctx.fillStyle='#030f08'; ctx.fillRect(0,0,w,h);
    [.25,.5,.75,1].forEach(f=>{
      ctx.beginPath();ctx.arc(cx,cy,r*f,0,Math.PI*2);
      ctx.strokeStyle='rgba(0,210,80,0.15)';ctx.lineWidth=1;ctx.stroke();
    });
    ctx.strokeStyle='rgba(0,210,80,0.12)';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(cx-r,cy);ctx.lineTo(cx+r,cy);ctx.stroke();
    ctx.beginPath();ctx.moveTo(cx,cy-r);ctx.lineTo(cx,cy+r);ctx.stroke();
    ctx.save();ctx.translate(cx,cy);
    ctx.beginPath();ctx.moveTo(0,0);ctx.arc(0,0,r,angle-1.2,angle);ctx.closePath();
    ctx.fillStyle='rgba(0,210,80,0.1)';ctx.fill();
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(Math.cos(angle)*r,Math.sin(angle)*r);
    ctx.strokeStyle='rgba(0,255,80,0.7)';ctx.lineWidth=2;ctx.stroke();
    ctx.restore();
    if(frame%120===0&&Math.random()>.3) blips.push({x:cx+(Math.random()-.5)*r*1.6,y:cy+(Math.random()-.5)*r*1.6,life:1});
    blips.forEach((b,i)=>{ b.life-=.006; if(b.life<=0){blips.splice(i,1);return;}
      ctx.beginPath();ctx.arc(b.x,b.y,3,0,Math.PI*2);ctx.fillStyle=`rgba(0,255,80,${b.life})`;ctx.fill();
    });
    ctx.fillStyle='rgba(0,210,80,0.6)';ctx.font='9px Share Tech Mono,monospace';
    ctx.fillText('RADAR · ACTIVE',6,h-7);
    angle+=.022; frame++; requestAnimationFrame(draw);
  }
  draw();
})();
```

### ACCESS — בקרת כניסה (לוח מקשים)
```javascript
(function() {
  const cv = document.getElementById('[CANVAS_ID]');
  if (!cv) return;
  const ctx = cv.getContext('2d', { willReadFrequently: true });
  function resize() { cv.width = cv.parentElement.clientWidth||400; cv.height = cv.parentElement.clientHeight||150; }
  resize(); window.addEventListener('resize', resize);
  const SEQ=[1,4,7,2,8,3];let step=0,state='typing',timer=0;
  const KEYS=[[1,2,3],[4,5,6],[7,8,9],['*',0,'#']];
  function draw() {
    const w=cv.width, h=cv.height;
    ctx.fillStyle='#030812'; ctx.fillRect(0,0,w,h);
    const kw=26,kh=18,gap=5,cols=3,rows=4;
    const totalW=cols*(kw+gap)-gap, totalH=rows*(kh+gap)-gap;
    const sx=(w-totalW)/2, sy=h/2-totalH/2-8;
    KEYS.forEach((row,ri)=>row.forEach((k,ci)=>{
      const kx=sx+ci*(kw+gap), ky=sy+ri*(kh+gap);
      const isLit=state==='typing'&&SEQ[step]===k;
      ctx.fillStyle=isLit?'rgba(0,180,255,0.4)':'rgba(0,100,180,0.12)';
      ctx.strokeStyle=isLit?'rgba(0,180,255,0.9)':'rgba(0,100,180,0.25)';
      ctx.lineWidth=1; ctx.beginPath();ctx.roundRect(kx,ky,kw,kh,3);ctx.fill();ctx.stroke();
      ctx.fillStyle=isLit?'#fff':'rgba(200,220,255,0.6)';
      ctx.font=`700 ${isLit?11:10}px Share Tech Mono,monospace`;
      ctx.textAlign='center';ctx.fillText(k,kx+kw/2,ky+kh/2+4);ctx.textAlign='left';
    }));
    for(let i=0;i<SEQ.length;i++){
      ctx.beginPath();ctx.arc((w-SEQ.length*16)/2+i*16+8,sy+totalH+14,4,0,Math.PI*2);
      ctx.fillStyle=i<step?'rgba(0,180,255,.9)':'rgba(0,100,180,.2)';ctx.fill();
    }
    if(state==='granted'||state==='denied'){
      const ok=state==='granted';
      ctx.fillStyle=ok?'rgba(0,255,100,.15)':'rgba(255,50,50,.15)';ctx.fillRect(0,h-22,w,22);
      ctx.fillStyle=ok?'#00ff88':'#ff4455';ctx.font='700 10px Share Tech Mono,monospace';
      ctx.textAlign='center';ctx.fillText(ok?'✓ ACCESS GRANTED':'✗ ACCESS DENIED',w/2,h-8);ctx.textAlign='left';
    }
    timer++;
    if(state==='typing'&&timer%35===0){step++;if(step>=SEQ.length){state='granted';timer=0;}}
    if((state==='granted'||state==='denied')&&timer>80){state='typing';step=0;timer=0;}
    requestAnimationFrame(draw);
  }
  draw();
})();
```

### FACE — זיהוי פנים
```javascript
(function() {
  const cv = document.getElementById('[CANVAS_ID]');
  if (!cv) return;
  const ctx = cv.getContext('2d', { willReadFrequently: true });
  function resize() { cv.width = cv.parentElement.clientWidth||400; cv.height = cv.parentElement.clientHeight||150; }
  resize(); window.addEventListener('resize', resize);
  let scanY=0,matched=false,timer=0;
  const PTS=[[.5,.25],[.35,.38],[.65,.38],[.42,.48],[.58,.48],[.35,.62],[.5,.62],[.65,.62],[.42,.72],[.58,.72],[.5,.78]];
  function draw() {
    const w=cv.width, h=cv.height;
    ctx.fillStyle='#050310'; ctx.fillRect(0,0,w,h);
    const cx=w/2,cy=h*.48,rx=w*.22,ry=h*.4;
    ctx.strokeStyle=matched?'rgba(0,255,100,.5)':'rgba(150,80,255,.35)';
    ctx.lineWidth=1.5; ctx.beginPath();ctx.ellipse(cx,cy,rx,ry,0,0,Math.PI*2);ctx.stroke();
    PTS.forEach(([px,py])=>{
      const lx=cx+(px-.5)*rx*2.2, ly=(cy-ry)+py*ry*2.3;
      ctx.beginPath();ctx.arc(lx,ly,2,0,Math.PI*2);
      ctx.fillStyle=matched?'rgba(0,255,100,.8)':'rgba(180,100,255,.7)';ctx.fill();
    });
    ctx.strokeStyle=matched?'rgba(0,255,100,.12)':'rgba(150,80,255,.1)';ctx.lineWidth=.8;
    for(let i=0;i<PTS.length-1;i++){
      const [ax,ay]=PTS[i],[bx,by]=PTS[i+1];
      ctx.beginPath();ctx.moveTo(cx+(ax-.5)*rx*2.2,(cy-ry)+ay*ry*2.3);
      ctx.lineTo(cx+(bx-.5)*rx*2.2,(cy-ry)+by*ry*2.3);ctx.stroke();
    }
    if(!matched){
      scanY=(scanY+1.5)%(h+20);
      const g=ctx.createLinearGradient(0,scanY-8,0,scanY+8);
      g.addColorStop(0,'rgba(180,80,255,0)');g.addColorStop(.5,'rgba(180,80,255,.3)');g.addColorStop(1,'rgba(180,80,255,0)');
      ctx.fillStyle=g;ctx.fillRect(0,scanY-8,w,16);
    }
    ctx.fillStyle=matched?'#00ff88':'rgba(180,80,255,.8)';
    ctx.font='700 9px Share Tech Mono,monospace';
    ctx.textAlign='center';ctx.fillText(matched?'✓ FACE MATCHED':'SCANNING...',w/2,h-8);ctx.textAlign='left';
    timer++;
    if(timer>200&&!matched){matched=true;timer=0;}
    if(timer>80&&matched){matched=false;timer=0;}
    requestAnimationFrame(draw);
  }
  draw();
})();
```

### GATE — שערים חשמליים
```javascript
(function() {
  const cv = document.getElementById('[CANVAS_ID]');
  if (!cv) return;
  const ctx = cv.getContext('2d', { willReadFrequently: true });
  function resize() { cv.width = cv.parentElement.clientWidth||400; cv.height = cv.parentElement.clientHeight||150; }
  resize(); window.addEventListener('resize', resize);
  const STATES=['CLOSED','OPENING','OPEN','CLOSING'];
  let si=0,st=0,pct=0,frame=0;
  const sparks=[];
  function draw() {
    const w=cv.width, h=cv.height;
    ctx.fillStyle='#03080e'; ctx.fillRect(0,0,w,h);
    ctx.fillStyle='rgba(240,180,41,.7)';ctx.font='700 9px Share Tech Mono,monospace';ctx.fillText('GATE CONTROL',8,15);
    const gW=w*.58,gH=h*.38,gx=(w-gW)/2,gy=h*.28,mid=gx+gW/2,post=8;
    ctx.fillStyle='#1a2a3a';ctx.strokeStyle='rgba(0,170,255,.3)';ctx.lineWidth=1;
    [[gx-post-2,gy-4,post,gH+8],[gx+gW+2,gy-4,post,gH+8]].forEach(([x,y,w2,h2])=>{ctx.fillRect(x,y,w2,h2);ctx.strokeRect(x,y,w2,h2);});
    const hw=(gW/2)*(1-pct*.95);
    [mid-hw,mid].forEach(x=>{
      ctx.fillStyle='rgba(8,20,36,.9)';ctx.strokeStyle='rgba(0,170,255,.5)';ctx.lineWidth=1;
      ctx.fillRect(x,gy,hw,gH);ctx.strokeRect(x,gy,hw,gH);
      for(let i=1;i<=4;i++){const bx=x+(hw/(4+1))*i;ctx.strokeStyle='rgba(0,170,255,.2)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(bx,gy+4);ctx.lineTo(bx,gy+gH-4);ctx.stroke();}
    });
    const state=STATES[si];
    if(state==='OPENING'||state==='CLOSING'){
      if(frame%5===0){[mid-hw,mid+hw].forEach(x=>{ for(let i=0;i<4;i++) sparks.push({x,y:gy+gH/2,vx:(Math.random()-.5)*2.5,vy:(Math.random()-1.5)*2,life:1}); });}
    }
    sparks.forEach((s,i)=>{s.x+=s.vx;s.y+=s.vy;s.life-=.08;if(s.life<=0){sparks.splice(i,1);return;}
      ctx.beginPath();ctx.arc(s.x,s.y,1.5,0,Math.PI*2);ctx.fillStyle=`rgba(240,220,60,${s.life})`;ctx.fill();});
    const cols={CLOSED:'#ff3344',OPENING:'#f0b429',OPEN:'#00ff88',CLOSING:'#f0b429'};
    const c=cols[state];
    ctx.beginPath();ctx.arc(w-18,h-12,4,0,Math.PI*2);ctx.fillStyle=c;ctx.fill();
    ctx.fillStyle=c;ctx.font='700 8px Share Tech Mono,monospace';ctx.textAlign='right';ctx.fillText(state,w-26,h-7);ctx.textAlign='left';
    st++;
    if(state==='CLOSED'&&st>100){si=1;st=0;}
    if(state==='OPENING'){pct=Math.min(1,pct+.012);if(pct>=1){si=2;st=0;}}
    if(state==='OPEN'&&st>90){si=3;st=0;}
    if(state==='CLOSING'){pct=Math.max(0,pct-.012);if(pct<=0){si=0;st=0;}}
    frame++;requestAnimationFrame(draw);
  }
  draw();
})();
```

---

## שרברבות, חשמל, מיזוג

### PIPE — שרברבות / מים / גז
```javascript
(function() {
  const cv = document.getElementById('[CANVAS_ID]');
  if (!cv) return;
  const ctx = cv.getContext('2d', { willReadFrequently: true });
  function resize() { cv.width = cv.parentElement.clientWidth||400; cv.height = cv.parentElement.clientHeight||150; }
  resize(); window.addEventListener('resize', resize);
  let frame=0;
  // מסלול הצנרת: נקודות עיקריות
  const droplets=[];
  function draw() {
    const w=cv.width, h=cv.height;
    ctx.fillStyle='#020a10'; ctx.fillRect(0,0,w,h);
    // צנרת אופקית + אנכית
    const pipes=[
      {x1:w*.05,y1:h*.4,x2:w*.95,y2:h*.4,w:10,color:'#1e4060'},    // ראשי
      {x1:w*.25,y1:h*.4,x2:w*.25,y2:h*.85,w:8,color:'#1e4060'},     // ירידה 1
      {x1:w*.6,y1:h*.4,x2:w*.6,y2:h*.15,w:8,color:'#1e4060'},      // עלייה 2
      {x1:w*.25,y1:h*.85,x2:w*.5,y2:h*.85,w:6,color:'#1e4060'},    // תחתון
    ];
    pipes.forEach(p=>{
      ctx.strokeStyle=p.color;ctx.lineWidth=p.w;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(p.x1,p.y1);ctx.lineTo(p.x2,p.y2);ctx.stroke();
      ctx.strokeStyle='rgba(0,170,255,0.15)';ctx.lineWidth=p.w-4;
      ctx.beginPath();ctx.moveTo(p.x1,p.y1);ctx.lineTo(p.x2,p.y2);ctx.stroke();
    });
    // חיבורי T / ברזים
    [[w*.25,h*.4],[w*.6,h*.4]].forEach(([x,y])=>{
      ctx.fillStyle='#2a5070';ctx.beginPath();ctx.arc(x,y,7,0,Math.PI*2);ctx.fill();
      ctx.strokeStyle='rgba(0,200,255,.4)';ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(x,y,7,0,Math.PI*2);ctx.stroke();
    });
    // טיפות מים זורמות
    if(frame%18===0) droplets.push({
      path:frame%36===0?1:0, t:0, spd:.015+Math.random()*.01
    });
    const paths=[
      (t)=>({x:w*.05+t*(w*.9), y:h*.4}),                            // אופקי
      (t)=>t<.5?{x:w*.25+t*2*(w*.35),y:h*.4}:{x:w*.6,y:h*.4-(t-.5)*2*(h*.25)}, // אופקי + עלייה
    ];
    droplets.forEach((d,i)=>{
      d.t+=d.spd; if(d.t>1){droplets.splice(i,1);return;}
      const pos=paths[d.path](d.t);
      const a=d.t<.1?d.t/.1:d.t>.9?(1-d.t)/.1:1;
      ctx.beginPath();ctx.arc(pos.x,pos.y,3,0,Math.PI*2);
      ctx.fillStyle=`rgba(0,180,255,${.85*a})`;ctx.fill();
      ctx.beginPath();ctx.arc(pos.x,pos.y,6,0,Math.PI*2);
      ctx.fillStyle=`rgba(0,180,255,${.2*a})`;ctx.fill();
    });
    // לחץ מד (gauge)
    const gx=w*.82,gy=h*.25,gr=18;
    ctx.beginPath();ctx.arc(gx,gy,gr,0,Math.PI*2);ctx.fillStyle='rgba(0,0,0,.5)';ctx.fill();
    ctx.strokeStyle='rgba(0,170,255,.4)';ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(gx,gy,gr,0,Math.PI*2);ctx.stroke();
    const pct=.55+Math.sin(frame*.04)*.15;
    const ga=Math.PI*.75+pct*Math.PI*1.5;
    ctx.strokeStyle='rgba(0,255,180,.9)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(gx,gy);ctx.lineTo(gx+Math.cos(ga)*gr*.7,gy+Math.sin(ga)*gr*.7);ctx.stroke();
    ctx.fillStyle='rgba(0,200,255,.6)';ctx.font='7px Share Tech Mono,monospace';ctx.textAlign='center';ctx.fillText('PSI',gx,gy+gr+10);ctx.textAlign='left';
    ctx.fillStyle='rgba(0,170,255,.5)';ctx.font='9px Share Tech Mono,monospace';ctx.fillText('PIPE FLOW · LIVE',6,h-7);
    frame++;requestAnimationFrame(draw);
  }
  draw();
})();
```

### ELECTRIC — חשמל / לוח חשמל / מחולל
```javascript
(function() {
  const cv = document.getElementById('[CANVAS_ID]');
  if (!cv) return;
  const ctx = cv.getContext('2d', { willReadFrequently: true });
  function resize() { cv.width = cv.parentElement.clientWidth||400; cv.height = cv.parentElement.clientHeight||150; }
  resize(); window.addEventListener('resize', resize);
  let frame=0;
  function sineWave(x, amplitude, frequency, phase) {
    return amplitude * Math.sin(frequency * x + phase);
  }
  const sparks=[];
  function draw() {
    const w=cv.width, h=cv.height;
    ctx.fillStyle='#060400'; ctx.fillRect(0,0,w,h);
    // גל סינוס — גל AC
    const wH=h*.35;
    ['rgba(255,200,0,0.7)','rgba(0,180,255,0.5)'].forEach((color,ci)=>{
      ctx.beginPath();ctx.strokeStyle=color;ctx.lineWidth=2;
      for(let x=0;x<w;x++){
        const y=h*.5+sineWave(x*.04,wH*.45,1,frame*.05+ci*Math.PI*.6);
        x===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
      }
      ctx.stroke();
    });
    // לוח חשמל — מימין
    const bx=w*.72,by=h*.15,bw=w*.22,bh=h*.7;
    ctx.fillStyle='rgba(20,15,0,.8)';ctx.strokeStyle='rgba(255,180,0,.3)';ctx.lineWidth=1;
    ctx.fillRect(bx,by,bw,bh);ctx.strokeRect(bx,by,bw,bh);
    // מפסקים (circuit breakers)
    for(let i=0;i<4;i++){
      const by2=by+10+i*((bh-20)/4);
      const on=Math.sin(frame*.02+i)>.1;
      ctx.fillStyle=on?'rgba(255,200,0,.8)':'rgba(100,80,0,.4)';
      ctx.fillRect(bx+10,by2,bw-20,10);
      ctx.strokeStyle=on?'rgba(255,220,0,.6)':'rgba(80,60,0,.4)';ctx.lineWidth=.5;
      ctx.strokeRect(bx+10,by2,bw-20,10);
    }
    // ברק / ניצוץ
    if(frame%70===0) sparks.push({x:bx+bw*.3,y:by+bh*.5,life:1});
    sparks.forEach((s,i)=>{s.life-=.07;if(s.life<=0){sparks.splice(i,1);return;}
      ctx.strokeStyle=`rgba(255,240,100,${s.life})`;ctx.lineWidth=1.5;
      for(let j=0;j<3;j++){
        ctx.beginPath();ctx.moveTo(s.x,s.y);
        ctx.lineTo(s.x+(Math.random()-.5)*20,s.y+(Math.random()-.5)*20);ctx.stroke();
      }
    });
    // מדד וולט
    ctx.fillStyle='rgba(255,200,0,.6)';ctx.font='700 9px Share Tech Mono,monospace';
    ctx.fillText(`${(220+Math.sin(frame*.03)*3).toFixed(0)}V · ${(50+Math.sin(frame*.07)*.5).toFixed(1)}Hz`,6,h-7);
    frame++;requestAnimationFrame(draw);
  }
  draw();
})();
```

### AC — מיזוג אוויר / HVAC
```javascript
(function() {
  const cv = document.getElementById('[CANVAS_ID]');
  if (!cv) return;
  const ctx = cv.getContext('2d', { willReadFrequently: true });
  function resize() { cv.width = cv.parentElement.clientWidth||400; cv.height = cv.parentElement.clientHeight||150; }
  resize(); window.addEventListener('resize', resize);
  let frame=0;
  const particles=[];
  function draw() {
    const w=cv.width, h=cv.height;
    ctx.fillStyle='#030a12'; ctx.fillRect(0,0,w,h);
    // יחידת מיזוג (מלבן)
    const ux=w*.05,uy=h*.15,uw=w*.45,uh=h*.4;
    ctx.fillStyle='rgba(10,30,50,.9)';ctx.strokeStyle='rgba(0,180,255,.4)';ctx.lineWidth=2;
    ctx.fillRect(ux,uy,uw,uh);ctx.strokeRect(ux,uy,uw,uh);
    // לוחות אוורור
    const slats=6;
    for(let i=0;i<slats;i++){
      const sy=uy+8+(i*(uh-16)/slats);
      const angle=Math.sin(frame*.03)*12;
      ctx.save();ctx.translate(ux+uw/2,sy);ctx.rotate(angle*Math.PI/180);
      ctx.strokeStyle='rgba(0,200,255,.5)';ctx.lineWidth=2;
      ctx.beginPath();ctx.moveTo(-uw*.35,0);ctx.lineTo(uw*.35,0);ctx.stroke();
      ctx.restore();
    }
    // פאן מסתובב
    const fx=ux+uw+30,fy=h*.45,fr=22;
    for(let i=0;i<4;i++){
      const a=(frame*.03)+(i*Math.PI/2);
      ctx.beginPath();ctx.moveTo(fx,fy);
      ctx.arc(fx,fy,fr,a,a+.9);ctx.closePath();
      ctx.fillStyle='rgba(0,180,255,.25)';ctx.fill();
      ctx.strokeStyle='rgba(0,200,255,.4)';ctx.lineWidth=1;ctx.stroke();
    }
    ctx.beginPath();ctx.arc(fx,fy,5,0,Math.PI*2);ctx.fillStyle='rgba(0,220,255,.7)';ctx.fill();
    // חלקיקי אוויר קר
    if(frame%8===0) particles.push({x:ux+uw,y:uy+uh/2+(Math.random()-.5)*uh*.6,vx:1.5+Math.random(),vy:(Math.random()-.5)*.5,life:1,temp:-5+Math.random()*3});
    particles.forEach((p,i)=>{p.x+=p.vx;p.y+=p.vy;p.life-=.015;if(p.life<=0||p.x>w){particles.splice(i,1);return;}
      const cold=p.temp<0;
      ctx.beginPath();ctx.arc(p.x,p.y,2,0,Math.PI*2);ctx.fillStyle=`rgba(${cold?'100,200,255':'255,150,100'},${p.life*.7})`;ctx.fill();
    });
    // טמפרטורה
    const temp=18+Math.sin(frame*.02)*2;
    ctx.fillStyle='rgba(0,200,255,.8)';ctx.font='700 11px Share Tech Mono,monospace';
    ctx.textAlign='right';ctx.fillText(`${temp.toFixed(1)}°C`,w-8,h-7);ctx.textAlign='left';
    ctx.fillStyle='rgba(0,170,255,.5)';ctx.font='9px Share Tech Mono,monospace';ctx.fillText('HVAC · COOLING',6,h-7);
    frame++;requestAnimationFrame(draw);
  }
  draw();
})();
```

---

## עיצוב פנים / ריהוט

### INTERIOR — עיצוב פנים / תלת-ממד
```javascript
(function() {
  const cv = document.getElementById('[CANVAS_ID]');
  if (!cv) return;
  const ctx = cv.getContext('2d', { willReadFrequently: true });
  function resize() { cv.width = cv.parentElement.clientWidth||400; cv.height = cv.parentElement.clientHeight||150; }
  resize(); window.addEventListener('resize', resize);
  let frame=0;
  const PALETTES=[['#c9a84c','#8b6914'],['#d4a5a5','#8b4e4e'],['#7ec8c8','#2a8080'],['#a8c4a2','#4a7a44']];
  let palIdx=0;
  function draw() {
    const w=cv.width, h=cv.height;
    ctx.fillStyle='#0a0806'; ctx.fillRect(0,0,w,h);
    // רצפה (פרספקטיבה)
    ctx.fillStyle='rgba(40,30,20,.6)';
    ctx.beginPath();ctx.moveTo(0,h*.7);ctx.lineTo(w,h*.7);ctx.lineTo(w,h);ctx.lineTo(0,h);ctx.closePath();ctx.fill();
    // אריחי רצפה
    for(let i=0;i<6;i++){
      const tx=i*(w/6),ty=h*.7,tw=w/6,depth=h*.3;
      ctx.strokeStyle='rgba(255,220,150,.1)';ctx.lineWidth=.5;
      ctx.beginPath();ctx.moveTo(tx,ty);ctx.lineTo(tx,h);ctx.stroke();
      ctx.beginPath();ctx.moveTo(0,h*.7+i*(depth/6));ctx.lineTo(w,h*.7+i*(depth/6));ctx.stroke();
    }
    // קיר אחורי + gradient
    const pal=PALETTES[palIdx%PALETTES.length];
    const wallG=ctx.createLinearGradient(0,0,w,h*.7);
    wallG.addColorStop(0,`${pal[0]}20`);wallG.addColorStop(1,`${pal[1]}10`);
    ctx.fillStyle=wallG;ctx.fillRect(0,0,w,h*.7);
    // ספה פשוטה (CSS box simulation)
    const sx=w*.15,sy=h*.5,sw=w*.5,sh=h*.18;
    ctx.fillStyle=pal[0]+'aa';ctx.fillRect(sx,sy,sw,sh);
    ctx.fillStyle=pal[0]+'cc';ctx.fillRect(sx,sy-sh*.35,sw,sh*.35);
    [0,sw-sh*.15].forEach(dx=>{ctx.fillStyle=pal[1]+'aa';ctx.fillRect(sx+dx,sy-sh*.35,sh*.15,sh*1.35);});
    // כרית
    ctx.fillStyle='rgba(255,255,255,.12)';ctx.beginPath();ctx.ellipse(sx+sw*.25,sy+sh*.3,sw*.1,sh*.2,0,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='rgba(255,255,255,.12)';ctx.beginPath();ctx.ellipse(sx+sw*.6,sy+sh*.3,sw*.1,sh*.2,0,0,Math.PI*2);ctx.fill();
    // שינוי פלטה כל 200 פריימים
    if(frame%200===0) palIdx++;
    // תווית
    const pName=['זהב','ורוד','טורקיז','ירוק'][palIdx%4];
    ctx.fillStyle=`${pal[0]}cc`;ctx.font='700 9px Share Tech Mono,monospace';
    ctx.textAlign='right';ctx.fillText(`PALETTE: ${pName}`,w-6,h-7);ctx.textAlign='left';
    ctx.fillStyle='rgba(200,180,140,.4)';ctx.font='9px Share Tech Mono,monospace';ctx.fillText('INTERIOR · 3D',6,h-7);
    frame++;requestAnimationFrame(draw);
  }
  draw();
})();
```

---

## חינוך / פסיכולוגיה / ייעוץ

### MINDMAP — מפת מחשבה / ייעוץ / חינוך
```javascript
(function() {
  const cv = document.getElementById('[CANVAS_ID]');
  if (!cv) return;
  const ctx = cv.getContext('2d', { willReadFrequently: true });
  function resize() {
    cv.width = cv.parentElement.clientWidth||400; cv.height = cv.parentElement.clientHeight||150;
    initNodes();
  }
  let nodes=[], frame=0;
  const LABELS=['למידה','יצירה','צמיחה','הצלחה','מיומנות','ידע'];
  function initNodes() {
    const w=cv.width, h=cv.height;
    nodes=[{x:w/2,y:h/2,r:12,main:true}];
    for(let i=0;i<6;i++){
      const a=(i/6)*Math.PI*2, r=Math.min(w,h)*.35;
      nodes.push({x:w/2+Math.cos(a)*r,y:h/2+Math.sin(a)*r,r:6,main:false,angle:a,label:LABELS[i],phase:i*0.5});
    }
  }
  initNodes(); window.addEventListener('resize',resize);
  function draw() {
    const w=cv.width, h=cv.height;
    ctx.fillStyle='#04060e'; ctx.fillRect(0,0,w,h);
    const t=frame*.02;
    nodes.slice(1).forEach((n,i)=>{
      n.x=w/2+Math.cos(n.angle+t*.1)*Math.min(w,h)*.35;
      n.y=h/2+Math.sin(n.angle+t*.1)*Math.min(w,h)*.35;
      // קו חיבור
      const pulse=Math.sin(t*2+n.phase)*.5+.5;
      ctx.beginPath();ctx.moveTo(w/2,h/2);ctx.lineTo(n.x,n.y);
      ctx.strokeStyle=`rgba(100,150,255,${.15+pulse*.2})`;ctx.lineWidth=1+pulse;ctx.stroke();
      // נקודה נלווה
      const g=ctx.createRadialGradient(n.x,n.y,0,n.x,n.y,n.r*3+pulse*4);
      g.addColorStop(0,'rgba(120,160,255,.6)');g.addColorStop(1,'rgba(120,160,255,0)');
      ctx.fillStyle=g;ctx.beginPath();ctx.arc(n.x,n.y,n.r*3+pulse*4,0,Math.PI*2);ctx.fill();
      ctx.fillStyle='rgba(150,180,255,.9)';ctx.beginPath();ctx.arc(n.x,n.y,n.r,0,Math.PI*2);ctx.fill();
      // תווית
      ctx.fillStyle='rgba(200,210,255,.7)';ctx.font='7px Heebo,sans-serif';
      ctx.textAlign='center';ctx.fillText(n.label,n.x,n.y-n.r-4);ctx.textAlign='left';
    });
    // מרכז
    const gC=ctx.createRadialGradient(w/2,h/2,0,w/2,h/2,20+Math.sin(t)*3);
    gC.addColorStop(0,'rgba(180,140,255,.9)');gC.addColorStop(1,'rgba(100,80,200,.2)');
    ctx.fillStyle=gC;ctx.beginPath();ctx.arc(w/2,h/2,15+Math.sin(t)*2,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='rgba(180,150,255,.5)';ctx.font='9px Share Tech Mono,monospace';
    ctx.fillText('MIND MAP · LIVE',6,h-7);
    frame++;requestAnimationFrame(draw);
  }
  draw();
})();
```

---

## רכבים / גרר / מוסך

### AUTO — רכב / מוסך / בדיקת רכב
```javascript
(function() {
  const cv = document.getElementById('[CANVAS_ID]');
  if (!cv) return;
  const ctx = cv.getContext('2d', { willReadFrequently: true });
  function resize() { cv.width = cv.parentElement.clientWidth||400; cv.height = cv.parentElement.clientHeight||150; }
  resize(); window.addEventListener('resize', resize);
  let frame=0;
  const params=[
    {label:'מנוע',val:87,color:'#f97316'},
    {label:'שמן',val:72,color:'#22d3ee'},
    {label:'בלמים',val:95,color:'#00ff88'},
    {label:'צמיגים',val:68,color:'#f0b429'},
  ];
  function draw() {
    const w=cv.width, h=cv.height;
    ctx.fillStyle='#040808'; ctx.fillRect(0,0,w,h);
    // OBD Scan display
    ctx.strokeStyle='rgba(0,200,150,.2)';ctx.lineWidth=1;
    ctx.strokeRect(6,6,w-12,h-12);
    ctx.fillStyle='rgba(0,200,150,.5)';ctx.font='700 9px Share Tech Mono,monospace';
    ctx.fillText('OBD-II SCAN',10,18);
    // מדדים כגאוג'ים מעגליים
    const gR=16, cols=4, gw=w/cols;
    params.forEach((p,i)=>{
      p.val=Math.max(40,Math.min(100,p.val+(Math.random()-.5)*1.5));
      const gx=gw/2+i*gw, gy=h*.55;
      // רקע גאוג'
      ctx.beginPath();ctx.arc(gx,gy,gR,Math.PI*.75,Math.PI*2.25);
      ctx.strokeStyle='rgba(255,255,255,.08)';ctx.lineWidth=5;ctx.stroke();
      // מילוי
      const angle=Math.PI*.75+(p.val/100)*Math.PI*1.5;
      ctx.beginPath();ctx.arc(gx,gy,gR,Math.PI*.75,angle);
      ctx.strokeStyle=p.color;ctx.lineWidth=5;ctx.stroke();
      // ערך
      ctx.fillStyle='#fff';ctx.font='700 9px Share Tech Mono,monospace';ctx.textAlign='center';
      ctx.fillText(`${Math.round(p.val)}%`,gx,gy+4);
      ctx.fillStyle='rgba(200,200,200,.6)';ctx.font='7px Heebo,sans-serif';
      ctx.fillText(p.label,gx,gy+gR+10);ctx.textAlign='left';
    });
    // סטטוס
    const ok=params.every(p=>p.val>60);
    ctx.fillStyle=ok?'#00ff88':'#ff3344';ctx.font='700 8px Share Tech Mono,monospace';
    ctx.textAlign='right';ctx.fillText(ok?'✓ ALL SYSTEMS OK':'⚠ CHECK REQUIRED',w-8,h-7);ctx.textAlign='left';
    frame++;requestAnimationFrame(draw);
  }
  draw();
})();
```

---

## IT / רשת / תקשורת

### NETWORK — טופולוגיית רשת
```javascript
(function() {
  const cv = document.getElementById('[CANVAS_ID]');
  if (!cv) return;
  const ctx = cv.getContext('2d', { willReadFrequently: true });
  function resize() {
    cv.width = cv.parentElement.clientWidth||400; cv.height = cv.parentElement.clientHeight||150;
    initNodes();
  }
  let nodes=[], packets=[], frame=0;
  function initNodes() {
    const w=cv.width, h=cv.height;
    nodes=[
      {x:w*.5,y:h*.5,r:7,label:'HUB',color:'#f0b429'},
      {x:w*.15,y:h*.25,r:5,label:'CAM1',color:'#00aaff'},{x:w*.85,y:h*.25,r:5,label:'CAM2',color:'#00aaff'},
      {x:w*.15,y:h*.75,r:5,label:'DVR',color:'#00aaff'},{x:w*.85,y:h*.75,r:5,label:'APP',color:'#00ff88'},
      {x:w*.5,y:h*.1,r:4,label:'NET',color:'#cc66ff'},
    ];
  }
  initNodes(); window.addEventListener('resize',resize);
  function draw() {
    const w=cv.width, h=cv.height;
    ctx.fillStyle='#030810'; ctx.fillRect(0,0,w,h);
    nodes.forEach((a,i)=>nodes.slice(i+1).forEach(b=>{
      const d=Math.hypot(a.x-b.x,a.y-b.y);
      ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);
      ctx.strokeStyle=`rgba(0,170,255,${d<200?.3:.12})`;ctx.lineWidth=d<200?1:.5;ctx.stroke();
    }));
    if(frame%40===0&&nodes.length>1){
      const a=nodes[0],b=nodes[Math.floor(Math.random()*(nodes.length-1))+1];
      packets.push({ax:a.x,ay:a.y,bx:b.x,by:b.y,t:0,spd:.03+Math.random()*.02});
    }
    packets.forEach((p,i)=>{p.t+=p.spd;if(p.t>1){packets.splice(i,1);return;}
      const px=p.ax+(p.bx-p.ax)*p.t,py=p.ay+(p.by-p.ay)*p.t;
      const fade=p.t<.1?p.t/.1:p.t>.9?(1-p.t)/.1:1;
      ctx.beginPath();ctx.arc(px,py,3,0,Math.PI*2);ctx.fillStyle=`rgba(240,180,41,${.95*fade})`;ctx.fill();
    });
    nodes.forEach(n=>{
      const g=ctx.createRadialGradient(n.x,n.y,0,n.x,n.y,n.r*3);
      g.addColorStop(0,n.color+'aa');g.addColorStop(1,n.color+'00');
      ctx.fillStyle=g;ctx.beginPath();ctx.arc(n.x,n.y,n.r*3,0,Math.PI*2);ctx.fill();
      ctx.fillStyle=n.color;ctx.beginPath();ctx.arc(n.x,n.y,n.r,0,Math.PI*2);ctx.fill();
      ctx.fillStyle='rgba(200,220,255,.7)';ctx.font='7px Share Tech Mono,monospace';ctx.textAlign='center';
      ctx.fillText(n.label,n.x,n.y-n.r-3);ctx.textAlign='left';
    });
    ctx.fillStyle='rgba(0,170,255,.6)';ctx.font='9px Share Tech Mono,monospace';ctx.fillText('NETWORK · LIVE',6,h-7);
    frame++;requestAnimationFrame(draw);
  }
  draw();
})();
```

### HEALTH — ניטור מערכת (CPU/RAM/...)
```javascript
(function() {
  const cv = document.getElementById('[CANVAS_ID]');
  if (!cv) return;
  const ctx = cv.getContext('2d', { willReadFrequently: true });
  function resize() { cv.width = cv.parentElement.clientWidth||400; cv.height = cv.parentElement.clientHeight||150; }
  resize(); window.addEventListener('resize', resize);
  let frame=0;
  const bars=[
    {label:'CPU',val:42,target:42,color:'#00aaff'},
    {label:'RAM',val:67,target:67,color:'#00ff88'},
    {label:'CAM',val:91,target:91,color:'#f0b429'},
    {label:'NET',val:24,target:24,color:'#cc66ff'},
  ];
  function draw() {
    const w=cv.width, h=cv.height;
    ctx.fillStyle='#030a10'; ctx.fillRect(0,0,w,h);
    ctx.fillStyle='rgba(0,170,255,.65)';ctx.font='700 9px Share Tech Mono,monospace';
    ctx.fillText('SYSTEM HEALTH MONITOR',8,17);
    ctx.strokeStyle='rgba(0,170,255,.18)';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(8,21);ctx.lineTo(w-8,21);ctx.stroke();
    const bh=13,bw=w-88,sx=52,sy=30,sp=25;
    bars.forEach((bar,i)=>{
      const y=sy+i*sp;
      if(frame%60===i*15) bar.target=20+Math.floor(Math.random()*75);
      bar.val+=(bar.target-bar.val)*.04;
      ctx.fillStyle='rgba(200,220,240,.75)';ctx.font='700 8px Share Tech Mono,monospace';ctx.fillText(bar.label,5,y+bh-1);
      ctx.fillStyle='rgba(255,255,255,.04)';ctx.fillRect(sx,y,bw,bh);
      const fw=(bar.val/100)*bw,bg=ctx.createLinearGradient(sx,0,sx+fw,0);
      bg.addColorStop(0,bar.color+'88');bg.addColorStop(1,bar.color);
      ctx.fillStyle=bg;ctx.fillRect(sx,y,fw,bh);
      ctx.fillStyle='#fff';ctx.font='700 8px Share Tech Mono,monospace';ctx.textAlign='right';
      ctx.fillText(Math.round(bar.val)+'%',w-5,y+bh-1);ctx.textAlign='left';
    });
    ctx.fillStyle='rgba(0,255,136,.55)';ctx.font='8px Share Tech Mono,monospace';ctx.fillText('STATUS · ONLINE',5,h-7);
    frame++;requestAnimationFrame(draw);
  }
  draw();
})();
```

---

## שיפוצים / בנייה

### BLUEPRINT — תוכניות אדריכל
```javascript
(function() {
  const cv = document.getElementById('[CANVAS_ID]');
  if (!cv) return;
  const ctx = cv.getContext('2d', { willReadFrequently: true });
  function resize() { cv.width = cv.parentElement.clientWidth||400; cv.height = cv.parentElement.clientHeight||150; }
  resize(); window.addEventListener('resize', resize);
  let frame=0;
  function draw() {
    const w=cv.width, h=cv.height;
    ctx.fillStyle='#020d1a'; ctx.fillRect(0,0,w,h);
    const gs=20;ctx.strokeStyle='rgba(0,150,255,.1)';ctx.lineWidth=.5;
    for(let x=0;x<w;x+=gs){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,h);ctx.stroke();}
    for(let y=0;y<h;y+=gs){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke();}
    const prog=Math.min(1,(frame%300)/200);
    const rooms=[[.1,.15,.35,.7],[.45,.15,.45,.7],[.1,.15,.8,.02],[.1,.85,.8,.02]];
    ctx.strokeStyle=`rgba(100,200,255,${.6+Math.sin(frame*.03)*.2})`;ctx.lineWidth=2;
    rooms.forEach(([rx,ry,rw,rh])=>{
      const x=rx*w,y=ry*h,rW=rw*w,rH=rh*h;
      const len=(rW*2+rH*2)*prog;
      ctx.save();ctx.beginPath();ctx.setLineDash([len,9999]);ctx.strokeRect(x,y,rW,rH);ctx.stroke();ctx.setLineDash([]);ctx.restore();
    });
    ctx.fillStyle='rgba(100,200,255,.6)';ctx.font='9px Share Tech Mono,monospace';ctx.fillText('BLUEPRINT · LIVE',6,h-7);
    frame++;requestAnimationFrame(draw);
  }
  draw();
})();
```

---

## טיפים לבחירת אנימציה לפי שירות

| שירות | אנימציה |
|---|---|
| מצלמות אבטחה | `CCTV` |
| מערכות אזעקה | `RADAR` |
| בקרת כניסה / כרטיסי חכם | `ACCESS` |
| אינטרקום / זיהוי פנים | `FACE` |
| שערים / גדרות חשמליות | `GATE` |
| תשתיות IT / רשת | `NETWORK` |
| תחזוקה / ניטור מערכות | `HEALTH` |
| שרברבות / מים / גז | `PIPE` |
| חשמל / לוחות חשמל | `ELECTRIC` |
| מיזוג אוויר / HVAC | `AC` |
| עיצוב פנים / ריהוט | `INTERIOR` |
| חינוך / פסיכולוגיה / ייעוץ | `MINDMAP` |
| רכבים / מוסך / גרר | `AUTO` |
| שיפוצים / בנייה / אדריכלות | `BLUEPRINT` |
| כל שירות כללי | `HEALTH` (שנה labels) |
