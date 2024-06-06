function createSubjudul(judul) {
  return judul.replace(/ /g, '_');
}

const getIdSeriesAndSubjudlFromUrl = () => {
  const url = window.location.href;
  let [id_series, subjudul] = url.split("/").pop().split(".");
  return [id_series, subjudul];
}

const getIdTayangan = () => {
  return getIdSeriesAndSubjudlFromUrl()[0];
}

const getData = async (id_series, subjudul) => {
  const url = `/api/series/${id_series}/episode/${subjudul}`;
  const response = await fetch(url);
  const data = await response.json();
  return data;
}

const renderData = async (data) => {
  const judul = document.getElementById('judul');
  judul.innerHTML = data.judul;

  const tayanganId = document.getElementById('tayangan-id');
  tayanganId.value = data.id_series;

  const subJudul = document.getElementById('sub-judul');
  subJudul.innerHTML = data.sub_judul;

  const otherEpisodes = document.getElementById('other-episodes');
  let otherEpisodeCards = data.other_episodes.map((eps) => `
      <div class="card my-2">
        <a href="/episode/${data.id_series}.${createSubjudul(eps.sub_judul)}" class="card-body">
          ${eps.sub_judul}
        </a>
      </div>
  `).join('\n');
  otherEpisodes.innerHTML = otherEpisodeCards;


  const durasi = document.getElementById('durasi');
  durasi.innerHTML = data.durasi;

  const releaseDateEpisode = document.getElementById('release-date');
  releaseDateEpisode.innerHTML = data.release_date;

  const urlVideoEpisode = document.getElementById('url-video');
  urlVideoEpisode.innerHTML = data.url_video;
  urlVideoEpisode.href = data.url_video;

  const sinopsis = document.getElementById('sinopsis');
  sinopsis.innerHTML = data.sinopsis;
}

window.onload = async () => {
  const [id_series, subjudul] = getIdSeriesAndSubjudlFromUrl();
  const data = await getData(id_series, subjudul);
  renderData(data);
}