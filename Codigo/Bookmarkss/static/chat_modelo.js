const messages = document.getElementById("messages");
const prompt = document.getElementById("prompt");
const sendBtn = document.getElementById("sendBtn");
const usarMarcadores = document.getElementById("usarMarcadores");

function addMessage(role, text) {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.textContent = `${role === "user" ? "Tú" : "Modelo"}: ${text}`;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

async function enviar() {
  const text = prompt.value.trim();
  if (!text) return;

  addMessage("user", text);
  prompt.value = "";
  sendBtn.disabled = true;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        pregunta: text,
        incluir_marcadores: usarMarcadores.checked,
      }),
    });

    const data = await res.json();
    if (!res.ok) {
      addMessage(
        "assistant",
        `Error: ${data.error || "No se pudo procesar la solicitud."}`,
      );
      return;
    }

    addMessage("assistant", data.respuesta || "[Sin respuesta]");
  } catch (err) {
    addMessage("assistant", `Error de conexión: ${err.message}`);
  } finally {
    sendBtn.disabled = false;
  }
}

sendBtn.addEventListener("click", enviar);
prompt.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    enviar();
  }
});
