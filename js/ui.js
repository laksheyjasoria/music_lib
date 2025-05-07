import { getQueue, getCurrentIndex, getFavorites, getRecentSearches, saveRecentSearches } from './storage.js';
export let isRepeating = false;

export function refreshCarousel(queue) {
  const c = document.getElementById('carouselContainer'); c.innerHTML = '';
  queue.slice(1).forEach(song => {
    const d = document.createElement('div'); d.className = 'carousel-item';
    d.innerHTML = `<img src="${song.thumbnail}"><p>${song.title}</p>`;
    d.onclick = () => insertAndPlay(song);
    c.appendChild(d);
  });
}

function insertAndPlay(song) {
  let queue = getQueue(), idx = getCurrentIndex();
  queue.splice(idx + 1, 0, song);
  saveQueue(queue);
  setCurrentIndex(idx + 1);
  import('./player.js').then(m=>m.fetchAudio(song.videoId, song.title, song.thumbnail));
}

export function populateSection(id, items) {
  const c = document.getElementById(id); c.innerHTML = '';
  items.forEach(song => {
    const d = document.createElement('div'); d.className = id.replace('Container','-item');
    d.innerHTML = `<img src="${song.thumbnail}"><p>${song.title}</p>`;
    d.onclick = () => insertAndPlay(song);
    c.appendChild(d);
  });
}

export function updateNowPlaying(title, thumbnail) {
  document.getElementById('videoResult').innerHTML = `<h2>${title}</h2><img src="${thumbnail}">`;
}

export function updateFavoriteButton(currentSong) {
  const heart = document.querySelector('.heart-icon');
  const favs = getFavorites();
  heart.classList.toggle('favorited', favs.some(f=>f.videoId===currentSong.videoId));
}

export function refreshFavoritesList() {
  const favs = getFavorites(), c = document.getElementById('favoritesSection'); c.innerHTML = '<h2>Your Favorite Songs</h2>';
  favs.forEach(song=>{
    const d=document.createElement('div'); d.className='favorite-item';
    d.innerHTML=`<img src="${song.thumbnail}"><p>${song.title}</p>`;
    d.onclick=()=>insertAndPlay(song);
    c.appendChild(d);
  });
}

export function refreshRecentSearches() {
  const rec = getRecentSearches(), c = document.getElementById('recentSearchesContainer'); c.innerHTML = '';
  rec.forEach(song=>{
    const d=document.createElement('div'); d.className='search-item';
    d.innerHTML=`<img src="${song.thumbnail}"><p>${song.title}</p>`;
    d.onclick=()=>insertAndPlay(song);
    c.appendChild(d);
  });
}

export function updateProgressBar(cur, dur) {
  const p = document.getElementById('progressBar'); p.value = (cur/dur)*100;
  document.getElementById('currentTime').textContent = format(cur);
  document.getElementById('totalDuration').textContent = format(dur);
}

function format(s) { const m=Math.floor(s/60), sec=Math.floor(s%60).toString().padStart(2,'0'); return `${m}:${sec}`; }

export function showNotification(msg) { const n=document.getElementById('notification'); n.textContent=msg; n.style.display='block'; setTimeout(()=>n.style.display='none',3000); }
export function showError(msg) { const e=document.getElementById('errorMessage'); e.textContent=msg; setTimeout(()=>e.textContent='',5000); }
