// Función para aplanar el árbol de marcadores (recursiva)
function obtenerUrls(nodos, lista = []) {
  nodos.forEach((nodo) => {
    if (nodo.url) {
      lista.push({
        title: nodo.title,
        url: nodo.url,
        dateAdded: nodo.dateAdded,
      });
    }
    if (nodo.children) {
      obtenerUrls(nodo.children, lista);
    }
  });
  return lista;
}

// Escuchar cuando se hace clic en el icono de la extensión (o al iniciar)
chrome.runtime.onInstalled.addListener(() => {
  chrome.bookmarks.getTree((arbol) => {
    const todosLosMarcadores = obtenerUrls(arbol);

    console.log(
      "Enviando " + todosLosMarcadores.length + " marcadores a Python...",
    );

    fetch("http://localhost:5000/recibir_todos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ marcadores: todosLosMarcadores }),
    })
      .then((res) => res.json())
      .then((data) => console.log("Servidor respondió:", data))
      .catch((err) => console.error("Error:", err));
  });
});
