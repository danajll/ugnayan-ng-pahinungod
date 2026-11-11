<script setup>

import { computed, ref } from 'vue';

import {

  Search,
  ChevronDown,
  CalendarDays,
  MapPin,
  UsersRound,
  Pencil,
  X,
  Flag,
  List,
  Bold,
  Italic,
  SlidersHorizontal,
  UploadCloud,
  Trash2,
  Map,
  UserRound,
  Clock3
} from 'lucide-vue-next';




const search = ref('');

const region = ref('Davao Region');

const regionOpen = ref(false);

const status = ref('All');

const category = ref('ALL MISSIONS');




const regions = [

  'All Regions',

  'National Capital Region (NCR)',

  'Cordillera Administrative Region (CAR)',

  'Ilocos Region (Region I)',

  'Cagayan Valley (Region II)',

  'Central Luzon (Region III)',

  'CALABARZON (Region IV-A)',

  'MIMAROPA (Region IV-B)',

  'Bicol Region (Region V)',

  'Western Visayas (Region VI)',

  'Negros Island Region (NIR)',

  'Central Visayas (Region VII)',

  'Eastern Visayas (Region VIII)',

  'Zamboanga Peninsula (Region IX)',

  'Northern Mindanao (Region X)',

  'Davao Region (Region XI)',

  'SOCCSKSARGEN (Region XII)',

  'Caraga (Region XIII)',

  'Bangsamoro Autonomous Region in Muslim Mindanao (BARMM)'

];



const selectRegion = (item) => {

  region.value = item;

  regionOpen.value = false;

};




const statuses = [

  'All',

  'Published',

  'Scheduled',

  'Drafts'

];




const categories = [

  'ALL MISSIONS',

  'HEALTH',

  'EDUCATION & LITERACY',

  'ENVIRONMENT & ECOLOGY',

  'NSTP / CWTS',

  'INDIGENOUS PEOPLES (IP)'

];




const events = ref([

  {

    id: 1,

    title: 'UPmin Bloodletting Activity',

    category: 'HEALTH',

    date: 'Dec 02 - Dec 04, 2026',

    location: 'Mintal, Davao City',

    region: 'Davao Region',

    description:

      'Lorem Ipsum is simply dummy text of the printing and typesetting industry...',

    image: '/images/programs/bloodletting.jpg',

    status: 'Published',

    displayStatus: 'COMPLETED',

    quota: 40,

    registered: 32,

    quotaLabel: 'Registered',

    tags: [

      'Healthcare Professionals/Med Personnel',

      'DHK Students',

      'NSTP Accredited'

    ],

    lead: 'Prof. D. Santiago (SOM)'

  },

  {

    id: 2,

    title:

      'Affirmative Action Program (AAP) UPCAT Campaign',

    category: 'EDUCATION & LITERACY',

    date: 'Dec 6 - Dec 8, 2026',

    location: 'Pantukan, Davao de Oro',

    region: 'Davao Region',

    description:

      'Lorem Ipsum is simply dummy text of the printing and typesetting industry...',

    image: '/images/programs/education.jpg',

    status: 'Published',

    displayStatus: 'ONGOING',

    quota: 25,

    registered: 18,

    quotaLabel: 'Registered',

    tags: [

      'All Iskolar Fellows',

      'Reading Mentorship',

      'CWTS Credit'

    ],

    lead: 'Pahinungod Literacy Desk'

  },

  {

    id: 3,

    title: 'Tree Planting Activity',

    category: 'ENVIRONMENT & ECOLOGY',

    date: 'Dec 14, 2026',

    location: 'Marahan Botanical Garden',

    region: 'Davao Region',

    description:

      'Lorem Ipsum is simply dummy text of the printing and typesetting industry...',

    image: '/images/programs/nature.jpg',

    status: 'Published',

    displayStatus: 'RECRUITING',

    quota: 50,

    registered: 50,

    quotaLabel: 'Filled',

    tags: [

      'CSM / Science Majors',

      'Field Logistics',

      'Ecological Survey'

    ],

    lead: 'Dept. of Biological Sciences'

  },

  {

    id: 4,

    title: 'Donation Drive',

    category: 'DONATION DRIVE',

    date: 'Dec 14, 2026',

    location: 'Mintal, Davao City',

    region: 'Davao Region',

    description:

      'Lorem Ipsum is simply dummy text of the printing and typesetting industry...',

    image: '/images/programs/donation.jpg',

    status: 'Published',

    displayStatus: 'RECRUITING',

    quota: 10,

    registered: 10,

    quotaLabel: 'Filled',

    tags: [

      'CSM / Science Majors',

      'Field Logistics',

      'Ecological Survey'

    ],

    lead: 'Dept. of Biological Sciences'

  },




  {

    id: 5,

    title: 'UPmin Bloodletting Activity',

    category: 'HEALTH',

    date: 'Dec 02 - Dec 04, 2026',

    location: 'Mintal, Davao City',

    region: 'Davao Region',

    description:

      'Lorem Ipsum is simply dummy text of the printing and typesetting industry...',

    image: '/images/programs/bloodletting.jpg',

    status: 'Scheduled',

    displayStatus: 'SCHEDULED',

    time: '7:00 pm',

    quota: 40,

    registered: 0,

    quotaLabel: 'Registered',

    tags: [

      'Healthcare Professionals/Med Personnel',

      'DHK Students',

      'NSTP Accredited'

    ],

    lead: 'Prof. D. Santiago (SOM)'

  },

  {

    id: 6,

    title:

      'Affirmative Action Program (AAP) UPCAT Campaign',

    category: 'EDUCATION & LITERACY',

    date: 'Dec 6 - Dec 8, 2026',

    location: 'Pantukan, Davao de Oro',

    region: 'Davao Region',

    description:

      'Lorem Ipsum is simply dummy text of the printing and typesetting industry...',

    image: '/images/programs/education.jpg',

    status: 'Scheduled',

    displayStatus: 'SCHEDULED',

    time: '7:00 pm',

    quota: 25,

    registered: 0,

    quotaLabel: 'Registered',

    tags: [

      'All Iskolar Fellows',

      'Reading Mentorship',

      'CWTS Credit'

    ],

    lead: 'Pahinungod Literacy Desk'

  },

  {

    id: 7,

    title: 'Tree Planting Activity',

    category: 'ENVIRONMENT & ECOLOGY',

    date: 'Dec 14, 2026',

    location: 'Marahan Botanical Garden',

    region: 'Davao Region',

    description:

      'Lorem Ipsum is simply dummy text of the printing and typesetting industry...',

    image: '/images/programs/nature.jpg',

    status: 'Scheduled',

    displayStatus: 'SCHEDULED',

    time: '7:00 pm',

    quota: 50,

    registered: 0,

    quotaLabel: 'Filled',

    tags: [

      'CSM / Science Majors',

      'Field Logistics',

      'Ecological Survey'

    ],

    lead: 'Dept. of Biological Sciences'

  },

  {

    id: 8,

    title: 'Donation Drive',

    category: 'DONATION DRIVE',

    date: 'Dec 14, 2026',

    location: 'Mintal, Davao City',

    region: 'Davao Region',

    description:

      'Lorem Ipsum is simply dummy text of the printing and typesetting industry...',

    image: '/images/programs/donation.jpg',

    status: 'Scheduled',

    displayStatus: 'SCHEDULED',

    time: '7:00 pm',

    quota: 10,

    registered: 0,

    quotaLabel: 'Filled',

    tags: [

      'CSM / Science Majors',

      'Field Logistics',

      'Ecological Survey'

    ],

    lead: 'Dept. of Biological Sciences'

  },




  {

    id: 9,

    title: 'UPmin Bloodletting Activity',

    category: 'HEALTH',

    date: 'Dec 02 - Dec 04, 2026',

    location: 'Mintal, Davao City',

    region: 'Davao Region',

    description:

      'Lorem Ipsum is simply dummy text of the printing and typesetting industry...',

    image: '/images/programs/bloodletting.jpg',

    status: 'Drafts',

    displayStatus: 'DRAFT',

    time: '7:00 pm',

    quota: 40,

    registered: 0,

    quotaLabel: 'Registered',

    tags: [

      'Healthcare Professionals/Med Personnel',

      'DHK Students',

      'NSTP Accredited'

    ],

    lead: 'Prof. D. Santiago (SOM)'

  },

  {

    id: 10,

    title:

      'Affirmative Action Program (AAP) UPCAT Campaign',

    category: 'EDUCATION & LITERACY',

    date: 'Dec 6 - Dec 8, 2026',

    location: 'Pantukan, Davao de Oro',

    region: 'Davao Region',

    description:

      'Lorem Ipsum is simply dummy text of the printing and typesetting industry...',

    image: '/images/programs/education.jpg',

    status: 'Drafts',

    displayStatus: 'DRAFT',

    time: '7:00 pm',

    quota: 25,

    registered: 0,

    quotaLabel: 'Registered',

    tags: [

      'All Iskolar Fellows',

      'Reading Mentorship',

      'CWTS Credit'

    ],

    lead: 'Pahinungod Literacy Desk'

  },

  {

    id: 11,

    title: 'Tree Planting Activity',

    category: 'ENVIRONMENT & ECOLOGY',

    date: 'Dec 14, 2026',

    location: 'Marahan Botanical Garden',

    region: 'Davao Region',

    description:

      'Lorem Ipsum is simply dummy text of the printing and typesetting industry...',

    image: '/images/programs/nature.jpg',

    status: 'Drafts',

    displayStatus: 'DRAFT',

    time: '7:00 pm',

    quota: 50,

    registered: 0,

    quotaLabel: 'Filled',

    tags: [

      'CSM / Science Majors',

      'Field Logistics',

      'Ecological Survey'

    ],

    lead: 'Dept. of Biological Sciences'

  }

]);




const filteredEvents = computed(() => {

  return events.value.filter((event) => {

    const searchValue =

      search.value

        .trim()

        .toLowerCase();

    const matchesSearch =

      event.title

        .toLowerCase()

        .includes(searchValue)

      ||

      event.location

        .toLowerCase()

        .includes(searchValue)

      ||

      event.lead

        .toLowerCase()

        .includes(searchValue);

    const matchesStatus =

      status.value === 'All'

      ||

      event.status === status.value;

    const matchesCategory =

      category.value === 'ALL MISSIONS'

      ||

      event.category === category.value;

    const matchesRegion =

      region.value === 'All Regions'

      ||

      event.region === region.value;

    return (

      matchesSearch

      &&

      matchesStatus

      &&

      matchesCategory

      &&

      matchesRegion

    );

  });

});




const getStatusClass = (event) => {

  if (event.displayStatus === 'COMPLETED') {

    return 'completed';

  }

  if (event.displayStatus === 'ONGOING') {

    return 'ongoing';

  }

  if (event.displayStatus === 'SCHEDULED') {

    return 'scheduled';

  }

  if (event.displayStatus === 'DRAFT') {

    return 'draft';

  }

  return 'recruiting';

};




const createModalOpen = ref(false);

const editingEvent = ref(null);

const newEvent = ref({

  title: '',

  category: 'HEALTH',

  description: '',

  startDate: '',

  endDate: '',

  region: 'Davao Region',

  venue: '',

  quota: 40,

  accreditedHours: 24,

  leadCoordinator: '',

  prerequisites: [],

  coverImage: null,

  publicationState: 'draft'

});



const prerequisiteOptions = [

  'Healthcare / SOM Medical',

  'CWTS / NSTP Accredited',

  'CSM / Science Majors',

  'First Aid Certified (BLS)',

  'Indigenous Language Fluent',

  'Open to All Iskolar Volunteers'

];



const togglePrerequisite = (item) => {

  if (newEvent.value.prerequisites.includes(item)) {

    newEvent.value.prerequisites =

      newEvent.value.prerequisites.filter(

        (prerequisite) =>

          prerequisite !== item

      );

    return;

  }

  newEvent.value.prerequisites.push(item);

};



const resetNewEvent = () => {

  newEvent.value = {

    title: '',

    category: 'HEALTH',

    description: '',

    startDate: '',

    endDate: '',

    region: 'Davao Region',

    venue: '',

    quota: 40,

    accreditedHours: 24,

    leadCoordinator: '',

    prerequisites: [],

    coverImage: null,

    publicationState: 'draft'

  };

};



const openCreateModal = () => {

  editingEvent.value = null;

  resetNewEvent();

  createModalOpen.value = true;

};



const formatDate = (date) => {

  if (!date) {

    return '';

  }

  const parts = date.split('-');

  return `${parts[1]}/${parts[2]}/${parts[0]}`;

};



const openEditModal = (event) => {

  editingEvent.value = event;

  newEvent.value = {

    title: event.title,

    category: event.category,

    description: event.description,

    startDate: '',

    endDate: '',

    region: event.region,

    venue: event.location,

    quota: event.quota,

    accreditedHours: 24,

    leadCoordinator: event.lead,

    prerequisites: [...event.tags],

    coverImage: null,

    publicationState:

      event.status === 'Drafts'

        ? 'draft'

        : event.status === 'Scheduled'

          ? 'scheduled'

          : 'published'

  };

  createModalOpen.value = true;

};



const closeCreateModal = () => {

  createModalOpen.value = false;

  editingEvent.value = null;

  resetNewEvent();

};




const saveNewEvent = (publicationState) => {

  let eventStatus = 'Drafts';

  let displayStatus = 'DRAFT';

  if (publicationState === 'scheduled') {

    eventStatus = 'Scheduled';

    displayStatus = 'SCHEDULED';

  }

  if (publicationState === 'published') {

    eventStatus = 'Published';

    displayStatus = 'RECRUITING';

  }



  const startDate =

    formatDate(newEvent.value.startDate);

  const endDate =

    formatDate(newEvent.value.endDate);



  let eventDate = 'Date to be announced';



  if (startDate && endDate) {

    eventDate =

      startDate === endDate

        ? startDate

        : `${startDate} - ${endDate}`;

  }



  const event = {

    id: Date.now(),

    title:

      newEvent.value.title ||

      'Untitled Mission',

    category:

      newEvent.value.category,

    date: eventDate,

    location:

      newEvent.value.venue ||

      'Location to be announced',

    region:

      newEvent.value.region,

    description:

      newEvent.value.description ||

      'Mission briefing and deployment details will be provided.',

    image:

      '/images/programs/bloodletting.jpg',

    status: eventStatus,

    displayStatus,

    time: '7:00 pm',

    quota:

      Number(newEvent.value.quota) || 0,

    registered: 0,

    quotaLabel: 'Registered',

    tags:

      [...newEvent.value.prerequisites],

    lead:

      newEvent.value.leadCoordinator ||

      'Pahinungod Coordination Office'

  };



  events.value.push(event);

  closeCreateModal();

};




const saveEditedEvent = () => {

  if (!editingEvent.value) {

    return;

  }



  const index =

    events.value.findIndex(

      (event) =>

        event.id === editingEvent.value.id

    );



  if (index === -1) {

    return;

  }



  const existingEvent =

    events.value[index];



  let eventStatus = 'Drafts';

  let displayStatus = 'DRAFT';



  if (

    newEvent.value.publicationState ===

    'scheduled'

  ) {

    eventStatus = 'Scheduled';

    displayStatus = 'SCHEDULED';

  }



  if (

    newEvent.value.publicationState ===

    'published'

  ) {

    eventStatus = 'Published';

    displayStatus =

      existingEvent.displayStatus ===

      'COMPLETED'

        ? 'COMPLETED'

        : existingEvent.displayStatus ===

          'ONGOING'

            ? 'ONGOING'

            : 'RECRUITING';

  }



  let eventDate =

    existingEvent.date;



  const startDate =

    formatDate(newEvent.value.startDate);

  const endDate =

    formatDate(newEvent.value.endDate);



  if (startDate && endDate) {

    eventDate =

      startDate === endDate

        ? startDate

        : `${startDate} - ${endDate}`;

  }



  events.value[index] = {

    ...existingEvent,

    title:

      newEvent.value.title ||

      existingEvent.title,

    category:

      newEvent.value.category,

    description:

      newEvent.value.description,

    date: eventDate,

    location:

      newEvent.value.venue ||

      existingEvent.location,

    region:

      newEvent.value.region,

    status: eventStatus,

    displayStatus,

    quota:

      Number(newEvent.value.quota) ||

      existingEvent.quota,

    tags:

      [...newEvent.value.prerequisites],

    lead:

      newEvent.value.leadCoordinator ||

      existingEvent.lead

  };



  closeCreateModal();

};




const saveEvent = () => {

  if (editingEvent.value) {

    saveEditedEvent();

    return;

  }



  saveNewEvent(

    newEvent.value.publicationState

  );

};




const deleteModalOpen = ref(false);

const selectedEvent = ref(null);

const deleteConfirmed = ref(false);



const openDeleteModal = (event) => {

  selectedEvent.value = event;

  deleteConfirmed.value = false;

  deleteModalOpen.value = true;

};



const closeDeleteModal = () => {

  deleteModalOpen.value = false;

  selectedEvent.value = null;

  deleteConfirmed.value = false;

};



const deleteEvent = () => {

  if (

    !deleteConfirmed.value ||

    !selectedEvent.value

  ) {

    return;

  }



  events.value =

    events.value.filter(

      (event) =>

        event.id !==

        selectedEvent.value.id

    );



  closeDeleteModal();

};

</script>



<template>

  <div class="admin-page events-page">

    <div class="events-inner">

      <!-- search toolbar -->

      <div class="events-toolbar">



        <!-- search -->

        <div class="events-search">

          <Search :size="18" />

          <input

            v-model="search"

            type="text"

            placeholder="Search missions, locations, or coordinators..."

          />

        </div>



        <!-- region  -->

        <div class="events-region-wrapper">

          <button

            class="events-region"

            @click="

              regionOpen = !regionOpen

            "

          >

            <span>

              {{ region }}

            </span>

            <ChevronDown

              :size="15"

              :class="{

                rotated: regionOpen

              }"

            />

          </button>



          <div

            v-if="regionOpen"

            class="events-region-dropdown"

          >

            <button

              v-for="item in regions"

              :key="item"

              :class="{

                selected:

                  region === item

              }"

              @click="

                selectRegion(item)

              "

            >

              {{ item }}

            </button>

          </div>

        </div>



        <!-- status  -->

        <div class="events-status-tabs">

          <button

            v-for="item in statuses"

            :key="item"

            :class="{

              active:

                status === item

            }"

            @click="

              status = item

            "

          >

            {{ item }}

          </button>

        </div>

      </div>      <!-- category filters -->

      <div class="events-categories">

        <button

          v-for="item in categories"

          :key="item"

          :class="{

            active:

              category === item

          }"

          @click="

            category = item

          "

        >

          {{ item }}

        </button>

      </div>      <!-- event grid -->

      <div class="events-grid">



        <!-- event card  -->

        <article

          v-for="event in filteredEvents"

          :key="event.id"

          class="event-card"

        >



          <!-- image  -->

          <div class="event-image-wrapper">

            <img

              :src="event.image"

              :alt="event.title"

              class="event-image"

            />



            <!-- status  -->

            <span

              class="event-status"

              :class="

                getStatusClass(event)

              "

            >

              <span></span>

              {{ event.displayStatus }}

            </span>



            <!-- time  -->

            <span

              v-if="

                (

                  status === 'Scheduled' ||

                  status === 'Drafts'

                ) &&

                event.time

              "

              class="event-time"

            >

              ◷ {{ event.time }}

            </span>

          </div>



          <!-- content  -->

          <div class="event-content">



            <!-- category  -->

            <span class="event-category">

              {{ event.category }}

            </span>



            <!-- DATE + LOCATION -->

            <div class="event-meta">

              <div>

                <CalendarDays :size="14" />

                <span>

                  {{ event.date }}

                </span>

              </div>



              <div>

                <MapPin :size="14" />

                <span>

                  {{ event.location }}

                </span>

              </div>

            </div>



            <!-- title  -->

            <h2 class="event-title">

              {{ event.title }}

            </h2>



            <!-- description  -->

            <p class="event-description">

              {{ event.description }}

            </p>



            <!-- quota  -->

            <div class="event-quota">

              <div

                class="event-quota-heading"

              >

                <span>

                  Volunteer Quota

                </span>

                <strong>

                  {{ event.registered }}

                  /

                  {{ event.quota }}

                  {{ event.quotaLabel }}

                </strong>

              </div>



              <div class="event-quota-bar">

                <span

                  :style="{

                    width:

                      `${Math.min(

                        (

                          event.registered /

                          event.quota

                        ) * 100,

                        100

                      )}%`

                  }"

                ></span>

              </div>

            </div>



            <!-- tags  -->

            <div class="event-tags">

              <span

                v-for="tag in event.tags"

                :key="tag"

              >

                {{ tag }}

              </span>

            </div>



            <!-- lead  -->

            <div class="event-lead">

              <span>

                Lead:

                {{ event.lead }}

              </span>



              <strong

                :class="{

                  waitlist:

                    event.registered >=

                    event.quota

                }"

              >

                {{

                  event.registered >=

                  event.quota

                    ? 'Waitlist open'

                    : `${event.quota -

                      event.registered}

                      slots left`

                }}

              </strong>

            </div>



            <!-- actions  -->

            <div class="event-actions">



              <!-- draft  -->

              <button

                v-if="

                  event.status === 'Drafts'

                "

                class="event-manage-button draft-button"

                @click="

                  openEditModal(event)

                "

              >

                <Pencil :size="15" />

                Edit Draft

              </button>



              <!-- normal  -->

              <button

                v-else

                class="event-manage-button"

                :class="{

                  disabled:

                    event.registered >=

                    event.quota

                }"

              >

                <UsersRound :size="15" />

                Manage

              </button>



              <!-- edit  -->

              <button

                class="event-edit-button"

                @click="

                  openEditModal(event)

                "

              >

                <Pencil :size="16" />

              </button>



              <!-- delete  -->

              <button

                class="event-delete-button"

                @click="

                  openDeleteModal(event)

                "

              >

                <Trash2 :size="16" />

              </button>

            </div>

          </div>

        </article>      <!-- add new event -->

        <article

          v-if="

            status === 'Drafts'

          "

          class="event-add-card"

        >

          <button

            @click="

              openCreateModal

            "

          >

            <span class="add-event-plus">

              +

            </span>

            ADD NEW EVENT

          </button>

        </article>

      </div>      <!-- create / edit event modal -->

      <div

        v-if="

          createModalOpen

        "

        class="event-modal-backdrop"

        @click.self="

          closeCreateModal

        "

      >

        <div

          class="event-create-modal"

        >



          <!-- header  -->

          <div class="event-modal-header">

            <div

              class="event-modal-title"

            >

              <div

                class="event-modal-icon"

              >

                <Flag :size="20" />

              </div>

              <h2>

                {{

                  editingEvent

                    ? 'Edit Event'

                    : 'Create New Event'

                }}

              </h2>

            </div>



            <button

              class="event-modal-close"

              @click="

                closeCreateModal

              "

            >

              <X :size="20" />

            </button>

          </div>



          <!-- body  -->

          <div

            class="event-modal-body"

          >      <!-- mission briefing -->

            <section

              class="event-form-section"

            >

              <div

                class="event-form-section-title"

              >

                <span>

                  01. MISSION BRIEFING

                </span>

              </div>



              <div

                class="

                  event-form-grid

                  event-form-grid-two

                "

              >



                <!-- mission title  -->

                <div

                  class="event-form-field"

                >

                  <div

                    class="event-form-label-row"

                  >

                    <label>

                      Mission Title

                      <span></span>

                    </label>

                    <small>

                      Max 80 chars

                    </small>

                  </div>



                  <div

                    class="event-input"

                  >

                    <Flag :size="16" />

                    <input

                      v-model="

                        newEvent.title

                      "

                      type="text"

                      maxlength="80"

                      placeholder="e.g. Panihapon sa Balay ni Nas"

                    />

                  </div>

                </div>



                <!-- category  -->

                <div

                  class="event-form-field"

                >

                  <label>

                    Category Track

                    <span></span>

                  </label>



                  <div

                    class="event-input"

                  >

                    <List :size="16" />

                    <select

                      v-model="

                        newEvent.category

                      "

                    >

                      <option

                        value="HEALTH"

                      >

                        Health Outreach

                      </option>

                      <option

                        value="EDUCATION & LITERACY"

                      >

                        Education & Literacy

                      </option>

                      <option

                        value="ENVIRONMENT & ECOLOGY"

                      >

                        Environment & ECOLOGY

                      </option>

                      <option

                        value="NSTP / CWTS"

                      >

                        NSTP / CWTS

                      </option>

                      <option

                        value="INDIGENOUS PEOPLES (IP)"

                      >

                        Indigenous Peoples (IP)

                      </option>

                    </select>

                  </div>

                </div>

              </div>



              <!-- description  -->

              <div

                class="event-form-field"

              >

                <div

                  class="event-form-label-row"

                >

                  <label>

                    Briefing Description &

                    Objectives

                    <span></span>

                  </label>



                  <div

                    class="event-editor-tools"

                  >

                    <Bold :size="14" />

                    <Italic :size="14" />

                    <List :size="14" />

                  </div>

                </div>



                <textarea

                  v-model="

                    newEvent.description

                  "

                  rows="3"

                  placeholder="Specify target communities, logistical assembly instructions, deliverables, and service scopes for deployment..."

                ></textarea>

              </div>

            </section>      <!-- schedule & deployment venue -->

            <section

              class="event-form-section"

            >

              <div

                class="event-form-section-title"

              >

                <span>

                  02. SCHEDULE &

                  DEPLOYMENT VENUE

                </span>

              </div>



              <div

                class="

                  event-form-grid

                  event-form-grid-four

                "

              >



                <!-- start date  -->

                <div

                  class="event-form-field"

                >

                  <label>

                    Start Date

                    <span></span>

                  </label>



                  <div

                    class="event-input"

                  >

                    <CalendarDays

                      :size="16"

                    />

                    <input

                      v-model="

                        newEvent.startDate

                      "

                      type="date"

                    />

                  </div>

                </div>



                <!-- end date  -->

                <div

                  class="event-form-field"

                >

                  <label>

                    End Date

                    <span></span>

                  </label>



                  <div

                    class="event-input"

                  >

                    <CalendarDays

                      :size="16"

                    />

                    <input

                      v-model="

                        newEvent.endDate

                      "

                      type="date"

                    />

                  </div>

                </div>



                <!-- region  -->

                <div

                  class="event-form-field"

                >

                  <label>

                    Administrative Region

                  </label>



                  <div

                    class="event-input"

                  >

                    <Map :size="16" />

                    <select

                      v-model="

                        newEvent.region

                      "

                    >

                      <option

                        v-for="

                          item in regions.filter(

                            (item) =>

                              item !==

                              'All Regions'

                          )

                        "

                        :key="item"

                        :value="item"

                      >

                        {{ item }}

                      </option>

                    </select>

                  </div>

                </div>



                <!-- venue  -->

                <div

                  class="event-form-field"

                >

                  <label>

                    Venue / Focal Point

                    <span></span>

                  </label>



                  <div

                    class="event-input"

                  >

                    <MapPin :size="16" />

                    <input

                      v-model="

                        newEvent.venue

                      "

                      type="text"

                      placeholder="Mugat, Sa balay ni Jay"

                    />

                  </div>

                </div>

              </div>

            </section>      <!-- volunteer metrics & personnel -->

            <section

              class="event-form-section"

            >

              <div

                class="event-form-section-title"

              >

                <span>

                  03. VOLUNTEER METRICS &

                  PERSONNEL

                </span>

              </div>



              <div

                class="

                  event-form-grid

                  event-form-grid-three

                "

              >



                <!-- quota  -->

                <div

                  class="event-form-field"

                >

                  <div

                    class="event-form-label-row"

                  >

                    <label>

                      Volunteer Quota

                    </label>

                    <small>

                      Slots

                    </small>

                  </div>



                  <div

                    class="event-input"

                  >

                    <UsersRound

                      :size="16"

                    />

                    <input

                      v-model="

                        newEvent.quota

                      "

                      type="number"

                      min="1"

                    />

                  </div>

                </div>



                <!-- hours  -->

                <div

                  class="event-form-field"

                >

                  <label>

                    Accredited Hours

                  </label>



                  <div

                    class="event-input"

                  >

                    <Clock3

                      :size="16"

                    />

                    <input

                      v-model="

                        newEvent.accreditedHours

                      "

                      type="number"

                      min="1"

                    />

                  </div>

                </div>



                <!-- lead  -->

                <div

                  class="event-form-field"

                >

                  <label>

                    Assigned Unit /

                    Lead Coordinator

                    <span></span>

                  </label>



                  <div

                    class="event-input"

                  >

                    <UserRound

                      :size="16"

                    />

                    <input

                      v-model="

                        newEvent.leadCoordinator

                      "

                      type="text"

                      placeholder="Office of Health Initiatives - Prof. D. Santiago (CSM)"

                    />

                  </div>

                </div>

              </div>



              <div

                class="event-form-lower-grid"

              >



                <!-- prerequisites  -->

                <div

                  class="event-form-field"

                >

                  <label>

                    Target Volunteer

                    Cohort / Prerequisites

                  </label>



                  <p

                    class="event-form-help"

                  >

                    Eligible constituents will

                    receive automatic priority

                    RSVP invitations.

                  </p>



                  <div

                    class="event-prerequisites"

                  >

                    <button

                      v-for="

                        item in prerequisiteOptions

                      "

                      :key="item"

                      type="button"

                      :class="{

                        selected:

                          newEvent

                            .prerequisites

                            .includes(item)

                      }"

                      @click="

                        togglePrerequisite(item)

                      "

                    >

                      <span

                        class="

                          event-check-box

                        "

                      >

                        ✓

                      </span>

                      {{ item }}

                    </button>

                  </div>

                </div>



                <!-- cover banner  -->

                <div

                  class="event-form-field"

                >

                  <label>

                    Mission Cover Banner

                  </label>



                  <label

                    class="

                      event-upload-box

                    "

                  >

                    <UploadCloud

                      :size="27"

                    />

                    <strong>

                      Drag and drop mission

                      cover photo

                    </strong>

                    <small>

                      PNG, JPG, or WEBP

                      up to 5MB

                      (16:9 ratio recommended)

                    </small>



                    <input

                      type="file"

                      accept="

                        image/png,

                        image/jpeg,

                        image/webp

                      "

                      @change="

                        newEvent.coverImage =

                          $event.target.files[0]

                      "

                    />

                  </label>

                </div>

              </div>

            </section>      <!-- publication state -->

            <div

              class="

                event-publication-state

              "

            >

              <div

                class="

                  event-publication-label

                "

              >

                <SlidersHorizontal

                  :size="17"

                />

                Deployment Publication

                State:

              </div>



              <div

                class="

                  event-publication-options

                "

              >

                <label>

                  <input

                    v-model="

                      newEvent.publicationState

                    "

                    type="radio"

                    value="draft"

                  />

                  Save as Draft

                </label>



                <label>

                  <input

                    v-model="

                      newEvent.publicationState

                    "

                    type="radio"

                    value="scheduled"

                  />

                  Schedule for Later

                </label>



                <label>

                  <input

                    v-model="

                      newEvent.publicationState

                    "

                    type="radio"

                    value="published"

                  />

                  Publish Immediately

                </label>

              </div>

            </div>

          </div>



          <!-- footer  -->

          <div

            class="event-modal-footer"

          >

            <button

              class="

                event-discard-button

              "

              @click="

                closeCreateModal

              "

            >

              Discard

            </button>



            <button

              class="

                event-save-button

              "

              @click="

                editingEvent

                  ? saveEditedEvent()

                  : saveNewEvent('draft')

              "

            >

              {{ editingEvent

                ? 'Save Changes'

                : 'Save Draft'

              }}

            </button>



            <button

              class="

                event-create-button

              "

              @click="saveEvent"

            >

              {{

                editingEvent

                  ? 'Save Changes'

                  : 'Create & Stage Event →'

              }}

            </button>

          </div>

        </div>

      </div>      <!-- delete event modal -->

      <div

        v-if="deleteModalOpen"

        class="

          event-modal-backdrop

        "

        @click.self="

          closeDeleteModal

        "

      >

        <div

          class="event-delete-modal"

        >

          <div

            class="

              event-delete-top-line

            "

          ></div>



          <div

            class="

              event-delete-content

            "

          >

            <div

              class="

                event-delete-heading

              "

            >

              <div

                class="

                  event-delete-icon

                "

              >

                <Trash2 :size="21" />

              </div>



              <div>

                <span

                  class="

                    event-delete-label

                  "

                >

                  DESTRUCTIVE ACTION

                </span>

                <h2>

                  Delete Volunteer Event?

                </h2>

              </div>

            </div>



            <p

              class="

                event-delete-description

              "

            >

              Are you sure you want to

              permanently delete this event?

              This action will immediately

              purge the record from the

              Pahinungod mission ledger and

              cannot be reversed.

            </p>



            <label

              class="

                event-delete-confirm

              "

            >

              <input

                v-model="

                  deleteConfirmed

                "

                type="checkbox"

              />

              <span>

                I understand that this draft

                deployment and its entire

                staging history will be

                irreversibly removed from

                UP Mindanao servers.

              </span>

            </label>

          </div>



          <div

            class="

              event-delete-actions

            "

          >

            <button

              class="

                event-delete-cancel

              "

              @click="

                closeDeleteModal

              "

            >

              Cancel, Keep Event

            </button>



            <button

              class="

                event-delete-permanent

              "

              :disabled="

                !deleteConfirmed

              "

              @click="

                deleteEvent

              "

            >

              <Trash2 :size="16" />

              Delete Event Permanently

            </button>

          </div>

        </div>

      </div>

    </div>

  </div>

</template>



<style>

@import '../../styles/admin.css';

@import '../../styles/admin/events.css';

</style>
