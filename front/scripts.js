const API_BASE = "http://127.0.0.1:5000";

const classificarVinho = async () => {
  
    console.log("Valor lido do campo 'nome':", document.getElementById("nome").value);

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

     console.log("Objeto 'vinho' a ser enviado:", vinho);
    
    if (vinho.nome.trim() === "") {
        alert("O campo 'nome' não pode estar vazio.");
        return;
    }
    for (const key in vinho) {
        if (key === "nome") {
            continue;
        }
                
        if (isNaN(vinho[key])) {
            alert(`Por favor, preencha o campo '${key}' com um número válido.`);
            return;
        }
    }
    
    //Envia os dados para a API usando o método POST
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
            clearForm();
            refreshList(); // Atualiza a lista na tela
        } else {
            // Exibe a mensagem de erro retornada pela API (ex: "Vinho já registrado")
            alert(`Erro: ${data.message}`);
        }

    } catch (error) {
        console.error("Erro ao adicionar vinho:", error);
        alert("Erro inesperado ao tentar classificar o vinho.");
    }
};

const refreshList = async () => {
    try {
        const response = await fetch(`${API_BASE}/vinhos`);
        const data = await response.json();

        const tableBody = document.getElementById("tabelaVinhos");
        // Limpa a tabela antes de adicionar os novos itens
        tableBody.innerHTML = "";

        // Itera sobre a lista de vinhos e adiciona cada um na tabela
        data.vinhos.forEach(vinho => {
            insertList(vinho.nome, vinho.quality_pred, vinho.class_label, vinho.id);
        });

    } catch (error) {
        console.error("Erro ao carregar a lista de vinhos:", error);
        alert("Não foi possível carregar a lista de vinhos.");
    }
};

const insertList = (nome, quality_pred, class_label, id) => {
    const table = document.getElementById("tabelaVinhos");
    const row = table.insertRow();

    row.setAttribute('data-vinho-id', id);

    const nomeCell = row.insertCell(0);
    const notaCell = row.insertCell(1);
    const classeCell = row.insertCell(2);
    const deleteCell = row.insertCell(3);

    nomeCell.textContent = nome;
    notaCell.textContent = quality_pred;
    classeCell.textContent = class_label.toUpperCase();

    insertDeleteButton(deleteCell, nome);
};

const insertDeleteButton = (parent, nomeVinho) => {
    let span = document.createElement("span");
    span.className = "close";
    span.innerHTML = "❌";
    span.onclick = () => {
        
        if (confirm(`Deseja remover o vinho "${nomeVinho}"?`)) {
            deleteItem(nomeVinho, parent.parentElement);
        }
    };
    parent.appendChild(span);
};

const deleteItem = async (nome, rowElement) => {
    try {
        const response = await fetch(`${API_BASE}/vinho?nome=${encodeURIComponent(nome)}`, {
            method: "DELETE",
        });
        const data = await response.json();
        if (response.ok) {
            alert(data.message);
            rowElement.remove(); // Remove a linha da tabela
        } else {
            alert(`Erro ao remover: ${data.message}`);
        }
    } catch (error) {
        console.error('Erro ao deletar vinho:', error);
        alert("Erro de comunicação ao tentar remover o vinho.");
    }
};

const clearForm = () => {
    const ids = ["nome", "fix_acid", "vol_acid", "cit_acid", "res_sugar", "chlorides", "free_sulf", "total_sulf", "density", "ph", "sulphates", "alcohol"];
    ids.forEach(id => document.getElementById(id).value = "");
};

// --- Execução Inicial ---
// Carrega a lista de vinhos assim que o script é executado.
document.addEventListener('DOMContentLoaded', refreshList);
