<script setup>
import { reactive, ref } from 'vue'

const showPassword = ref(false)

const form = reactive({
  identifier: '',
  password: '',
  rememberMe: false
})

const handleLogin = () => {
  console.log('Login attempt:', form)
}

const handleGoogleLogin = () => {
  console.log('Google SSO Triggered')
}

const handleAlumniLogin = () => {
  console.log('Alumni login requested')
}

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
          
          <button type="button" @click="handleGoogleLogin" class="btn-sso">
            <svg class="google-icon" viewBox="0 0 24 24" width="18" height="18">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
            </svg>
            Sign in with UP mail (@up.edu.ph)
          </button>
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

