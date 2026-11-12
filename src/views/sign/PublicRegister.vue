<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { meService } from '../../api/me'
import { volunteerService } from '../../api/volunteers'

const router = useRouter()
const currentStep = ref(1)
const submitting = ref(false)
const submitError = ref(null)

// Form Data
const formData = reactive({
  // Step 1
  lastName: '', firstName: '', middleName: '', nickName: '',
  age: '', sex: '', birthDate: '', ipAffiliation: '',
  mobile: '', facebookLink: '', hobbies: '', affiliatedOrgs: '',
  permanentAddress: '', upAddress: '',

  // Step 2
  affiliation: '', shsFinished: '', bachelorsDegree: '', studentNumber: '', courseProgram: '',
  firstInFamilyCollege: '', firstInFamilyGradStudies: '', firstInFamilyUP: '',

  // Step 3
  emergencyName: '', emergencyRelation: '', emergencyMobile: '', emergencyAddress: '',
  volunteerPrograms: [], affirmativeSubjects: [],

  // Step 4
  applicationStatus: '', tagapagUgnay: '', otherVolOrg: '',
  otherVolOrgName: '', whereHeard: '', agreedConsent: false,
})

// ─────────────────────────────────────────────────────────────
// Prefill from /api/me/ + /api/volunteers/<id>/
// ─────────────────────────────────────────────────────────────
const prefilling = ref(true)

onMounted(async () => {
  try {
    const { data: me } = await meService.get()

    if (me.volunteer?.id) {
      // Pull the full volunteer record
      const { data: full } = await volunteerService.get(me.volunteer.id)

      formData.firstName       = full.first_name || ''
      formData.middleName      = full.middle_name || ''
      formData.lastName        = full.last_name || ''
      formData.birthDate       = full.birthdate || ''
      formData.sex             = full.sex === 'M' ? 'Male' : full.sex === 'F' ? 'Female' : ''
      formData.mobile          = full.mobile_number || ''
      formData.facebookLink    = full.facebook_link || ''
      formData.permanentAddress = full.permanent_address || ''
      formData.upAddress       = full.up_address || ''
      formData.hobbies         = full.hobbies || ''
      formData.affiliatedOrgs  = full.affiliated_organizations || ''
      formData.ipAffiliation   = full.indigenous_affiliation || ''
      formData.nickName        = full.nickname || ''
    } else {
      // Fall back to User's first/last name from Google
      formData.firstName = me.first_name || ''
      formData.lastName  = me.last_name || ''
    }
  } catch (err) {
    // 401 → guard should have caught it, but be defensive
    if (err.response?.status === 401) {
      localStorage.removeItem('auth_token')
      router.push('/login')
    }
    console.warn('Prefill failed:', err)
  } finally {
    prefilling.value = false
  }
})

// ─────────────────────────────────────────────────────────────
// Navigation
// ─────────────────────────────────────────────────────────────
const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const handleNextOrSubmit = async () => {
  if (currentStep.value < 4) {
    currentStep.value++
    window.scrollTo({ top: 0, behavior: 'smooth' })
    return
  }

  submitError.value = null
  submitting.value = true

  try {
    const payload = buildOnboardingPayload()
    await volunteerService.onboard(payload)

    // Re-fetch /api/me/ to confirm is_profile_complete is now true
    // (optional but useful for debugging)
    // const { data: me } = await meService.get()

    router.push('/user')
  } catch (err) {
    const detail = err.response?.data
    if (detail && typeof detail === 'object') {
      submitError.value = prettyErrors(detail)
    } else if (detail?.detail) {
      submitError.value = detail.detail
    } else {
      submitError.value = 'Submission failed. Please check your data.'
    }
    console.error('Onboarding error:', detail || err)
    // Scroll to error
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } finally {
    submitting.value = false
  }
}

// Turn DRF's nested error object into readable text
const prettyErrors = (obj, prefix = '') => {
  let out = ''
  for (const key in obj) {
    const val = obj[key]
    const path = prefix ? `${prefix}.${key}` : key
    if (Array.isArray(val)) {
      out += `${path}: ${val.join(', ')}\n`
    } else if (typeof val === 'object' && val !== null) {
      out += prettyErrors(val, path)
    } else {
      out += `${path}: ${val}\n`
    }
  }
  return out.trim()
}

// ─────────────────────────────────────────────────────────────
// Build payload matching OnboardingSerializer
// ─────────────────────────────────────────────────────────────
const buildOnboardingPayload = () => ({
  personal_info: {
    first_name: formData.firstName,
    middle_name: formData.middleName || '',
    last_name: formData.lastName,
    nickname: formData.nickName,
    sex: formData.sex === 'Female' ? 'F' : 'M',
    birthdate: formData.birthDate,
    indigenous_affiliation: formData.ipAffiliation || '',
    mobile_number: formData.mobile,
    facebook_link: formData.facebookLink,
    hobbies: formData.hobbies,
    affiliated_organizations: formData.affiliatedOrgs,
    permanent_address: formData.permanentAddress,
    up_address: formData.upAddress || '',
    senior_high_school: formData.shsFinished || '',
  },
  affiliation_type: mapAffiliation(formData.affiliation),
  student_info: {
    student_number: formData.studentNumber || '',
    course: formData.courseProgram || '',
    bachelor_degree: formData.bachelorsDegree || '',
    first_to_college: formData.firstInFamilyCollege === 'YES' ? 'yes' : 'no',
    first_to_graduate:
      formData.firstInFamilyGradStudies === 'N/A'
        ? 'n_a'
        : formData.firstInFamilyGradStudies === 'YES' ? 'yes' : 'no',
    first_in_up: formData.firstInFamilyUP === 'YES' ? 'yes' : 'no',
  },
  emergency_contact: {
    contact_name: formData.emergencyName,
    relationship: formData.emergencyRelation,
    contact_mobile_number: formData.emergencyMobile,
    complete_address: formData.emergencyAddress || '',
  },
  programs: formData.volunteerPrograms
    .map(mapProgramCode)
    .filter(Boolean),
  affirmative_action_subjects: formData.affirmativeSubjects
    .map(mapSubjectCode)
    .filter(Boolean),
  background: {
    application_status: mapApplicationStatus(formData.applicationStatus),
    operations_group: formData.tagapagUgnay === 'YES' ? 'yes' : 'no',
    other_orgs: formData.otherVolOrg === 'YES' ? 'yes' : 'no',
    other_orgs_name: formData.otherVolOrgName || '',
    referral_source: formData.whereHeard || '',
  },
})

// ─────────────────────────────────────────────────────────────
// Lookup maps (verified against your DB)
// ─────────────────────────────────────────────────────────────
const PROGRAM_MAP = {
  'AFFIRMATIVE ACTION PROGRAM':                'AFFIRMATIVE_ACTION_PROGRAM',
  'TEACHER DEVELOPMENT PROGRAM':               'TEACHER_DEVELOPMENT_PROGRAM',
  'DISASTER RISK REDUCTION RELATED PROGRAM':   'DISASTER_RISK_REDUCTION',
  'UGNAYAN NG PAHINUNGOD ONLINE PROGRAM':      'UGNAYAN_NG_PAHINUNGOD_ONLINE',
  'TUTORIAL SERVICES PROGRAM':                 'TUTORIAL_SERVICE_PROGRAM',
  'ENVIRONMENTAL AWARENESS PROGRAM':           'ENVIRONMENTAL_AWARENESS_PROGRAM',
  'PROGRAMS UNDER THE UP BARMM-MBHTE MOU':     'UP_BARMM_MBHTE_MOU',
}
const mapProgramCode = (label) => PROGRAM_MAP[label] || null

const SUBJECT_MAP = {
  'READING COMPREHENSION FILIPINO': 'READING_COMP_FILIPINO',
  'READING COMPREHENSION ENGLISH':  'READING_COMP_ENGLISH',
  'LANGUAGE PROFICIENCY FILIPINO':  'LANG_PROF_FILIPINO',
  'LANGUAGE PROFICIENCY ENGLISH':   'LANG_PROF_ENGLISH',
  'MATHEMATICS':                    'MATH',
  'SCIENCE':                        null, // not in your DB yet — silently dropped
  'NONE':                           null, // NONE isn't a real Subject row
}
const mapSubjectCode = (label) => SUBJECT_MAP[label] ?? null

const mapAffiliation = (label) => {
  const v = (label || '').toLowerCase()
  if (v === 'student') return 'student'
  if (v === 'faculty') return 'faculty'
  if (v === 'alumni') return 'alumni'
  if (v === 'retiree') return 'alumni' // backend has no "retiree"
  if (v.includes('up reps') || v.includes('staff')) return 'staff'
  return 'student'
}

const mapApplicationStatus = (label) => {
  if (label === 'Already signed up no engagements') return 'previous_no_engagement'
  if (label === 'Already signed up with engagements') return 'previous_with_engagement'
  return 'first_time'
}
</script>

<style scoped>
@import "../../styles/sign/register.css";
</style>

<template>
  <div class="register-layout">
    <!-- Top Header Bar Overlapping Full Screen Width -->
    <header class="top-header">
      <router-link to="/" class="brand-link">
        <img src="/images/logos/pahinungod-logo.png" alt="pahinungod Logo" class="brand-logo" />
        <div class="brand-text">
          <span class="brand-univ">UNIVERSITY OF THE PHILIPPINES - MINDANAO</span>
          <span class="brand-program">UGNAYAN NG PAHINUNGÓD</span>
        </div>
      </router-link>
    </header>

    <!-- Left Hero Banner -->
    <div class="hero-sidebar">
      <div class="hero-content">
        <div class="oblation-container">
          <img src="/images/assets/oble.png" alt="Oblation" class="hero-logo" />
        </div>
        <h1 class="hero-title">
          MAKIBAHAGI<br />
          MAGLINGKOD<br />
          MAG<span class="highlight">PAHINUNGÓD</span>
        </h1>
      </div>
    </div>

    <!-- Right Form Section -->
    <div class="form-container">
      <div class="form-wrapper">
        <p v-if="prefilling" style="text-align:center; padding:20px; color:#666;">
          Loading your profile…
        </p>
        <!-- Brand Header & Progress Tracker -->
        <div class="form-header">
          <h1 class="brand-title">Ugnayan ng Pahinungód Mindanao</h1>
          <p class="brand-subtitle">Volunteer Sign-up Form</p>
          
          <div class="step-tracker">
            <span class="step-pill">Step {{ currentStep }} of 4</span>
            <div class="progress-bar-track">
              <div class="progress-bar-fill" :style="{ width: (currentStep * 25) + '%' }"></div>
            </div>
          </div>
        </div>

        <!-- Multi-Step Form -->
        <form @submit.prevent="handleNextOrSubmit" class="step-form">
          <div
            v-if="submitError"
            style="background:#fee2e2; color:#991b1b; padding:12px 16px; border-radius:8px; margin-bottom:16px; font-size:0.85rem;"
          >
            <strong>Could not submit:</strong>
            <pre style="margin:8px 0 0; white-space:pre-wrap; font-family:inherit;">{{ submitError }}</pre>
          </div>
          <!-- ==================== STEP 1: Personal Information ==================== -->
          <div v-if="currentStep === 1" class="form-step">
            <div class="section-title">
              <span class="bullet">●</span> PERSONAL INFORMATION
            </div>

            <div class="form-row two-col">
              <div class="form-group">
                <label>LAST NAME <span class="required">*</span></label>
                <input v-model="formData.lastName" type="text" placeholder="Santiago" required />
              </div>
              <div class="form-group">
                <label>FIRST NAME <span class="required">*</span></label>
                <input v-model="formData.firstName" type="text" placeholder="Dana Jill" required />
              </div>
            </div>

            <div class="form-row two-col">
              <div class="form-group">
                <label>MIDDLE NAME</label>
                <input v-model="formData.middleName" type="text" placeholder="Paisaje (Optional)" />
              </div>
              <div class="form-group">
                <label>NICKNAME <span class="required">*</span></label>
                <input v-model="formData.nickName" type="text" placeholder="Bibi" required />
              </div>
            </div>

            <div class="form-row three-col-custom">
              <div class="form-group col-age">
                <label>AGE <span class="required">*</span></label>
                <input v-model="formData.age" type="number" placeholder="e.g. 20" required />
              </div>
              <div class="form-group col-sex">
                <label>SEX ASSIGNED AT BIRTH <span class="required">*</span></label>
                <select v-model="formData.sex" required>
                  <option value="" disabled selected>Select sex</option>
                  <option value="Female">Female</option>
                  <option value="Male">Male</option>
                  <option value="Prefer not to say">Prefer not to say</option>
                </select>
              </div>
              <div class="form-group col-dob">
                <label>BIRTHDATE <span class="required">*</span></label>
                <input v-model="formData.birthDate" type="date" required />
              </div>
            </div>

            <div class="form-group">
              <label>INDIGENOUS PEOPLES / ETHNOLINGUISTIC AFFILIATION</label>
              <input 
                v-model="formData.ipAffiliation" 
                type="text" 
                placeholder="e.g., Bagobo Tagabawa, Mandaya, Maranao, Tausug, Cebuano, Ilocano, None" 
              />
              <span class="field-help">Specify if you belong to an IP community or ethnolinguistic group (indicate 'None' or leave blank if not applicable).</span>
            </div>

            <div class="form-row two-col">
              <div class="form-group">
                <label>MOBILE NUMBER <span class="required">*</span></label>
                <input v-model="formData.mobile" type="tel" placeholder="+63 9XX XXX XXXX" required />
              </div>
              <div class="form-group">
                <label>FACEBOOK PROFILE LINK <span class="required">*</span></label>
                <input v-model="formData.facebookLink" type="url" placeholder="https://facebook.com/username" required />
              </div>
            </div>

            <div class="form-group">
              <label>HOBBIES / INTERESTS <span class="required">*</span></label>
              <input 
                v-model="formData.hobbies" 
                type="text" 
                placeholder="e.g. Community teaching, graphic design, disaster relief, singing, public speaking..." 
                required 
              />
            </div>

            <div class="form-group">
              <label>LIST ANY ORGANIZATIONS TO WHICH YOU ARE AFFILIATED <span class="required">*</span></label>
              <textarea 
                v-model="formData.affiliatedOrgs" 
                rows="2" 
                placeholder="List academic, socio-civic, church, youth, or NGO groups (or write 'None')." 
                required
              ></textarea>
            </div>

            <div class="form-group">
              <label>PERMANENT ADDRESS <span class="required">*</span></label>
              <input v-model="formData.permanentAddress" type="text" placeholder="House/Street, Barangay, Municipality/City, Province" required />
            </div>

            <div class="form-group">
              <label>ADDRESS WHILE STUDYING/RESIDING IN UP</label>
              <input v-model="formData.upAddress" type="text" placeholder="House/Street, Barangay, Municipality/City, Province" />
            </div>
          </div>

          <!-- ==================== STEP 2: Affiliation & Demographics ==================== -->
          <div v-if="currentStep === 2" class="form-step">
            <div class="section-title-row">
              <div class="section-title">
                <span class="bullet">●</span> AFFILIATION TO UP
              </div>
              <span class="sub-note">Select primary relationship</span>
            </div>

            <div class="form-group">
              <label>IN WHAT WAY ARE YOU AFFILIATED TO UP? <span class="required">*</span></label>
              <div class="option-grid-step2">
                <label class="radio-box" :class="{ selected: formData.affiliation === 'STUDENT' }">
                  <input type="radio" value="STUDENT" v-model="formData.affiliation" required />
                  <span>STUDENT</span>
                </label>
                <label class="radio-box" :class="{ selected: formData.affiliation === 'ALUMNI' }">
                  <input type="radio" value="ALUMNI" v-model="formData.affiliation" />
                  <span>ALUMNI</span>
                </label>
                <label class="radio-box" :class="{ selected: formData.affiliation === 'RETIREE' }">
                  <input type="radio" value="RETIREE" v-model="formData.affiliation" />
                  <span>RETIREE</span>
                </label>
                <label class="radio-box" :class="{ selected: formData.affiliation === 'FACULTY' }">
                  <input type="radio" value="FACULTY" v-model="formData.affiliation" />
                  <span>FACULTY</span>
                </label>
                <label class="radio-box wide" :class="{ selected: formData.affiliation === 'UP REPS / ADMIN STAFF / NGS' }">
                  <input type="radio" value="UP REPS / ADMIN STAFF / NGS" v-model="formData.affiliation" />
                  <span>UP REPS / ADMIN STAFF / NGS</span>
                </label>
              </div>
            </div>

            <div class="section-title">
              <span class="bullet">●</span> STUDENT INFORMATION & DEMOGRAPHICS
            </div>

            <div class="form-group">
              <label>WHERE DID YOU FINISH YOUR SENIOR HIGH SCHOOL?</label>
              <span class="field-help">(For first-year undergraduate students and first-time volunteers)</span>
              <input v-model="formData.shsFinished" type="text" placeholder="Name of Senior High School, Municipality/City, Province" />
            </div>

            <!-- Visible only for students -->
            <div
              v-if="formData.affiliation === 'STUDENT'"
              class="form-row two-col"
            >
              <div class="form-group">
                <label>STUDENT NUMBER <span class="required">*</span></label>
                <input
                  v-model="formData.studentNumber"
                  type="text"
                  placeholder="e.g. 2024-13406"
                  required
                />
                <span class="field-help">Your UP Mindanao student number (format YYYY-NNNNN).</span>
              </div>
              <div class="form-group">
                <label>CURRENT DEGREE PROGRAM <span class="required">*</span></label>
                <input
                  v-model="formData.courseProgram"
                  type="text"
                  placeholder="e.g. BS Computer Science"
                  required
                />
                <span class="field-help">The degree you are currently enrolled in.</span>
              </div>
            </div>

            <!-- Completed bachelor's degree — for grad students / alumni / faculty -->
            <div class="form-group">
              <label>COMPLETED BACHELOR'S DEGREE (IF ANY)</label>
              <input
                v-model="formData.bachelorsDegree"
                type="text"
                placeholder="e.g. BS Biology, UP Mindanao (leave blank if still pursuing)"
              />
              <span class="field-help">
                For graduate students, alumni, and faculty — your completed undergraduate degree.
                Current undergrads can leave this blank.
              </span>
            </div>

            <div class="form-group">
              <label>ARE YOU THE FIRST IN YOUR FAMILY TO ENTER COLLEGE?</label>
              <span class="field-help">(For first-year undergraduate students and first-time volunteers)</span>
              <div class="inline-radios">
                <label class="radio-inline"><input type="radio" value="YES" v-model="formData.firstInFamilyCollege" /> YES</label>
                <label class="radio-inline"><input type="radio" value="NO" v-model="formData.firstInFamilyCollege" /> NO</label>
              </div>
            </div>

            <div class="form-group">
              <label>ARE YOU THE FIRST IN YOUR FAMILY TO PURSUE GRADUATE STUDIES?</label>
              <span class="field-help">(For graduate students)</span>
              <div class="inline-radios">
                <label class="radio-inline"><input type="radio" value="YES" v-model="formData.firstInFamilyGradStudies" /> YES</label>
                <label class="radio-inline"><input type="radio" value="NO" v-model="formData.firstInFamilyGradStudies" /> NO</label>
                <label class="radio-inline"><input type="radio" value="N/A" v-model="formData.firstInFamilyGradStudies" /> N/A</label>
              </div>
            </div>

            <div class="form-group">
              <label>ARE YOU THE FIRST IN YOUR FAMILY TO ENTER UP?</label>
              <span class="field-help">(For first-year undergraduate students and first-time volunteers)</span>
              <div class="inline-radios">
                <label class="radio-inline"><input type="radio" value="YES" v-model="formData.firstInFamilyUP" /> YES</label>
                <label class="radio-inline"><input type="radio" value="NO" v-model="formData.firstInFamilyUP" /> NO</label>
              </div>
            </div>
          </div>

          <!-- ==================== STEP 3: Emergency Contact & Programs ==================== -->
          <div v-if="currentStep === 3" class="form-step">
            <div class="section-title-row">
              <div class="section-title">
                <span class="bullet">●</span> 4. EMERGENCY CONTACT
              </div>
              <span class="sub-note">* Required</span>
            </div>

            <div class="sub-section-label">PERSON TO CONTACT IN CASE OF EMERGENCY *</div>
            <div class="form-row two-col">
              <div class="form-group">
                <label>CONTACT NAME <span class="required">*</span></label>
                <input v-model="formData.emergencyName" type="text" placeholder="Full name of emergency contact" required />
              </div>
              <div class="form-group">
                <label>RELATIONSHIP <span class="required">*</span></label>
                <input v-model="formData.emergencyRelation" type="text" placeholder="e.g. Parent, Guardian, Spouse, Sibling" required />
              </div>
            </div>

            <div class="form-row two-col">
              <div class="form-group">
                <label>CONTACT MOBILE NUMBER <span class="required">*</span></label>
                <input v-model="formData.emergencyMobile" type="tel" placeholder="+63 9XX XXX XXXX" required />
              </div>
              <div class="form-group">
                <label>COMPLETE ADDRESS <span class="required">*</span></label>
                <input v-model="formData.emergencyAddress" type="text" placeholder="Street, Barangay, City, Province" required />
              </div>
            </div>

            <div class="section-title">
              <span class="bullet">●</span> 5. PROGRAMS YOU WISH TO PARTICIPATE IN
            </div>

            <div class="form-group">
              <label>VOLUNTEER PROGRAMS <span class="required">*</span></label>
              <div class="checkbox-grid-step3">
                <label class="checkbox-box">
                  <input type="checkbox" value="AFFIRMATIVE ACTION PROGRAM" v-model="formData.volunteerPrograms" />
                  <span>AFFIRMATIVE ACTION PROGRAM</span>
                </label>
                <label class="checkbox-box">
                  <input type="checkbox" value="TEACHER DEVELOPMENT PROGRAM" v-model="formData.volunteerPrograms" />
                  <span>TEACHER DEVELOPMENT PROGRAM</span>
                </label>
                <label class="checkbox-box">
                  <input type="checkbox" value="DISASTER RISK REDUCTION RELATED PROGRAM" v-model="formData.volunteerPrograms" />
                  <span>DISASTER RISK REDUCTION RELATED PROGRAM</span>
                </label>
                <label class="checkbox-box">
                  <input type="checkbox" value="UGNAYAN NG PAHINUNGOD ONLINE PROGRAM" v-model="formData.volunteerPrograms" />
                  <span>UGNAYAN NG PAHINUNGOD ONLINE PROGRAM</span>
                </label>
                <label class="checkbox-box">
                  <input type="checkbox" value="TUTORIAL SERVICES PROGRAM" v-model="formData.volunteerPrograms" />
                  <span>TUTORIAL SERVICES PROGRAM</span>
                </label>
                <label class="checkbox-box">
                  <input type="checkbox" value="ENVIRONMENTAL AWARENESS PROGRAM" v-model="formData.volunteerPrograms" />
                  <span>ENVIRONMENTAL AWARENESS PROGRAM</span>
                </label>
                <label class="checkbox-box wide">
                  <input type="checkbox" value="PROGRAMS UNDER THE UP BARMM-MBHTE MOU" v-model="formData.volunteerPrograms" />
                  <span>PROGRAMS UNDER THE UP BARMM-MBHTE MOU</span>
                </label>
              </div>
            </div>

            <!-- Sub-interest box for Affirmative Action Program -->
            <div class="highlight-sub-box">
              <label class="highlight-box-title">
                UNDER THE AFFIRMATIVE ACTION PROGRAM, WHICH OF THE FOLLOWING SUBJECTS ARE YOU INTERESTED IN TEACHING FOR THE ACADEMIC ENHANCEMENT SESSIONS? *
              </label>
              <div class="two-col-checkboxes">
                <label class="checkbox-inline"><input type="checkbox" value="READING COMPREHENSION FILIPINO" v-model="formData.affirmativeSubjects" /> READING COMPREHENSION FILIPINO</label>
                <label class="checkbox-inline"><input type="checkbox" value="READING COMPREHENSION ENGLISH" v-model="formData.affirmativeSubjects" /> READING COMPREHENSION ENGLISH</label>
                <label class="checkbox-inline"><input type="checkbox" value="LANGUAGE PROFICIENCY FILIPINO" v-model="formData.affirmativeSubjects" /> LANGUAGE PROFICIENCY FILIPINO</label>
                <label class="checkbox-inline"><input type="checkbox" value="LANGUAGE PROFICIENCY ENGLISH" v-model="formData.affirmativeSubjects" /> LANGUAGE PROFICIENCY ENGLISH</label>
                <label class="checkbox-inline"><input type="checkbox" value="MATHEMATICS" v-model="formData.affirmativeSubjects" /> MATHEMATICS</label>
                <label class="checkbox-inline"><input type="checkbox" value="SCIENCE" v-model="formData.affirmativeSubjects" /> SCIENCE</label>
                <label class="checkbox-inline"><input type="checkbox" value="NONE" v-model="formData.affirmativeSubjects" /> NONE</label>
              </div>
            </div>
          </div>

          <!-- ==================== STEP 4: Background & Submission ==================== -->
          <div v-if="currentStep === 4" class="form-step">
            <div class="section-title">
              <span class="bullet">●</span> 6. VOLUNTEER BACKGROUND & AFFILIATION STATUS
            </div>

            <div class="form-group">
              <label>KINDLY CHOOSE THE STATUS OF YOUR VOLUNTEER APPLICATION TO UGNAYAN NG PAHINUNGOD MINDANAO <span class="required">*</span></label>
              <div class="stacked-radios-step4">
                <label class="radio-box wide" :class="{ selected: formData.applicationStatus === 'First time' }">
                  <input type="radio" value="First time" v-model="formData.applicationStatus" required />
                  <span>First time to apply as volunteer (no engagements yet)</span>
                </label>
                <label class="radio-box wide" :class="{ selected: formData.applicationStatus === 'Already signed up no engagements' }">
                  <input type="radio" value="Already signed up no engagements" v-model="formData.applicationStatus" />
                  <span>Already signed up in the previous sign up form but no engagements yet</span>
                </label>
                <label class="radio-box wide" :class="{ selected: formData.applicationStatus === 'Already signed up with engagements' }">
                  <input type="radio" value="Already signed up with engagements" v-model="formData.applicationStatus" />
                  <span>Signed up in the previous sign up form and already have engagements with Pahinungod</span>
                </label>
              </div>
            </div>

            <!-- Tagapag-ugnay Group Box -->
            <div class="grey-sub-box">
              <label class="grey-box-title">WOULD YOU LIKE TO BE PART OF THE TAGAPAG-UGNAY GROUP? <span class="required">*</span></label>
              <span class="field-help">(This group of volunteers is dedicated to helping with social media marketing, creating publication materials, and assisting during preparation of activities.)</span>
              <div class="inline-radios">
                <label class="radio-inline"><input type="radio" value="YES" v-model="formData.tagapagUgnay" required /> YES</label>
                <label class="radio-inline"><input type="radio" value="NO" v-model="formData.tagapagUgnay" /> NO</label>
              </div>
            </div>

            <!-- Other Volunteer Organizations -->
            <div class="form-row two-col align-top">
              <div class="form-group">
                <label>ARE YOU A PART OF ANY OTHER VOLUNTEER ORGANIZATION? <span class="required">*</span></label>
                <div class="inline-radios">
                  <label class="radio-inline"><input type="radio" value="YES" v-model="formData.otherVolOrg" required /> YES</label>
                  <label class="radio-inline"><input type="radio" value="NO" v-model="formData.otherVolOrg" /> NO</label>
                </div>
              </div>
              <div class="form-group">
                <label>WHAT IS THE NAME OF THE ORGANIZATION?</label>
                <span class="field-help">(If you answered yes in the previous question)</span>
                <input v-model="formData.otherVolOrgName" type="text" placeholder="Organization name" />
              </div>
            </div>

            <div class="form-group">
              <label>WHERE DID YOU HEAR ABOUT THE UGNAYAN NG PAHINUNGOD MINDANAO?</label>
              <span class="field-help">(For first time volunteers only)</span>
              <input v-model="formData.whereHeard" type="text" placeholder="e.g. Facebook page, UP Mindanao orientation, Friend / Colleague, Faculty announcement" />
            </div>

            <div class="thankyou-banner">
              <img src="/images/assets/heart-icon.svg" alt="Heart Icon" class="heart-icon" />
              <span>THANK YOU FOR SIGNING-UP / UPDATING YOUR INFORMATION!</span>
            </div>

            <!-- Consent Checkbox -->
            <div class="form-group">
              <label class="consent-box">
                <input type="checkbox" v-model="formData.agreedConsent" required />
                <span>Data Privacy Consent & Oath of Volunteerism</span>
              </label>
            </div>
          </div>

          <!-- Form Navigation Actions -->
          <div class="action-buttons">
            <router-link 
              v-if="currentStep === 1" 
              to="/" 
              class="btn-action btn-secondary"
            >
              BACK TO HOME
            </router-link>

            <button 
              v-if="currentStep > 1" 
              type="button" 
              class="btn-action btn-secondary" 
              @click="prevStep"
            >
              BACK
            </button>
            
            <button type="submit" class="btn-action btn-primary" :disabled="submitting">
              <span v-if="currentStep < 4">NEXT STEP →</span>
              <span v-else class="btn-content">
                {{ submitting ? 'SUBMITTING…' : 'SUBMIT / UPDATE REGISTRATION' }}
                <img v-if="!submitting" src="/images/assets/check-icon.svg" alt="Check" class="btn-icon" />
              </span>
            </button>
          </div>
        </form>

        <div class="form-footer">
          Already registered? <router-link to="/login">Sign in here</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

