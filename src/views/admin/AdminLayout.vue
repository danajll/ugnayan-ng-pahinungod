<script setup>

import { ref } from 'vue';

import {
  LayoutDashboard,
  CalendarDays,
  Users,
  BadgeCheck,
  ShieldCheck,
  PanelLeftClose,
  PanelLeftOpen,
  ArrowLeft,
  ExternalLink,
  ChevronDown
} from 'lucide-vue-next';


const sidebarCollapsed = ref(false);

const accountOpen = ref(false);


const toggleSidebar = () => {

  sidebarCollapsed.value = !sidebarCollapsed.value;

};


const navigation = [
  {
    name: 'Dashboard',
    path: '/admin',
    icon: LayoutDashboard
  },

  {
    name: 'Events',
    path: '/admin/events',
    icon: CalendarDays
  },

  {
    name: 'Volunteers Directory',
    path: '/admin/volunteers',
    icon: Users
  },

  {
    name: 'Volunteer Progress & Badges',
    path: '/admin/progress',
    icon: BadgeCheck
  },

  {
    name: 'Privacy & Settings',
    path: '/admin/settings',
    icon: ShieldCheck
  }
];

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
              Ugnayan ng Pahinungod
            </strong>

            <span>
              System Admin
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

          <button>
            Account Settings
          </button>

          <button>
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