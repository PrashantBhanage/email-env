from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from app import app as api_app

app = FastAPI(title="Email Triage Environment", version="1.0.0")

# include existing API paths (/reset /step /state /tasks etc.)
app.include_router(api_app.router)

@app.get("/", response_class=HTMLResponse)
def home():
    return """<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Email Triage Environment</title>
    <link href=\"https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@500;700;800&display=swap\" rel=\"stylesheet\">
    <style>
        :root {
            --bg: #020d07;
            --green: #22c55e;
            --light: #a8f7c2;
            --card-bg: rgba(255,255,255,0.03);
            --border: rgba(34,197,94,0.6);
            --line: rgba(34,197,94,0.15);
        }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            min-height: 100vh;
            background: var(--bg);
            color: #f4fff4;
            font-family: 'Inter', sans-serif;
            overflow-x: hidden;
        }
        .canvas-bg { position: fixed; inset: 0; z-index: -2; background: var(--bg); }
        #particleCanvas {
            width: 100%; height: 100%; display: block;
        }
        .orb {
            position: fixed;
            width: 220px;
            height: 220px;
            filter: blur(90px);
            opacity: 0.1;
            border-radius: 50%;
            z-index: -1;
        }
        .orb.a { top: -50px; left: -80px; background: radial-gradient(circle, rgba(34,197,94,0.5), transparent 70%); }
        .orb.b { top: 30%; right: -90px; background: radial-gradient(circle, rgba(16,185,129,0.5), transparent 70%); }
        .orb.c { bottom: -60px; left: 20%; background: radial-gradient(circle, rgba(5,150,105,0.5), transparent 70%); }

        .wrapper { position: relative; z-index: 1; max-width: 1200px; margin: 0 auto; padding: 40px 24px 80px; }
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            color: #a8f7c2;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.04em;
            margin-bottom:12px;
            animation: fadeSlideUp .7s ease forwards;
            opacity: 0;
        }
        .badge-dot {
            width: 9px; height: 9px; border-radius: 50%;
            background: var(--green); box-shadow: 0 0 14px var(--green);
            animation: pulse 1.2s infinite ease-in-out;
        }
        h1 {
            margin: 0;
            font-family: 'Syne', sans-serif;
            font-size: clamp(2.5rem, 6vw, 4.2rem);
            line-height: 1.1;
            letter-spacing: .02em;
            animation: fadeSlideUp .8s ease forwards;
            opacity: 0;
        }
        .subtitle {
            margin: 14px 0 20px;
            font-size: clamp(1.15rem, 2.3vw, 1.5rem);
            color: #a8f7c2;
            animation: fadeSlideUp .9s ease forwards;
            opacity: 0;
        }
        .desc {
            max-width: 720px;
            color: #c8f8d5;
            font-size: 1.05rem;
            line-height: 1.65;
            margin-bottom: 26px;
            animation: fadeSlideUp 1s ease forwards;
            opacity: 0;
        }
        .hero-cta {
            display: inline-flex;
            gap: 12px;
            align-items: center;
        }
        .btn {
            appearance: none;
            border: 1px solid rgba(34,197,94,.72);
            background: linear-gradient(135deg, rgba(34,197,94,.8), rgba(6,182,120,.8));
            color: #020d07;
            font-weight: 700;
            border-radius: 999px;
            padding: 12px 22px;
            cursor: pointer;
            text-decoration: none;
            transition: transform .2s ease, box-shadow .2s ease;
            box-shadow: 0 10px 22px rgba(34,197,94,.3);
            font-family: 'JetBrains Mono', monospace;
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 14px 26px rgba(34,197,94,.45); }

        .section { margin-top: 68px; animation: zoomFade .9s ease forwards; opacity: 0; }
        .section-title { font-family: 'Syne', sans-serif; font-size: clamp(1.7rem, 4vw, 2.4rem); margin-bottom: 18px; color: #e5ffe8; }
        .cards { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; }
        .card { background: var(--card-bg); border-left: 1px solid rgba(34,197,94,.35); border-top: 1px solid rgba(255,255,255,.08); border-radius:16px; padding: 20px; backdrop-filter: blur(18px); box-shadow: 0 8px 30px rgba(0,0,0,.3); transition: transform .3s ease, box-shadow .3s ease; }
        .card h3 { margin:0 0 8px; font-size: 1.2rem; }
        .card p { color: #afebc5; }
        .card:hover { transform: translateY(-8px); box-shadow: 0 16px 40px rgba(0,0,0,.4); border-color: rgba(34,197,94,1); }

        .demo { display:grid; gap:16px; background: rgba(0,0,0,.22); padding: 22px; border-radius:20px; border:1px solid rgba(34,197,94,.35); }
        .demo textarea { width:100%; min-height:120px; border-radius: 12px; border: 1px solid rgba(167,252,226,.45); background: #041009; color:#d6fff0; padding:12px; font-size:1rem; resize: vertical; font-family: 'JetBrains Mono', monospace; }
        .demo-actions { display:flex; flex-wrap:wrap; gap:10px; align-items:center; }
        .demo-actions button { margin:0; }
        .result-card { display:grid; grid-template-columns: repeat(auto-fit,minmax(150px,1fr)); gap: 10px; }
        .badge-pill { display:inline-flex; align-items:center; justify-content:center; border-radius:999px; padding:7px 14px; font-family:'JetBrains Mono', monospace; font-size:.88rem; letter-spacing:.02em; border:1px solid rgba(34,197,94,.72); }
        .badge-cat { background: rgba(34,197,94,.16); color:#c8fff0; }
        .overall { margin-top: 12px; padding: 12px 14px; border:1px solid rgba(34,197,94,.6); border-radius: 12px; background: rgba(5, 50, 30, 0.35); }

        .api-grid { display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: 12px; }
        .api-item { background: rgba(255,255,255,0.04); border:1px solid rgba(34,197,94,.25); border-radius:12px; padding:12px; font-family:'JetBrains Mono', monospace; color:#b8f9d0; }
        .api-item span { display:block; margin-bottom:6px; font-weight:600; color:#d7ffea; }

        footer { margin-top: 44px; text-align:center; color:#88d9a9; font-size:.86rem; }
        @media (max-width: 920px){ .cards,.api-grid{grid-template-columns:1fr;} .wrapper{padding: 24px 16px 50px;} }

        @keyframes pulse { 0%,100%{transform: scale(1);} 50%{transform: scale(1.35);} }
        @keyframes fadeSlideUp { from{opacity:0; transform:translateY(18px);} to{opacity:1; transform:translateY(0);} }
        @keyframes zoomFade { from{opacity:0; transform:scale(0.98);} to{opacity:1; transform:scale(1);} }
    </style>
</head>
<body>
    <div class="canvas-bg"><canvas id="particleCanvas"></canvas></div>
    <div class="orb a"></div>
    <div class="orb b"></div>
    <div class="orb c"></div>

    <main class="wrapper">
        <div class="badge"><span class="badge-dot"></span>System Running</div>
        <h1>Email Triage Environment</h1>
        <p class="subtitle">AI-Powered Email Classification & Smart Triage</p>
        <p class="desc">High fidelity email triage with automated category/piority/action recommendation through a simple API-integrated environment built on OpenEnv.</p>
        <a class="btn" href="/docs">View API</a>

        <section class="section" style="margin-top:50px;">
            <h2 class="section-title">Key Features</h2>
            <div class="cards">
                <article class="card"><h3>📧 Email Classification</h3><p>Billing, technical, or general.</p></article>
                <article class="card"><h3>⚡ Priority Detection</h3><p>Low, medium, or high urgency.</p></article>
                <article class="card"><h3>🤖 Smart Triage</h3><p>Reply, escalate, or ignore.</p></article>
            </div>
        </section>

        <section class="section">
            <h2 class="section-title">Try the Classifier</h2>
            <div class="demo">
                <textarea id="emailInput">Subject: Urgent billing issue\n\nHi, I was charged twice this month and need this resolved immediately.</textarea>
                <div class="demo-actions">
                    <button class="btn" id="fetchTaskBtn">Fetch Task (/reset)</button>
                    <button class="btn" id="classifyBtn">Submit Classification</button>
                    <span id="statusText" style="color:#a6f8d7;font-size:0.93rem;"></span>
                </div>
                <div id="taskView" style="background: rgba(10,20,15,0.45); border:1px solid rgba(34,197,94,.3); padding:12px; border-radius:12px; color:#c9f9db; min-height:76px;">Task not loaded yet.</div>
                <div id="resultOutput" class="result-card" style="margin-top:12px;"></div>
                <div class="overall" id="scoreOutput" style="display:none;"></div>
            </div>
        </section>

        <section class="section">
            <h2 class="section-title">API Endpoints</h2>
            <div class="api-grid">
                <div class="api-item"><span>GET /health</span>Status check</div>
                <div class="api-item"><span>POST /reset</span>Initialize task</div>
                <div class="api-item"><span>POST /step</span>Submit action</div>
                <div class="api-item"><span>GET /state</span>Current env state</div>
                <div class="api-item"><span>GET /tasks</span>List tasks</div>
            </div>
        </section>

        <footer>&copy; 2024 Email Triage Environment. Built for OpenEnv Hackathon.</footer>
    </main>

    <script>
        const canvas = document.getElementById('particleCanvas');
        const ctx = canvas.getContext('2d');
        const particles = [];
        const particleCount = 80;

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }

        function rand(min,max){return Math.random()*(max-min)+min;}
        function makeParticles(){
            particles.length=0;
            for(let i=0;i<particleCount;i++){
                particles.push({
                    x: rand(0,canvas.width),
                    y: rand(0,canvas.height),
                    r: rand(1.5,2.8),
                    vx: rand(-0.35,0.35),
                    vy: rand(-0.35,0.35),
                    alpha: rand(0.2,0.6)
                });
            }
        }

        function draw(){
            ctx.clearRect(0,0,canvas.width,canvas.height);
            particles.forEach(p=>{
                p.x += p.vx;
                p.y += p.vy;
                if(p.x<0||p.x>canvas.width){p.vx*=-1;}
                if(p.y<0||p.y>canvas.height){p.vy*=-1;}
                ctx.beginPath();
                ctx.fillStyle = `rgba(34,197,94,${p.alpha})`;
                ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
                ctx.fill();
            });
            for(let i=0;i<particleCount;i++){
                for(let j=i+1;j<particleCount;j++){
                    const a=particles[i], b=particles[j];
                    const dx=a.x-b.x, dy=a.y-b.y;
                    const d=Math.hypot(dx,dy);
                    if(d<130) {
                        ctx.strokeStyle=`rgba(34,197,94,${Math.max(0,0.15-(d/130)*0.14)})`;
                        ctx.lineWidth=1;
                        ctx.beginPath();
                        ctx.moveTo(a.x,a.y);
                        ctx.lineTo(b.x,b.y);
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(draw);
        }

        window.addEventListener('resize', ()=>{resizeCanvas(); makeParticles();});
        resizeCanvas(); makeParticles(); draw();

        const statusText=document.getElementById('statusText');
        const taskView=document.getElementById('taskView');
        const resultOutput=document.getElementById('resultOutput');
        const scoreOutput=document.getElementById('scoreOutput');

        document.getElementById('fetchTaskBtn').addEventListener('click', async ()=>{
            statusText.textContent='Loading task...';
            try {
                const res = await fetch('/reset', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({}) });
                const data = await res.json();
                const observation = data.observation || data || {};
                const text = observation.email_text || observation.task || 'No task text';
                taskView.textContent = 'Email: ' + text;
                statusText.textContent = 'Task loaded.';
            } catch(err) {
                statusText.textContent='Task fetch failed';
            }
        });

        function classifyByText(text){
            const lower=text.toLowerCase();
            const billing=['billing','charged','invoice','refund','payment'];
            const technical=['error','crash','bug','issue','login','fail'];
            if(billing.some(w=>lower.includes(w))) return {category:'billing',priority:'high',action:'escalate'};
            if(technical.some(w=>lower.includes(w))) return {category:'technical',priority:'medium',action:'reply'};
            return {category:'general',priority:'low',action:'reply'};
        }

        document.getElementById('classifyBtn').addEventListener('click', async ()=>{
            statusText.textContent='Submitting classification...';
            const emailText = document.getElementById('emailInput').value;
            const action = classifyByText(emailText);
            try {
                await fetch('/reset', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({}) });
                const stepRes = await fetch('/step', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(action) });
                const payload = await stepRes.json();
                const score = payload.reward ?? payload.score ?? 0;
                resultOutput.innerHTML = `
                    <div class='badge-pill badge-cat'>Category: ${action.category}</div>
                    <div class='badge-pill badge-cat'>Priority: ${action.priority}</div>
                    <div class='badge-pill badge-cat'>Action: ${action.action}</div>`;
                scoreOutput.style.display='block';
                scoreOutput.innerHTML = `Reward score: <strong>${score}</strong>`;
                statusText.textContent='Result received';
            } catch(e){
                statusText.textContent='Error on classification';
            }
        });
    </script>
</body>
</html>"""

@app.get("/health")
def health():
    return JSONResponse({"status": "ok", "name": "Email Triage Environment", "version": "1.0.0"})
