const getQueryParam = (query) => {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(query);
}

const updateSearchBar = (event) => {
  searchBar = document.getElementById('search-bar');
  searchBar.value = getQueryParam('q');
}

const onSearch = (event) => {
  event.preventDefault();
  const searchBar = document.getElementById('search-bar');
  console.log(searchBar.value);
  window.location.href = `/search?q=${searchBar.value}`;
}

const searchButton = document.getElementById('search-button');
searchButton.addEventListener('click', onSearch);


const getData = async () => {
  const keyword = getQueryParam('q');
  const url = (keyword) ? `/api/tayangan/search?keyword=${keyword}` : `/api/tayangan/search`;
  let result = await fetch(url);
  result = await result.json();
  return result;
}

function createSlug(judul) {
  return judul.toLowerCase().replace(/ /g, '_');
}

const renderData = async (data) => {
  const searchResultContainer = document.getElementById('search-result-tbody');
  const isAuthenticated = document.getElementById('header-tayangan') !== null;
  const tayanganCards = data.map((tayangan) => `
    <tr>
      <td>${tayangan.judul}</td>
      <td>${tayangan.sinopsis_trailer}</td>
      <td><a href="${tayangan.url_video_trailer}">${tayangan.url_video_trailer}</a></td>
      <td>${tayangan.release_date_trailer}</td>
      ${isAuthenticated && 
        `<td><a href="/${tayangan.type}/${tayangan.id}.${createSlug(tayangan.judul)}" type="button" class="btn btn-dark">View More</a></td>`
      }
    </tr>
  `);
  searchResultContainer.innerHTML = tayanganCards.join('\n');
}



window.onload = async () => {
  const data = await getData();
  renderData(data);
  updateSearchBar()
};
