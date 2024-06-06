const getIdTayangan = () => {
  const url = window.location.href;
  const slug = url.split("/").pop();
  const id = slug.split(".")[0];
  return id;
}

const getData = async (id) => {
  const url = `/api/film/${id}`;
  const response = await fetch(url);
  const data = await response.json();
  return data;
}

const renderData = async (data) => {
  const judul = document.getElementById('judul');
  judul.innerHTML = data.judul;

  const tayanganId = document.getElementById('tayangan-id');
  tayanganId.value = data.id;

  const totalView = document.getElementById('total-view');
  totalView.innerHTML = data.total_view;

  const rating = document.getElementById('rating');
  rating.innerHTML = parseFloat(data.avg_rating).toFixed(1);

  const durasiFilm = document.getElementById('durasi-film');
  durasiFilm.innerHTML = data.durasi_film;

  const releaseDateFilm = document.getElementById('release-date-film');
  releaseDateFilm.innerHTML = data.release_date_film;

  const urlVideoFilm = document.getElementById('url-video-film');
  urlVideoFilm.innerHTML = data.url_video_film;
  urlVideoFilm.href = data.url_video_film;

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

window.onload = async () => {
  const id = getIdTayangan();
  const data = await getData(id);
  renderData(data);
}