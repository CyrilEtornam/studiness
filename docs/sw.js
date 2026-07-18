// Bump this on every deploy that changes cached files, so clients pick up
// the new version instead of serving stale cache-first responses forever.
// scripts/merge_cards.py bumps this automatically whenever a course's data changes.
var CACHE_VERSION = 'studiness-v1';

var CORE_ASSETS = [
  './',
  'index.html',
  'style.css',
  'app.js',
  'manifest.webmanifest',
  'icons/icon-192.png',
  'icons/icon-512.png',
  'fonts/fraunces.woff2',
  'data/courses.json'
];

// Courses are discovered dynamically from data/courses.json at install time,
// so adding a course doesn't require hand-editing this file's asset list.
function courseAssetUrls(course) {
  var base = 'data/' + course.slug + '/';
  return fetch(base + 'reference-index.json')
    .then(function (res) { return res.ok ? res.json() : []; })
    .then(function (refIndex) {
      return [base + 'deck.json', base + 'curriculum.json', base + 'reference-index.json']
        .concat(refIndex.map(function (item) { return base + 'reference/' + item.file; }));
    })
    .catch(function () { return [base + 'deck.json', base + 'curriculum.json', base + 'reference-index.json']; });
}

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE_VERSION).then(function (cache) {
      return cache.addAll(CORE_ASSETS)
        .then(function () { return fetch('data/courses.json'); })
        .then(function (res) { return res.ok ? res.json() : []; })
        .then(function (courses) {
          return Promise.all(courses.map(courseAssetUrls));
        })
        .then(function (urlLists) {
          var allUrls = [].concat.apply([], urlLists);
          return Promise.all(allUrls.map(function (url) {
            return cache.add(url).catch(function () {});
          }));
        });
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE_VERSION; }).map(function (k) {
        return caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (event) {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then(function (cached) {
      var network = fetch(event.request).then(function (response) {
        if (response && response.ok) {
          var copy = response.clone();
          caches.open(CACHE_VERSION).then(function (cache) { cache.put(event.request, copy); });
        }
        return response;
      }).catch(function () { return cached; });
      return cached || network;
    })
  );
});
