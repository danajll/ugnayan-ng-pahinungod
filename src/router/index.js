import { createRouter, createWebHistory } from 'vue-router';

import PublicHome from '../views/PublicHome.vue';
import PublicRegister from '../views/sign/PublicRegister.vue'
import PublicLogin from '../views/sign/PublicLogin.vue'

import AdminLayout from '../views/admin/AdminLayout.vue';
import AdminDashboard from '../views/admin/AdminDashboard.vue';
import AdminEvents from '../views/admin/AdminEvents.vue';
import AdminVolunteers from '../views/admin/AdminVolunteers.vue';
import AdminProgress from '../views/admin/AdminProgress.vue';
import AdminSettings from '../views/admin/AdminSettings.vue';

import UserLayout from '../views/user/UserLayout.vue';
import UserHome from '../views/user/UserHome.vue';
import UserEvents from '../views/user/UserEvents.vue';
import UserPrograms from '../views/user/UserPrograms.vue';
import UserProfile from '../views/user/UserProfile.vue';
import UserProfileEdit from '../views/user/UserProfileEdit.vue';

const routes = [

  {
    path: '/',
    component: PublicHome
  },
  {
    path: '/register',
    name: 'register',
    component: PublicRegister,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'login',
    component: PublicLogin
  }, 
  {
    path: '/user',
    component: UserLayout,
    children: [
      { path: '', component: UserHome },
      { path: 'events', component: UserEvents },
      { path: 'programs', component: UserPrograms },
      { path: 'profile', component: UserProfile },
      { path: 'profile/edit', component: UserProfileEdit }
    ]
  },
  {
    path: '/admin',
    component: AdminLayout,

    children: [

      {
        path: '',
        component: AdminDashboard
      },

      {
        path: 'events',
        component: AdminEvents
      },

      {
        path: 'volunteers',
        component: AdminVolunteers
      },

      {
        path: 'progress',
        component: AdminProgress
      },

      {
        path: 'settings',
        component: AdminSettings
      }

    ]

  }

];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// ─────────────────────────────────────────────────────────────
// Auth guard
// ─────────────────────────────────────────────────────────────

// Cache /api/me/ response so we don't hit the backend on every nav
let cachedMe = null

async function fetchMe() {
  if (cachedMe) return cachedMe
  try {
    // Import here to avoid circular import issues at module load time
    const { meService } = await import('../api/me')
    const { data } = await meService.get()
    cachedMe = data
    return data
  } catch (err) {
    cachedMe = null
    return null
  }
}

// Clear the cache when signing out — add this line to sign-out handlers
export function invalidateMeCache() {
  cachedMe = null
}

router.beforeEach(async (to) => {
  const token = localStorage.getItem('auth_token')

  // 1. /register requires a token (Google login must happen first)
  if (to.path === '/register' && !token) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }

  // 2. Everything under /admin and /user requires a token
  const requiresAuth = to.path.startsWith('/admin') || to.path.startsWith('/user')
  if (requiresAuth && !token) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }

  // 3. /admin/* requires staff or superuser
  if (to.path.startsWith('/admin') && token) {
    const me = await fetchMe()

    if (!me) {
      // Token invalid / expired — nuke it and send to login
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user_id')
      localStorage.removeItem('volunteer_id')
      cachedMe = null
      return { path: '/login', query: { redirect: to.fullPath } }
    }

    if (!me.is_staff && !me.is_superuser) {
      // Logged in, but not an admin — redirect to their own dashboard
      return { path: '/user' }
    }
  }

  // Otherwise, proceed normally
  return true
})

export default router

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !localStorage.getItem('auth_token')) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }
})