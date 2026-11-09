/* PusatRiset Data: filter katalog auto-submit + formulir sanggahan. Tanpa dependensi. */
(function () {
  document.addEventListener('change', function (e) {
    var t = e.target;
    if (t && t.hasAttribute && t.hasAttribute('data-autosubmit') && t.form) t.form.submit();
  });
  document.addEventListener('focusout', function (e) {
    var t = e.target;
    if (t && t.hasAttribute && t.hasAttribute('data-autosubmit-blur') && t.form && t.defaultValue !== t.value) t.form.submit();
  });
  document.addEventListener('keydown', function (e) {
    var t = e.target;
    if (e.key === 'Enter' && t && t.hasAttribute && t.hasAttribute('data-autosubmit-blur') && t.form) { e.preventDefault(); t.form.submit(); }
  });
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f || !f.matches || !f.matches('.pr-dispute form')) return;
    e.preventDefault();
    var msg = f.querySelector('.pr-dispute-msg'), btn = f.querySelector('button[type=submit]');
    var body = { paperId: f.getAttribute('data-paper') };
    new FormData(f).forEach(function (v, k) { body[k] = v; });
    btn.disabled = true; msg.textContent = 'Mengirim...';
    fetch(f.getAttribute('data-endpoint'), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (r) { msg.textContent = r.ok ? 'Terima kasih, sanggahan Anda telah diterima.' : (r.j.message || 'Gagal mengirim.'); if (r.ok) f.reset(); })
      .catch(function () { msg.textContent = 'Gagal mengirim.'; })
      .then(function () { btn.disabled = false; });
  });
})();
