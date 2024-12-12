<template>
  <div>
    <header class="header">
      <div
        :class="['loader', {
          'loader--active': isLoading,
        }]"
      ></div>
      <div class="controls">
        <input
          v-model="trackName"
          :placeholder="placeholder"
          type="text"
          class="search-input"
          @keyup.enter="search"
        />
        <button
          class="search-button"
          :disabled="isLoading || trackName.length === 0"
          @click="search"
        >
          🔍
        </button>
      </div>
    </header>
    <div class="track-list">
      <div v-for="track of tracksWithoutAdded">
        <div
          v-for="album of track.albums"
          :key="`${album.id}-${track.id}`"
          class="track-album-item"
          @click="addTrack(track.id, album.id)"
        >
          <img
            class="cover"
            height="100"
            width="100"
            :src="`http://${album.cover.replaceAll('%%', '')}100x100`"
          >
          <h3 class="title">
            {{ track.title }} - {{ album.title }}
          </h3>
        </div>
      </div>
    </div>
    <div class="controls">
      <button
        v-if="page !== 0 && !isFailedSearchNext"
        class="search-button search-button--next"
        :disabled="isLoading"
        @click="searchNext"
      >
        Search next
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

const config = useRuntimeConfig();

console.log(config);

const page = ref(0);
const trackName = ref('');
const lastTrackName = ref('');
const isLoading = ref(false);
const isFailedSearchNext = ref(false);
const tracks = ref<any[]>([]);
const addedTrackIds = ref<number[]>([]);

const placeholder = computed(() => {
  if (isFailedSearchNext.value) {
    return 'Nothing is found :(';
  }
  return 'Apa Beba';
});

const tracksWithoutAdded = computed(() => tracks.value.filter(
  track => !addedTrackIds.value.includes(track.id)
));

const search = async () => {
  if (!trackName.value.length) {
    return;
  }

  try {
    isFailedSearchNext.value = false;
    page.value = 0;
    isLoading.value = true;

    const { data } = await useFetch<any>(`${config.public.apiBase}/search`, {
      query: {
        track_name: trackName.value,
        page: page.value,
      },
    });

    lastTrackName.value = trackName.value;
    page.value += 1;
    tracks.value = data.value;
  } finally {
    isLoading.value = false;
  }
};

const searchNext = async () => {
  try {
    isLoading.value = true;

    const { data } = await useFetch<any>(`${config.public.apiBase}/search`, {
      query: {
        track_name: lastTrackName.value,
        page: page.value,
      },
    });

    if (!data.value.length) {
      isFailedSearchNext.value = true;
    } else {
      page.value += 1;
      tracks.value = [...tracks.value, ...data.value];
    }
  } finally {
    isLoading.value = false;
  }
};

const addTrack = async (trackId: number, albumId: number) => {
  if (isLoading.value) {
    return;
  }

  try {
    isLoading.value = true;

    await useFetch<any>(`${config.public.apiBase}/add_track`, {
      method: 'POST',
      query: {
        track_id: `${trackId}`,
        album_id: `${albumId}`,
      },
    });

    addedTrackIds.value.push(trackId);
  } finally {
    isLoading.value = false;
  }
};
</script>

<style>
:root {
  --primary: palevioletred;
  --secondary: pink;
}

body {
  max-width: 777px;
  margin: 0 auto;
  padding-bottom: 20px;
  font-family: 'Courier New', Courier, monospace;
}

.header {
  padding: 16px;
  position: sticky;
  z-index: 1;
  top: 0;
  background-color: white;
  border-bottom: 1px solid var(--primary);
}

.loader {
  width: 100%;
  height: 5px;
  position: absolute;
  top: 0;
  left: 0;
  animation: loading 1s;
  animation-fill-mode: forwards;
  animation-iteration-count: infinite;
  animation-timing-function: linear;
  background: repeating-linear-gradient(to right, var(--primary), var(--secondary), var(--primary));
  background-position: 0 100%;
  background-size: 200% auto;
  opacity: 0;
}

.loader--active {
  opacity: 1;
}

.controls {
  display: flex;
  column-gap: 8px;
}

.controls * {
  appearance: none;
  box-sizing: border-box;
  padding: 0;
  margin: 0;
  outline: none;
  border: none;
  background-color: initial;
}

.search-input {
  flex-grow: 1;
  height: 48px;
  padding: 0 16px;
  border: 2px solid var(--primary);
  font-size: 18px;
}

.search-button {
  width: 48px;
  height: 48px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 24px;
  border: 2px solid var(--primary);
  cursor: pointer;
}

.search-button:active {
  background-color: var(--primary);
}

.search-button:disabled {
  opacity: 0.5;
}

.search-button--next {
  width: 100%;
  margin-top: 18px;
  margin-left: 16px;
  margin-right: 16px;
  font-size: 16px;
}

.search-button--next:active {
  color: white;
}

.track-list {
  padding: 20px 16px 0;
}

.track-album-item {
  margin-top: 15px;
  display: flex;
  border: 2px solid var(--secondary);
  border-radius: 4px;
  contain: content;
  cursor: pointer;
  transition: background-color 0.15s;
}

.track-album-item:active {
  background-color: var(--secondary);
}

.cover {
  margin-right: 30px;
}

.title {
  margin: 15px 15px 0 0;
  font-size: 14px;
}

@keyframes loading {
  0% {
    background-position: 0 0;
  }

  100% {
    background-position: -200% 0;
  }
}

@media (min-width: 540px) {
  .search-button:hover {
    background-color: var(--primary);
  }

  .search-button--next:hover {
    color: white;
  }

  .track-album-item:hover {
    background-color: var(--secondary);
  }

  .title {
    font-size: 18px;
  }
}

@media (min-width: 777px) {
  .header {
    border-left: 1px solid var(--primary);
    border-right: 1px solid var(--primary);
  }
}
</style>
