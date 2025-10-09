// Initialise CodeMirror
let editor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
    lineNumbers: true,
    mode: "python",
    theme: "default"
});

// Choix automatique selon l’environnement
const API_URL =
    window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
        ? "http://127.0.0.1:5000"
        : "http://195.15.242.197:5000";  // IP publique de la VM

// Fonction exécutée au clic sur "Run"
function runCode() {
    const code = editor.getValue();

    fetch(`${API_URL}/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: code })
    })
        .then(response => response.json())
        .then(data => {
            const outputElement = document.getElementById("output");

            if (data.output) outputElement.innerText = data.output;
            else if (data.error) outputElement.innerText = "Erreur : " + data.error;

            const envElement = document.getElementById("env");
            if (data.env)
                envElement.innerText = "Environnement :\n" + JSON.stringify(data.env, null, 2);
        })
        .catch(error => {
            document.getElementById("output").innerText = "Erreur réseau : " + error;
        });
}

// Bouton Run
document.getElementById("run").addEventListener("click", runCode);
