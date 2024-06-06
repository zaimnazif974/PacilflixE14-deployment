const getIdFromUrl = () => {
  const url = window.location.href;
  const slug = url.split("/").pop();
  const id = slug.split(".")[0];
  return id;
}

const getData = async (id) => {
  const url = `/api/series/${id}`;
  const response = await fetch(url);
  const data = await response.json();
  return data;
}

const renderData = async (data) => {
  const judul = document.getElementById('judul');
  judul.innerHTML = data.judul;

  const episode = document.getElementById('episode');
  let episodeCards = data.episodes.map((eps) => `
      <div class="card my-2">
        <a href="/episode/${data.id}.${createSubjudul(eps.sub_judul)}" class="card-body">
          ${eps.sub_judul}
        </a>
      </div>
  `).join('\n');
  episode.innerHTML = episodeCards;

  const totalView = document.getElementById('total-view');
  totalView.innerHTML = data.total_view;

  const rating = document.getElementById('rating');
  rating.innerHTML = data.avg_rating;

  const asalNegara = document.getElementById('asal-negara');
  asalNegara.innerHTML = data.asal_negara;

  const sinopsis = document.getElementById('sinopsis');
  sinopsis.innerHTML = data.sinopsis;

  const genre = document.getElementById('genre');
  genre.innerHTML = data.genres.map(x => x.genre).join(', ');

  const pemain = document.getElementById('pemain');
  pemain.innerHTML = data.pemain.map(x => `<a href="/daftar-kontributor/${x.id}">${x.nama}</a>`).join(',\n');

  const penulisSkenario = document.getElementById('penulis-skenario');
  penulisSkenario.innerHTML = data.penulis_skenario.map(x => `<a href="/daftar-kontributor/${x.id}">${x.nama}</a>`).join(',\n');

  const sutradara = document.getElementById('sutradara');
  sutradara.innerHTML = data.sutradara.nama;
  sutradara.href = `/daftar-kontributor/${data.sutradara.id}`;
}

function createSubjudul(judul) {
  return judul.replace(/ /g, '_');
}

window.onload = async () => {
  const id = getIdFromUrl();
  const data = await getData(id);
  renderData(data);
}