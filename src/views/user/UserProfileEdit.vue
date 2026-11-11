<script setup>
import { reactive, ref } from 'vue';
import { MapPin, GraduationCap, ArrowLeft, CheckCircle2 } from 'lucide-vue-next';

const saved = ref(false);

const profile = reactive({
  fullName: 'Dana Jill Santiago',
  nickname: 'Dana',
  sex: 'Female',
  birthdate: '2006-03-03',
  email: 'dpsantiago1@up.edu.ph',
  address: 'Mintal, Tugbok District, Davao City, 8000',
  emergencyName: 'Roronoa Zoro',
  emergencyRelationship: 'Spouse',
  emergencyPhone: '+63 917 000 0000',
  affiliation: 'Student Volunteer',
  university: 'UP Mindanao',
  degree: 'BS Computer Science',
  studentNumber: '2021-04921'
});

function saveProfile() {
  saved.value = true;
}
</script>

<template>
  <section class="user-content user-edit-page">
    <RouterLink class="user-back-link" to="/user/profile">
      <ArrowLeft :size="15" />
      Back to My Profile
    </RouterLink>

    <!-- profile banner -->
    <div class="user-profile-banner user-edit-banner">
      <img
        class="user-avatar-large"
        src="/images/gallery/gallery1.jpg"
        alt="Volunteer profile"
      />

      <div class="user-profile-summary">
        <div class="user-pills">
          <span class="pill-green">ACTIVE VOLUNTEER</span>
          <span class="pill-blue">CONSTITUENT: MINDANAO</span>
          <span class="pill-gold">ID: UPP-MIN-2024-04921</span>
        </div>

        <h1>{{ profile.fullName }}</h1>
        <p>Student ({{ profile.degree }}) · {{ profile.university }}</p>

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
        <button
          class="user-button user-button-primary"
          type="button"
          @click="saveProfile"
        >
          Save Profile
        </button>

        <RouterLink
          class="user-button user-button-light"
          to="/user/profile"
        >
          Cancel
        </RouterLink>
      </div>
    </div>

    <!-- edit profile form -->
    <form class="user-edit-form" @submit.prevent="saveProfile">
      <section class="user-info-section">
        <h2>Personal Information</h2>

        <div class="user-form-grid">
          <label>
            FULL LEGAL NAME
            <input v-model="profile.fullName" required />
          </label>

          <label>
            NICKNAME
            <input v-model="profile.nickname" />
          </label>

          <label>
            SEX ASSIGNED AT BIRTH
            <select v-model="profile.sex">
              <option>Female</option>
              <option>Male</option>
              <option>Prefer not to say</option>
            </select>
          </label>

          <label>
            BIRTHDATE
            <input v-model="profile.birthdate" type="date" />
          </label>
        </div>
      </section>

      <section class="user-info-section">
        <h2>Contact &amp; Address Information</h2>

        <div class="user-form-grid">
          <label class="full-width">
            OFFICIAL UP MAIL
            <input v-model="profile.email" type="email" required />
          </label>

          <label class="full-width">
            PERMANENT / RESIDENTIAL ADDRESS
            <input v-model="profile.address" />
          </label>

          <label>
            EMERGENCY CONTACT REPRESENTATIVE
            <input v-model="profile.emergencyName" />
          </label>

          <label>
            RELATIONSHIP
            <input v-model="profile.emergencyRelationship" />
          </label>

          <label>
            EMERGENCY CONTACT NUMBER
            <input v-model="profile.emergencyPhone" type="tel" />
          </label>
        </div>
      </section>

      <section class="user-info-section">
        <h2>UP Affiliation &amp; Civic Background</h2>

        <div class="user-form-grid">
          <label>
            INSTITUTIONAL AFFILIATION
            <input v-model="profile.affiliation" />
          </label>

          <label>
            CONSTITUENT UNIVERSITY
            <input v-model="profile.university" />
          </label>

          <label>
            DEGREE PROGRAM
            <input v-model="profile.degree" />
          </label>

          <label>
            STUDENT NUMBER
            <input v-model="profile.studentNumber" />
          </label>
        </div>

        <p class="user-form-note">
          Your student number and official university information may need
          verification by an authorized administrator.
        </p>
      </section>

      <div v-if="saved" class="user-save-message">
        <CheckCircle2 :size="17" />
        Changes are reflected in this form for now. Backend saving is not
        connected yet.
      </div>

      <div class="user-form-actions">
        <RouterLink
          class="user-button user-button-light"
          to="/user/profile"
        >
          Cancel
        </RouterLink>

        <button class="user-button user-button-primary" type="submit">
          Save Profile
        </button>
      </div>
    </form>
  </section>
</template>