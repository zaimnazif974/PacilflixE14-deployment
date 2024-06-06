import { appendAlert } from "./utils.js";

const updateRating = (e) => {
  e.preventDefault();
  const newRating = e.currentTarget.getAttribute('data-rating');
  document.getElementById('selected-rating').innerText = newRating;
  for (let i = 1; i <= 5; i++) {
    const star = document.getElementById(`your-rating-star-${i}`);
    if (i <= newRating) {
      star.classList.add('fa-solid');
      star.classList.remove('fa-regular');
    } else {
      star.classList.add('fa-regular');
      star.classList.remove('fa-solid');
    }
  }
}


Array.from(document.getElementsByClassName('btn-rating')).forEach((btn) => {
  btn.addEventListener('click', updateRating);
});

const getIdTayanganFromUrl = () => {
  const url = window.location.href;
  const slug = url.split("/").pop();
  const id = slug.split(".")[0];
  return id;
}

const getDataUlasan = async (id) => {
  const url = '/api/ulasan/' + id;
  let response = await fetch(url);
  response = await response.json();
  console.log(response);
  return response;
}

const createRatingStars = (rating) => {
  let stars = '';
  for (let i = 1; i <= 5; i++) {
    if (i <= rating) {
      stars += '<i class="fa-solid fa-star text-warning"></i>\n';
    } else {
      stars += '<i class="fa-regular fa-star text-warning"></i>\n';
    }
  }
  return stars;
}

const convertDate = (date) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Intl.DateTimeFormat('id-ID', options).format(Date.parse(date));
}

const renderDataUlasan = async (data) => {
  if (data.reviews.length !== 0) {
    const ulasanCards = data.reviews.map((ulasan) => `
    <div class="card">
      <div class="card-body">
        <div class="d-flex flex-row justify-content-between">
          <div>
            ${createRatingStars(ulasan.rating)}
            <span>${ulasan.rating}/5</span>
          </div>
          <div>${convertDate(ulasan.timestamp)}</div>
        </div>
        <div class="fw-bold fs-4">${ulasan.username}</div>
        <div>
          <span class="fw-bold">Description</span>
          <p>${ulasan.deskripsi}</p>
        </div>
      </div>
    </div>
  `)
    const cardWrapper = document.getElementById('cards-wrapper');
    cardWrapper.innerHTML = ulasanCards.join('\n');
  }

  if (data.current_user_review) {
    const ulasan = data.current_user_review;
    const currentUserReviewWrapper = document.getElementById('current-user-ulasan');
    const currentUserReviewCard = `
    <div class="card">
      <div class="card-body">
        <div class="d-flex flex-row justify-content-between">
          <div>
            ${createRatingStars(ulasan.rating)}
            <span>${ulasan.rating}/5</span>
          </div>
          <div>${convertDate(ulasan.timestamp)}</div>
        </div>
        <div class="fw-bold fs-4">${ulasan.username}</div>
        <div>
          <span class="fw-bold">Description</span>
          <p>${ulasan.deskripsi}</p>
        </div>
      </div>
    </div>
    `;
    currentUserReviewWrapper.innerHTML = currentUserReviewCard;
  }
}

const refreshUlasan = async () => {
  const id = getIdTayanganFromUrl();
  const data = await getDataUlasan(id);
  renderDataUlasan(data);
}

refreshUlasan();


const submitUlasan = async (e) => {

  e.preventDefault();
  const id = getIdTayanganFromUrl();
  const rating = document.getElementById('selected-rating').innerText;
  const deskripsi = document.getElementById('deskripsi-ulasan-input').value;

  const url = `/api/ulasan`;
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      id_tayangan: id,
      rating: parseInt(rating),
      deskripsi: deskripsi,
    }),
  });
  const data = await response.json();
  if(data.status === 'success') {
    appendAlert(data.message, 'success');
    refreshUlasan();
  } else {
    appendAlert(data.message, 'danger');
  }
}

document.getElementById('submit-ulasan-button').addEventListener('click', submitUlasan);