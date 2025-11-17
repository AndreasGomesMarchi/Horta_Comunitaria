// Função para buscar a lista de parcelas do backend
async function carregarParcelas() {
    try {
        const response = await fetch("http://127.0.0.1:8000/parcelas"); // URL do backend
        if (!response.ok) throw new Error("Erro ao buscar parcelas");
        const parcelas = await response.json();

        const container = document.getElementById("parcelas-list");
        if (parcelas.length === 0) {
            container.innerHTML = "<p>Nenhuma parcela cadastrada.</p>";
            return;
        }

        container.innerHTML = parcelas.map(p => `
            <div class="card">
                <strong>ID: ${p.id_parcela}</strong> - ${p.localizacao} - ${p.tamanho} m² - ${p.status}
                <button onclick="removerParcela(${p.id_parcela})">Excluir</button>
                <button onclick="editarParcela(${p.id_parcela}, '${p.localizacao}', ${p.tamanho}, '${p.status}')">Editar</button>
            </div>
        `).join("");
    } catch (error) {
        alert(error.message);
    }
}

// Função para criar parcela
async function criarParcela(dados) {
    try {
        const response = await fetch("http://127.0.0.1:8000/parcelas", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados)
        });
        if (!response.ok) throw new Error("Erro ao criar parcela");
        await response.json(); // para consumir a resposta
        return true;
    } catch (error) {
        alert(error.message);
        return false;
    }
}

// Função para remover parcela
async function removerParcela(id) {
    if (!confirm("Deseja realmente excluir esta parcela?")) return;
    try {
        const response = await fetch(`http://127.0.0.1:8000/parcelas/${id}`, {
            method: "DELETE"
        });
        if (!response.ok) throw new Error("Erro ao excluir parcela");
        carregarParcelas();
    } catch (error) {
        alert(error.message);
    }
}

// Função para editar parcela
async function editarParcela(id, localizacaoAtual, tamanhoAtual, statusAtual) {
    const novaLocalizacao = prompt("Nova localização:", localizacaoAtual);
    if (novaLocalizacao === null) return;

    const novoTamanho = parseFloat(prompt("Novo tamanho (m²):", tamanhoAtual));
    if (isNaN(novoTamanho)) {
        alert("Tamanho inválido!");
        return;
    }

    const novoStatus = prompt("Novo status (Livre, Cultivando, Em Repouso):", statusAtual);
    if (!novoStatus) return;

    try {
        const response = await fetch(`http://127.0.0.1:8000/parcelas/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                localizacao: novaLocalizacao,
                tamanho: novoTamanho,
                status: novoStatus
            })
        });
        if (!response.ok) throw new Error("Erro ao atualizar parcela");
        await response.json();
        carregarParcelas();
        alert("Parcela atualizada com sucesso!");
    } catch (error) {
        alert(error.message);
    }
}