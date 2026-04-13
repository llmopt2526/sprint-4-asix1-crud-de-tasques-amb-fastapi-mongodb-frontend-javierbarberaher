const API_URL = "http://127.0.0.1:8000/movies";

async function loadMovies() {
    try {
        const res = await fetch(API_URL);
        const movies = await res.json();
        const list = document.getElementById('movieList');
        list.innerHTML = '';
        
        movies.forEach(m => {
            list.innerHTML += `
                <div class="movie-card">
                    <button class="delete-btn" onclick="deleteMovie('${m._id}')">X</button>
                    <strong>${m.titol}</strong> <span class="tag">${m.genere}</span>
                    <p style="margin: 5px 0;">${m.descripcio}</p>
                    <small>Estat: <b>${m.estat}</b> | Nota: ⭐ ${m.puntuacio}/5 | Penjada per: <i>${m.usuari}</i></small>
                </div>
            `;
        });
    } catch (error) {
        console.error("Error carregant pelis:", error);
    }
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
        alert("Ei! Omple almenys el títol i l'usuari!");
        return;
    }

    await fetch(API_URL, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(movie)
    });
    
    // Netejar formulari
    document.getElementById('titol').value = '';
    document.getElementById('desc').value = '';
    
    loadMovies(); 
}

async function deleteMovie(id) {
    if (confirm("Segur que vols esborrar aquesta peli?")) {
        await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
        loadMovies();
    }
}

// Càrrega inicial quan s'obre la pàgina
window.onload = loadMovies;