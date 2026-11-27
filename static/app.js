// ---------- Configuración de cada sección ----------
const SECCIONES = {
clientes: {
    titulo: "Clientes",
    singular: "cliente",
    ruta: "/clientes/",
    campos: [
    { nombre: "nombre", etiqueta: "Nombre", tipo: "text", requerido: true },
    { nombre: "telefono", etiqueta: "Teléfono", tipo: "text", requerido: true },
    { nombre: "correo", etiqueta: "Correo", tipo: "email" },
    { nombre: "direccion", etiqueta: "Dirección", tipo: "text" },
    ],
},
productos: {
    titulo: "Productos",
    singular: "producto",
    ruta: "/productos/",
    campos: [
    { nombre: "nombre", etiqueta: "Nombre", tipo: "text", requerido: true },
    {
        nombre: "tipo", etiqueta: "Tipo", tipo: "select", requerido: true,
        opciones: ["pastel", "cupcake", "galleta", "postre", "otro"],
    },
    { nombre: "precio_base", etiqueta: "Precio base (L)", tipo: "number", paso: "0.01", requerido: true },
    ],
},
ingredientes: {
    titulo: "Ingredientes",
    singular: "ingrediente",
    ruta: "/ingredientes/",
    campos: [
    { nombre: "nombre", etiqueta: "Nombre", tipo: "text", requerido: true },
    { nombre: "unidad", etiqueta: "Unidad (kg, litro, unidad...)", tipo: "text", requerido: true },
    { nombre: "existencia", etiqueta: "Existencia", tipo: "number", paso: "any", requerido: true },
    ],
},
};

// ---------- Estado ----------
let token = sessionStorage.getItem("token");
let seccion = "clientes";
let registros = [];
let editandoId = null;
let temporizadorBusqueda = null;
let temporizadorMensaje = null;

const $ = (id) => document.getElementById(id);

// ---------- Mensajes de éxito o error ----------
function mostrarMensaje(texto, tipo = "exito") {
const caja = $("mensaje");
caja.textContent = texto;
caja.className = "mensaje " + tipo;
clearTimeout(temporizadorMensaje);
temporizadorMensaje = setTimeout(() => caja.classList.add("oculto"), 4000);
}

// ---------- Comunicación con la API ----------
function textoDeError(datos) {
if (!datos || !datos.detail) return "Ocurrió un error inesperado";
if (typeof datos.detail === "string") return datos.detail;
  // Errores de validación de Pydantic (422): una lista de problemas
return datos.detail.map((d) => d.loc[d.loc.length - 1] + ": " + d.msg).join("; ");
}

async function llamarApi(ruta, opciones = {}) {
const cabeceras = { ...(opciones.headers || {}) };
if (token) cabeceras["Authorization"] = "Bearer " + token;

const respuesta = await fetch(ruta, { ...opciones, headers: cabeceras });

if (respuesta.status === 401 && ruta !== "/auth/login") {
    cerrarSesion();
    throw new Error("Tu sesión expiró. Inicia sesión de nuevo.");
}
const datos = await respuesta.json().catch(() => null);
if (!respuesta.ok) throw new Error(textoDeError(datos));
return datos;
}

// ---------- Login y sesión ----------
function mostrarLogin() {
$("pantalla-login").classList.remove("oculto");
$("pantalla-app").classList.add("oculto");
}

function mostrarApp() {
$("pantalla-login").classList.add("oculto");
$("pantalla-app").classList.remove("oculto");
cambiarSeccion("clientes");
}

function cerrarSesion() {
token = null;
sessionStorage.removeItem("token");
mostrarLogin();
}

$("form-login").addEventListener("submit", async (evento) => {
evento.preventDefault();
try {
    const cuerpo = new URLSearchParams({
    username: $("login-usuario").value,
    password: $("login-clave").value,
    });
    const datos = await llamarApi("/auth/login", { method: "POST", body: cuerpo });
    token = datos.access_token;
    sessionStorage.setItem("token", token);
    $("login-clave").value = "";
    mostrarApp();
} catch (error) {
    mostrarMensaje(error.message, "error");
}
});

$("btn-salir").addEventListener("click", cerrarSesion);

// ---------- Menú y listado ----------
function dibujarMenu() {
const menu = $("menu");
menu.innerHTML = "";
for (const clave in SECCIONES) {
    const boton = document.createElement("button");
    boton.textContent = SECCIONES[clave].titulo;
    boton.className = clave === seccion ? "activo" : "";
    boton.addEventListener("click", () => cambiarSeccion(clave));
    menu.appendChild(boton);
}
}

function cambiarSeccion(clave) {
seccion = clave;
$("buscador").value = "";
$("titulo").textContent = SECCIONES[clave].titulo;
dibujarMenu();
cargarLista();
}

async function cargarLista() {
const config = SECCIONES[seccion];
const texto = $("buscador").value.trim();
const ruta = texto ? config.ruta + "?buscar=" + encodeURIComponent(texto) : config.ruta;
try {
    registros = await llamarApi(ruta);
    dibujarTabla();
} catch (error) {
    mostrarMensaje(error.message, "error");
}
}

function agregarCelda(fila, texto) {
const celda = document.createElement("td");
  celda.textContent = texto; // textContent evita que se ejecute HTML o scripts escritos por un usuario
fila.appendChild(celda);
}

function crearBoton(texto, clase, accion) {
const boton = document.createElement("button");
boton.textContent = texto;
boton.className = clase;
boton.addEventListener("click", accion);
return boton;
}

function dibujarTabla() {
const config = SECCIONES[seccion];

const encabezado = $("encabezado");
encabezado.innerHTML = "";
const filaTitulos = document.createElement("tr");
for (const nombre of ["ID", ...config.campos.map((c) => c.etiqueta), "Acciones"]) {
    const th = document.createElement("th");
    th.textContent = nombre;
    filaTitulos.appendChild(th);
}
encabezado.appendChild(filaTitulos);

const cuerpo = $("filas");
cuerpo.innerHTML = "";

if (registros.length === 0) {
    const fila = document.createElement("tr");
    const celda = document.createElement("td");
    celda.colSpan = config.campos.length + 2;
    celda.textContent = "No hay registros";
    celda.className = "vacio";
    fila.appendChild(celda);
    cuerpo.appendChild(fila);
    return;
}

for (const registro of registros) {
    const fila = document.createElement("tr");
    agregarCelda(fila, registro.id);
    for (const campo of config.campos) {
    agregarCelda(fila, registro[campo.nombre] ?? "");
    }
    const acciones = document.createElement("td");
    acciones.appendChild(crearBoton("Editar", "secundario", () => abrirFormulario(registro)));
    acciones.appendChild(crearBoton("Eliminar", "peligro", () => eliminar(registro.id)));
    fila.appendChild(acciones);
    cuerpo.appendChild(fila);
}
}

// ---------- Búsqueda ----------
$("buscador").addEventListener("input", () => {
clearTimeout(temporizadorBusqueda);
  temporizadorBusqueda = setTimeout(cargarLista, 300); // espera 0.3 s después de dejar de escribir
});

// ---------- Crear y editar ----------
function abrirFormulario(registro = null) {
const config = SECCIONES[seccion];
editandoId = registro ? registro.id : null;
$("titulo-form").textContent = (registro ? "Editar " : "Nuevo ") + config.singular;
$("error-form").textContent = "";

const contenedor = $("campos");
contenedor.innerHTML = "";
for (const campo of config.campos) {
    const etiqueta = document.createElement("label");
    etiqueta.textContent = campo.etiqueta;

    let entrada;
    if (campo.tipo === "select") {
    entrada = document.createElement("select");
    for (const opcion of campo.opciones) {
        const o = document.createElement("option");
        o.value = opcion;
        o.textContent = opcion;
        entrada.appendChild(o);
    }
    } else {
    entrada = document.createElement("input");
    entrada.type = campo.tipo;
    if (campo.paso) entrada.step = campo.paso;
    }
    entrada.name = campo.nombre;
    entrada.required = Boolean(campo.requerido);
    if (registro && registro[campo.nombre] != null) entrada.value = registro[campo.nombre];

    etiqueta.appendChild(entrada);
    contenedor.appendChild(etiqueta);
}
$("dialogo").showModal();
}

$("btn-nuevo").addEventListener("click", () => abrirFormulario());
$("btn-cancelar").addEventListener("click", () => $("dialogo").close());

$("form-registro").addEventListener("submit", async (evento) => {
evento.preventDefault();
const config = SECCIONES[seccion];

const datos = {};
for (const campo of config.campos) {
    const valor = evento.target.elements[campo.nombre].value.trim();
    if (campo.tipo === "number") datos[campo.nombre] = Number(valor);
    else datos[campo.nombre] = valor === "" && !campo.requerido ? null : valor;
}

const editando = editandoId !== null;
const ruta = editando ? config.ruta + editandoId : config.ruta;
try {
    await llamarApi(ruta, {
    method: editando ? "PUT" : "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
    });
    $("dialogo").close();
    mostrarMensaje(editando ? "Registro actualizado correctamente" : "Registro creado correctamente");
    cargarLista();
} catch (error) {
    $("error-form").textContent = error.message; // el aviso va dentro de la ventana, que tapa al resto
}
});

// ---------- Eliminar (con confirmación) ----------
async function eliminar(id) {
const config = SECCIONES[seccion];
const seguro = confirm("¿Seguro que deseas eliminar este " + config.singular + "? Esta acción no se puede deshacer.");
if (!seguro) return;
try {
    const respuesta = await llamarApi(config.ruta + id, { method: "DELETE" });
    mostrarMensaje(respuesta.mensaje);
    cargarLista();
} catch (error) {
    mostrarMensaje(error.message, "error");
}
}

// ---------- Inicio ----------
if (token) mostrarApp();
else mostrarLogin();