<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../../api/auth'

const router = useRouter()
const showPassword = ref(false)
const loading = ref(false)
const error = ref(null)

const form = reactive({
  identifier: '',
  password: '',
  rememberMe: false,
})

// ─── Handle Google credential response ───
const handleCredentialResponse = async (response) => {
  error.value = null
  loading.value = true
  try {
    const { data } = await authService.googleLogin(response.credential)

    // Persist the DRF token for the Axios interceptor
    localStorage.setItem('auth_token', data.token)
    localStorage.setItem('user_id', data.user_id)
    if (data.volunteer_id) localStorage.setItem('volunteer_id', data.volunteer_id)

    // Branch on onboarding status
    if (!data.is_profile_complete) {
      // New user — must finish onboarding first
      router.push({ path: '/register', query: { from: 'google' } })
    } else if (data.is_staff || data.is_superuser) {
      // Admin / staff — straight to the admin panel
      router.push('/admin')
    } else {
      // Regular volunteer — into the user layout
      router.push('/user')
    }
  } catch (err) {
    const detail = err.response?.data?.detail || 'Google login failed.'
    error.value = detail
    console.error(err.response?.data || err)
  } finally {
    loading.value = false
  }
}

// ─── Initialize Google button ───
onMounted(() => {
  if (!window.google) {
    error.value = 'Google SDK failed to load. Check your internet connection.'
    return
  }
  window.google.accounts.id.initialize({
    client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
    callback: handleCredentialResponse,
    ux_mode: 'popup',
  })
  window.google.accounts.id.renderButton(
    document.getElementById('google-signin-btn'),
    {
      theme: 'outline',
      size: 'large',
      width: 400,
      text: 'signin_with',
      shape: 'rectangular',
    }
  )
})

// ─── Legacy fallback (still not wired) ───
const handleLogin = () => {
  error.value = 'Please use UP Google Sign-On above.'
}
const handleGoogleLogin = () => {} // no-op, the SDK renders its own button
const handleAlumniLogin = () => {}
const handleForgotPassword = () => {
  alert('Password reset instructions requested.')
}
</script>

<style scoped>
@import "../../styles/sign/login.css";
</style>

<template>
  <div class="login-layout">
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
        <!-- Header -->
        <div class="form-header">
          <span class="portal-category">UP MINDANAO · VOLUNTEER SERVICE</span>
          <h1 class="portal-title">Volunteer Portal Log-In</h1>
          <p class="portal-subtitle">Access your missions, accredited hours, and volunteer profile</p>
        </div>

        <!-- UP Single Sign-On -->
        <div class="sso-section">
          <span class="section-label">UP SINGLE SIGN-ON</span>

          <!-- Google SDK renders its button inside this div -->
          <div id="google-signin-btn" style="display:flex; justify-content:center;"></div>

          <p v-if="loading" style="text-align:center; font-size:0.85rem; margin-top:8px;">
            Verifying with Google…
          </p>
          <p v-if="error" style="color:#d32f2f; font-size:0.85rem; text-align:center; margin-top:8px;">
            {{ error }}
          </p>
        </div>

        <!-- Divider -->
        <div class="divider">
          <span>OR ALUMNI / VOLUNTEER CREDENTIALS</span>
        </div>

        <!-- Credentials Form -->
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label>USERNAME, UP MAIL, OR REGISTERED ALUMNI EMAIL <span class="required">*</span></label>
            <input 
              v-model="form.identifier" 
              type="text" 
              placeholder="Username, @up.edu.ph, or personal email (e.g. gmail.com)" 
              required 
            />
            <span class="field-help">Alumni volunteers may use their registered personal email address or alumni ID.</span>
          </div>

          <div class="form-group">
            <div class="label-row">
              <label>PASSWORD <span class="required">*</span></label>
              <a href="#" @click.prevent="handleForgotPassword" class="forgot-link">Forgot password?</a>
            </div>
            <div class="password-input-wrapper">
              <input 
                v-model="form.password" 
                :type="showPassword ? 'text' : 'password'" 
                placeholder="Enter your password" 
                required 
              />
              <button 
                type="button" 
                class="toggle-password" 
                @click="showPassword = !showPassword"
                title="Toggle Password Visibility"
              >
                <!-- Eye Icon -->
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
              </button>
            </div>
          </div>

          <div class="remember-row">
            <label class="remember-me">
              <input type="checkbox" v-model="form.rememberMe" />
              <span>Remember me</span>
            </label>
          </div>

          <!-- Buttons Row -->
          <div class="action-buttons">
            <router-link to="/register" class="btn-action btn-secondary">
              REGISTER
            </router-link>

            <button type="submit" class="btn-action btn-primary">
              LOG IN
            </button>
          </div>
        </form>

        <!-- Footer -->
        <div class="form-footer">
          <span class="footer-register">
            Don't have a volunteer account yet? 
            <router-link to="/register">Register here</router-link>
          </span>
          <span class="footer-version">Pahinungód v2.6</span>
        </div>
      </div>
    </div>
  </div>
</template>

