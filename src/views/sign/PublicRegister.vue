<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const currentStep = ref(1)

const formData = reactive({
  // Step 1: Personal Information
  lastName: '',
  firstName: '',
  middleName: '',
  nickName: '',
  age: '',
  sex: '',
  birthDate: '',
  ipAffiliation: '',
  mobile: '',
  facebookLink: '',
  hobbies: '',
  affiliatedOrgs: '',
  permanentAddress: '',
  upAddress: '',

  // Step 2: Affiliation & Demographics
  affiliation: '',
  shsFinished: '',
  bachelorsDegree: '',
  firstInFamilyCollege: '',
  firstInFamilyGradStudies: '',
  firstInFamilyUP: '',

  // Step 3: Emergency Contact & Programs
  emergencyName: '',
  emergencyRelation: '',
  emergencyMobile: '',
  emergencyAddress: '',
  volunteerPrograms: [],
  affirmativeSubjects: [],

  // Step 4: Background & Consent
  applicationStatus: '',
  tagapagUgnay: '',
  otherVolOrg: '',
  otherVolOrgName: '',
  whereHeard: '',
  agreedConsent: false
})

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const handleNextOrSubmit = () => {
  if (currentStep.value < 4) {
    currentStep.value++
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } else {
    console.log('Final Form Data Submitted:', formData)
    alert('Registration successfully submitted!')
    router.push('/login')
  }
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

            <div class="form-group">
              <label>WHERE DID YOU OBTAIN YOUR BACHELOR'S DEGREE AND WHAT IS YOUR DEGREE PROGRAM?</label>
              <span class="field-help">(For graduate students)</span>
              <input v-model="formData.bachelorsDegree" type="text" placeholder="e.g. BS Biology, UP Mindanao (or other university)" />
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
            
            <button type="submit" class="btn-action btn-primary">
              <span v-if="currentStep < 4">NEXT STEP &rarr;</span>
              <span v-else class="btn-content">
                SUBMIT / UPDATE REGISTRATION
                <img src="/images/assets/check-icon.svg" alt="Check" class="btn-icon" />
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

