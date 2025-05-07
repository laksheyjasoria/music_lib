export function getQueue() { return JSON.parse(localStorage.getItem('queue')) || []; }
export function saveQueue(queue) { localStorage.setItem('queue', JSON.stringify(queue)); }
export function getCurrentIndex() { return parseInt(localStorage.getItem('currentIndex'), 10) || 0; }
export function setCurrentIndex(idx) { localStorage.setItem('currentIndex', idx); }
export function getFavorites() { return JSON.parse(localStorage.getItem('favorites')) || []; }
export function saveFavorites(favs) { localStorage.setItem('favorites', JSON.stringify(favs)); }
export function getRecentSearches() { return JSON.parse(localStorage.getItem('recentSearches')) || []; }
export function saveRecentSearches(list) { localStorage.setItem('recentSearches', JSON.stringify(list)); }
