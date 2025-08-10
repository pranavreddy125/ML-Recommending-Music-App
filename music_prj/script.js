let songList = [];

function addSong() {
  const title = document.getElementById('title').value;
  const artist = document.getElementById('artist').value;
  const song_id = document.getElementById('song_id').value;

  if (!title || !artist || !song_id) {
    alert("Please fill in all fields.");
    return;
  }

  const song = { title, artist, song_id };
  songList.push(song);

  displaySongs();
  clearInputs();
}

function displaySongs() {
  const ul = document.getElementById('songList');
  ul.innerHTML = '';

  songList.forEach(song => {
    const li = document.createElement('li');
    li.textContent = `${song.title} by ${song.artist} (ID: ${song.song_id})`;
    ul.appendChild(li);
  });
}

function clearInputs() {
  document.getElementById('title').value = '';
  document.getElementById('artist').value = '';
  document.getElementById('song_id').value = '';
}
