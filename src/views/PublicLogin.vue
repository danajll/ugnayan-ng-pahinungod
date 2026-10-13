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

          <div class="alumni-notice">
            <span class="notice-text">Alumni without UP Mail?</span>
            <a href="#" @click.prevent="handleAlumniLogin" class="notice-link">Log in with verified personal email or UPAA credentials</a>
          </div>
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
.login-layout {
  position: relative;
  display: flex;
  min-height: 100vh;
  width: 100%;
  background-color: #ffffff;
}

.required {
  color: #EF4444;
}

/* Full Width Overlapping Header */
.top-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 50;

  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2.5rem;
  box-sizing: border-box;

  border-bottom: 1px solid rgba(241, 184, 45, 0.25);
  background: #520F18;
  backdrop-filter: blur(6px);
}

.brand-logo {
  width: 32px;
  height: auto;
  margin-bottom: -0.5rem;
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-univ {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: #ffffff;
  opacity: 0.9;
}

.brand-program {
  font-size: 0.85rem;
  font-weight: 800;
  letter-spacing: 0.03em;
  color: #ffffff;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
  transition: opacity 0.15s ease;
}

.brand-link:hover {
  opacity: 0.9;
}

/* Left Hero Banner Styling (Mirrored from Register Page) */
.hero-sidebar {
  flex: 0 0 45%;
  max-width: 45%;
  height: 100vh;
  position: sticky;
  top: 0;
  background: #520F18;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 3rem;
  padding-top: 80px; /* Offset for floating top bar */
  box-sizing: border-box;
}

.hero-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: 100%;
  max-width: 400px;
}

.oblation-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: -0.5rem;
}

.hero-logo {
  max-height: 140px;
  width: auto;
  object-fit: contain;
  margin-bottom: 0.825rem; 
  transform: translateY(40px);
}

.hero-title {
   color: #fff;
  text-align: center;
  font-family: "Inter";
  font-size: 40px;
  font-style: normal;
  font-weight: 900;
  line-height: 52px;
  letter-spacing: 2.6px;
  margin-bottom: .5rem;
  text-transform: uppercase;
}

.hero-title .highlight {
  color: #eb6c00;
}

/* Right Container Styling */
.form-container {
  flex: 1;
  background-color: #ffffff;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 6rem 4rem 3rem 4rem; /* Offset for floating top bar */
  box-sizing: border-box;
}

.form-wrapper {
  width: 100%;
  max-width: 480px;
  background: #ffffff;
  padding: 0;
}

/* Brand Header */
.form-header {
  margin-bottom: 1.5rem;
}

.portal-category {
  color: #641320;
  font-family: Inter;
  font-size: 12px;
  font-style: normal;
  font-weight: 400;
  line-height: 18px; /* 150% */
  letter-spacing: 0.6px;
  text-transform: uppercase;
}

.portal-title {
  margin: 0.2rem 0 0.25rem 0;
  color: #EA580C;
  font-family: Inter;
  font-size: 36px;
  font-style: normal;
  font-weight: 700;
  line-height: 45px; /* 125% */
  letter-spacing: -0.9px;
}

.portal-subtitle {
  font-size: 0.8rem;
  color: #6b7280;
  margin: 0;
}

/* Single Sign-On Section */
.sso-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}

.section-label {
  color: #641320;
  font-family: Inter;
  font-size: 12px;
  font-style: normal;
  font-weight: 400;
  line-height: 18px; /* 150% */
  letter-spacing: 0.6px;
  text-transform: uppercase;
}

.btn-sso {
  width: 100%;
  height: 40px;
  background-color: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.825rem;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.btn-sso:hover {
  background-color: #f9fafb;
}

.alumni-notice {
  background-color: #fdf8f6;
  border: 1px solid #f3e8e2;
  border-radius: 4px;
  padding: 0.45rem 0.75rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.7rem;
}

.notice-text {
  color: #6b7280;
}

.notice-link {
  color: #520F18;
  font-weight: 700;
  text-decoration: none;
}

.notice-link:hover {
  text-decoration: underline;
}

/* Divider */
.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 1.25rem 0;
  color: #6B7280;
  font-family: Inter;
  font-size: 12px;
  font-style: normal;
  font-weight: 500;
  line-height: 18px; /* 150% */
  letter-spacing: 0.6px;
  text-transform: uppercase;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid #e5e7eb;
}

.divider span {
  padding: 0 0.75rem;
}

/* Form Controls (Mirrored from Register) */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.form-group label {
  font-size: 0.725rem;
  font-weight: 700;
  color: #374151;
  letter-spacing: 0.02em;
}

.label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.forgot-link {
  font-size: 0.7rem;
  color: #eb6c00;
  font-weight: 700;
  text-decoration: none;
}

.forgot-link:hover {
  text-decoration: underline;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 0.5rem 0.65rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 0.85rem;
  box-sizing: border-box;
  color: #1f2937;
  background-color: #ffffff;
}

input::placeholder {
  color: #9ca3af;
  font-size: 0.85rem;
}

input:focus {
  outline: none;
  border-color: #eb6c00;
  box-shadow: 0 0 0 2px rgba(235, 108, 0, 0.15);
}

.password-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.password-input-wrapper input {
  padding-right: 2.25rem;
}

.toggle-password {
  position: absolute;
  right: 0.5rem;
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.2rem;
}

.toggle-password:hover {
  color: #374151;
}

.field-help {
  font-size: 0.7rem;
  color: #6b7280;
  margin-top: 0.05rem;
}

.remember-row {
  margin-top: -0.25rem;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: #4b5563;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 0.5rem;
}

.btn-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  padding: 0 1.5rem;
  font-size: 0.85rem;
  font-weight: 800;
  letter-spacing: 0.02em;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  box-sizing: border-box;
  transition: all 0.15s ease;
}

.btn-primary {
  background-color: #eb6c00;
  color: #ffffff;
  border: 1px solid #eb6c00;
  min-width: 120px;
}

.btn-primary:hover {
  background-color: #d05f00;
  border-color: #d05f00;
}

.btn-secondary {
  background-color: #ffffff;
  color: #374151;
  border: 1px solid #d1d5db;
  min-width: 120px;
}

.btn-secondary:hover {
  background-color: #f3f4f6;
  color: #111827;
}

/* Footer Links */
.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 2rem;
  font-size: 0.85rem;
}

.footer-register {
  color: #6b7280;
}

.footer-register a {
  color: #eb6c00;
  font-weight: 700;
  text-decoration: none;
}

.footer-register a:hover {
  text-decoration: underline;
}

.footer-version {
  color: #9ca3af;
  font-size: 0.75rem;
}

@media (max-width: 900px) {
  .login-layout {
    flex-direction: column;
  }
  .top-header {
    position: relative;
  }
  .hero-sidebar {
    width: 100%;
    max-width: 100%;
    height: auto;
    position: relative;
    padding: 2.5rem 1.5rem;
    padding-top: 2.5rem;
  }
  .form-container {
    padding: 2.5rem 1.5rem;
  }
  .alumni-notice {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
}
</style>