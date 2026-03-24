# Design System — 3D Landing Page

## CSS Variables (העתק לכל פרויקט)

```css
:root {
  --bg:      #04090f;   /* רקע ראשי — כמעט שחור */
  --bg2:     #060d18;   /* רקע sections */
  --bg3:     #08111f;   /* רקע cards */
  --glass:   rgba(8,17,32,0.8);
  --border:  rgba(0,180,255,0.12);
  --border-g:rgba(201,168,76,0.2);
  --cyan:    #00aaff;
  --cyan-dim:rgba(0,170,255,0.12);
  --gold:    #f0b429;
  --gold-l:  #ffd060;
  --gold-dim:rgba(240,180,41,0.12);
  --green:   #00ff88;
  --wa:      #25d366;   /* WhatsApp */
  --txt:     #c8d8f0;
  --txt-dim: rgba(200,216,240,0.5);
  --mono:    'Share Tech Mono', monospace;
  --navy:    #0a1628;
}
```

### שינוי פלטת צבעים לפי תחום

| תחום | bg | accent1 | accent2 |
|---|---|---|---|
| אבטחה / טכנולוגיה | `#04090f` | `#f0b429` (gold) | `#00aaff` (blue) |
| שיפוצים / בנייה | `#0a0f08` | `#f97316` (orange) | `#84cc16` (green) |
| רפואה / קוסמטיקה | `#040912` | `#a855f7` (purple) | `#06b6d4` (teal) |
| מסעדה / קייטרינג | `#0f0805` | `#ef4444` (red) | `#f59e0b` (amber) |
| עסקים / פיננסים | `#050a14` | `#3b82f6` (blue) | `#10b981` (emerald) |
| כללי (ברירת מחדל) | `#04090f` | `#f0b429` (gold) | `#00aaff` (blue) |

---

## Three.js Hero — קוד מלא

```html
<section id="hero">
  <canvas id="hero-3d"></canvas>
  <!-- HUD elements -->
  <div class="hero-hud left"><span class="rec-dot"></span>REC</div>
  <div class="hero-hud right" id="hero-ts">CAM-01 &nbsp;00:00:00</div>
  <!-- Content -->
  <div class="container">
    <div class="hero-body">
      <div class="hero-badge">🛡️ [TAGLINE]</div>
      <h1 class="hero-title">[TITLE]<br><span class="hl">[HIGHLIGHT]</span></h1>
      <p class="hero-sub">[SUBTITLE]</p>
      <div class="hero-btns">
        <a href="#contact" class="btn btn-gold">קבל הצעת מחיר</a>
        <a href="https://wa.me/972XXXXXXXXX" class="btn btn-wa">WhatsApp עכשיו</a>
      </div>
    </div>
  </div>
  <div class="hero-scroll"><i class="fas fa-chevron-down"></i><span>גלול</span></div>
</section>
```

```javascript
/* ===== THREE.JS HERO ===== */
(function() {
  const heroEl = document.getElementById('hero');
  const canvas = document.getElementById('hero-3d');
  if (!canvas || !window.THREE) return;

  const scene = new THREE.Scene();
  const W = heroEl.offsetWidth, H = heroEl.offsetHeight;
  const camera = new THREE.PerspectiveCamera(60, W/H, 0.1, 1000);
  camera.position.set(0, 0, 8);

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(W, H);

  // אובייקט מרכזי — ניתן להחליף geometry לפי תחום
  const coreGeo = new THREE.IcosahedronGeometry(1.8, 0);
  const coreMat = new THREE.MeshPhongMaterial({
    color: 0x0a1f5e, emissive: 0x001133,
    specular: 0x00aaff, shininess: 80,
    transparent: true, opacity: 0.85
  });
  const core = new THREE.Mesh(coreGeo, coreMat);
  scene.add(core);

  // Wireframe חיצוני
  const wire = new THREE.Mesh(
    new THREE.IcosahedronGeometry(2.3, 1),
    new THREE.MeshBasicMaterial({ color: 0x00aaff, wireframe: true, transparent: true, opacity: 0.4 })
  );
  scene.add(wire);

  // טבעות זהב
  const ringMat = new THREE.MeshBasicMaterial({ color: 0xf0b429, transparent: true, opacity: 0.6 });
  const ring1 = new THREE.Mesh(new THREE.TorusGeometry(3.2, 0.03, 8, 80), ringMat);
  ring1.rotation.x = Math.PI / 3;
  scene.add(ring1);
  const ring2 = new THREE.Mesh(new THREE.TorusGeometry(3.2, 0.03, 8, 80),
    new THREE.MeshBasicMaterial({ color: 0xf0b429, transparent: true, opacity: 0.35 }));
  ring2.rotation.x = -Math.PI / 3; ring2.rotation.y = Math.PI / 4;
  scene.add(ring2);

  // חלקיקים
  const N = 600;
  const pos = new Float32Array(N * 3), col = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) {
    const t = Math.random()*Math.PI*2, p = Math.acos(2*Math.random()-1), r = 4+Math.random()*6;
    pos[i*3]=r*Math.sin(p)*Math.cos(t); pos[i*3+1]=r*Math.sin(p)*Math.sin(t); pos[i*3+2]=r*Math.cos(p);
    if (Math.random()>.7) { col[i*3]=.95; col[i*3+1]=.71; col[i*3+2]=.16; } // gold
    else                  { col[i*3]=0;   col[i*3+1]=.67; col[i*3+2]=1;   } // blue
  }
  const pGeo = new THREE.BufferGeometry();
  pGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  pGeo.setAttribute('color',    new THREE.BufferAttribute(col, 3));
  const particles = new THREE.Points(pGeo, new THREE.PointsMaterial({ size: 0.08, vertexColors: true, transparent: true, opacity: 0.7 }));
  scene.add(particles);

  // תאורה
  scene.add(new THREE.AmbientLight(0x001133, 0.5));
  const bl = new THREE.PointLight(0x00b4ff, 2, 15); bl.position.set(5,5,5); scene.add(bl);
  const gl = new THREE.PointLight(0xf0b429, 1.5, 15); gl.position.set(-5,-3,-5); scene.add(gl);

  // Mouse parallax
  let mx = 0, my = 0;
  document.addEventListener('mousemove', e => {
    mx = (e.clientX/innerWidth - .5) * 3;
    my = (e.clientY/innerHeight - .5) * 2;
  });

  // Resize
  function onResize() {
    const W = heroEl.offsetWidth, H = heroEl.offsetHeight;
    camera.aspect = W/H; camera.updateProjectionMatrix();
    renderer.setSize(W, H);
  }
  window.addEventListener('resize', onResize);

  // Animation loop
  (function animate() {
    requestAnimationFrame(animate);
    core.rotation.y += .006; core.rotation.x += .002;
    wire.rotation.y -= .004; wire.rotation.z += .003;
    ring1.rotation.z += .004; ring2.rotation.z -= .003;
    particles.rotation.y += .001;
    camera.position.x += (mx - camera.position.x) * .04;
    camera.position.y += (-my - camera.position.y) * .04;
    camera.lookAt(0,0,0);
    renderer.render(scene, camera);
  })();
})();
```

### החלפת geometry לפי תחום

| תחום | geometry מומלץ |
|---|---|
| אבטחה | `IcosahedronGeometry(1.8, 0)` |
| שיפוצים | `BoxGeometry(2.5, 2.5, 2.5)` |
| רפואה | `SphereGeometry(2, 32, 32)` |
| משפטים | `OctahedronGeometry(2, 0)` |
| פיננסים | `TorusKnotGeometry(1.5, 0.4, 64, 16)` |

---

## CSS 3D Cards

```css
/* Container */
.srv-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  perspective: 1800px;
}
@media (max-width: 900px) { .srv-grid { grid-template-columns: repeat(2,1fr); } }
@media (max-width: 560px) { .srv-grid { grid-template-columns: 1fr; } }

/* Card */
.srv-card {
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
  transform-style: preserve-3d;
  transition: transform .4s cubic-bezier(.2,.8,.3,1.2), box-shadow .4s;
  cursor: pointer;
  position: relative;
}
/* עובי כרטיס — שכבת עומק */
.srv-card::before {
  content: '';
  position: absolute; inset: 0;
  border-radius: 16px;
  transform: translateZ(-14px);
  background: linear-gradient(135deg, #020912, #010408);
  border: 1px solid rgba(0,170,255,.08);
}
/* גלו תחתון */
.srv-card:hover {
  box-shadow: 0 30px 80px rgba(0,0,0,.7), 0 0 40px rgba(0,170,255,.15);
}

/* Display window (canvas) */
.srv-display {
  position: relative;
  height: 150px;
  background: #020810;
  overflow: hidden;
}
.srv-display canvas { width: 100%; height: 100%; display: block; }

/* Tag badge */
.srv-tag {
  display: inline-flex; align-items: center; gap: .4rem;
  font: 700 10px var(--mono);
  color: var(--cyan);
  background: var(--cyan-dim);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: .25rem .6rem;
  margin: .75rem .75rem 0;
  letter-spacing: .05em;
}
.srv-card h3 { padding: .5rem .75rem .25rem; font-size: 1.05rem; color: #fff; }
.srv-card p  { padding: 0 .75rem .75rem; font-size: .85rem; color: var(--txt-dim); line-height: 1.5; }
```

---

## CSS Typography 3D

```css
/* כותרות section */
.ttl {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 900;
  color: #fff;
  text-shadow:
    0 1px 0 rgba(0,170,255,.3),
    0 2px 0 rgba(0,170,255,.2),
    0 3px 0 rgba(0,170,255,.1),
    0 10px 20px rgba(0,0,0,.5);
  margin-bottom: .5rem;
}
.ttl span { color: var(--gold); }

/* Counter numbers */
.cnt-num {
  font-size: 2.8rem; font-weight: 900; color: #fff;
  text-shadow: 0 2px 0 rgba(0,170,255,.3), 0 4px 0 rgba(0,170,255,.15), 0 8px 20px rgba(0,0,0,.5);
  font-family: var(--mono);
}
```

---

## CSS Sections Dividers (אלכסוניים)

```css
#counters {
  clip-path: polygon(0 0, 100% 4%, 100% 100%, 0 96%);
  padding: 5rem 0; margin: -2rem 0; position: relative; z-index: 2;
  background: var(--bg2);
}
#services {
  clip-path: polygon(0 4%, 100% 0, 100% 96%, 0 100%);
  padding: 7rem 0; margin: -2rem 0; position: relative; z-index: 1;
}
```

---

## Hero Grid Floor (פרספקטיבה)

```css
.hero-grid {
  position: absolute; bottom: 0; left: 0; right: 0; height: 40%;
  background-image:
    linear-gradient(rgba(0,170,255,.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,170,255,.06) 1px, transparent 1px);
  background-size: 60px 60px;
  transform: perspective(300px) rotateX(60deg);
  transform-origin: bottom center;
  mask-image: linear-gradient(to top, rgba(0,170,255,.3), transparent);
  pointer-events: none;
}
```

---

## CSS Utilities (animations)

```css
/* Reveal on scroll */
.reveal { opacity: 0; transform: translateY(30px); transition: opacity .6s, transform .6s; }
.reveal.visible { opacity: 1; transform: none; }
.reveal.d1 { transition-delay: .1s; }
.reveal.d2 { transition-delay: .2s; }
.reveal.d3 { transition-delay: .3s; }

/* Floating badge */
@keyframes float3d {
  0%,100% { transform: translateY(0); }
  50%      { transform: translateY(-10px); }
}
.hero-badge { animation: float3d 4s ease-in-out infinite; }

/* REC blink */
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
.rec-dot { display:inline-block; width:8px; height:8px; border-radius:50%; background:#ff3344; animation:blink 1s infinite; margin-left:.4rem; }

/* WhatsApp pulse */
@keyframes wa-pulse { 0%,100%{box-shadow:0 0 0 0 rgba(37,211,102,.4)} 50%{box-shadow:0 0 0 12px rgba(37,211,102,0)} }
.wa-float { animation: wa-pulse 2s infinite; }
```
