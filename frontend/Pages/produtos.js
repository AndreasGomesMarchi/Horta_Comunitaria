const API_BASE = "http://127.0.0.1:8000"; // seu backend local

// Funções genéricas
async function fetchList(endpoint) {
    try {
        const res = await fetch(`${API_BASE}/${endpoint}`);
        if (!res.ok) throw new Error("Erro ao buscar dados");
        return await res.json();
    } catch (err) {
        console.error(err);
        return [];
    }
}

async function createItem(endpoint, dados) {
    try {
        const res = await fetch(`${API_BASE}/${endpoint}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados)
        });
        if (!res.ok) throw new Error("Erro ao criar item");
        return await res.json();
    } catch (err) {
        console.error(err);
        return null;
    }
}

async function updateItem(endpoint, dados) {
    try {
        const res = await fetch(`${API_BASE}/${endpoint}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados)
        });
        if (!res.ok) throw new Error("Erro ao atualizar item");
        return await res.json();
    } catch (err) {
        console.error(err);
        return null;
    }
}

async function deleteItem(endpoint) {
    try {
        const res = await fetch(`${API_BASE}/${endpoint}`, { method: "DELETE" });
        return res.ok;
    } catch (err) {
        console.error(err);
        return false;
    }
}

// Funções específicas de produto
async function carregarProdutos() {
    const produtos = await fetchList("produtos");
    const container = document.getElementById("produtos-list");
    container.innerHTML = produtos.map(p => `
        <div class="card" id="produto-${p.id_produto}">
            <strong>${p.nome}</strong> - ${p.tipo} - ${p.epoca_plantio || '-'} 
            <button onclick="editarProduto('${p.id_produto}')">Editar</button>
            <button onclick="removerProduto('${p.id_produto}')">Excluir</button>
        </div>
    `).join("");
}

async function criarProduto(dados) {
    const novo = await createItem("produtos", dados);
    return novo != null;
}

async function removerProduto(id) {
    const sucesso = await deleteItem(`produtos/${id}`);
    if (sucesso) carregarProdutos();
}

// Edição simples
async function editarProduto(id) {
    const nome = prompt("Novo nome do produto:");
    if (!nome) return;
    const tipo = prompt("Novo tipo (Verdura, Legume, Fruta, Hortaliça):");
    if (!tipo) return;
    const epoca = prompt("Nova época de plantio:");
    const sucesso = await updateItem(`produtos/${id}`, { nome, tipo, epoca_plantio: epoca });
    if (sucesso) carregarProdutos();
}
