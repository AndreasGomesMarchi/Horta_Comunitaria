const API_BASE = "http://127.0.0.1:8000"; // seu backend local

// ---------------------------
// Funções de fetch genéricas
// ---------------------------
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

// ---------------------------
// Funções específicas de usuário
// ---------------------------
async function carregarUsuarios() {
    const usuarios = await fetchList("usuarios");
    const container = document.getElementById("usuarios-list");
    container.innerHTML = usuarios.map(u => `
        <div class="card" id="usuario-${u.id_usuario}">
            <strong>${u.nome}</strong> - ${u.email} - ${u.telefone} 
            <button onclick="editarUsuario('${u.id_usuario}')">Editar</button>
            <button onclick="removerUsuario('${u.id_usuario}')">Excluir</button>
        </div>
    `).join("");
}

async function criarUsuario(dados) {
    const novo = await createItem("usuarios", dados);
    return novo != null;
}

async function removerUsuario(id) {
    const sucesso = await deleteItem(`usuarios/${id}`);
    if (sucesso) carregarUsuarios();
}

// Formulário de edição (simples)
async function editarUsuario(id) {
    const nome = prompt("Novo nome:");
    if (!nome) return;
    const sucesso = await updateItem(`usuarios/${id}`, { nome });
    if (sucesso) carregarUsuarios();
}
