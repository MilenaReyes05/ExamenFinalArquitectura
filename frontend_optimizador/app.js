
const apiBase = document.getElementById('apiBase');
const btnDocs = document.getElementById('btnDocs');
const capacidad = document.getElementById('capacidad');
const objetosBody = document.getElementById('objetosBody');
const agregarFila = document.getElementById('agregarFila');
const limpiar = document.getElementById('limpiar');
const optimizar = document.getElementById('optimizar');
const estado = document.getElementById('estado');
const resultados = document.getElementById('resultados');
const gananciaTotal = document.getElementById('gananciaTotal');
const pesoTotal = document.getElementById('pesoTotal');
const seleccionadosBody = document.getElementById('seleccionadosBody');
const enlaceOpenApi = document.getElementById('enlaceOpenApi');

function log(msg) {
  const ts = new Date().toLocaleTimeString();
  estado.textContent = `[${ts}] ${msg}\n` + estado.textContent;
}

function crearFila(nombre='', peso='', ganancia='') {
  const tr = document.createElement('tr');

  const tdNombre = document.createElement('td');
  const inpNombre = document.createElement('input');
  inpNombre.type = 'text';
  inpNombre.placeholder = 'Ej: Proyecto A';
  inpNombre.value = nombre;
  tdNombre.appendChild(inpNombre);

  const tdPeso = document.createElement('td');
  const inpPeso = document.createElement('input');
  inpPeso.type = 'number';
  inpPeso.min = '0';
  inpPeso.step = '1';
  inpPeso.placeholder = 'Ej: 2000';
  inpPeso.value = peso;
  tdPeso.appendChild(inpPeso);

  const tdGan = document.createElement('td');
  const inpGan = document.createElement('input');
  inpGan.type = 'number';
  inpGan.min = '0';
  inpGan.step = '1';
  inpGan.placeholder = 'Ej: 1500';
  inpGan.value = ganancia;
  tdGan.appendChild(inpGan);

  const tdAcc = document.createElement('td');
  const btnDel = document.createElement('button');
  btnDel.textContent = 'Eliminar';
  btnDel.className = 'secondary';
  btnDel.onclick = () => tr.remove();
  tdAcc.appendChild(btnDel);

  tr.appendChild(tdNombre);
  tr.appendChild(tdPeso);
  tr.appendChild(tdGan);
  tr.appendChild(tdAcc);

  objetosBody.appendChild(tr);
}

function leerObjetos() {
  const rows = [...objetosBody.querySelectorAll('tr')];
  return rows.map(r => {
    const [n, p, g] = r.querySelectorAll('input');
    return {
      nombre: String(n.value || '').trim(),
      peso: Number(p.value || 0),
      ganancia: Number(g.value || 0),
    };
  }).filter(o => o.nombre.length > 0);
}

function pintarResultados(data) {
  resultados.classList.remove('hidden');
  gananciaTotal.textContent = data.ganancia_total;
  pesoTotal.textContent = data.peso_total;
  seleccionadosBody.innerHTML = '';
  (data.seleccionados || []).forEach((nom, i) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${i+1}</td><td>${nom}</td>`;
    seleccionadosBody.appendChild(tr);
  });
}

async function doOptimizar() {
  const url = (apiBase.value || '').replace(/\/$/, '') + '/optimizar';
  const payload = {
    capacidad: Number(capacidad.value || 0),
    objetos: leerObjetos(),
  };

  log('Enviando POST ' + url + ' ...');
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const text = await res.text();
    let data;
    try { data = JSON.parse(text); } catch { data = { raw:text }; }
    if (!res.ok) {
      log('Error HTTP ' + res.status + ': ' + text);
      alert('Error ' + res.status + ': ' + text);
      return;
    }
    log('OK ' + res.status);
    pintarResultados(data);
  } catch (err) {
    console.error(err);
    log('Error de red: ' + err.message);
    alert('No se pudo conectar con la API. Revisa la URL o CORS.');
  }
}

function initDemo() {
  crearFila('A', 2000, 1500);
  crearFila('B', 4000, 3500);
  crearFila('C', 5000, 4000);
  crearFila('D', 3000, 2500);
  enlaceOpenApi.href = apiBase.value.replace(/\/$/, '') + '/openapi.json';
}

agregarFila.onclick = () => crearFila();
limpiar.onclick = () => { objetosBody.innerHTML = ''; resultados.classList.add('hidden'); };
optimizar.onclick = doOptimizar;
btnDocs.onclick = () => window.open(apiBase.value.replace(/\/$/, '') + '/docs', '_blank');

apiBase.addEventListener('change', () => {
  enlaceOpenApi.href = apiBase.value.replace(/\/$/, '') + '/openapi.json';
});

initDemo();
