<script setup>

import { ref } from 'vue';

import {
  Menu,
  ArrowUpRight,
  CalendarDays,
  Mail,
  Facebook,
  Instagram,
  Linkedin
} from 'lucide-vue-next';

const menuopen = ref(false);

const programs = [
  {
    category: 'HEALTH',
    title: 'Bloodletting & Health Outreach',
    image: '/images/programs/bloodletting.jpg',
    text: 'Promoting community healthcare and voluntary blood donation drives.'
  },
  {
    category: 'EDUCATION AND TUTORING',
    title: 'Affirmative Action Program (AAP)',
    image: '/images/programs/aap.jpg',
    text: 'Providing intensive tutorial sessions, college admission test preparation, and customized learning materials.'
  },
  {
    category: 'COMMUNITY DEVELOPMENT',
    title: 'Gurong Pahinungod & Literacy',
    image: '/images/programs/gurongpahinungod.jpg',
    text: 'Developing capable volunteers and student teachers for rural schools in Davao Region and BARMM.'
  }
];

const events = Array.from({ length: 6 }, () => ({
  title: 'Community Health Outreach 2026',
  date: 'March 03, 2026',
  location: 'Davao Region',
  slots: '32 slots left'
}));

const locations = [
  [
    'Davao Region',
    'Community literacy and volunteer service stations across the region.',
    '14 Projects'
  ],
  [
    'South Cotabato',
    'Agricultural support and indigenous community education hubs.',
    '8 Projects'
  ],
  [
    'BARMM',
    'Peace education and high school admission tutoring programs.',
    '6 Projects'
  ],
  [
    'Bukidnon',
    'Upland watershed protection and rural clinic assistance.',
    '5 Projects'
  ],
  [
    'Cotabato',
    'Peace education and community-based education programs.',
    '5 Projects'
  ]
];

</script>

<template>

  <div class="site">

    <!-- navbar -->

    <header class="navbar">

      <a class="brand" href="#home">

        <img
          src="/images/logos/pahinungod-logo.png"
          alt="Ugnayan ng Pahinungod"
          class="brand-logo"
        />

        <div>

          <div class="brand-univ">
            UNIVERSITY OF THE PHILIPPINES - MINDANAO
          </div>

          <div class="brand-name">
            UGNAYAN NG PAHINUNGOD
          </div>

        </div>

      </a>

      <button
        class="menu-toggle"
        @click="menuopen = !menuopen"
        aria-label="Toggle menu"
      >
        <Menu :size="20" />
      </button>

      <nav :class="{ open: menuopen }">

        <a class="active" href="#home">Home</a>
        <a href="#about">About</a>
        <a href="#programs">Programs</a>
        <a href="#events">Upcoming Events</a>
        <a href="#register">Register</a>
        <a href="#login">Log in</a>

      </nav>

    </header>

    <main>

      <!-- hero -->

      <section id="home" class="hero">

        <div class="hero-overlay"></div>

        <div class="hero-content">

          <h1>
            Make a difference.<br />
            Volunteer with Pahinungód.
          </h1>

          <p>
            MAKIBAHAGI, MAPLINGKOD, MAG PAHINUNGÓD
          </p>

        </div>

      </section>

      <!-- about -->

      <section id="about" class="about section">

        <div class="about-gallery">

          <div class="gallery-tile tile-1">

            <img
              src="/images/gallery/gallery1.jpg"
              alt="Ugnayan ng Pahinungod activity"
            />

          </div>

          <div class="gallery-tile tile-2">

            <img
              src="/images/gallery/gallery2.jpg"
              alt="Ugnayan ng Pahinungod activity"
            />

          </div>

          <div class="gallery-tile tile-3">

            <img
              src="/images/gallery/gallery3.jpg"
              alt="Ugnayan ng Pahinungod activity"
            />

          </div>

          <div class="gallery-tile tile-4">

            <img
              src="/images/gallery/gallery4.jpg"
              alt="Ugnayan ng Pahinungod activity"
            />

          </div>

          <div class="gallery-tile tile-5">

            <img
              src="/images/gallery/gallery5.jpg"
              alt="Ugnayan ng Pahinungod activity"
            />

          </div>

          <div class="gallery-tile tile-6">

            <img
              src="/images/gallery/gallery6.jpg"
              alt="Ugnayan ng Pahinungod activity"
            />

          </div>

          <div class="gallery-tile tile-7">

            <img
              src="/images/gallery/gallery7.jpg"
              alt="Ugnayan ng Pahinungod activity"
            />

          </div>

          <div class="gallery-tile tile-8">

            <img
              src="/images/gallery/gallery8.jpg"
              alt="Ugnayan ng Pahinungod activity"
            />

          </div>

          <div class="gallery-tile tile-9">

            <img
              src="/images/gallery/gallery9.jpg"
              alt="Ugnayan ng Pahinungod activity"
            />

          </div>

        </div>

        <div class="about-copy">

          <div class="eyebrow">
            UP MINDANAO · VOLUNTEER SERVICE
          </div>

          <h2>About Us.</h2>

          <div class="about-block">

            <h3>Vision</h3>

            <p>
              UP in the service of the underserved communities through
              volunteerism.
            </p>

          </div>

          <div class="about-block">

            <h3>Mission</h3>

            <p>
              To lead in innovative and transformative engagements as the
              public service university committed to the empowerment of
              the people and selfless service to the nation.
            </p>

          </div>

          <div class="about-block">

            <h3>Guiding Principles</h3>

            <ul>

              <li>The University is in the service of the nation</li>

              <li>Prioritization of the underserved communities</li>

              <li>The volunteer as the embodiment of public service</li>

              <li>
                Mutuality of interests: University, volunteers & communities
              </li>

            </ul>

          </div>

        </div>

      </section>

      <!-- programs -->

      <section id="programs" class="section programs-section">

        <div class="section-heading">

          <h2>Featured Programs.</h2>

        </div>

        <div class="program-grid">

          <article
            v-for="program in programs"
            :key="program.title"
            class="program-card"
          >

            <img
              :src="program.image"
              :alt="program.title"
            />

            <div class="card-body">

              <span class="card-category">
                {{ program.category }}
              </span>

              <h3>
                {{ program.title }}
              </h3>

              <p>
                {{ program.text }}
              </p>

              <a href="#">

                Learn more

                <ArrowUpRight :size="13" />

              </a>

            </div>

          </article>

        </div>

      </section>

      <!-- events -->

      <section id="events" class="section events-section">

        <h2>Upcoming Events.</h2>

        <div class="event-grid">

          <article
            v-for="(event, index) in events"
            :key="index"
            class="event-card"
          >

            <div class="event-top">

              <span>
                EVENT DETAILS
              </span>

              <small>
                {{ event.slots }}
              </small>

            </div>

            <h3>
              {{ event.title }}
            </h3>

            <div class="event-meta">

              <CalendarDays :size="12" />

              {{ event.date }} · {{ event.location }}

            </div>

            <p>
              Multi-specialty wellness camp, medical distribution,
              and hygiene education in partner barangays.
            </p>

            <button>

              Sign Up

              <ArrowUpRight :size="12" />

            </button>

          </article>

        </div>

      </section>

      <!-- map -->

      <section class="section map-section">

        <div class="map-card">

          <div class="mindanao-map">

            <img
              src="/images/map/mindanao-map.png"
              alt="Map of Mindanao"
              class="mindanao-map-image"
            />

            <div class="map-marker marker-barmm">

              <span></span>

              BARMM

            </div>

            <div class="map-marker marker-south-cotabato">

              <span></span>

              SOUTH COTABATO

            </div>

            <div class="map-marker marker-davao">

              <span></span>

              DAVAO

            </div>

            <div class="map-marker marker-bukidnon">

              <span></span>

              BUKIDNON

            </div>

            <div class="map-marker marker-cotabato">

              <span></span>

              COTABATO

            </div>

          </div>

          <div class="locations">

            <div class="eyebrow">
              ACTIVITY LOCATIONS
            </div>

            <h3>
              Active Operational Clusters
            </h3>

            <div
              v-for="location in locations"
              :key="location[0]"
              class="location-row"
            >

              <div>

                <strong>

                  <span class="dot"></span>

                  {{ location[0] }}

                </strong>

                <p>
                  {{ location[1] }}
                </p>

              </div>

              <small>
                {{ location[2] }}
              </small>

            </div>

            <a href="#" class="directory-link">

              Explore Full Regional Directory

              <ArrowUpRight :size="13" />

            </a>

          </div>

        </div>

      </section>

      <!-- cta -->

      <section id="register" class="cta-section">

        <div class="cta">

          <span class="pill">
            READY TO MAKE A DIFFERENCE?
          </span>

          <h2>
            Serve with Pahinungód.<br />
            Be the change Mindanao needs.
          </h2>

          <p>
            Whether you are a student exploring your first community
            immersion, an alumnus giving back, or a community partner
            seeking collaborative impact, there is a place for your
            compassion and skills.
          </p>

          <div class="cta-buttons">

            <a class="primary-btn" href="#">

              Register as Volunteer

              <ArrowUpRight :size="14" />

            </a>

            <a class="secondary-btn" href="#">
              Partner with Us
            </a>

          </div>

          <div class="cta-features">

            <span>✓ Free comprehensive orientation</span>

            <span>✓ UP-accredited service hours</span>

            <span>✓ Official certificate of community service</span>

          </div>

        </div>

      </section>

    </main>

    <!-- footer -->

    <footer>

      <div class="footer-main">

        <div class="footer-brand">

          <div class="footer-logos">

            <img
              src="/images/logos/uplogo.png"
              alt="UP Mindanao"
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

          <div class="footer-title">
            QUICK LINKS
          </div>

          <a href="#">Public Portal</a>

          <a href="#about">About Us</a>

          <a href="#programs">Featured Programs</a>

          <a href="#events">Upcoming Events</a>

        </div>

        <div>

          <div class="footer-title">
            PORTALS & ACCESS
          </div>

          <a href="#">Student Volunteer Login</a>

          <a href="#">Faculty Coordinator Portal</a>

          <a href="#">Partner Organization</a>

          <a href="#">Admin Console</a>

          <a href="#">New Volunteer Onboarding</a>

        </div>

        <div>

          <div class="footer-title">
            ENGAGEMENT
          </div>

          <p>
            Join the movement. Receive volunteer dispatches and
            emergency mobilization calls.
          </p>

          <div class="email-row">

            <input
              type="email"
              placeholder="Your email address"
            />

            <button>
              Join
            </button>

          </div>

          <div class="socials">

            <Mail :size="14" />

            <Facebook :size="14" />

            <Instagram :size="14" />

            <Linkedin :size="14" />

          </div>

        </div>

      </div>

      <div class="footer-bottom">

        <span>

          © 2026 Ugnayan ng Pahinungód · UP Mindanao.
          University of the Philippines System.
          All rights reserved.

        </span>

        <span>

          Privacy Policy &nbsp;&nbsp;
          Terms of Service &nbsp;&nbsp;
          UP System Mandate

        </span>

      </div>

    </footer>

  </div>

</template>