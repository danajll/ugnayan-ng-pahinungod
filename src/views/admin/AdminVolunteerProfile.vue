<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, MapPin, Phone, ShieldAlert, GraduationCap, Mail } from 'lucide-vue-next'
import { volunteerService } from '../../api/volunteers'

const route = useRoute()
const router = useRouter()
const volunteerId = route.params.id

const loading = ref(true)
const error = ref(null)
const volunteer = ref(null)
const profile = ref({ contact: {}, address: {}, emergency: {}, background: {} })

const isVerified = computed(() => volunteer.value?.status === 'active')

const handleApprove = async () => {
  if (!volunteer.value?.id) return
  try {
    await volunteerService.approve(volunteer.value.id)
    const [volRes, profRes] = await Promise.all([
      volunteerService.get(volunteer.value.id),
      volunteerService.getProfile(volunteer.value.id)
    ])
    volunteer.value = volRes.data
    profile.value = profRes.data
    alert('Volunteer verified and onboarded.')
  } catch (err) {
    alert('Failed to verify volunteer: ' + (err.response?.data?.detail || err.message))
    console.error(err)
  }
}

const handleReject = async () => {
  if (!volunteer.value?.id) return
  if (!confirm('Reject this volunteer application?')) return
  try {
    await volunteerService.reject(volunteer.value.id)
    const [volRes, profRes] = await Promise.all([
      volunteerService.get(volunteer.value.id),
      volunteerService.getProfile(volunteer.value.id)
    ])
    volunteer.value = volRes.data
    profile.value = profRes.data
    alert('Volunteer application rejected.')
  } catch (err) {
    alert('Failed to reject volunteer: ' + (err.response?.data?.detail || err.message))
    console.error(err)
  }
}

onMounted(async () => {
  try {
    const [volRes, profRes] = await Promise.all([
      volunteerService.get(volunteerId),
      volunteerService.getProfile(volunteerId)
    ])
    volunteer.value = volRes.data
    profile.value = profRes.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load volunteer profile.'
  } finally {
    loading.value = false
  }
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
  <div class="admin-page">
    <div class="admin-page-inner">
      
      <!-- Back button & Header -->
      <div style="margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between;">
        <button @click="router.push('/admin/volunteers')" style="display: flex; align-items: center; gap: 8px; background: none; border: none; color: #666; cursor: pointer; font-weight: 600;">
          <ArrowLeft :size="18" /> Back to Directory
        </button>
      </div>

      <div v-if="loading" style="padding: 40px; text-align: center; color: #666;">
        Loading volunteer data...
      </div>

      <div v-else-if="error" style="padding: 40px; text-align: center; color: #b91c1c;">
        {{ error }}
      </div>

      <div v-else-if="volunteer" class="profile-container">
        
        <!-- Header Banner -->
        <div style="background: #fff; border-radius: 12px; padding: 30px; margin-bottom: 24px; border: 1px solid #e5e7eb; display: flex; align-items: flex-start; gap: 24px;">
          <div style="width: 80px; height: 80px; border-radius: 50%; background: #2e4a3a; color: white; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: bold;">
            {{ volunteer.first_name[0] }}{{ volunteer.last_name[0] }}
          </div>
          
          <div style="flex: 1;">
            <div style="display: flex; gap: 12px; margin-bottom: 8px;">
              <span style="background: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 99px; font-size: 0.75rem; font-weight: bold;">{{ volunteer.status.toUpperCase() }}</span>
              <span style="background: #e0f2fe; color: #075985; padding: 4px 12px; border-radius: 99px; font-size: 0.75rem; font-weight: bold;">ID: {{ volunteer.volunteer_identifier }}</span>
            </div>
            
            <h1 style="margin: 0 0 4px 0; font-size: 2rem; color: #111827;">{{ volunteer.full_name }}</h1>
            <p style="margin: 0; color: #4b5563; font-size: 1.1rem;">
              {{ volunteer.affiliation_type | capitalize }} Volunteer 
              <span v-if="volunteer.degree"> · {{ volunteer.degree }}</span>
            </p>
          </div>
        </div>

        <!-- Verification actions (only for unverified accounts) -->
        <div v-if="!isVerified" style="display: flex; gap: 10px; margin-bottom: 24px;">
          <button
            @click="handleApprove"
            style="display: inline-flex; align-items: center; gap: 6px; padding: 10px 18px; border: 0; border-radius: 8px; background: #16a34a; color: white; font-weight: 700; cursor: pointer;"
          >
            <ShieldAlert :size="16" /> Verify & Approve
          </button>
          <button
            @click="handleReject"
            style="display: inline-flex; align-items: center; gap: 6px; padding: 10px 18px; border: 0; border-radius: 8px; background: #dc2626; color: white; font-weight: 700; cursor: pointer;"
          >
            Reject Application
          </button>
        </div>

        <!-- Two Column Layout -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
          
          <!-- Left Column: Core & Academic -->
          <div style="display: flex; flex-direction: column; gap: 24px;">
            
            <!-- Personal Info -->
            <section style="background: #fff; border-radius: 12px; padding: 24px; border: 1px solid #e5e7eb;">
              <h2 style="margin-top: 0; font-size: 1.1rem; border-bottom: 2px solid #f3f4f6; padding-bottom: 12px; margin-bottom: 20px;">Personal Information</h2>
              
              <div style="display: grid; gap: 16px;">
                <div>
                  <small style="color: #6b7280; font-weight: 600; display: block; margin-bottom: 4px;">FULL LEGAL NAME</small>
                  <strong>{{ volunteer.full_name }}</strong>
                </div>
                <div>
                  <small style="color: #6b7280; font-weight: 600; display: block; margin-bottom: 4px;">NICKNAME</small>
                  <strong>{{ volunteer.nickname || 'N/A' }}</strong>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                  <div>
                    <small style="color: #6b7280; font-weight: 600; display: block; margin-bottom: 4px;">SEX</small>
                    <strong>{{ displaySex }}</strong>
                  </div>
                  <div>
                    <small style="color: #6b7280; font-weight: 600; display: block; margin-bottom: 4px;">BIRTHDATE</small>
                    <strong>{{ formatDate(volunteer.birthdate) }} ({{ volunteer.age }})</strong>
                  </div>
                </div>
                <div>
                  <small style="color: #6b7280; font-weight: 600; display: block; margin-bottom: 4px;">INDIGENOUS AFFILIATION</small>
                  <strong>{{ volunteer.indigenous_affiliation || 'None' }}</strong>
                </div>
              </div>
            </section>

            <!-- Academic / Affiliation -->
            <section style="background: #fff; border-radius: 12px; padding: 24px; border: 1px solid #e5e7eb;">
              <h2 style="margin-top: 0; font-size: 1.1rem; border-bottom: 2px solid #f3f4f6; padding-bottom: 12px; margin-bottom: 20px;">Affiliation & Academic</h2>
              
              <div style="display: grid; gap: 16px;">
                <div>
                  <small style="color: #6b7280; font-weight: 600; display: block; margin-bottom: 4px;">AFFILIATION TYPE</small>
                  <strong>{{ volunteer.affiliation_type | capitalize }}</strong>
                </div>
                <div>
                  <small style="color: #6b7280; font-weight: 600; display: block; margin-bottom: 4px;">DEGREE PROGRAM</small>
                  <strong>{{ volunteer.degree || 'N/A' }}</strong>
                </div>
                <div>
                  <small style="color: #6b7280; font-weight: 600; display: block; margin-bottom: 4px;">STUDENT NUMBER</small>
                  <strong>{{ volunteer.student_number || 'N/A' }}</strong>
                </div>
                <div>
                  <small style="color: #6b7280; font-weight: 600; display: block; margin-bottom: 4px;">SENIOR HIGH SCHOOL</small>
                  <strong>{{ volunteer.senior_high_school || 'N/A' }}</strong>
                </div>
              </div>
            </section>

          </div>

          <!-- Right Column: Contact & Emergency -->
          <div style="display: flex; flex-direction: column; gap: 24px;">
            
            <!-- Contact Details -->
            <section style="background: #fff; border-radius: 12px; padding: 24px; border: 1px solid #e5e7eb;">
              <h2 style="margin-top: 0; font-size: 1.1rem; border-bottom: 2px solid #f3f4f6; padding-bottom: 12px; margin-bottom: 20px;">Contact & Address</h2>
              
              <div style="display: grid; gap: 16px;">
                <div>
                  <small style="color: #6b7280; font-weight: 600; display: block; margin-bottom: 4px;">MOBILE NUMBER</small>
                  <strong style="display: flex; align-items: center; gap: 6px;">
                    <Phone :size="14" /> {{ volunteer.mobile_number || 'N/A' }}
                  </strong>
                </div>
                <div>
                  <small style="color: #6b7280; font-weight: 600; display: block; margin-bottom: 4px;">FACEBOOK LINK</small>
                  <strong>
                    <a v-if="volunteer.facebook_link" :href="volunteer.facebook_link" target="_blank" style="color: #2563eb; text-decoration: none;">
                      {{ volunteer.facebook_link }}
                    </a>
                    <span v-else>N/A</span>
                  </strong>
                </div>
                <div>
                  <small style="color: #6b7280; font-weight: 600; display: block; margin-bottom: 4px;">PERMANENT ADDRESS</small>
                  <strong style="display: flex; align-items: flex-start; gap: 6px;">
                    <MapPin :size="14" style="margin-top: 4px; flex-shrink: 0;" /> 
                    {{ volunteer.permanent_address || 'N/A' }}
                  </strong>
                </div>
              </div>
            </section>

            <!-- Emergency Contact -->
            <section style="background: #fff; border-radius: 12px; padding: 24px; border: 1px solid #e5e7eb;">
              <h2 style="margin-top: 0; font-size: 1.1rem; border-bottom: 2px solid #f3f4f6; padding-bottom: 12px; margin-bottom: 20px;">Emergency Contact</h2>
              
              <div v-if="profile.emergency && profile.emergency.contact_name" style="display: grid; gap: 16px;">
                <div>
                  <small style="color: #6b7280; font-weight: 600; display: block; margin-bottom: 4px;">NAME</small>
                  <strong>{{ profile.emergency.contact_name }} ({{ profile.emergency.relationship }})</strong>
                </div>
                <div>
                  <small style="color: #6b7280; font-weight: 600; display: block; margin-bottom: 4px;">MOBILE NUMBER</small>
                  <strong style="display: flex; align-items: center; gap: 6px;">
                    <ShieldAlert :size="14" /> {{ profile.emergency.contact_mobile_number || 'N/A' }}
                  </strong>
                </div>
                <div>
                  <small style="color: #6b7280; font-weight: 600; display: block; margin-bottom: 4px;">COMPLETE ADDRESS</small>
                  <strong>{{ profile.emergency.complete_address || 'N/A' }}</strong>
                </div>
              </div>
              <div v-else style="color: #6b7280; font-style: italic;">
                No emergency contact on file.
              </div>
            </section>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-container p {
  text-transform: capitalize;
}
</style>