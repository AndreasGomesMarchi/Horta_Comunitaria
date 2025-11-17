// ======================
// colheitas.js (com GET único e DELETE robusto)
// ======================

const BASE = "http://127.0.0.1:8000";

// ======================
// Buscar 1 colheita
// ======================
async function getColheita(id) {
    try {
        const res = await fetch(`${BASE}/colheitas/${id}`);
        if (!res.ok) {
            const text = await res.text();
            throw new Error(`Erro ao buscar colheita: ${res.status} ${text}`);
        }
        return await res.json();
    } catch (err) {
        alert(err.message);
        return null;
    }
}

// ======================
// Carregar colheitas (lista)
// ======================
async function carregarColheitas() {
    try {
        const response = await fetch(`${BASE}/colheitas`);
        if (!response.ok) {
            const txt = await response.text();
            throw new Error("Erro ao buscar colheitas: " + txt);
        }

        const colheitas = await response.json();
        const container = document.getElementById("colheitas-list");

        if (!Array.isArray(colheitas) || colheitas.length === 0) {
            container.innerHTML = "<p>Nenhuma colheita registrada.</p>";
            return;
        }

        container.innerHTML = colheitas.map(c => `
            <div class="card">
                🏷 <strong>ID Colheita:</strong> ${c.id_colheita}<br>
                🌿 <strong>Produto:</strong> ${c.id_produto}<br>
                📍 <strong>Parcela:</strong> ${c.id_parcela}<br>
                📅 <strong>Data:</strong> ${c.data_colheita}<br>
                ⚖ <strong>Quantidade:</strong> ${c.quantidade_kg} Kg<br><br>

                <button onclick="abrirEditarColheita(${c.id_colheita})">✏ Editar</button>
                <button onclick="removerColheita(${c.id_colheita})">🗑 Excluir</button>
            </div>
        `).join("");

    } catch (error) {
        alert(error.message);
    }
}

// ======================
// Criar Colheita
// ======================
async function criarColheita(dados) {
    try {
        const response = await fetch(`${BASE}/colheitas`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados)
        });

        if (!response.ok) {
            const err = await response.text();
            throw new Error("Erro ao criar colheita: " + err);
        }

        return true;
    } catch (error) {
        alert(error.message);
        return false;
    }
}

// ======================
// Abrir UI de edição (usa getColheita para preencher)
// ======================
async function abrirEditarColheita(id) {
    const item = await getColheita(id);
    if (!item) return;

    // aqui troquei pelo prompt simples como nos outros módulos
    const novaQtd = prompt("Quantidade (Kg):", item.quantidade_kg);
    if (novaQtd === null) return;

    const novoObj = {
        id_produto: item.id_produto,
        id_parcela: item.id_parcela,
        data_colheita: item.data_colheita,
        quantidade_kg: Number(novaQtd)
    };

    try {
        const res = await fetch(`${BASE}/colheitas/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(novoObj)
        });
        if (!res.ok) {
            const txt = await res.text();
            throw new Error("Erro ao atualizar colheita: " + txt);
        }
        alert("Colheita atualizada!");
        carregarColheitas();
    } catch (err) {
        alert(err.message);
    }
}

// ======================
// Remover Colheita (DELETE) — trata 204 corretamente
// ======================
async function removerColheita(id) {
    if (!confirm("Tem certeza que quer excluir esta colheita?")) return;

    try {
        const res = await fetch(`${BASE}/colheitas/${id}`, { method: "DELETE" });

        if (res.status === 204) {
            alert("Colheita removida!");
            carregarColheitas();
            return;
        }
        // Se não for 204, tenta ler body com erro
        const txt = await res.text();
        throw new Error(`Erro ao excluir: ${res.status} ${txt}`);
    } catch (err) {
        alert(err.message);
    }
}

// carregar ao abrir
document.addEventListener("DOMContentLoaded", carregarColheitas);
