<script setup>
import { ref, onMounted, computed } from 'vue'
import { MapPin, GraduationCap, ArrowRight } from 'lucide-vue-next'
import { meService } from '../../api/me'
import { volunteerService } from '../../api/volunteers'
import { participationService } from '../../api/participations'

function exportRecord() {
  window.print()
}

// Badges are still hardcoded (partner's task)
const badges = [
  { name: 'Sibol Lingkod', image: '/images/badges/b1.png' },
  { name: 'Tapat Gampan', image: '/images/badges/b2.png' },
  { name: 'Tapat Pahinungod', image: '/images/badges/b3.png' },
  { name: 'Kalingang Likas', image: '/images/badges/b4.png' },
  { name: 'Lawak Lingap', image: '/images/badges/b5.png' },
  { name: 'Tanglaw Dunong', image: '/images/badges/b6.png' }
];

const loading = ref(true)
const user = ref(null)
const volunteer = ref(null)
const emergency = ref(null)
const participations = ref([])

const activeParticipations = computed(() =>
  participations.value.filter(p => p.status !== 'cancelled')
)

onMounted(async () => {
  try {
    const { data: me } = await meService.get()
    user.value = me

    if (me.volunteer?.id) {
      const [volRes, profileRes, partRes] = await Promise.all([
        volunteerService.get(me.volunteer.id),
        volunteerService.myProfile(),
        participationService.myParticipations()
      ])
      volunteer.value = volRes.data
      emergency.value = profileRes.data.emergency
      participations.value = partRes.data
    }
  } catch (err) {
    console.error('Failed to load profile:', err)
  } finally {
    loading.value = false
  }
})

// Helpers for display
const displayAffiliation = computed(() => {
  if (!volunteer.value) return 'Volunteer'
  const t = volunteer.value.affiliation_type
  return t.charAt(0).toUpperCase() + t.slice(1) + ' Volunteer'
})

const displaySex = computed(() => {
  if (volunteer.value?.sex === 'M') return 'Male'
  if (volunteer.value?.sex === 'F') return 'Female'
  return 'Not specified'
})

const formatDate = (iso) => {
  if (!iso) return 'N/A'
  return new Date(iso).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
}
</script>

<template>
  <section class="user-content user-profile-page">
    <!-- profile banner -->
    <div class="user-profile-banner">
      <img
        class="user-avatar-large"
        src="/images/gallery/cat.jpg"
        alt="Volunteer profile"
      />

      <div class="user-profile-summary">
        <div class="user-pills">
          <span class="pill-green">ACTIVE VOLUNTEER</span>
          <span class="pill-blue">CONSTITUENT: MINDANAO</span>
          <span class="pill-gold">ID: {{ volunteer?.volunteer_identifier || 'N/A' }}</span>
        </div>

        <h1>{{ volunteer?.full_name || user?.full_name || 'Loading...' }}</h1>
        <p>{{ displayAffiliation }} <span v-if="volunteer?.degree">({{ volunteer.degree }})</span> · UP Mindanao</p>

        <div class="user-summary-meta">
          <span>
            <GraduationCap :size="15" />
            Class of {{ volunteer?.birthdate ? new Date(volunteer.birthdate).getFullYear() + 4 : 'N/A' }}
          </span>
          <span>
            <MapPin :size="14" />
            {{ volunteer?.permanent_address || 'Address not set' }}
          </span>
        </div>
      </div>

      <div class="user-profile-actions">
        <RouterLink class="user-button user-button-primary" to="/user/profile/edit">
          Edit Profile
        </RouterLink>
        <button class="user-button user-button-light" type="button" @click="exportRecord">
          Export Record
        </button>
      </div>
    </div>

    <!-- activity and badges -->
    <div class="user-profile-columns">
      <section class="user-panel user-recent-panel">
        <div class="user-panel-heading">
          <h2>Recent Activity Log</h2>

          <RouterLink to="/user/events">
            Find events
            <ArrowRight :size="14" />
          </RouterLink>
        </div>

        <article v-for="p in activeParticipations.slice(0, 2)" :key="p.id" class="user-profile-activity">
          <img src="/images/programs/bloodletting.jpg" alt="Event image" />
          <div>
            <span class="user-eyebrow">{{ p.status.toUpperCase() }}</span>
            <h3>{{ p.event_name }}</h3>
            <p>Registered on {{ formatDate(p.registered_at) }}</p>
            <span class="user-activity-status">
              Participation record
            </span>
          </div>
        </article>
        
        <div v-if="activeParticipations.length === 0" style="padding: 20px; color: #666;">
          No recent activity yet. Join an event to get started!
        </div>

        <article class="user-profile-activity">
          <img
            src="/images/programs/bloodletting.jpg"
            alt="Health outreach"
          />

          <div>
            <span class="user-eyebrow">HEALTH</span>
            <h3>Bloodletting &amp; Health Outreach</h3>
            <p>
              Community healthcare and voluntary blood donation support.
            </p>
            <span class="user-activity-status">
              Activity history · Sample data
            </span>
          </div>
        </article>
      </section>

      <aside class="user-panel user-profile-badges">
        <div class="user-panel-heading">
          <h2>Badges</h2>
          <span>6 badges</span>
        </div>

        <div class="user-badge-grid">
          <div
            v-for="badge in badges"
            :key="badge.name"
            class="user-badge-item"
          >
            <img
              :src="badge.image"
              :alt="badge.name"
              @error="$event.target.style.display = 'none'"
            />
            <span>{{ badge.name }}</span>
          </div>
        </div>

        <p class="user-badge-quote">
          “Katangulan at dangal ang maglingkod sa sambayanan.”
        </p>
      </aside>
    </div>

    <!-- personal info -->
    <section class="user-info-section">
      <h2>Personal Information</h2>

      <div class="user-info-grid">
        <div>
          <small>FULL LEGAL NAME</small>
          <strong>{{ volunteer?.full_name || user?.full_name }}</strong>
        </div>
        <div>
          <small>NICKNAME</small>
          <strong>{{ volunteer?.nickname || 'N/A' }}</strong>
        </div>
        <div>
          <small>SEX ASSIGNED AT BIRTH</small>
          <strong>{{ displaySex }}</strong>
        </div>
        <div>
          <small>BIRTHDATE &amp; AGE</small>
          <strong>
            {{ formatDate(volunteer?.birthdate) }}
            <span v-if="volunteer?.age">({{ volunteer.age }} years old)</span>
          </strong>
        </div>
      </div>
    </section>

    <!-- contact and address -->
    <section class="user-info-section">
      <h2>Contact &amp; Address Information</h2>

      <div class="user-info-grid one-column">
        <div>
          <small>OFFICIAL EMAIL</small>
          <strong>{{ user?.email }}</strong>
        </div>

        <div>
          <small>PERMANENT / RESIDENTIAL ADDRESS</small>
          <strong>
            <MapPin :size="14" />
            {{ volunteer?.permanent_address || 'N/A' }}
          </strong>
        </div>

        <div class="user-emergency-info">
          <small>EMERGENCY CONTACT REPRESENTATIVE</small>
          <strong v-if="emergency?.contact_name">
            {{ emergency.contact_name }}
            <span v-if="emergency.relationship">({{ emergency.relationship }})</span>
          </strong>
          <strong v-else>Not set</strong>
        </div>
      </div>
    </section>

    <!-- UP affiliation -->
    <section class="user-info-section">
      <h2>UP Affiliation &amp; Civic Background</h2>

      <div class="user-info-grid">
        <div>
          <small>INSTITUTIONAL AFFILIATION</small>
          <strong>{{ displayAffiliation }}</strong>
        </div>
        <div>
          <small>CONSTITUENT UNIVERSITY (CU)</small>
          <strong>UP Mindanao</strong>
        </div>
        <div>
          <small>DEGREE PROGRAM</small>
          <strong>{{ volunteer?.degree || 'N/A' }}</strong>
        </div>
        <div>
          <small>STUDENT NUMBER</small>
          <strong>{{ volunteer?.student_number || 'N/A' }}</strong>
        </div>
        
        <!-- You can leave the program interests hardcoded or remove them -->
        <div class="user-service-pill-row">
          <small>DESIGNATED PROGRAM INTERESTS &amp; SERVICE PILLARS</small>
          <span>Affirmative Action Program</span>
          <span>Environmental Awareness</span>
        </div>
      </div>
    </section>

  </section>
</template>