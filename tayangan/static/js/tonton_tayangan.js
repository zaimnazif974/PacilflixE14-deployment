import { appendAlert } from "./utils.js";

const onChangeProgressTonton = async (e) => {
  let progress = e.target.value;
  const progressPercentageElement = document.getElementById('progress-percentage');
  progressPercentageElement.innerHTML = progress;
}

document.getElementById('progress-input').addEventListener('input', onChangeProgressTonton);

const onSubmitProgress = async (e) => {
  e.preventDefault();
  const progress_percentage = document.getElementById('progress-input').value;
  const tayanganId = document.getElementById('tayangan-id').value;
  const url = `/api/tayangan/tonton`;
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      id_tayangan: tayanganId,
      progress_percentage: parseInt(progress_percentage)
    })
  });
  const data = await response.json();
  if (response.ok) {
    appendAlert(data.message, 'success');
  } else {
    appendAlert(data.message, 'danger');
  }
}

document.getElementById('tonton-button').addEventListener('click', onSubmitProgress);