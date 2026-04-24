const API_URL = '/personajes';

function toggleCustomRaza(value, customInputId) {
    const customInput = document.getElementById(customInputId);
    if (value === 'Personalizada') {
        customInput.style.display = 'inline-block';
        customInput.required = true;
    } else {
        customInput.style.display = 'none';
        customInput.required = false;
    }
}

async function cargarPersonajes() {
    const res = await fetch(API_URL);
    const personajes = await res.json();
    const tbody = document.getElementById('tabla-body');
    const peleador1 = document.getElementById('peleador1');
    const peleador2 = document.getElementById('peleador2');
    
    tbody.innerHTML = '';
    peleador1.innerHTML = '<option value="">Selecciona Luchador 1</option>';
    peleador2.innerHTML = '<option value="">Selecciona Luchador 2</option>';

    personajes.forEach(p => {
        tbody.innerHTML += `
            <tr>
                <td>${p.id}</td>
                <td>${p.nombre}</td>
                <td>${p.raza}</td>
                <td>${p.color_piel}</td>
                <td>${p.fuerza}</td>
                <td>${p.agilidad}</td>
                <td>${p.magia}</td>
                <td>${p.conocimiento}</td>
                <td>
                    <button onclick="eliminarPersonaje(${p.id})">Eliminar</button>
                    <button onclick="editarPersonaje(${p.id})">Editar</button>
                </td>
            </tr>
        `;
        
        peleador1.innerHTML += `<option value="${p.id}">${p.nombre} (${p.raza})</option>`;
        peleador2.innerHTML += `<option value="${p.id}">${p.nombre} (${p.raza})</option>`;
    });

    // Actualizar JSON Viewer
    const jsonPre = document.getElementById('json-personajes');
    if (jsonPre) {
        jsonPre.textContent = JSON.stringify(personajes, null, 4);
    }
}

async function crearPersonaje() {
    let razaVal = document.getElementById('raza').value;
    if (razaVal === 'Personalizada') {
        razaVal = document.getElementById('raza_custom').value;
    }

    const nuevo = {
        nombre: document.getElementById('nombre').value,
        raza: razaVal,
        color_piel: document.getElementById('color_piel').value,
        fuerza: document.getElementById('fuerza').value,
        agilidad: document.getElementById('agilidad').value,
        magia: document.getElementById('magia').value,
        conocimiento: document.getElementById('conocimiento').value
    };

    await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(nuevo)
    });

    document.querySelectorAll('.form-container input').forEach(inp => inp.value = '');
    cargarPersonajes();
}

async function editarPersonaje(id) {
    // Obtenemos los datos actuales
    const res = await fetch(`${API_URL}/${id}`);
    const personaje = await res.json();
    
    // Llenamos el formulario modal
    document.getElementById('edit_id').value = personaje.id;
    document.getElementById('edit_nombre').value = personaje.nombre;
    
    // Logica para select y raza custom
    const razasComunes = ['Humano', 'Elfo', 'Orco', 'Enano'];
    if (razasComunes.includes(personaje.raza)) {
        document.getElementById('edit_raza').value = personaje.raza;
        toggleCustomRaza(personaje.raza, 'edit_raza_custom');
    } else {
        document.getElementById('edit_raza').value = 'Personalizada';
        toggleCustomRaza('Personalizada', 'edit_raza_custom');
        document.getElementById('edit_raza_custom').value = personaje.raza;
    }

    document.getElementById('edit_color_piel').value = personaje.color_piel;
    document.getElementById('edit_fuerza').value = personaje.fuerza;
    document.getElementById('edit_agilidad').value = personaje.agilidad;
    document.getElementById('edit_magia').value = personaje.magia;
    document.getElementById('edit_conocimiento').value = personaje.conocimiento;

    // Mostramos el modal
    document.getElementById('editarModal').style.display = "block";
}

function cerrarModal() {
    document.getElementById('editarModal').style.display = "none";
}

// Cerrar el modal si el usuario hace clic fuera de él
window.onclick = function(event) {
    const modal = document.getElementById('editarModal');
    if (event.target == modal) {
        cerrarModal();
    }
}

async function guardarEdicion() {
    const id = document.getElementById('edit_id').value;
    let razaVal = document.getElementById('edit_raza').value;
    if (razaVal === 'Personalizada') {
        razaVal = document.getElementById('edit_raza_custom').value;
    }

    const editado = {
        nombre: document.getElementById('edit_nombre').value,
        raza: razaVal,
        color_piel: document.getElementById('edit_color_piel').value,
        fuerza: document.getElementById('edit_fuerza').value,
        agilidad: document.getElementById('edit_agilidad').value,
        magia: document.getElementById('edit_magia').value,
        conocimiento: document.getElementById('edit_conocimiento').value
    };

    await fetch(`${API_URL}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(editado)
    });

    cerrarModal();
    cargarPersonajes();
}

async function eliminarPersonaje(id) {
    if(confirm('¿Eliminar personaje?')) {
        await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
        cargarPersonajes();
    }
}

async function simularCombate() {
    const id1 = document.getElementById('peleador1').value;
    const id2 = document.getElementById('peleador2').value;
    const resDiv = document.getElementById('resultado-combate');

    if(!id1 || !id2) {
        alert("Selecciona 2 luchadores.");
        return;
    }
    if (id1 === id2) {
        alert("Un personaje no puede luchar consigo mismo.");
        return;
    }

    resDiv.style.display = 'block';
    
    const divLog = document.getElementById('combate-structured');
    const jsonPre = document.getElementById('json-combate');
    
    divLog.innerHTML = "<em>Simulando combate...</em>";
    jsonPre.textContent = "Cargando...";

    const res = await fetch('/combate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id1, id2 })
    });
    
    const data = await res.json();
    
    if(data.error) {
        divLog.innerHTML = `<span style="color:red;">Error: ${data.error}</span>`;
        jsonPre.textContent = JSON.stringify(data, null, 4);
        return;
    }

    let htmlLog = `<h4 style="color: #5b8a62; font-size: 1.2em;">Ganador: ${data.ganador}</h4>`;
    htmlLog += `<ul style="font-family: 'Courier New', monospace; font-size: 14px; background: #fffcf9; padding: 15px; border: 1px solid #e8e5e1; border-radius: 8px; list-style: none;">`;
    data.log.forEach(linea => {
        htmlLog += `<li style="margin-bottom: 8px; border-bottom: 1px dashed #eee; padding-bottom: 4px;">${linea}</li>`;
    });
    htmlLog += `</ul>`;
    
    divLog.innerHTML = htmlLog;
    jsonPre.textContent = JSON.stringify(data, null, 4);
}

// Cargar personajes al abrir la página
cargarPersonajes();