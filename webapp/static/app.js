document.getElementById('boyDate').value = '';
document.getElementById('girlDate').value = '';
document.getElementById('boyTime').value = '';
document.getElementById('girlTime').value = '';

function formatTimezoneOffset() {
  const offsetMinutes = -new Date().getTimezoneOffset();
  const sign = offsetMinutes >= 0 ? '+' : '-';
  const absMinutes = Math.abs(offsetMinutes);
  const hours = String(Math.floor(absMinutes / 60)).padStart(2, '0');
  const minutes = String(absMinutes % 60).padStart(2, '0');
  return `${sign}${hours}:${minutes}`;
}

document.getElementById('checkBtn').addEventListener('click', async () => {
  const boy = document.getElementById('boy').value.trim();
  const girl = document.getElementById('girl').value.trim();
  if (!boy || !girl) {
    alert('दोनों नाम डालें.');
    return;
  }

  const tz = formatTimezoneOffset();
  const boyDate = document.getElementById('boyDate').value;
  const boyTime = document.getElementById('boyTime').value;
  const girlDate = document.getElementById('girlDate').value;
  const girlTime = document.getElementById('girlTime').value;

  const payload = {
    boy: { name: boy, date: boyDate, time: boyTime, timezone: tz },
    girl: { name: girl, date: girlDate, time: girlTime, timezone: tz },
  };

  const btn = document.getElementById('checkBtn');
  btn.disabled = true;
  btn.textContent = 'जांच रहा है...';
  try {
    const res = await fetch('/api/milan', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    showResult(data);
  } catch (e) {
    alert('Server error: ' + e.message);
  } finally {
    btn.disabled = false;
    btn.textContent = 'मिलान करें';
  }
});

function showResult(data){
  const section = document.getElementById('result');
  const tbody = document.querySelector('#kootTable tbody');
  tbody.innerHTML = '';
  if (data.error){
    alert(data.error);
    return;
  }
  // Fill summary
  document.getElementById('score').textContent = data.total_gunas || '';
  document.getElementById('percent').textContent = data.percentage || '';
  document.getElementById('outcome').textContent = data.result || '';

  const asht = data.ashtakoot || {};
  for (const [k,v] of Object.entries(asht)){
    const tr = document.createElement('tr');
    const a = document.createElement('td'); a.textContent = k;
    const b = document.createElement('td'); b.textContent = v;
    tr.appendChild(a); tr.appendChild(b); tbody.appendChild(tr);
  }

  const doshasEl = document.getElementById('doshas');
  doshasEl.innerHTML = '';
  (data.doshas||[]).forEach(d=>{
    const p = document.createElement('div'); p.textContent = d; doshasEl.appendChild(p);
  });

  section.classList.remove('hidden');
  // scroll to results on mobile
  section.scrollIntoView({behavior:'smooth'});
}
