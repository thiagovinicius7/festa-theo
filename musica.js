// Música do convite.
// Se existir "musica.mp3" no site, toca ela em loop.
// Senão, toca uma melodia original gerada no navegador (pentatônica, cordas dedilhadas + gongo).

const btn = document.getElementById('btnMusica');
const dica = document.getElementById('dicaMusica');
let tocando = false;
let modo = null;          // 'arquivo' | 'sintese'
let audio = null;

/* ---------- Arquivo musica.mp3 (opcional) ---------- */
function testaArquivo() {
  return new Promise(ok => {
    const a = new Audio();
    a.preload = 'auto';
    a.loop = true;
    a.volume = 0.6;
    a.oncanplay = () => ok(a);
    a.onerror = () => ok(null);
    a.src = 'musica.mp3';
    setTimeout(() => ok(null), 4000);
  });
}

/* ---------- Melodia gerada ---------- */
let ctx, mestre, eco, timer, proximo = 0, passo = 0;
const BPM = 84, COLCHEIA = 60 / BPM / 2;
// Ré menor pentatônica (D F G A C) em duas oitavas
const ESCALA = [146.83, 174.61, 196.0, 220.0, 261.63, 293.66, 349.23, 392.0, 440.0, 523.25];
let grau = 4;
// Ritmo de 2 compassos (16 colcheias): 1 = toca, 0 = pausa
const RITMO = [1,0,1,1, 1,0,1,0, 1,1,1,0, 1,0,0,0];

function iniciaContexto() {
  ctx = new (window.AudioContext || window.webkitAudioContext)();
  mestre = ctx.createGain(); mestre.gain.value = 0.0001;
  eco = ctx.createDelay(1.5); eco.delayTime.value = COLCHEIA * 3;
  const fb = ctx.createGain(); fb.gain.value = 0.28;
  const ecoVol = ctx.createGain(); ecoVol.gain.value = 0.35;
  eco.connect(fb); fb.connect(eco); eco.connect(ecoVol); ecoVol.connect(mestre);
  mestre.connect(ctx.destination);

  // Bordão suave (Ré + Lá graves)
  [73.42, 110.0].forEach((f, i) => {
    const o = ctx.createOscillator(), g = ctx.createGain();
    o.type = 'sine'; o.frequency.value = f; g.gain.value = i ? 0.025 : 0.035;
    const lfo = ctx.createOscillator(), lg = ctx.createGain();
    lfo.frequency.value = 0.08 + i * 0.05; lg.gain.value = 0.012;
    lfo.connect(lg); lg.connect(g.gain);
    o.connect(g); g.connect(mestre); o.start(); lfo.start();
  });
}

function dedilha(freq, t, vol = 0.22) {
  // corda: triângulo + seno uma oitava acima, ataque rápido e decaimento longo
  [[freq, 'triangle', vol], [freq * 2, 'sine', vol * 0.35]].forEach(([f, tipo, v]) => {
    const o = ctx.createOscillator(), g = ctx.createGain();
    o.type = tipo; o.frequency.setValueAtTime(f * 1.004, t); o.frequency.exponentialRampToValueAtTime(f, t + 0.08);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(v, t + 0.006);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 1.4);
    o.connect(g); g.connect(mestre); g.connect(eco);
    o.start(t); o.stop(t + 1.5);
  });
}

function gongo(t) {
  [[98, 0.18], [147.5, 0.09], [221, 0.05], [331, 0.03]].forEach(([f, v]) => {
    const o = ctx.createOscillator(), g = ctx.createGain();
    o.type = 'sine'; o.frequency.value = f;
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(v, t + 0.02);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 4.5);
    o.connect(g); g.connect(mestre); o.start(t); o.stop(t + 4.6);
  });
}

function agenda() {
  while (proximo < ctx.currentTime + 0.25) {
    const pos = passo % 16;
    if (passo % 64 === 0) gongo(proximo);
    if (RITMO[pos]) {
      // caminhada suave pela escala, voltando ao centro
      const salto = [-2, -1, -1, 0, 1, 1, 2][Math.floor(Math.random() * 7)];
      grau = Math.max(0, Math.min(ESCALA.length - 1, grau + salto));
      if (pos === 12) grau = [4, 3, 0][Math.floor(Math.random() * 3)]; // pouso no fim da frase
      dedilha(ESCALA[grau], proximo, pos % 4 === 0 ? 0.24 : 0.16);
      if (pos === 0 && Math.random() < 0.5) dedilha(ESCALA[grau] / 2, proximo, 0.12);
    }
    proximo += COLCHEIA * (pos % 2 ? 0.92 : 1.08); // leve balanço
    passo++;
  }
}

function tocaSintese() {
  if (!ctx) iniciaContexto();
  ctx.resume();
  proximo = ctx.currentTime + 0.1;
  mestre.gain.cancelScheduledValues(ctx.currentTime);
  mestre.gain.setTargetAtTime(0.9, ctx.currentTime, 0.4);
  agenda(); timer = setInterval(agenda, 60);
}
function paraSintese() {
  clearInterval(timer);
  mestre.gain.setTargetAtTime(0.0001, ctx.currentTime, 0.25);
}

/* ---------- Botão ---------- */
function atualizaBotao() {
  btn.classList.toggle('on', tocando);
  btn.setAttribute('aria-pressed', tocando);
  btn.setAttribute('aria-label', tocando ? 'Pausar música' : 'Tocar música');
  btn.querySelector('.ic').textContent = tocando ? '❚❚' : '♪';
}

const pronto = testaArquivo().then(a => { audio = a; modo = a ? 'arquivo' : 'sintese'; });

btn.addEventListener('click', async () => {
  if (dica) dica.classList.add('sumiu');
  if (!modo) { btn.classList.add('carregando'); await pronto; btn.classList.remove('carregando'); }
  tocando = !tocando;
  try {
    if (modo === 'arquivo') tocando ? await audio.play() : audio.pause();
    else tocando ? tocaSintese() : paraSintese();
  } catch (e) { tocando = false; }
  atualizaBotao();
});

// Esconde a dica depois de alguns segundos
setTimeout(() => dica && dica.classList.add('sumiu'), 7000);
// Pausa ao sair da aba
document.addEventListener('visibilitychange', () => {
  if (document.hidden && tocando) btn.click();
});
