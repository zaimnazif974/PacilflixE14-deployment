const onSearch = (event) => {
  event.preventDefault();
  const searchBar = document.getElementById('search-bar');
  window.location.href = `/search?q=${searchBar.value}`;
}

const searchButton = document.getElementById('search-button');
searchButton.addEventListener('click', onSearch);



// read from ../dummy/tayangan.json
const getData = async () => {
  const response = await fetch('/static/dummy/daftar_tayangan.json');
  const data = await response.json();
  return data;
}

const renderData = async (data) => {
  renderTayanganTerbaik(data['best_tayangan']);
  renderFilm(data['film']);
  renderSeries(data['series']);
}

function renderTayanganTerbaik(data) {
  const bestTayangan = document.getElementById('tayangan-terbaik-tbody');
  const tayanganCards = data.map((tayangan) => `
    <tr>
      <td>${tayangan.peringkat}</td>
      <td>${tayangan.judul}</td>
      <td>${tayangan.sinopsis}</td>
      <td><a href="${tayangan.url_video_trailer}">${tayangan.url_video_trailer}</a></td>
      <td>${tayangan.release_date_trailer}</td>
      <td>${tayangan.total_views}</td>
    </tr>
    `);
  bestTayangan.innerHTML = tayanganCards.join('\n');
}

async function renderFilm(data) {
  const film = document.getElementById('film-tbody');
  const filmCards = data.map((film) => `
  <tr>
    <td>${film.judul}</td>
    <td>${film.sinopsis}</td>
    <td><a href="${film.url_video_trailer}">${film.url_video_trailer}</a></td>
    <td>${film.release_date_trailer}</td>
  </tr>
  `);
  film.innerHTML = filmCards.join('\n');
}

async function renderSeries(data) {
  const series = document.getElementById('series-tbody');
  const seriesCards = data.map((series) => `
  <tr>
    <td>${series.judul}</td>
    <td>${series.sinopsis}</td>
    <td><a href="${series.url_video_trailer}">${series.url_video_trailer}</a></td>
    <td>${series.release_date_trailer}</td>
  </tr>
  `);
  series.innerHTML = seriesCards.join('\n');
}

function createSlug(judul) {
  return judul.toLowerCase().replace(/ /g, '_');
}

window.onload = async () => {
  const data = await getData();
  renderData(data);
}