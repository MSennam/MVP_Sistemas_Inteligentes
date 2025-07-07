const API_BASE = "http://127.0.0.1:5000";

// Função para carregar todos os vinhos
const classificarVinho = async () => {
  const vinho = {
    nome: document.getElementById("nome").value,
    fix_acid: parseFloat(document.getElementById("fix_acid").value),
    vol_acid: parseFloat(document.getElementById("vol_acid").value),
    cit_acid: parseFloat(document.getElementById("cit_acid").value),
    res_sugar: parseFloat(document.getElementById("res_sugar").value),
    chlorides: parseFloat(document.getElementById("chlorides").value),
    free_sulf: parseFloat(document.getElementById("free_sulf").value),
    total_sulf: parseFloat(document.getElementById("total_sulf").value),
    density: parseFloat(document.getElementById("density").value),
    ph: parseFloat(document.getElementById("ph").value),
    sulphates: parseFloat(document.getElementById("sulphates").value),
    alcohol: parseFloat(document.getElementById("alcohol").value)
  };

  // Validação simples: todos os campos devem ser preenchidos
  for (let key in vinho) {
    if (vinho[key] === "" || isNaN(vinho[key]) && key !== "nome") {
      alert("Por favor, preencha todos os campos corretamente.");
      return;
    }
  }

  try {
    const response = await fetch(`${API_BASE}/vinho`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(vinho)
    });

    const data = await response.json();

    if (response.ok) {
      alert(`Vinho classificado com sucesso! Qualidade: ${data.quality_pred} (${data.class_label})`);
      refreshList(); // atualiza a lista
    } else {
      alert(`Erro: ${data.message}`);
    }

  } catch (error) {
    console.error("Erro ao adicionar vinho:", error);
    alert("Erro inesperado ao tentar classificar o vinho.");
  }
};

// Cria botão de exclusão
const insertDeleteButton = (parent) => {
  let span = document.createElement("span");
  span.className = "close";
  span.innerHTML = "❌";
  parent.appendChild(span);
};

// Remove vinho da API e da tabela
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  for (let i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      const row = this.parentElement.parentElement;
      const nomeVinho = row.getElementsByTagName("td")[0].innerText;
      if (confirm(`Deseja remover o vinho "${nomeVinho}"?`)) {
        deleteItem(nomeVinho);
        row.remove();
      }
    };
  }
};

const deleteItem = (nome) => {
  fetch(`${API_BASE}/vinho?nome=${encodeURIComponent(nome)}`, {
    method: "delete",
  })
    .then((res) => res.json())
    .catch((error) => {
      console.error('Erro ao deletar vinho:', error);
    });
};

// Adiciona novo vinho à lista
const addVinho = async () => {
  const campos = [
    "fix_acid", "vol_acid", "cit_acid", "res_sugar",
    "chlorides", "free_sulf", "total_sulf", "density",
    "ph", "sulphates", "alcohol"
  ];

  const vinho = {};

  // Validação do campo "nome"
  const nome = document.getElementById("nome").value.trim();
  if (!nome) {
    alert("O campo 'nome' não pode estar vazio.");
    return;
  }
  vinho.nome = nome;

  // Validação dos campos numéricos
  for (let campo of campos) {
    const valor = document.getElementById(campo).value.trim();
    if (valor === "") {
      alert(`O campo '${campo}' não pode estar vazio.`);
      return;
    }

    const numero = parseFloat(valor);
    if (isNaN(numero)) {
      alert(`O valor no campo '${campo}' não é um número válido.`);
      return;
    }

    vinho[campo] = numero;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/vinho", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(vinho)
    });

    const result = await response.json();

    if (response.ok) {
      alert(`Vinho classificado como: ${result.class_label.toUpperCase()} (Qualidade ${result.quality_pred})`);
    } else {
      alert(`Erro: ${result.message}`);
    }
  } catch (error) {
    console.error("Erro ao classificar vinho:", error);
    alert("Erro de rede ao enviar vinho.");
  }
};
  // Validação básica
  if (!vinho.nome || Object.values(vinho).some(v => v === "" || isNaN(v))) {
    alert("Preencha corretamente todos os campos.");
    return;
  }

  fetch(`${API_BASE}/vinho`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(vinho)
  })
    .then((response) => response.json())
    .then((data) => {
      alert(`Vinho "${data.nome}" classificado como: ${data.class_label.toUpperCase()}`);
      refreshList();
      clearForm();
    })
    .catch((error) => {
      console.error("Erro ao adicionar vinho:", error);
    });
  

// Limpa os campos do formulário
const clearForm = () => {
  const ids = ["nome", "fix_acid", "vol_acid", "cit_acid", "res_sugar", "chlorides", "free_sulf", "total_sulf", "density", "ph", "sulphates", "alcohol"];
  ids.forEach(id => document.getElementById(id).value = "");
};

// Insere vinho na tabela
const insertList = (nome, quality_pred, class_label) => {
  const table = document.getElementById("tabelaVinhos");
  const row = table.insertRow();

  const nomeCell = row.insertCell(0);
  const notaCell = row.insertCell(1);
  const classeCell = row.insertCell(2);
  const deleteCell = row.insertCell(3);

  nomeCell.textContent = nome;
  notaCell.textContent = quality_pred;
  classeCell.textContent = class_label.toUpperCase();

  insertDeleteButton(deleteCell);
  removeElement();
};