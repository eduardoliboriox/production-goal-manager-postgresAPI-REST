
async function calcularPCP() {
  const turnos = [];
  document.querySelectorAll('input[type=checkbox]:checked').forEach(c => {
    turnos.push(parseInt(c.value));
  });

  const payload = {
    total_op: document.getElementById("totalOp").value,
    produzido: document.getElementById("produzido").value,
    hora_inicio: document.getElementById("horaInicio").value,
    meta_hora: document.getElementById("metaHora").value,
    blank: document.getElementById("blank").value,
    turnos: turnos,
    refeicao: document.getElementById("refeicao").value === "true"
  };

  const r = await fetch("/api/pcp/calcular", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const data = await r.json();

  let html = "";

  if (data.conclusao) {
    html += `<h5 class="text-success">Conclusão prevista: ${data.conclusao}</h5>`;
  }

  if (data.timeline) {
    html += "<ul>";
    data.timeline.forEach(t => {
      html += `<li>${t.referencia} (${t.inicio} - ${t.fim}): ${t.produzido} placas</li>`;
    });
    html += "</ul>";
  }

  document.getElementById("resultadoPCP").innerHTML = html;
}

function limparPCP() {
  // inputs
  document.getElementById("totalOp").value = "";
  document.getElementById("produzido").value = "";
  document.getElementById("horaInicio").value = "";
  document.getElementById("metaHora").value = "";
  document.getElementById("blank").value = "";

  // checkboxes de turno
  document.querySelectorAll('input[type=checkbox]').forEach(c => {
    c.checked = false;
  });

  // refeição volta para "Não"
  document.getElementById("refeicao").value = "false";

  // limpa resultado
  document.getElementById("resultadoPCP").innerHTML = "";

  // foco no primeiro campo (UX profissional)
  document.getElementById("totalOp").focus();
}


