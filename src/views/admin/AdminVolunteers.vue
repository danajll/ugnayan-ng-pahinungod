<script setup>
import { computed, ref, onMounted } from 'vue'
import { Search, ChevronLeft, ChevronRight, Eye } from 'lucide-vue-next'
import { volunteerService } from '../../api/volunteers'

const search = ref('')
const volunteers = ref([]) // Start empty
const loading = ref(true)
const error = ref(null)

// Fetch real data on mount
onMounted(async () => {
  try {
    const { data } = await volunteerService.list()
    // Map Django output to match your table's expected fields
    volunteers.value = data.map(v => ({
      name: `${v.first_name} ${v.last_name}`,
      id: v.volunteer_identifier,
      affiliation: v.affiliation_type, // 'student', 'faculty', etc.
      degree: v.degree || 'N/A',
      timeIn: 'N/A', // Backend doesn't track this yet
      timeOut: 'N/A'
    }))
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load volunteers.'
  } finally {
    loading.value = false
  }
})

const filteredVolunteers = computed(() => {
  const value = search.value.toLowerCase()
  return volunteers.value.filter((volunteer) => {
    return (
      volunteer.name.toLowerCase().includes(value) ||
      volunteer.id.toLowerCase().includes(value) ||
      volunteer.degree.toLowerCase().includes(value)
    )
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
                TIME OUT
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
                    {{ volunteer.id }}
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
                {{ volunteer.timeOut }}
              </td>


              <td>

                <button class="directory-view-button">

                  <Eye
                    :size="15"
                  />

                  View Profile

                </button>

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