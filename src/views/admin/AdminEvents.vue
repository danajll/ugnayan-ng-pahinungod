<script setup>
import { computed, ref, onMounted } from 'vue'
import {
  Search, ChevronDown, CalendarDays, MapPin, UsersRound,
  Pencil, X, Flag, List, Bold, Italic, SlidersHorizontal,
  UploadCloud, Trash2, Map, UserRound, Clock3
} from 'lucide-vue-next'
import { eventService } from '../../api/events'

// ─── UI state ───
const search = ref('')
const region = ref('All Regions')
const regionOpen = ref(false)
const status = ref('All')
const category = ref('ALL MISSIONS')

const cities = [
  'Bayugan City', 'Bislig City', 'Cagayan de Oro City', 'Cotabato City',
  'Dapitan City', 'Davao City', 'Digos City', 'Dipolog City', 'Gingoog City',
  'Iligan City', 'Isabela City', 'Kidapawan City', 'Koronadal City',
  'Lamitan City', 'Mati City', 'Malaybalay City', 'Marawi City',
  'Oroquieta City', 'Ozamiz City', 'Pagadian City', 'Panabo City',
  'Samal City', 'Surigao City', 'Tacurong City', 'Tagum City',
  'Tangub City', 'Tandag City', 'Valencia City', 'Zamboanga City'
]
const regions = [
  'All Regions', 'National Capital Region (NCR)', 'Cordillera Administrative Region (CAR)',
  'Ilocos Region (Region I)', 'Cagayan Valley (Region II)', 'Central Luzon (Region III)',
  'CALABARZON (Region IV-A)', 'MIMAROPA (Region IV-B)', 'Bicol Region (Region V)',
  'Western Visayas (Region VI)', 'Negros Island Region (NIR)', 'Central Visayas (Region VII)',
  'Eastern Visayas (Region VIII)', 'Zamboanga Peninsula (Region IX)',
  'Northern Mindanao (Region X)', 'Davao Region (Region XI)',
  'SOCCSKSARGEN (Region XII)', 'Caraga (Region XIII)',
  'Bangsamoro Autonomous Region in Muslim Mindanao (BARMM)'
]
const statuses = ['All', 'Published', 'Scheduled', 'Drafts']
const categories = [
  'ALL MISSIONS', 'HEALTH', 'EDUCATION & LITERACY',
  'ENVIRONMENT & ECOLOGY', 'NSTP / CWTS', 'INDIGENOUS PEOPLES (IP)'
]
const selectRegion = (item) => { region.value = item; regionOpen.value = false }

// ─── API state ───
const events = ref([])
const loading = ref(true)
const loadError = ref(null)

// Map a Django Event to the shape the template expects
const mapEvent = (e) => ({
  id: e.id,
  title: e.name,
  category: e.category,
  date: new Date(e.start_datetime).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric'
  }),
  // Keep raw ISO strings so the edit modal can prefill date inputs
  start_datetime: e.start_datetime,
  end_datetime: e.end_datetime,
  location: e.location || 'Location to be announced',
  region: e.city || 'Davao Region',
  city: e.city || 'Davao City',
  description: e.description || '',
  image: e.cover_image || '/images/programs/bloodletting.jpg',
  status: e.status,
  live_status: e.live_status || 'Scheduled',
  displayStatus:
    e.status === 'Published' ? 'RECRUITING'
    : e.status === 'Scheduled' ? 'SCHEDULED'
    : 'DRAFT',
  time: null,
  quota: e.quota ?? 0,
  registered: e.registered_count ?? 0,
  quotaLabel: 'Registered',
  tags: e.prerequisites || [],
  lead: 'Pahinungod Office' // not on the model yet
})

async function refreshEvents() {
  loading.value = true
  loadError.value = null
  try {
    const { data } = await eventService.list()
    events.value = data.map(mapEvent)
  } catch (err) {
    loadError.value = err.response?.data?.detail || 'Failed to load events.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(refreshEvents)

// ─── Filtering ───
const filteredEvents = computed(() => {
  const s = search.value.trim().toLowerCase()
  return events.value.filter((event) => {
    const matchesSearch =
      event.title.toLowerCase().includes(s) ||
      event.location.toLowerCase().includes(s) ||
      event.lead.toLowerCase().includes(s)
    const matchesStatus = status.value === 'All' || event.status === status.value
    const matchesCategory = category.value === 'ALL MISSIONS' || event.category === category.value
    const matchesRegion = region.value === 'All Regions' || event.region === region.value
    return matchesSearch && matchesStatus && matchesCategory && matchesRegion
  })
})

const getEventStatus = (event) => {
  const slotsLeft = Math.max((event.quota || 0) - (event.registered || 0), 0)
  const live = event.live_status || 'Scheduled'

  // Concluded
  if (live === 'Concluded') {
    return { label: 'Concluded', class: 'concluded' }
  }

  // Closed (slots filled or less than 1 day left)
  if (slotsLeft <= 0) {
    return { label: 'Closed', class: 'closed' }
  }
  const end = event.end_datetime ? new Date(event.end_datetime) : null
  const now = new Date()
  if (end && (end - now) / (1000 * 60 * 60 * 24) < 1) {
    return { label: 'Closed', class: 'closed' }
  }

  // Live statuses
  if (live === 'Happening Soon') return { label: 'Happening Soon', class: 'ongoing' }
  if (live === 'Happening Now') return { label: 'Happening Now', class: 'ongoing' }

  // Recruiting
  return { label: 'Recruiting', class: 'recruiting' }
}

// ─── Create / Edit modal ───
const createModalOpen = ref(false)
const editingEvent = ref(null)

const emptyEvent = () => ({
  title: '',
  category: 'HEALTH',
  description: '',
  startDate: '',
  endDate: '',
  city: 'Davao City',
  venue: '',
  quota: 40,
  accreditedHours: 24,
  leadCoordinator: '',
  prerequisites: [],
  coverImage: null,
  publicationState: 'draft'
})
const newEvent = ref(emptyEvent())

const prerequisiteOptions = [
  'Healthcare / SOM Medical', 'CWTS / NSTP Accredited', 'CSM / Science Majors',
  'First Aid Certified (BLS)', 'Indigenous Language Fluent', 'Open to All Iskolar Volunteers'
]

const togglePrerequisite = (item) => {
  if (newEvent.value.prerequisites.includes(item)) {
    newEvent.value.prerequisites = newEvent.value.prerequisites.filter(p => p !== item)
  } else {
    newEvent.value.prerequisites.push(item)
  }
}

const resetNewEvent = () => { newEvent.value = emptyEvent() }

const openCreateModal = () => {
  editingEvent.value = null
  resetNewEvent()
  createModalOpen.value = true
}

const openEditModal = (event) => {
  editingEvent.value = event
  // Extract YYYY-MM-DD from the ISO datetime for <input type="date">
  const toDateInput = (iso) => iso ? iso.slice(0, 10) : ''
  newEvent.value = {
    title: event.title,
    category: event.category,
    description: event.description,
    startDate: toDateInput(event.start_datetime),
    endDate: toDateInput(event.end_datetime),
    city: event.city,
    venue: event.location,
    quota: event.quota,
    accreditedHours: 24,
    leadCoordinator: event.lead,
    prerequisites: [...event.tags],
    coverImage: null,
    publicationState:
      event.status === 'Drafts' ? 'draft'
      : event.status === 'Scheduled' ? 'scheduled'
      : 'published'
  }
  createModalOpen.value = true
}

const closeCreateModal = () => {
  createModalOpen.value = false
  editingEvent.value = null
  resetNewEvent()
}

// Build a payload that matches the EventSerializer
const buildPayload = () => {
  const toIso = (dateStr, timeStr = '08:00:00') => {
    if (!dateStr) return null
    return new Date(`${dateStr}T${timeStr}`).toISOString()
  }
  const statusMap = {
    draft: 'Drafts',
    scheduled: 'Scheduled',
    published: 'Published',
  }
  return {
    name: newEvent.value.title || 'Untitled Mission',
    description: newEvent.value.description,
    location: newEvent.value.venue,
    city: newEvent.value.city,
    category: newEvent.value.category,
    status: statusMap[newEvent.value.publicationState] || 'Drafts',
    quota: Number(newEvent.value.quota) || 0,
    prerequisites: newEvent.value.prerequisites,
    start_datetime: toIso(newEvent.value.startDate, '08:00:00'),
    end_datetime: toIso(newEvent.value.endDate || newEvent.value.startDate, '17:00:00'),
  }
}

const saveEvent = async () => {
  try {
    const payload = buildPayload()
    if (editingEvent.value) {
      await eventService.patch(editingEvent.value.id, payload)
    } else {
      await eventService.create(payload)
    }
    await refreshEvents()
    closeCreateModal()
  } catch (err) {
    const msg = err.response?.data
      ? JSON.stringify(err.response.data, null, 2)
      : err.message
    alert('Error saving event:\n' + msg)
    console.error(err)
  }
}

// Keep these two so the existing footer buttons don't break.
// "Save Draft" forces state=draft; "Save Changes" uses the chosen state.
const saveNewEvent = async (publicationState) => {
  newEvent.value.publicationState = publicationState
  await saveEvent()
}
const saveEditedEvent = async () => { await saveEvent() }

// ─── Manage modal ───
const manageModalOpen = ref(false)
const manageEvent = ref(null)
const manageParticipants = ref([])
const manageLoading = ref(false)

const formatTimeRemaining = (iso) => {
  if (!iso) return null
  const end = new Date(iso)
  const now = new Date()
  const diffMs = end - now
  if (diffMs <= 0) return null
  const totalSecs = Math.floor(diffMs / 1000)
  const days = Math.floor(totalSecs / 86400)
  const hours = Math.floor((totalSecs % 86400) / 3600)
  const minutes = Math.floor((totalSecs % 3600) / 60)
  const parts = []
  if (days > 0) parts.push(`${days} day${days !== 1 ? 's' : ''}`)
  if (hours > 0) parts.push(`${hours} hr${hours !== 1 ? 's' : ''}`)
  if (minutes > 0) parts.push(`${minutes} min`)
  return parts.length ? parts.join(' ') : '< 1 min'
}

const eventStatusLabel = (e) => {
  if (!e) return ''
  return e.live_status || 'Scheduled'
}

const openManageModal = async (event) => {
  manageEvent.value = event
  manageParticipants.value = []
  manageLoading.value = true
  manageModalOpen.value = true
  try {
    const { data } = await eventService.participants(event.id)
    manageParticipants.value = data
  } catch (err) {
    console.error('Failed to load participants:', err)
    manageParticipants.value = []
  } finally {
    manageLoading.value = false
  }
}

const closeManageModal = () => {
  manageModalOpen.value = false
  manageEvent.value = null
  manageParticipants.value = []
}

// ─── Delete modal ───
const deleteModalOpen = ref(false)
const selectedEvent = ref(null)
const deleteConfirmed = ref(false)

const openDeleteModal = (event) => {
  selectedEvent.value = event
  deleteConfirmed.value = false
  deleteModalOpen.value = true
}

const closeDeleteModal = () => {
  deleteModalOpen.value = false
  selectedEvent.value = null
  deleteConfirmed.value = false
}

const deleteEvent = async () => {
  if (!deleteConfirmed.value || !selectedEvent.value) return
  try {
    await eventService.remove(selectedEvent.value.id)
    events.value = events.value.filter(e => e.id !== selectedEvent.value.id)
    closeDeleteModal()
  } catch (err) {
    const msg = err.response?.data
      ? JSON.stringify(err.response.data, null, 2)
      : err.message
    alert('Error deleting event:\n' + msg)
    console.error(err)
  }
}
</script>



<template>

  <div class="admin-page events-page">

    <div class="events-inner">

      <!-- search toolbar -->

      <div class="events-toolbar">



        <!-- search -->

        <div class="events-search">

          <Search :size="18" />

          <input

            v-model="search"

            type="text"

            placeholder="Search missions, locations, or coordinators..."

          />

        </div>



        <!-- region  -->

        <div class="events-region-wrapper">

          <button

            class="events-region"

            @click="

              regionOpen = !regionOpen

            "

          >

            <span>

              {{ region }}

            </span>

            <ChevronDown

              :size="15"

              :class="{

                rotated: regionOpen

              }"

            />

          </button>



          <div

            v-if="regionOpen"

            class="events-region-dropdown"

          >

            <button

              v-for="item in regions"

              :key="item"

              :class="{

                selected:

                  region === item

              }"

              @click="

                selectRegion(item)

              "

            >

              {{ item }}

            </button>

          </div>

        </div>



        <!-- status  -->

        <div class="events-status-tabs">

          <button

            v-for="item in statuses"

            :key="item"

            :class="{

              active:

                status === item

            }"

            @click="

              status = item

            "

          >

            {{ item }}

          </button>

        </div>

      
      <button class="events-add-button" @click="openCreateModal()">
        <span>+</span> Add Event  <!-- MAKE THIS LOOK BETTER LATER -->
      </button>

      </div>      <!-- category filters -->

      <div class="events-categories">

        <button

          v-for="item in categories"

          :key="item"

          :class="{

            active:

              category === item

          }"

          @click="

            category = item

          "

        >

          {{ item }}

        </button>

      </div>      <!-- event grid -->

      <div class="events-grid">



        <!-- event card  -->

        <article

          v-for="event in filteredEvents"

          :key="event.id"

          class="event-card"

        >



          <!-- image  -->

          <div class="event-image-wrapper">

            <img

              :src="event.image"

              :alt="event.title"

              class="event-image"

            />



            <!-- status  -->

            <span

              class="event-status"

              :class="getEventStatus(event).class"

            >

              <span></span>

              {{ getEventStatus(event).label }}

            </span>



            <!-- time  -->

            <span

              v-if="

                (

                  status === 'Scheduled' ||

                  status === 'Drafts'

                ) &&

                event.time

              "

              class="event-time"

            >

              ◷ {{ event.time }}

            </span>

          </div>



          <!-- content  -->

          <div class="event-content">



            <!-- category  -->

            <span class="event-category">

              {{ event.category }}

            </span>



            <!-- DATE + LOCATION -->

            <div class="event-meta">

              <div>

                <CalendarDays :size="14" />

                <span>

                  {{ event.date }}

                </span>

              </div>



              <div>

                <MapPin :size="14" />

                <span>

                  {{ event.location }}

                </span>

              </div>

            </div>



            <!-- title  -->

            <h2 class="event-title">

              {{ event.title }}

            </h2>



            <!-- description  -->

            <p class="event-description">

              {{ event.description }}

            </p>



            <!-- quota  -->

            <div class="event-quota">

              <div

                class="event-quota-heading"

              >

                <span>

                  Volunteer Quota

                </span>

                <strong>

                  {{ event.registered }}

                  /

                  {{ event.quota }}

                  {{ event.quotaLabel }}

                </strong>

              </div>



              <div class="event-quota-bar">

                <span

                  :style="{

                    width:

                      `${Math.min(

                        (

                          event.registered /

                          event.quota

                        ) * 100,

                        100

                      )}%`

                  }"

                ></span>

              </div>

            </div>



            <!-- tags  -->

            <div class="event-tags">

              <span

                v-for="tag in event.tags"

                :key="tag"

              >

                {{ tag }}

              </span>

            </div>



            <!-- lead  -->

            <div class="event-lead">

              <span>

                Lead:

                {{ event.lead }}

              </span>



              <strong

                :class="{

                  waitlist:

                    event.registered >=

                    event.quota

                }"

              >

                {{

                  event.registered >=

                  event.quota

                    ? 'Waitlist open'

                    : `${event.quota -

                      event.registered}

                      slots left`

                }}

              </strong>

            </div>



            <!-- actions  -->

            <div class="event-actions">



              <!-- draft  -->

              <button

                v-if="

                  event.status === 'Drafts'

                "

                class="event-manage-button draft-button"

                @click="

                  openEditModal(event)

                "

              >

                <Pencil :size="15" />

                Edit Draft

              </button>



              <!-- normal  -->

              <button

                v-else

                class="event-manage-button"

                :class="{

                  disabled:

                    event.registered >=

                    event.quota

                }"

                @click="openManageModal(event)"

              >

                <UsersRound :size="15" />

                Manage

              </button>



              <!-- edit  -->

              <button

                class="event-edit-button"

                @click="

                  openEditModal(event)

                "

              >

                <Pencil :size="16" />

              </button>



              <!-- delete  -->

              <button

                class="event-delete-button"

                @click="

                  openDeleteModal(event)

                "

              >

                <Trash2 :size="16" />

              </button>

            </div>

          </div>

        </article>      <!-- add new event -->

        <article

          v-if="

            status === 'Drafts'

          "

          class="event-add-card"

        >

          <button

            @click="

              openCreateModal()

            "

          >

            <span class="add-event-plus">

              +

            </span>

            ADD NEW EVENT

          </button>

        </article>

      </div>      <!-- create / edit event modal -->

      <div

        v-if="

          createModalOpen

        "

        class="event-modal-backdrop"

        @click.self="

          closeCreateModal

        "

      >

        <div

          class="event-create-modal"

        >



          <!-- header  -->

          <div class="event-modal-header">

            <div

              class="event-modal-title"

            >

              <div

                class="event-modal-icon"

              >

                <Flag :size="20" />

              </div>

              <h2>

                {{

                  editingEvent

                    ? 'Edit Event'

                    : 'Create New Event'

                }}

              </h2>

            </div>



            <button

              class="event-modal-close"

              @click="

                closeCreateModal

              "

            >

              <X :size="20" />

            </button>

          </div>



          <!-- body  -->

          <div

            class="event-modal-body"

          >      <!-- mission briefing -->

            <section

              class="event-form-section"

            >

              <div

                class="event-form-section-title"

              >

                <span>

                  01. MISSION BRIEFING

                </span>

              </div>



              <div

                class="

                  event-form-grid

                  event-form-grid-two

                "

              >



                <!-- mission title  -->

                <div

                  class="event-form-field"

                >

                  <div

                    class="event-form-label-row"

                  >

                    <label>

                      Mission Title

                      <span></span>

                    </label>

                    <small>

                      Max 80 chars

                    </small>

                  </div>



                  <div

                    class="event-input"

                  >

                    <Flag :size="16" />

                    <input

                      v-model="

                        newEvent.title

                      "

                      type="text"

                      maxlength="80"

                      placeholder="e.g. Panihapon sa Balay ni Nas"

                    />

                  </div>

                </div>



                <!-- category  -->

                <div

                  class="event-form-field"

                >

                  <label>

                    Category Track

                    <span></span>

                  </label>



                  <div

                    class="event-input"

                  >

                    <List :size="16" />

                    <select

                      v-model="

                        newEvent.category

                      "

                    >

                      <option

                        value="HEALTH"

                      >

                        Health Outreach

                      </option>

                      <option

                        value="EDUCATION & LITERACY"

                      >

                        Education & Literacy

                      </option>

                      <option

                        value="ENVIRONMENT & ECOLOGY"

                      >

                        Environment & ECOLOGY

                      </option>

                      <option

                        value="NSTP / CWTS"

                      >

                        NSTP / CWTS

                      </option>

                      <option

                        value="INDIGENOUS PEOPLES (IP)"

                      >

                        Indigenous Peoples (IP)

                      </option>

                    </select>

                  </div>

                </div>

              </div>



              <!-- description  -->

              <div

                class="event-form-field"

              >

                <div

                  class="event-form-label-row"

                >

                  <label>

                    Briefing Description &

                    Objectives

                    <span></span>

                  </label>



                  <div

                    class="event-editor-tools"

                  >

                    <Bold :size="14" />

                    <Italic :size="14" />

                    <List :size="14" />

                  </div>

                </div>



                <textarea

                  v-model="

                    newEvent.description

                  "

                  rows="3"

                  placeholder="Specify target communities, logistical assembly instructions, deliverables, and service scopes for deployment..."

                ></textarea>

              </div>

            </section>      <!-- schedule & deployment venue -->

            <section

              class="event-form-section"

            >

              <div

                class="event-form-section-title"

              >

                <span>

                  02. SCHEDULE &

                  DEPLOYMENT VENUE

                </span>

              </div>



              <div

                class="

                  event-form-grid

                  event-form-grid-four

                "

              >



                <!-- start date  -->

                <div

                  class="event-form-field"

                >

                  <label>

                    Start Date

                    <span></span>

                  </label>



                  <div

                    class="event-input"

                  >

                    <CalendarDays

                      :size="16"

                    />

                    <input

                      v-model="

                        newEvent.startDate

                      "

                      type="date"

                    />

                  </div>

                </div>



                <!-- end date  -->

                <div

                  class="event-form-field"

                >

                  <label>

                    End Date

                    <span></span>

                  </label>



                  <div

                    class="event-input"

                  >

                    <CalendarDays

                      :size="16"

                    />

                    <input

                      v-model="

                        newEvent.endDate

                      "

                      type="date"

                    />

                  </div>

                </div>



                <!-- region  -->

                <div

                  class="event-form-field"

                >

                  <label>

                    City

                  </label>



                  <div

                    class="event-input"

                  >

                    <Map :size="16" />

                    <select

                      v-model="

                        newEvent.city

                      "

                    >

                      <option

                        v-for="

                          item in cities


                        "

                        :key="item"

                        :value="item"

                      >

                        {{ item }}

                      </option>

                    </select>

                  </div>

                </div>



                <!-- venue  -->

                <div

                  class="event-form-field"

                >

                  <label>

                    Venue / Focal Point

                    <span></span>

                  </label>



                  <div

                    class="event-input"

                  >

                    <MapPin :size="16" />

                    <input

                      v-model="

                        newEvent.venue

                      "

                      type="text"

                      placeholder="Mugat, Sa balay ni Jay"

                    />

                  </div>

                </div>

              </div>

            </section>      <!-- volunteer metrics & personnel -->

            <section

              class="event-form-section"

            >

              <div

                class="event-form-section-title"

              >

                <span>

                  03. VOLUNTEER METRICS &

                  PERSONNEL

                </span>

              </div>



              <div

                class="

                  event-form-grid

                  event-form-grid-three

                "

              >



                <!-- quota  -->

                <div

                  class="event-form-field"

                >

                  <div

                    class="event-form-label-row"

                  >

                    <label>

                      Volunteer Quota

                    </label>

                    <small>

                      Slots

                    </small>

                  </div>



                  <div

                    class="event-input"

                  >

                    <UsersRound

                      :size="16"

                    />

                    <input

                      v-model="

                        newEvent.quota

                      "

                      type="number"

                      min="1"

                    />

                  </div>

                </div>



                <!-- hours  -->

                <div

                  class="event-form-field"

                >

                  <label>

                    Accredited Hours

                  </label>



                  <div

                    class="event-input"

                  >

                    <Clock3

                      :size="16"

                    />

                    <input

                      v-model="

                        newEvent.accreditedHours

                      "

                      type="number"

                      min="1"

                    />

                  </div>

                </div>



                <!-- lead  -->

                <div

                  class="event-form-field"

                >

                  <label>

                    Assigned Unit /

                    Lead Coordinator

                    <span></span>

                  </label>



                  <div

                    class="event-input"

                  >

                    <UserRound

                      :size="16"

                    />

                    <input

                      v-model="

                        newEvent.leadCoordinator

                      "

                      type="text"

                      placeholder="Office of Health Initiatives - Prof. D. Santiago (CSM)"

                    />

                  </div>

                </div>

              </div>



              <div

                class="event-form-lower-grid"

              >



                <!-- prerequisites  -->

                <div

                  class="event-form-field"

                >

                  <label>

                    Target Volunteer

                    Cohort / Prerequisites

                  </label>



                  <p

                    class="event-form-help"

                  >

                    Eligible constituents will

                    receive automatic priority

                    RSVP invitations.

                  </p>



                  <div

                    class="event-prerequisites"

                  >

                    <button

                      v-for="

                        item in prerequisiteOptions

                      "

                      :key="item"

                      type="button"

                      :class="{

                        selected:

                          newEvent

                            .prerequisites

                            .includes(item)

                      }"

                      @click="

                        togglePrerequisite(item)

                      "

                    >

                      <span

                        class="

                          event-check-box

                        "

                      >

                        ✓

                      </span>

                      {{ item }}

                    </button>

                  </div>

                </div>



                <!-- cover banner  -->

                <div

                  class="event-form-field"

                >

                  <label>

                    Mission Cover Banner

                  </label>



                  <label

                    class="

                      event-upload-box

                    "

                  >

                    <UploadCloud

                      :size="27"

                    />

                    <strong>

                      Drag and drop mission

                      cover photo

                    </strong>

                    <small>

                      PNG, JPG, or WEBP

                      up to 5MB

                      (16:9 ratio recommended)

                    </small>



                    <input

                      type="file"

                      accept="

                        image/png,

                        image/jpeg,

                        image/webp

                      "

                      @change="

                        newEvent.coverImage =

                          $event.target.files[0]

                      "

                    />

                  </label>

                </div>

              </div>

            </section>      <!-- publication state -->

            <div

              class="

                event-publication-state

              "

            >

              <div

                class="

                  event-publication-label

                "

              >

                <SlidersHorizontal

                  :size="17"

                />

                Deployment Publication

                State:

              </div>



              <div

                class="

                  event-publication-options

                "

              >

                <label>

                  <input

                    v-model="

                      newEvent.publicationState

                    "

                    type="radio"

                    value="draft"

                  />

                  Save as Draft

                </label>



                <label>

                  <input

                    v-model="

                      newEvent.publicationState

                    "

                    type="radio"

                    value="scheduled"

                  />

                  Schedule for Later

                </label>



                <label>

                  <input

                    v-model="

                      newEvent.publicationState

                    "

                    type="radio"

                    value="published"

                  />

                  Publish Immediately

                </label>

              </div>

            </div>

          </div>



          <!-- footer  -->

          <div

            class="event-modal-footer"

          >

            <button

              class="

                event-discard-button

              "

              @click="

                closeCreateModal

              "

            >

              Discard

            </button>



            <button

              class="

                event-save-button

              "

              @click="

                editingEvent

                  ? saveEditedEvent()

                  : saveNewEvent('draft')

              "

            >

              {{ editingEvent

                ? 'Save Changes'

                : 'Save Draft'

              }}

            </button>



            <button

              class="

                event-create-button

              "

              @click="saveEvent"

            >

              {{

                editingEvent

                  ? 'Save Changes'

                  : 'Create & Stage Event →'

              }}

            </button>

          </div>

        </div>

      </div>      <!-- manage event modal -->

      <div

        v-if="manageModalOpen"

        class="event-modal-backdrop"

        @click.self="closeManageModal"

      >

        <div class="event-manage-modal">

          <!-- header  -->

          <div class="event-modal-header">

            <div class="event-modal-title">

              <div class="event-modal-icon">

                <UsersRound :size="20" />

              </div>

              <h2>{{ manageEvent?.name }}</h2>

            </div>

            <button

              class="event-modal-close"

              @click="closeManageModal"

            >

              <X :size="20" />

            </button>

          </div>

          <!-- body  -->

          <div class="event-modal-body">

            <!-- event status & time remaining  -->

            <div style="display:flex; align-items:center; gap:12px; margin-bottom:18px; padding:12px 16px; background:#f5f2f2; border-radius:8px;">

              <span

                style="display:inline-flex; align-items:center; gap:6px; padding:4px 10px; border-radius:99px; font-size:0.75rem; font-weight:700; text-transform:uppercase;"

                :style="{

                  background: manageEvent?.status === 'Published' ? '#dcfce7' : '#fef3c7',

                  color: manageEvent?.status === 'Published' ? '#166534' : '#92400e'

                }"

              >

                {{ eventStatusLabel(manageEvent) }}

              </span>

              <span v-if="manageEvent?.end_datetime" style="font-size:0.9rem; color:#6b7280;">

                Time remaining: {{ formatTimeRemaining(manageEvent.end_datetime) || 'Concluded' }}

              </span>

            </div>

            <!-- participants list  -->

            <div style="margin-bottom:16px;">

              <div style="font-weight:700; font-size:0.85rem; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:10px; color:#625b5c;">

                Volunteers Signed Up ({{ manageParticipants.length }})

              </div>

              <div v-if="manageLoading" style="padding:20px; text-align:center; color:#6b7280;">

                Loading participants…

              </div>

              <div v-else-if="manageParticipants.length === 0" style="padding:20px; text-align:center; color:#6b7280;">

                No volunteers have signed up yet.

              </div>

              <table v-else style="width:100%; border-collapse:collapse; font-size:0.9rem;">

                <thead>

                  <tr style="text-align:left;">

                    <th style="padding:8px 0; color:#625b5c; font-weight:600; border-bottom:1px solid #e5dfdf;">Volunteer</th>

                    <th style="padding:8px 0; color:#625b5c; font-weight:600; border-bottom:1px solid #e5dfdf;">Status</th>

                    <th style="padding:8px 0; color:#625b5c; font-weight:600; border-bottom:1px solid #e5dfdf;">Registered</th>

                  </tr>

                </thead>

                <tbody>

                  <tr

                    v-for="p in manageParticipants"

                    :key="p.id"

                    style="border-bottom:1px solid #f0eded;"

                  >

                    <td style="padding:10px 0;">{{ p.volunteer_name }}</td>

                    <td style="padding:10px 0;">

                      <span

                        :style="{

                          background: p.status === 'attended' ? '#dcfce7' : p.status === 'registered' ? '#fef3c7' : '#e5e7eb',

                          color: p.status === 'attended' ? '#166534' : p.status === 'registered' ? '#92400e' : '#6b7280',

                          padding: '2px 8px',

                          borderRadius: '99px',

                          fontSize: '0.75rem',

                          fontWeight: '700',

                          textTransform: 'uppercase',

                          display: 'inline-block'

                        }"

                      >

                        {{ p.status }}

                      </span>

                    </td>

                    <td style="padding:10px 0; color:#6b7280; font-size:0.85rem;">

                      {{ p.registered_at ? new Date(p.registered_at).toLocaleString('en-PH', { month:'short', day:'numeric', year:'numeric', hour:'2-digit', minute:'2-digit' }) : 'N/A' }}

                    </td>

                  </tr>

                </tbody>

              </table>

            </div>

          </div>

        </div>

      </div>

      <div

        v-if="deleteModalOpen"

        class="

          event-modal-backdrop

        "

        @click.self="

          closeDeleteModal

        "

      >

        <div

          class="event-delete-modal"

        >

          <div

            class="

              event-delete-top-line

            "

          ></div>



          <div

            class="

              event-delete-content

            "

          >

            <div

              class="

                event-delete-heading

              "

            >

              <div

                class="

                  event-delete-icon

                "

              >

                <Trash2 :size="21" />

              </div>



              <div>

                <span

                  class="

                    event-delete-label

                  "

                >

                  DESTRUCTIVE ACTION

                </span>

                <h2>

                  Delete Volunteer Event?

                </h2>

              </div>

            </div>



            <p

              class="

                event-delete-description

              "

            >

              Are you sure you want to

              permanently delete this event?

              This action will immediately

              purge the record from the

              Pahinungod mission ledger and

              cannot be reversed.

            </p>



            <label

              class="

                event-delete-confirm

              "

            >

              <input

                v-model="

                  deleteConfirmed

                "

                type="checkbox"

              />

              <span>

                I understand that this draft

                deployment and its entire

                staging history will be

                irreversibly removed from

                UP Mindanao servers.

              </span>

            </label>

          </div>



          <div

            class="

              event-delete-actions

            "

          >

            <button

              class="

                event-delete-cancel

              "

              @click="

                closeDeleteModal

              "

            >

              Cancel, Keep Event

            </button>



            <button

              class="

                event-delete-permanent

              "

              :disabled="

                !deleteConfirmed

              "

              @click="

                deleteEvent

              "

            >

              <Trash2 :size="16" />

              Delete Event Permanently

            </button>

          </div>

        </div>

      </div>

    </div>

  </div>

</template>



<style>

@import '../../styles/admin.css';

@import '../../styles/admin/events.css';

</style>
