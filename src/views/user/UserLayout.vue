
<template>
  <div class="site user-site">
    <!-- navbar -->
    <header class="navbar">
      <router-link to="/user" class="brand">
        <img
          src="/images/logos/pahinungod-logo.png"
          alt="Ugnayan ng Pahinungod"
          class="brand-logo"
        />

        <div>
          <div class="brand-univ">
            UNIVERSITY OF THE PHILIPPINES - MINDANAO
          </div>
          <div class="brand-name">UGNAYAN NG PAHINUNGÓD</div>
        </div>
      </router-link>

      <button
        class="menu-toggle"
        type="button"
        @click="menuOpen = !menuOpen"
        aria-label="Toggle navigation"
      >
        <Menu v-if="!menuOpen" :size="20" />
        <X v-else :size="20" />
      </button>

      <nav :class="{ open: menuOpen }">
        <router-link
          to="/user"
          :class="{ active: route.path === '/user' }"
          @click="menuOpen = false"
        >
          Home
        </router-link>

        <router-link
          to="/user/events"
          :class="{ active: route.path.includes('/events') }"
          @click="menuOpen = false"
        >
          Upcoming Events
        </router-link>

        <router-link
          to="/user/programs"
          :class="{ active: route.path.includes('/programs') }"
          @click="menuOpen = false"
        >
          Programs
        </router-link>

        <router-link
          to="/user/profile"
          :class="{ active: route.path.includes('/profile') }"
          @click="menuOpen = false"
        >
          Profile
        </router-link>
      </nav>
    </header>

    <!-- user portal pages -->
    <main class="user-layout-content">
      <router-view />
    </main>

    <!-- footer -->
    <footer>
      <div class="footer-main">
        <div class="footer-brand">
          <div class="footer-logos">
            <img
              src="/images/logos/uplogo.png"
              alt="University of the Philippines"
            />
            <img
              src="/images/logos/pahinungod-logo.png"
              alt="Ugnayan ng Pahinungód"
            />
            <img
              src="/images/logos/upminlogo.png"
              alt="UP Mindanao"
            />
          </div>
        </div>

        <div>
          <div class="footer-title">QUICK LINKS</div>

          <router-link to="/">Public Portal</router-link>
          <a href="/#about">About Us</a>
          <a href="/#programs">Featured Programs</a>
          <a href="/#events">Upcoming Events</a>
        </div>

        <div>
          <div class="footer-title">PORTALS &amp; ACCESS</div>

          <router-link to="/user">Student Volunteer Login</router-link>
          <a href="#">Faculty Coordinator Portal</a>
          <a href="#">Partner Organization</a>
          <router-link to="/admin">Admin Console</router-link>
          <a href="#">New Volunteer Onboarding</a>
        </div>

        <div>
          <div class="footer-title">ENGAGEMENT</div>

          <p>
            Join the movement. Receive volunteer dispatches and
            emergency mobilization calls.
          </p>

          <form class="email-row" @submit.prevent="joinMailingList">
            <input
              v-model="email"
              type="email"
              placeholder="Your email address"
              aria-label="Your email address"
              required
            />
            <button type="submit">Join</button>
          </form>

          <div class="socials">
            <a href="mailto:" aria-label="Email">
              <Mail :size="14" />
            </a>
            <a href="#" aria-label="Facebook">
              <Facebook :size="14" />
            </a>
            <a href="#" aria-label="Instagram">
              <Instagram :size="14" />
            </a>
            <a href="#" aria-label="LinkedIn">
              <Linkedin :size="14" />
            </a>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <div class="container">
          <div class="footer-bottom-content">
            <p>
              © {{ new Date().getFullYear() }} Ugnayan ng Pahinungód -
              UP Mindanao. All rights reserved.
            </p>

            <div class="footer-bottom-links">
              <a href="#">Privacy Policy</a>
              <a href="#">Accessibility</a>
              <a href="#">Terms of Use</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import '../../styles/user.css';
import {
  Menu,
  X,
  Mail,
  Facebook,
  Instagram,
  Linkedin
} from 'lucide-vue-next';

const route = useRoute();
const menuOpen = ref(false);
const email = ref('');

function joinMailingList() {
  // connect this form to the mailing-list backend pls
  email.value = '';
}
</script>
