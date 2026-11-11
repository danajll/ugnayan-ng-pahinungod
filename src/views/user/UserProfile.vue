<script setup>
import { MapPin, GraduationCap, ArrowRight } from 'lucide-vue-next';

function exportRecord() {
  window.print();
}

const badges = [
  { name: 'Sibol Lingkod', image: '/images/badges/b1.png' },
  { name: 'Tapat Gampan', image: '/images/badges/b2.png' },
  { name: 'Tapat Pahinungod', image: '/images/badges/b3.png' },
  { name: 'Kalingang Likas', image: '/images/badges/b4.png' },
  { name: 'Lawak Lingap', image: '/images/badges/b5.png' },
  { name: 'Tanglaw Dunong', image: '/images/badges/b6.png' }
];
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
          <span class="pill-gold">ID: UPP-MIN-2024-04921</span>
        </div>

        <h1>Dana Jill Santiago</h1>
        <p>Student (BS Computer Science) · UP Mindanao</p>

        <div class="user-summary-meta">
          <span>
            <GraduationCap :size="15" />
            Class of 2028
          </span>
          <span>
            <MapPin :size="14" />
            Mintal, Davao City
          </span>
        </div>
      </div>

      <div class="user-profile-actions">
        <RouterLink
          class="user-button user-button-primary"
          to="/user/profile/edit"
        >
          Edit Profile
        </RouterLink>

        <button
          class="user-button user-button-light"
          type="button"
          @click="exportRecord"
        >
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

        <article class="user-profile-activity">
          <img
            src="/images/programs/aap.jpg"
            alt="Affirmative Action Program"
          />

          <div>
            <span class="user-eyebrow">EDUCATION AND TUTORING</span>
            <h3>Affirmative Action Program (AAP)</h3>
            <p>
              Providing intensive tutorial sessions, college admission test
              prep, and customized learning materials.
            </p>
            <span class="user-activity-status">
              Participation record · Sample data
            </span>
          </div>
        </article>

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
          <strong>Dana Jill Santiago</strong>
        </div>

        <div>
          <small>NICKNAME</small>
          <strong>Dana</strong>
        </div>

        <div>
          <small>SEX ASSIGNED AT BIRTH</small>
          <strong>Female</strong>
        </div>

        <div>
          <small>BIRTHDATE &amp; AGE</small>
          <strong>
            March 03, 2006
            <span>(20 years old)</span>
          </strong>
        </div>
      </div>
    </section>

    <!-- contact and address -->
    <section class="user-info-section">
      <h2>Contact &amp; Address Information</h2>

      <div class="user-info-grid one-column">
        <div>
          <small>OFFICIAL UP MAIL</small>
          <strong>dpsantiago1@up.edu.ph</strong>
        </div>

        <div>
          <small>PERMANENT / RESIDENTIAL ADDRESS</small>
          <strong>
            <MapPin :size="14" />
            Mintal, Tugbok District, Davao City, 8000
          </strong>
        </div>

        <div class="user-emergency-info">
          <small>EMERGENCY CONTACT REPRESENTATIVE</small>
          <strong>
            Roronoa Zoro
            <span>(Spouse)</span>
          </strong>
        </div>
      </div>
    </section>

    <!-- UP affiliation -->
    <section class="user-info-section">
      <h2>UP Affiliation &amp; Civic Background</h2>

      <div class="user-info-grid">
        <div>
          <small>INSTITUTIONAL AFFILIATION</small>
          <strong>Student Volunteer</strong>
        </div>

        <div>
          <small>CONSTITUENT UNIVERSITY (CU)</small>
          <strong>UP Mindanao</strong>
        </div>

        <div>
          <small>DEGREE PROGRAM</small>
          <strong>BS Computer Science</strong>
        </div>

        <div>
          <small>STUDENT NUMBER</small>
          <strong>2021-04921</strong>
        </div>

        <div class="user-service-pill-row">
          <small>DESIGNATED PROGRAM INTERESTS &amp; SERVICE PILLARS</small>
          <span>Affirmative Action Program</span>
          <span>Environmental Awareness</span>
        </div>
      </div>
    </section>

    <p class="user-demo-note">
      This profile currently uses my sample display information. Connect the fields
      to approved user/account API. (I'll remove this later.)
    </p>
  </section>
</template>