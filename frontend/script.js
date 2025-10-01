document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('analyzeButton').addEventListener('click', async () => {
    const fileInput = document.getElementById('file');
    const textInput = document.getElementById('text');
    let emailContent = '';

    if (fileInput.files.length > 0) {
      const file = fileInput.files[0];
      const reader = new FileReader();
      reader.onload = async function () {
        emailContent = reader.result;
        await sendEmailContent(emailContent);
      };
      reader.readAsText(file);
    } else if (textInput.value.trim() !== '') {
      emailContent = textInput.value;
      await sendEmailContent(emailContent);
    } else {
      alert("Por favor, insira um texto ou selecione um arquivo.");
    }
  });

  async function sendEmailContent(content) {
    const formData = new FormData();
    formData.append("text", content);

    try {
      const response = await fetch('http://127.0.0.1:8000/analyze/', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      document.getElementById('resultado').style.display = 'block';
      document.getElementById('categoria').textContent = data.category;
      document.getElementById('resposta_sugerida').textContent = data.response;
    } catch (error) {
      console.error("Erro ao conectar com o backend:", error);
      alert("Ocorreu um erro ao conectar com o servidor.");
    }
  }
});
