<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  LayoutDashboard, CalendarDays, Users, BadgeCheck, ShieldCheck,
  PanelLeftClose, PanelLeftOpen, ArrowLeft, ExternalLink, ChevronDown
} from 'lucide-vue-next'
import { meService } from '../../api/me'

const router = useRouter()
const sidebarCollapsed = ref(false)
const accountOpen = ref(false)

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

// ─── Current user ───
const me = ref(null)
const meLoading = ref(true)

onMounted(async () => {
  try {
    const { data } = await meService.get()
    me.value = data
  } catch (err) {
    console.warn('Could not load current user:', err.response?.status)
    localStorage.removeItem('auth_token')
    router.push('/login')
  } finally {
    meLoading.value = false
  }
})

const displayName = computed(() => me.value?.full_name || 'Loading…')
const displayRole = computed(() => {
  if (!me.value) return ''
  if (me.value.is_superuser) return 'Super Admin'
  if (me.value.is_staff) return 'System Admin'
  return 'Volunteer'
})

const handleSignOut = () => {
  localStorage.removeItem('auth_token')
  localStorage.removeItem('user_id')
  router.push('/login')
}

const navigation = [
  { name: 'Dashboard', path: '/admin', icon: LayoutDashboard },
  { name: 'Events', path: '/admin/events', icon: CalendarDays },
  { name: 'Volunteers Directory', path: '/admin/volunteers', icon: Users },
  { name: 'Volunteer Progress & Badges', path: '/admin/progress', icon: BadgeCheck },
  { name: 'Privacy & Settings', path: '/admin/settings', icon: ShieldCheck },
]
</script>


<template>

  <div
    class="admin-layout"
    :class="{
      'sidebar-collapsed': sidebarCollapsed
    }"
  >

    <!-- topbar -->

    <header class="admin-topbar">

      <div class="admin-account">

        <button
          class="admin-account-button"
          @click="accountOpen = !accountOpen"
        >

          <div class="admin-account-logo">

            <img
              src="/images/logos/pahinungod-logo.png"
              alt="Ugnayan ng Pahinungod"
            />

          </div>


          <div class="admin-account-info">

            <strong>
              {{ displayName }}
            </strong>

            <span>
              {{ displayRole }}
            </span>

          </div>


          <ChevronDown
            :size="15"
            class="admin-account-chevron"
            :class="{
              rotated: accountOpen
            }"
          />

        </button>


        <div
          v-if="accountOpen"
          class="admin-account-menu"
        >

          <button @click="router.push('/admin/settings'); accountOpen = false">
            Account Settings
          </button>

          <button @click="handleSignOut">
            Sign Out
          </button>

        </div>

      </div>

    </header>


    <!-- sidebar -->

    <aside class="admin-sidebar">

      <!-- brand -->

      <div class="admin-sidebar-brand">

        <div class="admin-brand-content">

          <img
            src="/images/logos/pahinungod-logo.png"
            alt="Ugnayan ng Pahinungod"
            class="admin-brand-logo"
          />


          <div class="admin-brand-text">

            <span class="admin-brand-university">
              UNIVERSITY OF THE PHILIPPINES · MINDANAO
            </span>

            <strong>
              UGNAYAN NG PAHINUNGOD
            </strong>

          </div>

        </div>


        <button
          class="admin-sidebar-toggle"
          @click="toggleSidebar"
          :aria-label="
            sidebarCollapsed
              ? 'Expand sidebar'
              : 'Collapse sidebar'
          "
        >

          <PanelLeftClose
            v-if="!sidebarCollapsed"
            :size="22"
          />

          <PanelLeftOpen
            v-else
            :size="22"
          />

        </button>

      </div>


      <!-- navigation -->

      <nav class="admin-navigation">

        <RouterLink
          v-for="item in navigation"
          :key="item.path"
          :to="item.path"
          class="admin-nav-item"
          :title="
            sidebarCollapsed
              ? item.name
              : ''
          "
        >

          <component
            :is="item.icon"
            :size="21"
            :stroke-width="1.8"
          />

          <span>
            {{ item.name }}
          </span>

        </RouterLink>

      </nav>


      <!-- bottom -->

      <div class="admin-sidebar-bottom">

        <RouterLink
          to="/"
          class="admin-back-link"
          title="Back to Public Portal"
        >

          <ArrowLeft
            :size="18"
          />

          <span>
            Back to Public Portal
          </span>

          <ExternalLink
            :size="15"
            class="admin-external-icon"
          />

        </RouterLink>

      </div>

    </aside>


    <!-- main -->

    <main class="admin-main">

      <RouterView />

    </main>

  </div>

</template>