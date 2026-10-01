<script setup>

import {
  Trophy,
  Medal,
  Star,
  Award
} from 'lucide-vue-next';


const badges = [
  {
    title: 'First Service',
    description: 'Completed your first volunteer mission.',
    icon: Star,
    progress: 100
  },

  {
    title: 'Community Builder',
    description: 'Participated in five community missions.',
    icon: Medal,
    progress: 80
  },

  {
    title: 'Pahinungod Champion',
    description: 'Completed ten volunteer missions.',
    icon: Trophy,
    progress: 40
  },

  {
    title: 'Service Leader',
    description: 'Led or coordinated a volunteer activity.',
    icon: Award,
    progress: 20
  }
];

</script>


<template>

  <div class="admin-page progress-page">

    <div class="admin-page-inner">

      <!-- header -->

      <div class="progress-header">

        <div>

          <h1>
            VOLUNTEER PROGRESS & BADGES
          </h1>

          <p>
            Monitor volunteer participation and recognition.
          </p>

        </div>

      </div>


      <!-- summary -->

      <div class="progress-summary">

        <div class="progress-summary-card">

          <span>
            ACTIVE VOLUNTEERS
          </span>

          <strong>
            1,143
          </strong>

        </div>


        <div class="progress-summary-card">

          <span>
            MISSIONS COMPLETED
          </span>

          <strong>
            328
          </strong>

        </div>


        <div class="progress-summary-card">

          <span>
            BADGES AWARDED
          </span>

          <strong>
            2,418
          </strong>

        </div>

      </div>


      <!-- badge progress -->

      <h2 class="progress-section-title">
        BADGE PROGRESS
      </h2>


      <div class="badge-grid">

        <article
          v-for="badge in badges"
          :key="badge.title"
          class="badge-card"
        >

          <div class="badge-icon">

            <component
              :is="badge.icon"
              :size="25"
            />

          </div>


          <h3>
            {{ badge.title }}
          </h3>


          <p>
            {{ badge.description }}
          </p>


          <div class="badge-progress">

            <div>

              <span>
                Progress
              </span>

              <strong>
                {{ badge.progress }}%
              </strong>

            </div>


            <div class="badge-progress-bar">

              <span
                :style="{
                  width: `${badge.progress}%`
                }"
              ></span>

            </div>

          </div>

        </article>

      </div>

    </div>

  </div>

</template>


<style>

@import '../../styles/admin.css';

@import '../../styles/admin/progress.css';

</style>