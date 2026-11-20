<script setup>
import { ref, computed, onMounted } from 'vue'
import { ArrowRight, Search } from 'lucide-vue-next'
import api from '../../api/client'
import { eventService } from '../../api/events'
import { useRoute } from 'vue-router'

// ─── Marketing metadata per backend Program.code ───
const PROGRAM_DETAILS = {
  AFFIRMATIVE_ACTION_PROGRAM: {
    category: 'Education and Tutoring',
    image: '/images/programs/aap.jpg',
    description: 'Providing intensive tutorial sessions, college admission test prep, and customized learning materials.',
    eventCategories: ['EDUCATION & LITERACY'],
  },
  DISASTER_RISK_REDUCTION: {
    category: 'Community Development',
    image: '/images/programs/donation.jpg',
    description: 'Training communities for disaster preparedness and emergency response.',
    eventCategories: ['NSTP / CWTS'],
  },
  TUTORIAL_SERVICE_PROGRAM: {
    category: 'Education and Tutoring',
    image: '/images/programs/education.jpg',
    description: 'Helping communities access learning support and educational activities.',
    eventCategories: ['EDUCATION & LITERACY'],
  },
  UP_BARMM_MBHTE_MOU: {
    category: 'Community Development',
    image: '/images/programs/bloodletting.jpg',
    description: 'Peace education and community assistance in the Bangsamoro region.',
    eventCategories: ['INDIGENOUS PEOPLES (IP)'],
  },
  TEACHER_DEVELOPMENT_PROGRAM: {
    category: 'Education and Tutoring',
    image: '/images/programs/gurongpahinungod.jpg',
    description: 'Deploying graduate volunteers and student teachers to rural schools in Davao Region and BARMM.',
    eventCategories: ['EDUCATION & LITERACY'],
  },
  UGNAYAN_NG_PAHINUNGOD_ONLINE: {
    category: 'Community Development',
    image: '/images/programs/education.jpg',
    description: 'Remote volunteer opportunities for online learning and outreach.',
    eventCategories: [],
  },
  ENVIRONMENTAL_AWARENESS_PROGRAM: {
    category: 'Environment',
    image: '/images/programs/nature.jpg',
    description: 'Supporting environmental awareness, conservation, and community-led activities.',
    eventCategories: ['ENVIRONMENT & ECOLOGY'],
  },
}

const FALLBACK = {
  category: 'Community Development',
  image: '/images/programs/bloodletting.jpg',
  description: 'A volunteer initiative by Ugnayan ng Pahinungód.',
  eventCategories: [],
}

// ─── State ───
const search = ref('')
const category = ref('All programs')
const programs = ref([])
const eventsByCategory = ref({})
const loading = ref(true)
const loadError = ref(null)

const route = useRoute()
if (route.query.category) {
  category.value = route.query.category
}

const categories = [
  'All programs',
  'Health',
  'Education and Tutoring',
  'Community Development',
  'Environment',
]

// ─── Fetch on mount ───
onMounted(async () => {
  try {
    const [progRes, eventsRes] = await Promise.all([
      api.get('/programs/'),
      eventService.list(),
    ])

    programs.value = progRes.data.map(p => {
      const meta = PROGRAM_DETAILS[p.code] || FALLBACK
      return {
        id: p.id,
        code: p.code,
        title: p.name,
        category: meta.category,
        image: meta.image,
        description: meta.description,
        eventCategories: meta.eventCategories,
      }
    })

    const now = new Date()
    const counts = {}
    for (const ev of eventsRes.data) {
      if (new Date(ev.start_datetime) < now) continue
      const cat = ev.category || 'Unknown'
      counts[cat] = (counts[cat] || 0) + 1
    }
    eventsByCategory.value = counts
  } catch (err) {
    loadError.value = err.response?.data?.detail || 'Failed to load programs.'
    console.error(err)
  } finally {
    loading.value = false
  }
})

const filteredPrograms = computed(() => {
  return programs.value.filter(p => {
    const matchesCategory =
      category.value === 'All programs' || p.category === category.value

    const matchesSearch =
      `${p.title} ${p.description}`
        .toLowerCase()
        .includes(search.value.toLowerCase())

    return matchesCategory && matchesSearch
  })
})
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

    <!-- Loading -->
    <div v-if="loading" class="user-empty-state">
      <p>Loading programs…</p>
    </div>

    <!-- Load error -->
    <div v-else-if="loadError" class="user-empty-state">
      <h2>Could not load programs</h2>
      <p>{{ loadError }}</p>
    </div>

    <!-- Program grid -->
    <div v-else-if="filteredPrograms.length" class="user-program-grid">
      <article
        v-for="program in filteredPrograms"
        :key="program.id"
        class="user-program-card user-program-page-card"
      >
        <img :src="program.image" :alt="program.title" />

        <div class="user-program-card-body">
          <span class="user-eyebrow">{{ program.category }}</span>
          <h2>{{ program.title }}</h2>
          <p>{{ program.description }}</p>

          <RouterLink
            v-if="program.eventCategories.length"
            :to="{ path: '/user/events', query: { category: program.eventCategories[0] } }"
          >
            Find related events
            <ArrowRight :size="15" />
          </RouterLink>

          <RouterLink v-else to="/user/events">
            Browse events
            <ArrowRight :size="15" />
          </RouterLink>
        </div>
      </article>
    </div>

    <!-- Empty after filter -->
    <div v-else class="user-empty-state">
      <h2>No programs found</h2>
      <p>Try another search term or category.</p>
    </div>
  </section>
</template>