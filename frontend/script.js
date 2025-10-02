document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('analyzeButton').addEventListener('click', async () => {
    const fileInput = document.getElementById('file');
    const textInput = document.getElementById('text');

    if (fileInput.files.length > 0) {
      const formData = new FormData();
      formData.append("file", fileInput.files[0]);
      await sendFormData(formData);
      fileInput.value = "";
      textInput.value = "";
    } else if (textInput.value.trim() !== '') {
      const formData = new FormData();
      formData.append("text", textInput.value);
      await sendFormData(formData);
      fileInput.value = "";
      textInput.value = "";
    } else {
      alert("Por favor, insira um texto ou selecione um arquivo.");
    }
  });

  async function sendFormData(formData) {
    try {
      const response = await fetch("/api/analyze/", {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      document.getElementById('resultado').classList.remove('hidden');
      document.getElementById('categoria').textContent = data.category;
      document.getElementById('resposta_sugerida').textContent = data.response;
    } catch (error) {
      console.error("Erro ao conectar com o backend:", error);
      alert("Ocorreu um erro ao conectar com o servidor.");
    }
  }

  function applyTheme(theme) {
    const html = document.documentElement;
    const button = document.getElementById("themeButton");
    if (theme === "dark") {
      html.classList.add("dark");
      html.classList.remove("light");
      button.innerHTML = "☀️ Alternar Tema";
      localStorage.setItem("theme", "dark");
    } else {
      html.classList.remove("dark");
      html.classList.add("light");
      button.innerHTML = "🌙 Alternar Tema";
      localStorage.setItem("theme", "light");
    }
  }

  window.toggleTheme = function () {
    const currentTheme = localStorage.getItem("theme") || "light";
    const newTheme = currentTheme === "light" ? "dark" : "light";
    applyTheme(newTheme);
  };

  const savedTheme = localStorage.getItem("theme") || "light";
  applyTheme(savedTheme);
});
