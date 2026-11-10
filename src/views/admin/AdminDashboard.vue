<script setup>
import { ref, onMounted, computed } from 'vue'
import { CalendarDays, MapPin, Search, ArrowRight, ChevronLeft, ChevronRight } from 'lucide-vue-next'
import { eventService } from '../../api/events'
import { volunteerService } from '../../api/volunteers'

const eventFilter = ref('All Active')
const volunteerSearch = ref('')
const eventFilters = ['All Active', 'Field Deployment', 'Tutoring', 'Medical Mission', 'Others']

// Start empty
const events = ref([])
const volunteers = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const [evRes, volRes] = await Promise.all([
      eventService.list(),
      volunteerService.list()
    ])

    // Map events. Note: Backend doesn't have "status" or "capacity" yet, 
    // so we mock some UI fields.
    events.value = evRes.data.map(e => ({
      id: e.id,
      status: 'Open for Registration', 
      title: e.name,
      location: e.location,
      date: new Date(e.start_datetime).toLocaleDateString(),
      capacity: 50, // Mock
      confirmed: 45, // Mock
      coordinator: 'Admin', // Mock
      role: 'Coordinator'
    }))

    // Map volunteers (reuse logic from AdminVolunteers)
    volunteers.value = volRes.data.map(v => ({
      name: `${v.first_name} ${v.last_name}`,
      id: v.volunteer_identifier,
      affiliation: v.affiliation_type,
      timeIn: 'N/A',
      timeOut: 'N/A'
    }))

  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})

const filteredEvents = computed(() => {
  // Simple mock filter since backend doesn't have categories yet
  return events.value
})
</script>

<template>

  <div class="admin-page dashboard-page">

    <div class="admin-page-inner dashboard-inner">

      <!-- events -->
      <section class="dashboard-events-section">

        <div class="dashboard-section-header">

          <h2 class="admin-section-title">
            CURRENT & ONGOING EVENTS
          </h2>

          <div class="dashboard-event-tabs">

            <button
              v-for="filter in eventFilters"
              :key="filter"
              class="dashboard-event-tab"
              :class="{ active: eventFilter === filter }"
              @click="eventFilter = filter"
            >
              {{ filter }}
            </button>

          </div>

        </div>

        <div class="dashboard-event-grid">

          <article
            v-for="event in events"
            :key="event.status"
            class="dashboard-event-card"
          >

            <div class="dashboard-event-top">

              <span
                class="dashboard-event-status"
                :class="{
                  'open': event.status === 'Open for Registration',
                  'booked': event.status === 'Fully Booked'
                }"
              >

                <span class="status-dot"></span>

                {{ event.status }}

              </span>

              <span class="dashboard-event-date">

                <CalendarDays :size="14" />

                {{ event.date }}

              </span>

            </div>

            <h3 class="dashboard-event-title">
              {{ event.title }}
            </h3>

            <div class="dashboard-event-location">

              <MapPin :size="16" />

              {{ event.location }}

            </div>

            <div class="dashboard-capacity">

              <div class="dashboard-capacity-heading">

                <span>
                  Capacity
                </span>

                <strong>
                  {{ event.confirmed }} / {{ event.capacity }} Confirmed
                </strong>

              </div>

              <div class="dashboard-capacity-bar">

                <span
                  :style="{
                    width: `${(event.confirmed / event.capacity) * 100}%`
                  }"
                ></span>

              </div>

            </div>

            <div class="dashboard-event-footer">

              <div class="dashboard-coordinator">

                <div class="dashboard-avatar">
                  DJ
                </div>

                <div>

                  <strong>
                    {{ event.coordinator }}
                  </strong>

                  <span>
                    {{ event.role }}
                  </span>

                </div>

              </div>

              <button class="dashboard-manage-button">

                Manage

                <ArrowRight :size="15" />

              </button>

            </div>

          </article>

        </div>

        <div class="dashboard-more-events">

          <RouterLink to="/admin/events">

            More Events

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
                  TIME IN
                </th>

                <th>
                  TIME OUT
                </th>

                <th>
                  QUICK ACTION
                </th>

              </tr>

            </thead>

            <tbody>

              <tr
                v-for="volunteer in volunteers"
                :key="volunteer.affiliation"
              >

                <td>

                  <div class="volunteer-name">

                    <strong>
                      {{ volunteer.name }}
                    </strong>

                    <span>
                      {{ volunteer.id }}
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
                  {{ volunteer.timeIn }}
                </td>

                <td>
                  {{ volunteer.timeOut }}
                </td>

                <td>

                  <button class="view-profile-button">
                    View Profile
                  </button>

                </td>

              </tr>

            </tbody>

          </table>

          <div class="dashboard-table-footer">

            <span>
              Showing 2 of 1,143 registered volunteer records
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