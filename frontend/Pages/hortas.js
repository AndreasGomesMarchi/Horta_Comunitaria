// ====================================
//  🔐 VERIFICA SE ESTÁ LOGADO
// ====================================
const token = localStorage.getItem("access_token");
const grupo = (localStorage.getItem("grupo_usuario") || "").toUpperCase();


if (!token) {
    alert("Você precisa estar logado!");
    window.location.href = "login.html";
}

// ====================================
//  GET → LISTAR HORTAS
// ====================================
async function carregarHortas() {
    try {
        const response = await fetch("http://127.0.0.1:8000/hortas", {
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (!response.ok) throw new Error("Erro ao carregar hortas");

        const hortas = await response.json();
        const container = document.getElementById("hortas-list");

        if (hortas.length === 0) {
            container.innerHTML = "<p>Nenhuma horta cadastrada.</p>";
            return;
        }

        container.innerHTML = hortas.map(h => `
            <div class="card">
                <strong>${h.nome}</strong><br>
                📍 ${h.localizacao}<br>
                📅 Criada em: ${h.data_criacao}<br><br>

                ${
                    grupo === "ADMIN" ? `
                        <button onclick="editarHorta('${h.id_horta}', '${h.nome}', '${h.localizacao}')">✏ Editar</button>
                        <button onclick="removerHorta('${h.id_horta}')">🗑 Excluir</button>
                    `
                    : ""
                }
            </div>
        `).join("");

    } catch (erro) {
        alert(erro.message);
    }
}

// ====================================
//  POST → CRIAR HORTA (ADMIN)
// ====================================
async function criarHorta(dados) {
    if (grupo !== "ADMIN") {
        alert("Apenas administradores podem criar hortas!");
        return false;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/hortas", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(dados)
        });

        return response.ok;
    } catch {
        alert("Erro ao criar horta");
        return false;
    }
}

// ====================================
//  DELETE → REMOVER HORTA (ADMIN)
// ====================================
async function removerHorta(id) {
    if (grupo !== "ADMIN") return alert("Sem permissão!");
    if (!confirm("Tem certeza que deseja excluir esta horta?")) return;

    try {
        await fetch(`http://127.0.0.1:8000/hortas/${id}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        });

        carregarHortas();
    } catch {
        alert("Erro ao remover horta");
    }
}

// ====================================
//  PUT → EDITAR HORTA (ADMIN)
// ====================================
async function editarHorta(id, nomeAtual, localAtual) {
    if (grupo !== "ADMIN") return alert("Sem permissão!");

    const novoNome = prompt("Novo nome:", nomeAtual);
    if (!novoNome) return;

    const novaLoc = prompt("Nova localização:", localAtual);
    if (!novaLoc) return;

    try {
        await fetch(`http://127.0.0.1:8000/hortas/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                nome: novoNome,
                localizacao: novaLoc
            })
        });

        alert("Horta atualizada!");
        carregarHortas();
    } catch {
        alert("Erro ao editar horta!");
    }
}

document.addEventListener("DOMContentLoaded", carregarHortas);
