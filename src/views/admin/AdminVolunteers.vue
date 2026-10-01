<script setup>

import { computed, ref } from 'vue';

import {
  Search,
  ChevronLeft,
  ChevronRight,
  Eye
} from 'lucide-vue-next';


const search = ref('');

const volunteers = [

  {
    name: 'Dana Jill Santiago',
    id: '2024-13406',
    affiliation: 'Student',
    degree: 'BS Computer Science',
    timeIn: '3:03 am',
    timeOut: '3:03 pm'
  },

  {
    name: 'Dana Jill Santiago',
    id: '2024-13406',
    affiliation: 'Faculty',
    degree: 'Computer Science',
    timeIn: '3:03 am',
    timeOut: '3:03 pm'
  },

  {
    name: 'Maria Santos',
    id: '2023-10521',
    affiliation: 'Student',
    degree: 'BS Biology',
    timeIn: '7:15 am',
    timeOut: '4:00 pm'
  }

];


const filteredVolunteers = computed(() => {

  const value = search.value.toLowerCase();

  return volunteers.filter((volunteer) => {

    return (
      volunteer.name.toLowerCase().includes(value) ||
      volunteer.id.toLowerCase().includes(value) ||
      volunteer.degree.toLowerCase().includes(value)
    );

  });

});

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
            Showing {{ filteredVolunteers.length }} of 1,143 registered volunteer records
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