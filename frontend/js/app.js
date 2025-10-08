// Initialise CodeMirror
let editor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
    lineNumbers: true,
    mode: "python", // coloration
    theme: "default"
});

// Fonction exécutée au clic sur "Run"
function runCode() {
    const code = editor.getValue();

    fetch("http://127.0.0.1:5000/run", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ code: code })
    })
    .then(response => response.json())
    .then(data => {
        const outputElement = document.getElementById("output");

        if (data.output) {
            outputElement.innerText = data.output;
        } else if (data.error) {
            outputElement.innerText = "Erreur : " + data.error;
        }

        // Afficher l'environnement (variables)
        const envElement = document.getElementById("env");
        if (data.env) {
            envElement.innerText = "Environnement :\n" + JSON.stringify(data.env, null, 2);
        }
    })
    .catch(error => {
        document.getElementById("output").innerText = "Erreur réseau : " + error;
    });
}

// Bouton Run
document.getElementById("run").addEventListener("click", runCode);
