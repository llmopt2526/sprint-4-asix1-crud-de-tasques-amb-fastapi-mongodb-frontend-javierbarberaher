const API_URL = "http://127.0.0.1:8000/movies";
const USER_API_URL = "http://127.0.0.1:8000/users";

let allMovies = [];

async function loadMovies() {
    try {
        const res = await fetch(API_URL);
        allMovies = await res.json();
        renderMovies(allMovies); // Cridem a la funció que les dibuixa
    } catch (error) {
        console.error("Error carregant pelis:", error);
    }
}

function renderMovies(moviesToDisplay) {
    const list = document.getElementById('movieList');
    list.innerHTML = '';
    
    moviesToDisplay.forEach(m => {
        const estatColor = m.estat === 'vista' ? '#28a745' : '#ff9900';
        
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

function filterMovies() {
    const textGenere = document.getElementById('filterGenere').value.toLowerCase();
    const notaSeleccionada = document.getElementById('filterNota').value;

    const filtered = allMovies.filter(m => {
        const matchGenere = m.genere.toLowerCase().includes(textGenere);
        
        let matchNota = true;
        if (notaSeleccionada !== "totes") {
            matchNota = m.puntuacio === parseInt(notaSeleccionada);
        }

        return matchGenere && matchNota;
    });

    renderMovies(filtered);
}

function clearFilters() {
    document.getElementById('filterGenere').value = '';
    document.getElementById('filterNota').value = 'totes';
    renderMovies(allMovies);
}

async function addMovie() {
    const movie = {
        titol: document.getElementById('titol').value,
        descripcio: document.getElementById('desc').value,
        estat: document.getElementById('estat').value,
        puntuacio: parseInt(document.getElementById('puntuacio').value),
        genere: document.getElementById('genere').value,
        usuari: document.getElementById('usuari').value
    };

    if (!movie.titol || !movie.usuari) {
        alert("Falten dades!");
        return;
    }

    const res = await fetch(API_URL, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(movie)
    });

    if (res.ok) {
        document.getElementById('titol').value = '';
        document.getElementById('desc').value = '';
        loadMovies(); 
    } else {
        const errorData = await res.json();
        alert("Error: " + errorData.detail);
    }
}

async function toggleStatus(id) {
    const res = await fetch(`${API_URL}/${id}/toggle-status`, { method: 'PATCH' });
    if (res.ok) loadMovies();
}

async function deleteMovie(id) {
    if (confirm("Segur que vols esborrar-la?")) {
        await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
        loadMovies();
    }
}

async function createUser() {
    const username = document.getElementById('new_username').value;
    const email = document.getElementById('new_email').value;

    if (!username || !email) return alert("Falten dades!");

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

window.onload = loadMovies;