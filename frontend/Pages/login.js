async function login() {
    const email = document.getElementById("email").value.trim();
    const senha = document.getElementById("senha").value.trim();
    const msg = document.getElementById("msg");

    msg.textContent = ""; // limpa mensagens antigas

    if (!email || !senha) {
        msg.textContent = "Preencha email e senha!";
        return;
    }

    const formData = new FormData();
    formData.append("username", email); // O FastAPI exige esse nome
    formData.append("password", senha);

    try {
        const response = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            body: formData  // ⚠ NÃO colocar headers!
        });

        if (response.ok) {
    const data = await response.json();

    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("grupo_usuario", data.nome_grupo);  // <<< IMPORTANTE

    alert("Login efetuado com sucesso!");
    window.location.href = "index.html";
    }
    
        const data = await response.json();

        // Guarda o token para o resto do sistema
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("grupo_usuario", data.nome_grupo);

        alert("Login realizado com sucesso!");

        // 🔁 Redirecionar para a página principal do sistema
        window.location.href = "index.html"; // Troque se quiser

    } catch (error) {
        msg.textContent = "Erro ao conectar ao servidor!";
        console.error(error);
    }
}
