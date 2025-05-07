import { getQueue, saveQueue, getCurrentIndex, setCurrentIndex, getFavorites } from './storage.js';
import * as ui from './ui.js';
const BACKEND_URL = 'https://musiclib-production.up.railway.app';
const audioPlayer = document.getElementById('audioPlayer');
let currentSong = null;

export async function fetchAudio(videoId, title, thumbnail, retryCount = 0) {
  try {
    const res = await fetch(`${BACKEND_URL}/get_audio?videoId=${videoId}`);
    const data = await res.json();
    audioPlayer.src = data.audioUrl;
    await audioPlayer.play();
    currentSong = { videoId, title, thumbnail, apiCalled: false };
    ui.updateNowPlaying(title, thumbnail);
    ui.updateFavoriteButton(currentSong);
  } catch (e) {
    if (retryCount < 1) return fetchAudio(videoId, title, thumbnail, retryCount + 1);
    nextSong();
  }
}

export function prevSong() {
  let idx = getCurrentIndex();
  if (idx > 0) {
    idx--;
    setCurrentIndex(idx);
    const song = getQueue()[idx];
    fetchAudio(song.videoId, song.title, song.thumbnail);
  }
}

export function nextSong() {
  let queue = getQueue();
  let idx = getCurrentIndex();
  if (idx < queue.length - 1) idx++; else if (ui.isRepeating) idx = 0;
  setCurrentIndex(idx);
  const song = queue[idx];
  fetchAudio(song.videoId, song.title, song.thumbnail);
}

export function shuffleQueue() {
  let queue = getQueue();
  for (let i = queue.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1)); [queue[i], queue[j]] = [queue[j], queue[i]];
  }
  saveQueue(queue);
  ui.refreshCarousel(queue);
}

export function toggleRepeat() { ui.isRepeating = !ui.isRepeating; }
export function togglePlayPause() { audioPlayer.paused ? audioPlayer.play() : audioPlayer.pause(); }
export function updateProgress() {
  ui.updateProgressBar(audioPlayer.currentTime, audioPlayer.duration);
  if (currentSong && audioPlayer.currentTime / audioPlayer.duration >= 0.75 && !currentSong.apiCalled) {
    fetch(`${BACKEND_URL}/track_play`, { method: 'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ videoId: currentSong.videoId }) });
    currentSong.apiCalled = true;
  }
}

audioPlayer.ontimeupdate = updateProgress;
audioPlayer.onended = nextSong;
