// ======================
// Função para pegar o token
// ======================
function getToken() {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Você precisa fazer login!");
        window.location.href = "login.html";
        return null;
    }
    return token;
}

// ======================
// Carregar eventos
// ======================
async function carregarEventos() {
    const token = getToken();
    if (!token) return;

    try {
        const response = await fetch("http://127.0.0.1:8000/eventos", {
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (!response.ok) throw new Error("Erro ao buscar eventos");

        const eventos = await response.json();
        const container = document.getElementById("eventos-list");

        if (eventos.length === 0) {
            container.innerHTML = "<p>Nenhum evento cadastrado.</p>";
            return;
        }

        container.innerHTML = eventos.map(e => `
            <div class="card">
                <strong>${e.nome}</strong><br>
                📅 ${e.data_evento}<br>
                📍 ${e.local_evento}<br>
                📝 ${e.descricao ?? "Sem descrição"}<br><br>

                <button onclick="editarEvento(${e.id_evento}, '${e.nome}', '${e.data_evento}', '${e.descricao ?? ""}', '${e.local_evento}')">
                    ✏ Editar
                </button>

                <button onclick="removerEvento(${e.id_evento})">
                    🗑 Excluir
                </button>
            </div>
        `).join("");

    } catch (error) {
        alert(error.message);
    }
}

// ======================
// Criar evento
// ======================
async function criarEvento(dados) {
    const token = getToken();
    if (!token) return;

    try {
        const response = await fetch("http://127.0.0.1:8000/eventos", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}` 
            },
            body: JSON.stringify(dados)
        });

        if (!response.ok) throw new Error("Erro ao criar evento");

        alert("Evento criado com sucesso!");
        carregarEventos();
        return true;

    } catch (error) {
        alert(error.message);
        return false;
    }
}

// ======================
// Remover evento
// ======================
async function removerEvento(id) {
    const token = getToken();
    if (!token) return;

    if (!confirm("Tem certeza que deseja excluir este evento?")) return;

    try {
        const response = await fetch(`http://127.0.0.1:8000/eventos/${id}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (!response.ok) throw new Error("Erro ao excluir evento");

        alert("Evento removido!");
        carregarEventos();

    } catch (error) {
        alert(error.message);
    }
}

// ======================
// Editar
