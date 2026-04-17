//Les URL de la API.
const API_URL = "http://127.0.0.1:8000/movies";
const USER_API_URL = "http://127.0.0.1:8000/users";
// Variable global per guardar les pelis que venen de la base de dades.
// S'utilitza per poder filtrar pelicules sense tenir que demanar-les a l'API cada cop que les filtrem.
let allMovies = [];
// Funció per a demanar les pel·lícules a la API.
async function loadMovies() {
    try {
        const res = await fetch(API_URL); // Petició GET.
        allMovies = await res.json(); // Convertir GET a JSON.
        renderMovies(allMovies); // Crida a la funció per renderitzar les pelicules al HTML.
    } catch (error) {
        console.error("Error carregant pelis:", error); // Missatge d'error.
    }
}
// Funció que genera el contingut visual desde el array de dades de pel·lícules.
function renderMovies(moviesToDisplay) {
    const list = document.getElementById('movieList');
    list.innerHTML = ''; // Netega la llista abans de tornar a dibuixar per evitar duplicats.
    
    moviesToDisplay.forEach(m => {
        // Cambía el color del text depenent de si la pel·lícula esta vista o no.
        const estatColor = m.estat === 'vista' ? '#28a745' : '#ff9900';
        // Injecta el codi HTML dins del div 'movieList'
        list.innerHTML += `
            <div class="movie-card">
                <button class="delete-btn" onclick="deleteMovie('${m._id}')">X</button>
                <strong>${m.titol}</strong> <span class="tag">${m.genere}</span>
                <p style="margin: 5px 0;">${m.descripcio}</p>
                <div style="margin-bottom: 8px;">
                    <small>
                        Estat: <b style="color: ${estatColor}">${m.estat}</b> 
                        <button style="padding: 2px 8px; font-size: 11px; margin-left: 10px; cursor:pointer;" 
                                onclick="toggleStatus('${m._id}')">Canviar estat</button>
                    </small>
                </div>
                <small>Nota: ${m.puntuacio}/5 | Penjada per: <i>${m.usuari}</i></small>
            </div>
        `;
    });
}
// Filtra les pel·lícules segons el que l'usuari escriu o selecciona.
function filterMovies() {
    // Defineix el valors d'input del usuari.
    const textGenere = document.getElementById('filterGenere').value.toLowerCase();
    const notaSeleccionada = document.getElementById('filterNota').value;

    const filtered = allMovies.filter(m => {
        // Comprova si el gènere coincideix parcialment amb el text escrit.
        const matchGenere = m.genere.toLowerCase().includes(textGenere);
        // Comprova quina nota hem seleccionat.
        let matchNota = true;
        if (notaSeleccionada !== "totes") {
            matchNota = m.puntuacio === parseInt(notaSeleccionada);
        }

        return matchGenere && matchNota; // Només retorna les pel·lícules que compleixen les dues condicions.
    });

    renderMovies(filtered); // Redibuixem la llista només amb les filtrades.
}
// Funció per a tornar els valors de busqueda als per defecte.
function clearFilters() {
    document.getElementById('filterGenere').value = '';
    document.getElementById('filterNota').value = 'totes';
    renderMovies(allMovies); // Redibuixem la llista
}
// Funció que recull les dades del formulari i les envia a l'API.
async function addMovie() {
    const movie = {
        titol: document.getElementById('titol').value,
        descripcio: document.getElementById('desc').value,
        estat: document.getElementById('estat').value,
        puntuacio: parseInt(document.getElementById('puntuacio').value),
        genere: document.getElementById('genere').value,
        usuari: document.getElementById('usuari').value
    };
    // Comprova que estan totes les dades.
    if (!movie.titol || !movie.usuari) {
        alert("Falten dades!");
        return;
    }
    
    const res = await fetch(API_URL, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(movie) // Converteix l'objecte JS a text JSON.
    });

    if (res.ok) {
        // Netega els camps del formulari si ha anat bé.
        document.getElementById('titol').value = '';
        document.getElementById('desc').value = '';
        loadMovies(); // Torna a carregar les pelis.
    } else {
        const errorData = await res.json();
        alert("Error: " + errorData.detail);
    }
}
// Funció que crida a l'endpoint que hem creat per alternar entre 'vista' i 'pendent'.
async function toggleStatus(id) {
    const res = await fetch(`${API_URL}/${id}/toggle-status`, { method: 'PATCH' });
    if (res.ok) loadMovies();
}
// Funció per eliminar una pel·lícula.
async function deleteMovie(id) {
    if (confirm("Segur que vols esborrar-la?")) {
        await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
        loadMovies();
    }
}
// Funció per crear Usuaris.
async function createUser() {
    const username = document.getElementById('new_username').value;
    const email = document.getElementById('new_email').value;
    // Comprova que estan totes les dades.
    if (!username || !email) return alert("Falten dades!");
    // Post del nou uusari.
    const res = await fetch(USER_API_URL, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ username, email })
    });

    if (res.ok) {
        alert(`Usuari ${username} registrat!`);
        document.getElementById('new_username').value = '';
        document.getElementById('new_email').value = '';
    } else {
        alert("L'usuari ja existeix o dades invàlides.");
    }
}
// Quan la finestra s'acaba de carregar, demana les pelis a l'API per primer cop
window.onload = loadMovies;
