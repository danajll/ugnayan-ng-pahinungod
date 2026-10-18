import { createRouter, createWebHistory } from 'vue-router';

import PublicHome from '../views/PublicHome.vue';
import PublicRegister from '../views/PublicRegister.vue'
import PublicLogin from '../views/PublicLogin.vue'

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
    component: PublicRegister
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

  routes

});

export default router;