
<script setup>
import { computed, ref } from 'vue';
import { Search, CalendarDays, MapPin, Users } from 'lucide-vue-next';

const search = ref('');
const region = ref('All locations');
const dateRange = ref('Any time');
const category = ref('All');

const categories = ['All', 'Health', 'Education', 'Environment', 'Others'];

const events = [
  {
    title: 'UPMin Bloodletting Activity',
    category: 'Health',
    date: 'Dec 02 - Dec 04, 2026',
    location: 'Mintal, Davao City',
    image: '/images/programs/bloodletting.jpg',
    description: 'Help support community blood donation and healthcare outreach.',
    tags: ['Healthcare Professionals/Med Personnel', 'DHK Students', 'NSTP Accredited'],
    lead: 'Prof. D. Santiago (SOM)',
    slots: 8
  },
  {
    title: 'Affirmative Action Program',
    category: 'Education',
    date: 'Dec 05, 2026',
    location: 'Davao Region',
    image: '/images/programs/aap.jpg',
    description: 'Support learners through tutorials and college admission test preparation.',
    tags: ['Education', 'Student Volunteers'],
    lead: 'AAP Coordinators',
    slots: 12
  },
  {
    title: 'Gurong Pahinungod & Literacy',
    category: 'Education',
    date: 'Dec 10, 2026',
    location: 'Davao Region',
    image: '/images/programs/gurongpahinungod.jpg',
    description: 'Help bring learning support and educational resources to communities.',
    tags: ['Teaching', 'Community'],
    lead: 'Program Coordinators',
    slots: 6
  },
  {
    title: 'Community Environmental Day',
    category: 'Environment',
    date: 'Dec 12, 2026',
    location: 'South Cotabato',
    image: '/images/programs/nature.jpg',
    description: 'Join local partners in environmental awareness and community care.',
    tags: ['Environment', 'Community'],
    lead: 'Environmental Team',
    slots: 15
  },
  {
    title: 'Community Donation Drive',
    category: 'Others',
    date: 'Dec 15, 2026',
    location: 'Davao Region',
    image: '/images/programs/donation.jpg',
    description: 'Assist with organizing and distributing donated supplies.',
    tags: ['Donation Drive', 'Outreach'],
    lead: 'Volunteer Coordinators',
    slots: 10
  }
];

const filteredEvents = computed(() => {
  return events.filter(event => {
    const matchesSearch = `${event.title} ${event.location} ${event.description}`
      .toLowerCase()
      .includes(search.value.toLowerCase());

    const matchesCategory = category.value === 'All' || event.category === category.value;
    const matchesRegion = region.value === 'All locations' || event.location.includes(region.value);

    return matchesSearch && matchesCategory && matchesRegion;
  });
});

const signedUp = ref([]);

function signUp(title) {
  if (!signedUp.value.includes(title)) {
    signedUp.value.push(title);
  }
}
</script>

<template>
  <section class="user-hero user-hero-events">
    <div>
      <h1>Make a difference.<br />Volunteer with Pahinungód.</h1>
      <p>MAKIBAHAGI, MAGLINGKOD, MAG PAHINUNGÓD</p>
    </div>
  </section>

  <section class="user-content user-events-content">
    <div class="user-event-filters">
      <label class="user-search">
        <Search :size="16" />
        <input v-model="search" placeholder="Search missions, locations, or coordinators..." />
      </label>

      <select v-model="region" aria-label="Filter by location">
        <option>All locations</option>
        <option>Davao Region</option>
        <option>Davao City</option>
        <option>South Cotabato</option>
      </select>

      <select v-model="dateRange" aria-label="Filter by date">
        <option>Any time</option>
        <option>Last 7 Days</option>
        <option>This Month</option>
        <option>Upcoming</option>
      </select>

      <div class="user-category-tabs">
        <button
          v-for="item in categories"
          :key="item"
          type="button"
          :class="{ active: category === item }"
          @click="category = item"
        >
          {{ item }}
        </button>
      </div>
    </div>

    <div class="user-results-line">
      <span>{{ filteredEvents.length }} volunteer opportunities</span>
      <span>Find an activity that works for you.</span>
    </div>

    <div v-if="filteredEvents.length" class="user-event-grid">
      <article
        v-for="event in filteredEvents"
        :key="event.title"
        class="user-event-card"
      >
        <img class="user-event-image" :src="event.image" :alt="event.title" />

        <div class="user-event-body">
          <span
            class="user-category-pill"
            :class="`category-${event.category.toLowerCase()}`"
          >
            {{ event.category }}
          </span>

          <p class="user-event-meta">
            <CalendarDays :size="13" />
            {{ event.date }}
          </p>

          <p class="user-event-meta">
            <MapPin :size="13" />
            {{ event.location }}
          </p>

          <h2>{{ event.title }}</h2>
          <p class="user-event-description">{{ event.description }}</p>

          <div class="user-event-tags">
            <span v-for="tag in event.tags" :key="tag">
              {{ tag }}
            </span>
          </div>

          <div class="user-event-lead">
            <span>Lead: {{ event.lead }}</span>
            <strong>
              <Users :size="13" />
              {{ event.slots }} slots left
            </strong>
          </div>

          <RouterLink class="user-button user-button-outline" to="/user/events">
            More Details
          </RouterLink>

          <button
            class="user-button user-button-primary"
            type="button"
            :disabled="signedUp.includes(event.title)"
            @click="signUp(event.title)"
          >
            {{ signedUp.includes(event.title) ? 'Signed Up' : 'Be a Volunteer' }}
          </button>
        </div>
      </article>
    </div>

    <div v-else class="user-empty-state">
      <Search :size="30" />
      <h2>No events found</h2>
      <p>Try changing your search or filters.</p>

      <button
        class="user-button user-button-outline"
        type="button"
        @click="search = ''; region = 'All locations'; category = 'All'"
      >
        Clear filters
      </button>
    </div>

    <p class="user-demo-note">
      Event listings and sign-up actions are currently sample frontend data and are not yet saved to the backend.
    </p>
  </section>
</template>
