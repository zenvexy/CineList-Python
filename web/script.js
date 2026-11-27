const API_URL = "https://cinelist-backend.vercel.app";

const filmGrid = document.querySelector("#film-grid");
const filmCount = document.querySelector("#film-count");
const feedback = document.querySelector("#feedback");
const searchInput = document.querySelector("#search-input");
const typeFilter = document.querySelector("#type-filter");
const statusFilter = document.querySelector("#status-filter");
const dialog = document.querySelector("#film-dialog");
const form = document.querySelector("#film-form");
const formError = document.querySelector("#form-error");
const saveButton = document.querySelector("#save-button");

const state = {
  films: [],
};

const labels = {
  FILME: "Filme",
  SERIE: "Série",
  PENDENTE: "Quero assistir",
  ASSISTIDO: "Assistido",
  ASSISTINDO: "Assistindo",
};

async function request(path, options = {}) {
  const headers = { ...options.headers };

  if (options.body !== undefined) {
    headers["Content-Type"] = "application/json";
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let message = `Não foi possível concluir a solicitação (${response.status}).`;

    try {
      const error = await response.json();

      if (typeof error.detail === "string") {
        message = error.detail;
      } else if (Array.isArray(error.detail)) {
        message = error.detail.map((item) => item.msg).join(" ");
      }
    } catch (error) {
      if (!(error instanceof SyntaxError)) {
        throw error;
      }
    }

    throw new Error(message);
  }

  return response.json();
}

function getLabel(value) {
  return labels[value] ?? value;
}

function setOptions(select, values, placeholder) {
  select.replaceChildren(new Option(placeholder, ""));

  values.forEach((value) => {
    select.add(new Option(getLabel(value), value));
  });
}

function makeElement(tag, className, text) {
  const element = document.createElement(tag);

  if (className) {
    element.className = className;
  }

  if (text !== undefined) {
    element.textContent = text;
  }

  return element;
}

function getImageUrl(value) {
  try {
    const url = new URL(value);

    if (url.protocol === "https:" || url.protocol === "http:") {
      return url.href;
    }
  } catch (error) {
    if (!(error instanceof TypeError)) {
      throw error;
    }
  }

  return "";
}

function createFilmCard(film) {
  const card = makeElement("article", "film-card");
  const poster = makeElement("div", "film-poster");
  const imageUrl = getImageUrl(film.imagem);

  if (imageUrl) {
    const image = makeElement("img", "film-image");
    image.src = imageUrl;
    image.alt = `Capa de ${film.titulo}`;
    image.loading = "lazy";
    image.addEventListener(
      "error",
      () => {
        image.remove();
        poster.append(makeElement("span", "poster-fallback", "CineList"));
      },
      { once: true },
    );
    poster.append(image);
  } else {
    poster.append(makeElement("span", "poster-fallback", "CineList"));
  }

  const content = makeElement("div", "film-content");
  const metadata = makeElement("div", "film-metadata");
  metadata.append(
    makeElement("span", "film-type", getLabel(film.tipo)),
    makeElement("span", "film-year", String(film.ano)),
  );

  const title = makeElement("h3", "film-title", film.titulo);
  const genre = makeElement("p", "film-genre", film.genero);
  const status = makeElement(
    "span",
    `status-badge status-${film.status.toLowerCase()}`,
    getLabel(film.status),
  );

  content.append(metadata, title, genre);

  if (film.descricao) {
    content.append(makeElement("p", "film-description", film.descricao));
  }

  const footer = makeElement("div", "film-footer");
  footer.append(status);

  if (film.nota !== null && film.nota !== undefined) {
    footer.append(makeElement("span", "film-rating", `★ ${film.nota}`));
  }

  const actions = makeElement("div", "film-actions");
  const editButton = makeElement("button", "text-button", "Editar");
  editButton.type = "button";
  editButton.addEventListener("click", () => openForm(film));

  const deleteButton = makeElement(
    "button",
    "text-button text-button-danger",
    "Excluir",
  );
  deleteButton.type = "button";
  deleteButton.addEventListener("click", () => deleteFilm(film));
  actions.append(editButton, deleteButton);
  footer.append(actions);
  content.append(footer);
  card.append(poster, content);

  return card;
}

function getVisibleFilms() {
  const search = searchInput.value.trim().toLocaleLowerCase("pt-BR");

  return state.films.filter((film) => {
    const matchesSearch = `${film.titulo} ${film.genero}`
      .toLocaleLowerCase("pt-BR")
      .includes(search);
    const matchesType = !typeFilter.value || film.tipo === typeFilter.value;
    const matchesStatus = !statusFilter.value || film.status === statusFilter.value;

    return matchesSearch && matchesType && matchesStatus;
  });
}

function renderFilms() {
  const films = getVisibleFilms();
  filmGrid.replaceChildren();

  if (state.films.length === 0) {
    filmCount.textContent = "0 títulos";
    filmGrid.append(
      makeElement(
        "div",
        "empty-state",
        "Sua lista está vazia. Adicione seu primeiro título.",
      ),
    );
    return;
  }

  filmCount.textContent = `${films.length} ${
    films.length === 1 ? "título" : "títulos"
  }`;

  if (films.length === 0) {
    filmGrid.append(
      makeElement(
        "div",
        "empty-state",
        "Nenhum título encontrado com esses filtros.",
      ),
    );
    return;
  }

  filmGrid.append(...films.map(createFilmCard));
}

async function loadFilms() {
  feedback.textContent = "";
  filmCount.textContent = "Carregando...";

  try {
    const films = await request("/api/filmes/listar");

    if (!Array.isArray(films)) {
      throw new Error("A API retornou uma lista de títulos inválida.");
    }

    state.films = films;
    renderFilms();
  } catch (error) {
    filmCount.textContent = "";
    feedback.textContent = `${error.message} Confira sua conexão com a API.`;
    filmGrid.replaceChildren();
  }
}

function openForm(film) {
  form.reset();
  formError.textContent = "";
  document.querySelector("#film-id").value = film?.id ?? "";
  document.querySelector("#form-title").textContent = film
    ? "Editar título"
    : "Adicionar título";
  saveButton.textContent = film ? "Salvar alterações" : "Salvar título";

  if (film) {
    form.elements.titulo.value = film.titulo;
    form.elements.tipo.value = film.tipo;
    form.elements.ano.value = film.ano;
    form.elements.genero.value = film.genero;
    form.elements.status.value = film.status;
    form.elements.imagem.value = film.imagem;
    form.elements.descricao.value = film.descricao ?? "";
    form.elements.nota.value = film.nota ?? "";
  } else {
    form.elements.ano.value = new Date().getFullYear();
    form.elements.status.value = "PENDENTE";
  }

  dialog.showModal();
  form.elements.titulo.focus();
}

function closeForm() {
  dialog.close();
  formError.textContent = "";
}

async function saveFilm(event) {
  event.preventDefault();
  formError.textContent = "";
  saveButton.disabled = true;

  const formData = new FormData(form);
  const note = formData.get("nota");
  const film = {
    titulo: formData.get("titulo").trim(),
    tipo: formData.get("tipo"),
    genero: formData.get("genero").trim(),
    imagem: formData.get("imagem").trim(),
    ano: Number(formData.get("ano")),
    descricao: formData.get("descricao").trim() || null,
    nota: note === "" ? null : Number(note),
    status: formData.get("status"),
  };
  const id = formData.get("id");
  const path = id
    ? `/api/filmes/atualizar/${encodeURIComponent(id)}`
    : "/api/filmes/cadastrar";

  try {
    await request(path, {
      method: id ? "PUT" : "POST",
      body: JSON.stringify(film),
    });
    closeForm();
    await loadFilms();
  } catch (error) {
    formError.textContent = error.message;
  } finally {
    saveButton.disabled = false;
  }
}

async function deleteFilm(film) {
  const confirmed = window.confirm(
    `Deseja excluir "${film.titulo}" da sua lista?`,
  );

  if (!confirmed) {
    return;
  }

  feedback.textContent = "";

  try {
    await request(`/api/filmes/excluir/${encodeURIComponent(film.id)}`, {
      method: "DELETE",
    });
    await loadFilms();
  } catch (error) {
    feedback.textContent = error.message;
  }
}

async function initialize() {
  try {
    const [types, statuses] = await Promise.all([
      request("/api/enums/tipos-filme/listar"),
      request("/api/enums/status-filme/listar"),
    ]);

    if (!Array.isArray(types) || !Array.isArray(statuses)) {
      throw new Error("A API retornou opções de formulário inválidas.");
    }

    setOptions(typeFilter, types, "Todos os tipos");
    setOptions(statusFilter, statuses, "Todos os status");
    setOptions(document.querySelector("#film-type"), types, "Selecione");
    setOptions(document.querySelector("#film-status"), statuses, "Selecione");
    await loadFilms();
  } catch (error) {
    filmCount.textContent = "";
    feedback.textContent = `${error.message} Não foi possível carregar as opções da API.`;
  }
}

document
  .querySelector("#new-film-button")
  .addEventListener("click", () => openForm());
document
  .querySelector("#close-dialog-button")
  .addEventListener("click", closeForm);
document
  .querySelector("#cancel-button")
  .addEventListener("click", closeForm);
form.addEventListener("submit", saveFilm);
searchInput.addEventListener("input", renderFilms);
typeFilter.addEventListener("change", renderFilms);
statusFilter.addEventListener("change", renderFilms);
dialog.addEventListener("click", (event) => {
  if (event.target === dialog) {
    closeForm();
  }
});

initialize();
