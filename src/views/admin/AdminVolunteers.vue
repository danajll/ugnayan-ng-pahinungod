<script setup>
import { computed, ref, onMounted } from 'vue'
import { Search, ChevronLeft, ChevronRight, Eye, Filter } from 'lucide-vue-next'
import { volunteerService } from '../../api/volunteers'

const search = ref('')
const affiliationFilter = ref('all')
const volunteers = ref([]) // Start empty
const loading = ref(true)
const error = ref(null)

const affiliationOptions = [
  { value: 'all', label: 'All Affiliations' },
  { value: 'student', label: 'Student' },
  { value: 'faculty', label: 'Faculty' },
  { value: 'staff', label: 'Staff' },
  { value: 'alumni', label: 'Alumni' },
]

const formatDateTime = (iso) => {
  if (!iso) return 'N/A'
  return new Date(iso).toLocaleString('en-PH', {
    month: 'short', day: 'numeric', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}

// Fetch real data on mount
onMounted(async () => {
  try {
    const { data } = await volunteerService.list()
    // Map Django output to match your table's expected fields
    volunteers.value = data.map(v => ({
      id: v.id, // <-- Actual DB ID for routing
      identifier: v.volunteer_identifier, // <-- Display ID
      name: `${v.first_name} ${v.last_name}`,
      affiliation: v.affiliation_type,
      degree: v.degree || 'N/A',
      status: v.status, // <-- 'pending' | 'active' | 'inactive' | 'suspended'
      timeIn: formatDateTime(v.onboarding_completed_at),
    }))
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load volunteers.'
  } finally {
    loading.value = false
  }
})

const filteredVolunteers = computed(() => {
  const value = search.value.toLowerCase()
  const aff = affiliationFilter.value
  return volunteers.value.filter((volunteer) => {
    const matchesSearch =
      volunteer.name.toLowerCase().includes(value) ||
      volunteer.identifier.toLowerCase().includes(value)
    const matchesAffiliation = aff === 'all' || volunteer.affiliation === aff
    return matchesSearch && matchesAffiliation
  })
})
</script>


<template>

  <div class="admin-page volunteers-page">

    <div class="admin-page-inner">

      <!-- header -->

      <div class="volunteers-header">

        <div>

          <h1>
            VOLUNTEER DIRECTORY
          </h1>

          <p>
            View and manage registered volunteer records.
          </p>

        </div>


        <div class="volunteers-search">

          <Filter
            :size="17"
          />

          <select
            v-model="affiliationFilter"
            class="affiliation-filter"
          >
            <option
              v-for="opt in affiliationOptions"
              :key="opt.value"
              :value="opt.value"
            >
              {{ opt.label }}
            </option>
          </select>

          <Search
            :size="17"
          />

          <input
            v-model="search"
            type="text"
            placeholder="Search volunteers..."
          />

        </div>

      </div>


      <!-- table -->

      <div class="volunteers-table-wrapper">

        <table class="volunteers-table">

          <thead>

            <tr>

              <th>
                VOLUNTEER NAME & ID
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
                ACTION
              </th>

            </tr>

          </thead>


          <tbody>

            <tr
              v-for="volunteer in filteredVolunteers"
              :key="volunteer.id + volunteer.affiliation"
            >

              <td>

                <div class="volunteer-directory-name">

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
                  class="directory-affiliation"
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
                  class="directory-status"
                  :class="`status-${volunteer.status}`"
                >
                  {{ volunteer.status === 'active' ? 'Onboarded' : 'Pending Verification' }}
                </span>
              </td>


              <td>
                <RouterLink :to="`/admin/volunteers/${volunteer.id}`" class="directory-view-button" style="text-decoration: none; display: inline-flex; align-items: center; gap: 6px;">
                  <Eye :size="15" />
                  View Profile
                </RouterLink>
              </td>

            </tr>

          </tbody>

        </table>


        <!-- footer -->

        <div class="volunteers-footer">

          <span>
            Showing {{ filteredVolunteers.length }} records
          </span>


          <div class="directory-pagination">

            <button disabled>

              <ChevronLeft
                :size="15"
              />

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

              <ChevronRight
                :size="15"
              />

            </button>

          </div>

        </div>

      </div>

    </div>

  </div>

</template>


<style>

@import '../../styles/admin.css';

@import '../../styles/admin/volunteers.css';

</style>