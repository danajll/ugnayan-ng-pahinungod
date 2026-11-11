<script setup>
import { ref, computed } from 'vue';
import { ArrowRight, Search } from 'lucide-vue-next';

const search = ref('');
const category = ref('All programs');

const categories = [
  'All programs',
  'Health',
  'Education and Tutoring',
  'Community Development',
  'Environment'
];

const programs = [
  {
    title: 'Bloodletting & Health Outreach',
    category: 'Health',
    image: '/images/programs/bloodletting.jpg',
    description: 'Promoting community healthcare, voluntary blood donation drives, and missions across remote clinics.'
  },
  {
    title: 'Affirmative Action Program (AAP)',
    category: 'Education and Tutoring',
    image: '/images/programs/aap.jpg',
    description: 'Providing intensive tutorial sessions, college admission test prep, and customized learning materials.'
  },
  {
    title: 'Gurong Pahinungod & Literacy',
    category: 'Community Development',
    image: '/images/programs/gurongpahinungod.jpg',
    description: 'Deploying graduate volunteers and student teachers to rural schools in Davao Region and BARMM.'
  },
  {
    title: 'Environmental Awareness',
    category: 'Environment',
    image: '/images/programs/nature.jpg',
    description: 'Supporting environmental awareness, conservation, and community-led activities.'
  },
  {
    title: 'Community Donation Drive',
    category: 'Community Development',
    image: '/images/programs/donation.jpg',
    description: 'Connecting volunteers with donation drives and community assistance initiatives.'
  },
  {
    title: 'Education Outreach',
    category: 'Education and Tutoring',
    image: '/images/programs/education.jpg',
    description: 'Helping communities access learning support and educational activities.'
  }
];

const filteredPrograms = computed(() => {
  return programs.filter(program => {
    const matchesCategory =
      category.value === 'All programs' ||
      program.category === category.value;

    const matchesSearch =
      `${program.title} ${program.description}`
        .toLowerCase()
        .includes(search.value.toLowerCase());

    return matchesCategory && matchesSearch;
  });
});
</script>

<template>
  <!-- hero -->
  <section class="user-hero user-hero-programs">
    <div>
      <h1>Find your way to serve.</h1>
      <p>
        Explore programs and discover where your skills can make a difference.
      </p>
    </div>
  </section>

  <!-- programs -->
  <section class="user-content user-programs-content">
    <div class="user-page-heading">
      <div>
        <span class="user-eyebrow">SERVE WITH PURPOSE</span>
        <h1>Featured Programs</h1>
        <p>Get to know the initiatives you can be part of.</p>
      </div>

      <label class="user-program-search">
        <Search :size="16" />
        <input
          v-model="search"
          placeholder="Search programs..."
        />
      </label>
    </div>

    <div class="user-program-tabs">
      <button
        v-for="item in categories"
        :key="item"
        :class="{ active: category === item }"
        @click="category = item"
      >
        {{ item }}
      </button>
    </div>

    <div class="user-program-grid">
      <article
        v-for="program in filteredPrograms"
        :key="program.title"
        class="user-program-card user-program-page-card"
      >
        <img :src="program.image" :alt="program.title" />

        <div class="user-program-card-body">
          <span class="user-eyebrow">{{ program.category }}</span>
          <h2>{{ program.title }}</h2>
          <p>{{ program.description }}</p>

          <RouterLink to="/user/events">
            Find related events
            <ArrowRight :size="15" />
          </RouterLink>
        </div>
      </article>
    </div>

    <div v-if="!filteredPrograms.length" class="user-empty-state">
      <h2>No programs found</h2>
      <p>Try another search term or category.</p>
    </div>
  </section>
</template>