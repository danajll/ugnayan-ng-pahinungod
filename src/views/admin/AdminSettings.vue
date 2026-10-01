<script setup>

import { ref } from 'vue';

import {
  ShieldCheck,
  Bell,
  Lock,
  UserRound
} from 'lucide-vue-next';


const notifications = ref(true);

const twoFactor = ref(false);

</script>


<template>

  <div class="admin-page settings-page">

    <div class="admin-page-inner">

      <!-- header -->

      <div class="settings-header">

        <h1>
          PRIVACY & SETTINGS
        </h1>

        <p>
          Manage administrator preferences, security, and notifications.
        </p>

      </div>


      <!-- account & security -->

      <section class="settings-section">

        <div class="settings-section-heading">

          <ShieldCheck
            :size="20"
          />

          <div>

            <h2>
              Account & Security
            </h2>

            <p>
              Manage administrator account security.
            </p>

          </div>

        </div>


        <div class="settings-row">

          <div class="settings-row-icon">

            <UserRound
              :size="19"
            />

          </div>


          <div class="settings-row-content">

            <strong>
              Administrator Account
            </strong>

            <span>
              Ugnayan ng Pahinungod · System Admin
            </span>

          </div>


          <button>
            Manage
          </button>

        </div>


        <div class="settings-row">

          <div class="settings-row-icon">

            <Lock
              :size="19"
            />

          </div>


          <div class="settings-row-content">

            <strong>
              Two-Factor Authentication
            </strong>

            <span>
              Add another layer of security to your account.
            </span>

          </div>


          <label class="settings-switch">

            <input
              v-model="twoFactor"
              type="checkbox"
            />

            <span></span>

          </label>

        </div>

      </section>


      <!-- notifications -->

      <section class="settings-section">

        <div class="settings-section-heading">

          <Bell
            :size="20"
          />

          <div>

            <h2>
              Notifications
            </h2>

            <p>
              Choose which administrator notifications you receive.
            </p>

          </div>

        </div>


        <div class="settings-row">

          <div class="settings-row-content">

            <strong>
              Event & Volunteer Updates
            </strong>

            <span>
              Receive updates when event or volunteer information changes.
            </span>

          </div>


          <label class="settings-switch">

            <input
              v-model="notifications"
              type="checkbox"
            />

            <span></span>

          </label>

        </div>

      </section>

    </div>

  </div>

</template>


<style>

@import '../../styles/admin.css';

@import '../../styles/admin/settings.css';

</style>