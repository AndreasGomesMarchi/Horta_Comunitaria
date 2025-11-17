// ======================
// Carregar cultivos
// ======================
async function carregarCultivos() {
    try {
        const response = await fetch("http://127.0.0.1:8000/cultivos");
        if (!response.ok) throw new Error("Erro ao buscar cultivos");

        const cultivos = await response.json();
        const container = document.getElementById("cultivos-list");

        if (cultivos.length === 0) {
            container.innerHTML = "<p>Nenhum cultivo registrado.</p>";
            return;
        }

        container.innerHTML = cultivos.map(c => `
            <div class="card">
                🌿 <strong>Produto:</strong> ${c.id_produto}<br>
                🏷 <strong>Parcela:</strong> ${c.id_parcela}<br>
                📅 <strong>Plantio:</strong> ${c.data_plantio}<br>
                📌 <strong>Status:</strong> ${c.status_cultivo}<br><br>

                <button onclick="atualizarStatus(${c.id_produto}, ${c.id_parcela}, '${c.data_plantio}', '${c.status_cultivo}')">
                    ✏ Atualizar Status
                </button>

                <button onclick="removerCultivo(${c.id_produto}, ${c.id_parcela}, '${c.data_plantio}')">
                    🗑 Excluir
                </button>
            </div>
        `).join("");

    } catch (error) {
        alert(error.message);
    }
}


// ======================
// Criar cultivo
// ======================
async function criarCultivo(dados) {
    try {
        const response = await fetch("http://127.0.0.1:8000/cultivos", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados)
        });

        if (!response.ok) {
            const err = await response.text();
            throw new Error("❌ Erro ao criar cultivo: " + err);
        }

        alert("Cultivo criado com sucesso!");
        carregarCultivos();
        return true;
    } catch (error) {
        alert(error.message);
        return false;
    }
}


// ======================
// Atualizar status
// ======================
async function atualizarStatus(id_produto, id_parcela, data_plantio, statusAtual) {
    const novoStatus = prompt(
        `Status atual: ${statusAtual}\nDigite novo status:\n- Plantado\n- Crescendo\n- ProntoParaColheita\n- Colhido`,
        statusAtual
    );

    if (!novoStatus) return;

    try {
        const response = await fetch(`http://127.0.0.1:8000/cultivos/${id_produto}/${id_parcela}/${data_plantio}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status_cultivo: novoStatus })
        });

        if (!response.ok) throw new Error("Erro ao atualizar cultivo");

        alert("Cultivo atualizado!");
        carregarCultivos();
    } catch (error) {
        alert(error.message);
    }
}


// ======================
// Remover cultivo
// ======================
async function removerCultivo(id_produto, id_parcela, data_plantio) {
    if (!confirm("Tem certeza que deseja excluir este cultivo?")) return;

    try {
        const response = await fetch(`http://127.0.0.1:8000/cultivos/${id_produto}/${id_parcela}/${data_plantio}`, {
            method: "DELETE"
        });

        if (!response.ok) throw new Error("Erro ao excluir cultivo");

        alert("Cultivo removido!");
        carregarCultivos();
    } catch (error) {
        alert(error.message);
    }
}


// 🔄 Carregar ao abrir página
document.addEventListener("DOMContentLoaded", carregarCultivos);
