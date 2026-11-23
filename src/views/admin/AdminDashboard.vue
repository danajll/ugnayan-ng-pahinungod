<script setup>
import { computed, ref, onMounted } from 'vue'
import { CalendarDays, MapPin, Search, ArrowRight, ChevronLeft, ChevronRight, Eye, UsersRound, X, Clock3 } from 'lucide-vue-next'
import { eventService } from '../../api/events'
import { volunteerService } from '../../api/volunteers'

const volunteerSearch = ref('')
const eventProximity = ref('all')

const events = ref([])
const volunteers = ref([])
const loading = ref(true)

const eventProximities = ['All', 'Today', 'This Week', 'This Month']

const formatDate = (iso) =>
  iso ? new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : ''

const formatDateTime = (iso) => {
  if (!iso) return 'N/A'
  return new Date(iso).toLocaleString('en-PH', {
    month: 'short', day: 'numeric', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}

const daysFromNow = (iso) => {
  if (!iso) return null
  const start = new Date(iso)
  const now = new Date()
  now.setHours(0, 0, 0, 0)
  start.setHours(0, 0, 0, 0)
  return Math.round((start - now) / (1000 * 60 * 60 * 24))
}

// Map a Django Event to the shape the dashboard card expects
const mapEvent = (e) => ({
  id: e.id,
  title: e.name,
  category: e.category,
  date: formatDate(e.start_datetime),
  start_datetime: e.start_datetime,
  end_datetime: e.end_datetime,
  location: e.location || 'Location to be announced',
  city: e.city || '',
  status: e.status,
  live_status: e.live_status || 'Scheduled',
  quota: e.quota ?? 0,
  registered: e.registered_count ?? 0,
})

const getEventStatus = (event) => {
  const slotsLeft = Math.max((event.quota || 0) - (event.registered || 0), 0)
  const live = event.live_status || 'Scheduled'

  if (live === 'Concluded') {
    return { label: 'Concluded', class: 'concluded' }
  }
  if (slotsLeft <= 0) {
    return { label: 'Closed', class: 'closed' }
  }
  const end = event.end_datetime ? new Date(event.end_datetime) : null
  const now = new Date()
  if (end && (end - now) / (1000 * 60 * 60 * 24) < 1) {
    return { label: 'Closed', class: 'closed' }
  }
  if (live === 'Happening Soon') return { label: 'Happening Soon', class: 'ongoing' }
  if (live === 'Happening Now') return { label: 'Happening Now', class: 'ongoing' }

  return { label: 'Recruiting', class: 'recruiting' }
}

onMounted(async () => {
  try {
    const [evRes, volRes] = await Promise.all([
      eventService.list(),
      volunteerService.list()
    ])

    events.value = evRes.data.map(mapEvent)

    volunteers.value = volRes.data.map(v => ({
      id: v.id,
      identifier: v.volunteer_identifier,
      name: `${v.first_name} ${v.last_name}`,
      affiliation: v.affiliation_type,
      degree: v.degree || 'N/A',
      status: v.status,
      timeIn: formatDateTime(v.onboarding_completed_at),
    }))

  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})

const filteredEvents = computed(() => {
  return events.value.filter((event) => {
    if (event.live_status === 'Concluded') return false

    const days = daysFromNow(event.start_datetime)
    let matchesProximity = true
    if (eventProximity.value === 'Today') {
      matchesProximity = days === 0
    } else if (eventProximity.value === 'This Week') {
      matchesProximity = days !== null && days >= 0 && days <= 7
    } else if (eventProximity.value === 'This Month') {
      matchesProximity = days !== null && days >= 0 && days <= 30
    }

    return matchesProximity
  })
})

const filteredVolunteers = computed(() => {
  const value = volunteerSearch.value.toLowerCase()
  return volunteers.value.filter((volunteer) => {
    const matchesSearch =
      volunteer.name.toLowerCase().includes(value) ||
      volunteer.identifier.toLowerCase().includes(value)
    const isFacultyOrStaff =
      volunteer.affiliation === 'faculty' || volunteer.affiliation === 'staff'
    return matchesSearch && isFacultyOrStaff
  })
})
</script>

<template>

  <div class="admin-page dashboard-page">

    <div class="admin-page-inner dashboard-inner">

      <!-- events -->
      <section class="dashboard-events-section">

        <div class="dashboard-section-header">

          <h2 class="admin-section-title">
            ONGOING & UPCOMING EVENTS
          </h2>

          <div class="dashboard-event-toolbar">

            <div class="dashboard-event-tabs">
              <button
                v-for="item in eventProximities"
                :key="item"
                class="dashboard-event-tab"
                :class="{ active: eventProximity === item }"
                @click="eventProximity = item"
              >
                {{ item }}
              </button>
            </div>

          </div>

        </div>

        <div class="dashboard-event-grid">

          <article
            v-for="event in filteredEvents"
            :key="event.id"
            class="dashboard-event-card"
          >

            <div class="dashboard-event-top">

              <span
                class="dashboard-event-status"
                :class="getEventStatus(event).class"
              >
                <span class="status-dot"></span>
                {{ getEventStatus(event).label }}
              </span>

              <span class="dashboard-event-date">
                <CalendarDays :size="14" />
                {{ event.date }}
              </span>

            </div>

            <span class="dashboard-event-category">
              {{ event.category }}
            </span>

            <h3 class="dashboard-event-title">
              {{ event.title }}
            </h3>

            <div class="dashboard-event-location">
              <MapPin :size="16" />
              {{ event.location }}{{ event.city ? ', ' + event.city : '' }}
            </div>

            <div class="dashboard-capacity">
              <div class="dashboard-capacity-heading">
                <span>Volunteer Quota</span>
                <strong>
                  {{ event.registered }} / {{ event.quota }} Registered
                </strong>
              </div>
              <div class="dashboard-capacity-bar">
                <span
                  :style="{
                    width: event.quota ? `${(event.registered / event.quota) * 100}%` : '0%'
                  }"
                ></span>
              </div>
            </div>

          </article>

        </div>

        <div class="dashboard-more-events">
          <RouterLink to="/admin/events">
            Go to Event Dashboard
            <ArrowRight :size="16" />
          </RouterLink>
        </div>

      </section>

      <!-- personnel -->
      <section class="dashboard-personnel-section">

        <div class="dashboard-personnel-heading">

          <h2 class="admin-section-title">
            PERSONNEL REGISTRY
          </h2>

          <div class="dashboard-personnel-actions">

            <div class="dashboard-search">
              <Search :size="17" />
              <input
                v-model="volunteerSearch"
                type="text"
                placeholder="Filter by name, degree, ID..."
              />
            </div>

            <RouterLink
              to="/admin/volunteers"
              class="dashboard-view-all"
            >
              View All Volunteers
              <ArrowRight :size="16" />
            </RouterLink>

          </div>

        </div>

        <div class="dashboard-table-wrapper">

          <table class="dashboard-table">

            <thead>
              <tr>
                <th>
                  VOLUNTEER<br>
                  NAME & ID
                </th>
                <th>
                  AFFILIATION
                </th>
                <th>
                  DEGREE / PROGRAM
                </th>
                <th>
                  TIME IN
                </th>
                <th>
                  STATUS
                </th>
                <th>
                  QUICK ACTION
                </th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="volunteer in filteredVolunteers"
                :key="volunteer.id"
              >

                <td>
                  <div class="volunteer-name">
                    <strong>
                      {{ volunteer.name }}
                    </strong>
                    <span>
                      {{ volunteer.identifier }}
                    </span>
                  </div>
                </td>

                <td>
                  <span
                    class="affiliation-badge"
                    :class="volunteer.affiliation.toLowerCase()"
                  >
                    {{ volunteer.affiliation }}
                  </span>
                </td>

                <td>
                  {{ volunteer.degree }}
                </td>

                <td>
                  {{ volunteer.timeIn }}
                </td>

                <td>
                  <span
                    class="dashboard-status"
                    :class="volunteer.status === 'active' ? 'active' : 'pending'"
                  >
                    {{ volunteer.status === 'active' ? 'Onboarded' : 'Pending Verification' }}
                  </span>
                </td>

                <td>
                  <RouterLink
                    :to="`/admin/volunteers/${volunteer.id}`"
                    class="view-profile-button"
                  >
                    View Profile
                  </RouterLink>
                </td>

              </tr>
            </tbody>

          </table>

          <div class="dashboard-table-footer">
            <span>
              Showing {{ filteredVolunteers.length }} of {{ volunteers.length }} registered volunteer records
            </span>
            <div class="dashboard-pagination">
              <button disabled>
                <ChevronLeft :size="15" />
                Previous
              </button>
              <button class="active">
                1
              </button>
              <button>
                2
              </button>
              <button>
                3
              </button>
              <span>
                ...
              </span>
              <button>
                250
              </button>
              <button>
                Next
                <ChevronRight :size="15" />
              </button>
            </div>
          </div>

        </div>

      </section>

    </div>

  </div>

</template>

<style>

@import '../../styles/admin.css';

@import '../../styles/admin/dashboard.css';

</style>