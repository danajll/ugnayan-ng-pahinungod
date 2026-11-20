<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { MapPin, GraduationCap, ArrowLeft, CheckCircle2 } from 'lucide-vue-next'
import { meService } from '../../api/me'
import { volunteerService } from '../../api/volunteers'

const router = useRouter()
const loading = ref(true)
const saving = ref(false)
const saved = ref(false)
const error = ref(null)
const volunteerId = ref(null)

const form = reactive({
  first_name: '',
  middle_name: '',
  last_name: '',
  nickname: '',
  sex: '',
  birthdate: '',
  mobile_number: '',
  permanent_address: '',
  emergency_name: '',
  emergency_relationship: '',
  emergency_mobile: '',
  emergency_address: ''
})

onMounted(async () => {
  try {
    const { data: me } = await meService.get()
    if (!me.volunteer?.id) throw new Error("No volunteer profile")
    
    volunteerId.value = me.volunteer.id
    
    const [volRes, profileRes] = await Promise.all([
      volunteerService.get(me.volunteer.id),
      volunteerService.myProfile()
    ])
    
    const v = volRes.data
    form.first_name = v.first_name
    form.middle_name = v.middle_name
    form.last_name = v.last_name
    form.nickname = v.nickname
    form.sex = v.sex // 'M' or 'F'
    form.birthdate = v.birthdate
    form.mobile_number = v.mobile_number
    form.permanent_address = v.permanent_address
    
    const em = profileRes.data.emergency
    if (em) {
      form.emergency_name = em.contact_name
      form.emergency_relationship = em.relationship
      form.emergency_mobile = em.contact_mobile_number
      form.emergency_address = em.complete_address
    }
  } catch (err) {
    error.value = 'Failed to load profile data.'
  } finally {
    loading.value = false
  }
})

async function saveProfile() {
  saving.value = true
  saved.value = false
  error.value = null
  
  try {
    // 1. Update core volunteer info
    await volunteerService.patch(volunteerId.value, {
      first_name: form.first_name,
      middle_name: form.middle_name,
      last_name: form.last_name,
      nickname: form.nickname,
      sex: form.sex,
      birthdate: form.birthdate,
      mobile_number: form.mobile_number,
      permanent_address: form.permanent_address,
    })
    
    // 2. Update emergency contact
    await volunteerService.updateProfile({
      emergency: {
        contact_name: form.emergency_name,
        relationship: form.emergency_relationship,
        contact_mobile_number: form.emergency_mobile,
        complete_address: form.emergency_address
      }
    })
    
    saved.value = true
    setTimeout(() => { saved.value = false }, 3000)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to save changes.'
  } finally {
    saving.value = false
  }
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
      <img class="user-avatar-large" src="/images/gallery/gallery1.jpg" alt="Volunteer profile" />

      <div class="user-profile-summary">
        <div class="user-pills">
          <span class="pill-green">ACTIVE VOLUNTEER</span>
          <span class="pill-blue">CONSTITUENT: MINDANAO</span>
        </div>

        <h1>{{ form.first_name || 'Loading...' }} {{ form.last_name }}</h1>
        <p>{{ form.sex === 'F' ? 'Female' : form.sex === 'M' ? 'Male' : '' }} Volunteer · UP Mindanao</p>

        <div class="user-summary-meta">
          <span>
            <MapPin :size="14" />
            {{ form.permanent_address || 'Address not set' }}
          </span>
        </div>
      </div>

      <div class="user-profile-actions">
        <button class="user-button user-button-primary" type="button" @click="saveProfile" :disabled="saving">
          {{ saving ? 'Saving...' : 'Save Profile' }}
        </button>
        <RouterLink class="user-button user-button-light" to="/user/profile">
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
            FIRST NAME
            <input v-model="form.first_name" required />
          </label>
          <label>
            LAST NAME
            <input v-model="form.last_name" required />
          </label>
          <label>
            MIDDLE NAME
            <input v-model="form.middle_name" />
          </label>
          <label>
            NICKNAME
            <input v-model="form.nickname" />
          </label>
          <label>
            SEX ASSIGNED AT BIRTH
            <select v-model="form.sex">
              <option value="F">Female</option>
              <option value="M">Male</option>
            </select>
          </label>
          <label>
            BIRTHDATE
            <input v-model="form.birthdate" type="date" />
          </label>
        </div>
      </section>

      <section class="user-info-section">
        <h2>Contact &amp; Address Information</h2>

        <div class="user-form-grid">
          <label class="full-width">
            MOBILE NUMBER
            <input v-model="form.mobile_number" type="tel" />
          </label>

          <label class="full-width">
            PERMANENT / RESIDENTIAL ADDRESS
            <input v-model="form.permanent_address" />
          </label>

          <label>
            EMERGENCY CONTACT NAME
            <input v-model="form.emergency_name" />
          </label>
          <label>
            RELATIONSHIP
            <input v-model="form.emergency_relationship" />
          </label>
          <label>
            EMERGENCY CONTACT NUMBER
            <input v-model="form.emergency_mobile" type="tel" />
          </label>
          <label>
            EMERGENCY COMPLETE ADDRESS
            <input v-model="form.emergency_address" />
          </label>
        </div>
      </section>

      <section class="user-info-section">
        <h2>UP Affiliation &amp; Civic Background</h2>

        <div class="user-form-grid">
          <label>
            INSTITUTIONAL AFFILIATION
            <input value="Volunteer" disabled />
          </label>
          <label>
            CONSTITUENT UNIVERSITY
            <input value="UP Mindanao" disabled />
          </label>
          <label>
            DEGREE PROGRAM
            <input value="Contact Admin to change" disabled />
          </label>
          <label>
            STUDENT NUMBER
            <input value="Contact Admin to change" disabled />
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

      <div v-if="saved" class="user-save-message" style="background: #dcfce7; color: #166534; padding: 10px; border-radius: 6px; margin-bottom: 15px; display: flex; align-items: center; gap: 8px;">
        <CheckCircle2 :size="17" />
        Profile updated successfully!
      </div>

      <div v-if="error" style="color: #b91c1c; margin-bottom: 15px;">
        {{ error }}
      </div>

      <div class="user-form-actions">
        <RouterLink class="user-button user-button-light" to="/user/profile">
          Cancel
        </RouterLink>
        <button class="user-button user-button-primary" type="submit" :disabled="saving">
          {{ saving ? 'Saving...' : 'Save Profile' }}
        </button>
      </div>
    </form>
  </section>
</template>