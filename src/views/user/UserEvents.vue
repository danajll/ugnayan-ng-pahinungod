<script setup>
import { computed, ref, onMounted } from 'vue'
import { Search, CalendarDays, MapPin, Users } from 'lucide-vue-next'
import { eventService } from '../../api/events'
import { participationService } from '../../api/participations'

// ─── Filters ───
const search = ref('')
const region = ref('All locations')
const dateRange = ref('Any time')
const category = ref('All')

// Align with backend EventCategory choices
const categories = [
  { label: 'All',                value: 'All' },
  { label: 'Health',             value: 'HEALTH' },
  { label: 'Education',          value: 'EDUCATION & LITERACY' },
  { label: 'Environment',        value: 'ENVIRONMENT & ECOLOGY' },
  { label: 'NSTP / CWTS',        value: 'NSTP / CWTS' },
  { label: 'IP',                 value: 'INDIGENOUS PEOPLES (IP)' },
]

// ─── State ───
const events = ref([])
const participations = ref([])   // [{ id, event, status, ... }]
const loading = ref(true)
const loadError = ref(null)
const actionError = ref(null)
const busyEventId = ref(null)    // for button loading state

// Map eventId → participationId (only for ACTIVE joins)
const activeJoinMap = computed(() => {
  const map = new Map()
  for (const p of participations.value) {
    if (p.status === 'registered' || p.status === 'attended') {
      map.set(p.event, p.id)
    }
  }
  return map
})

// ─── Fetch ───
async function loadAll() {
  loading.value = true
  loadError.value = null
  try {
    const [evRes, partRes] = await Promise.all([
      eventService.list(),
      participationService.myParticipations(),
    ])
    events.value = evRes.data
    participations.value = partRes.data
  } catch (err) {
    loadError.value = err.response?.data?.detail || 'Failed to load events.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(loadAll)

// ─── Helpers ───
const categoryLabel = (value) => {
  const c = categories.find(x => x.value === value)
  return c ? c.label : value
}

const slotsLeft = (event) => {
  const quota = event.quota || 0
  const taken = event.registered_count || 0
  return Math.max(quota - taken, 0)
}

const isJoined = (eventId) => activeJoinMap.value.has(eventId)

const formatDate = (iso) => {
  if (!iso) return 'Date to be announced'
  const d = new Date(iso)
  return d.toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric'
  })
}

// ─── Filtered list (works on raw API fields) ───
const filteredEvents = computed(() => {
  const s = search.value.trim().toLowerCase()
  return events.value.filter(event => {
    const matchesSearch = !s || [
      event.name, event.location, event.description
    ].some(f => (f || '').toLowerCase().includes(s))

    const matchesCategory = category.value === 'All' || event.category === category.value

    const matchesRegion =
      region.value === 'All locations' ||
      (event.location || '').toLowerCase().includes(region.value.toLowerCase())

    // Date filter
    let matchesDate = true
    if (dateRange.value === 'Upcoming') {
      matchesDate = new Date(event.start_datetime) >= new Date()
    } else if (dateRange.value === 'This Month') {
      const now = new Date()
      const start = new Date(event.start_datetime)
      matchesDate = start.getMonth() === now.getMonth() &&
                    start.getFullYear() === now.getFullYear()
    } else if (dateRange.value === 'Last 7 Days') {
      const now = new Date()
      const start = new Date(event.start_datetime)
      const diff = (now - start) / (1000 * 60 * 60 * 24)
      matchesDate = diff >= 0 && diff <= 7
    }

    return matchesSearch && matchesCategory && matchesRegion && matchesDate
  })
})

// ─── Actions ───
async function joinEvent(eventId) {
  actionError.value = null
  busyEventId.value = eventId
  try {
    const { data } = await eventService.join(eventId)
    // Add or replace the participation row
    const idx = participations.value.findIndex(p => p.event === eventId)
    if (idx !== -1) participations.value[idx] = data
    else participations.value.push(data)

    // Optimistically bump registered_count
    const ev = events.value.find(e => e.id === eventId)
    if (ev) ev.registered_count = (ev.registered_count || 0) + 1
  } catch (err) {
    actionError.value = err.response?.data?.detail || 'Could not join event.'
    console.error(err)
  } finally {
    busyEventId.value = null
  }
}

async function cancelSignup(eventId) {
  const participationId = activeJoinMap.value.get(eventId)
  if (!participationId) return

  actionError.value = null
  busyEventId.value = eventId
  try {
    const { data } = await participationService.cancel(participationId)
    const idx = participations.value.findIndex(p => p.id === participationId)
    if (idx !== -1) participations.value[idx] = data

    // Optimistically decrement registered_count
    const ev = events.value.find(e => e.id === eventId)
    if (ev && ev.registered_count > 0) ev.registered_count -= 1
  } catch (err) {
    actionError.value = err.response?.data?.detail || 'Could not cancel signup.'
    console.error(err)
  } finally {
    busyEventId.value = null
  }
}
</script>

<template>
  <section class="user-hero user-hero-events">
    <div>
      <h1>Make a difference.<br />Volunteer with Pahinungód.</h1>
      <p>MAKIBAHAGI, MAGLINGKOD, MAG PAHINUNGÓD</p>
    </div>
  </section>

  <section class="user-content user-events-content">
    <div class="user-event-filters">
      <label class="user-search">
        <Search :size="16" />
        <input v-model="search" placeholder="Search missions, locations, or coordinators..." />
      </label>

      <select v-model="region" aria-label="Filter by location">
        <option>All locations</option>
        <option>Davao Region</option>
        <option>Davao City</option>
        <option>South Cotabato</option>
      </select>

      <select v-model="dateRange" aria-label="Filter by date">
        <option>Any time</option>
        <option>Last 7 Days</option>
        <option>This Month</option>
        <option>Upcoming</option>
      </select>

      <div class="user-category-tabs">
        <button
          v-for="cat in categories"
          :key="cat.value"
          type="button"
          :class="{ active: category === cat.value }"
          @click="category = cat.value"
        >
          {{ cat.label }}
        </button>
      </div>
    </div>

    <div class="user-results-line">
      <span>{{ filteredEvents.length }} volunteer opportunities</span>
      <span>Find an activity that works for you.</span>
    </div>

    <div v-if="loading" class="user-empty-state">
      <p>Loading events…</p>
    </div>

    <div v-else-if="loadError" class="user-empty-state">
      <h2>Could not load events</h2>
      <p>{{ loadError }}</p>
      <button class="user-button user-button-outline" @click="loadAll">Retry</button>
    </div>

    <div v-else-if="filteredEvents.length" class="user-event-grid">
      <article
        v-for="event in filteredEvents"
        :key="event.id"
        class="user-event-card"
      >
        <img
          class="user-event-image"
          :src="event.cover_image || '/images/programs/bloodletting.jpg'"
          :alt="event.name"
        />

        <div class="user-event-body">
          <span
            class="user-category-pill"
            :class="`category-${(event.category || '').toLowerCase().replace(/[^a-z]/g, '-')}`"
          >
            {{ categoryLabel(event.category) }}
          </span>

          <p class="user-event-meta">
            <CalendarDays :size="13" />
            {{ formatDate(event.start_datetime) }}
          </p>

          <p class="user-event-meta">
            <MapPin :size="13" />
            {{ event.location || 'Location to be announced' }}
          </p>

          <h2>{{ event.name }}</h2>
          <p class="user-event-description">{{ event.description }}</p>

          <div class="user-event-tags">
            <span v-for="tag in (event.prerequisites || [])" :key="tag">
              {{ tag }}
            </span>
          </div>

          <div class="user-event-lead">
            <span>
              {{ isJoined(event.id) ? '✅ You are registered' : '' }}
            </span>
            <strong>
              <Users :size="13" />
              {{ slotsLeft(event) }} slots left
            </strong>
          </div>

          <button
            v-if="!isJoined(event.id)"
            class="user-button user-button-primary"
            type="button"
            :disabled="busyEventId === event.id || slotsLeft(event) <= 0"
            @click="joinEvent(event.id)"
          >
            {{ busyEventId === event.id ? 'Joining…' : (slotsLeft(event) <= 0 ? 'Fully Booked' : 'Be a Volunteer') }}
          </button>

          <button
            v-else
            class="user-button user-button-outline"
            type="button"
            :disabled="busyEventId === event.id"
            @click="cancelSignup(event.id)"
          >
            {{ busyEventId === event.id ? 'Cancelling…' : 'Cancel Signup' }}
          </button>
        </div>
      </article>
    </div>

    <div v-else class="user-empty-state">
      <Search :size="30" />
      <h2>No events found</h2>
      <p>Try changing your search or filters.</p>
      <button
        class="user-button user-button-outline"
        type="button"
        @click="search = ''; region = 'All locations'; category = 'All'; dateRange = 'Any time'"
      >
        Clear filters
      </button>
    </div>

    <p v-if="actionError" style="color:#d32f2f; font-size:0.9rem; text-align:center; padding: 12px;">
      {{ actionError }}
    </p>

    <div v-else class="user-empty-state">
      <Search :size="30" />
      <h2>No events found</h2>
      <p>Try changing your search or filters.</p>

      <button
        class="user-button user-button-outline"
        type="button"
        @click="search = ''; region = 'All locations'; category = 'All'"
      >
        Clear filters
      </button>
    </div>

  </section>
</template>
