<template>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/material-design-iconic-font/2.2.0/css/material-design-iconic-font.min.css" integrity="sha256-3sPp8BkKUE7QyPSl6VfBByBroQbKxKG7tsusY2mhbVY=" crossorigin="anonymous" />
  <div class="container">
    <div class="row">
      <div class="col-lg-10 mx-auto">
        <div class="career-search mb-60">
          <form action="#" class="career-form mb-60">
            <div class="col-md-6 col-lg-3 my-3">
              <div class="select-container">
                <select v-model="selected" class="custom-select">
                  <option value="">Все</option>
                  <option v-for="service in services" :value="service.id">{{ service.title }}</option>
                </select>
              </div>
            </div>
          </form>
          <div class="filter-result">
            <div v-for="specialist in specialists" :key="specialist.id" class="job-box d-md-flex align-items-center justify-content-between mb-30">
              <div class="job-left my-4 d-md-flex align-items-center flex-wrap">
                <div class="img-holder mr-md-4 mb-md-0 mb-4 mx-auto mx-md-0 d-md-none d-lg-flex">
                  {{ specialist.user.first_name.slice(0, 1) }}{{ specialist.user.last_name.slice(0, 1) }}
                </div>
                <div class="job-content">
                  <h5 class="text-center text-md-left"><router-link :to="`/specialist/${specialist.user.slug}`">{{ specialist.user.first_name }} {{ specialist.user.last_name }}</router-link></h5>
                  <ul class="d-md-flex flex-wrap text-capitalize ff-open-sans">
                    <li class="mr-md-4">
                      <i class="bi bi-geo-alt-fill"></i> {{ specialist.location }}
                    </li>
                    <li class="mr-md-4">
                      <i class="bi bi-person-fill"></i> {{ specialist.service }}
                    </li>
                  </ul>
                </div>
              </div>
              <div class="job-right my-4 flex-shrink-0">
                <button @click="getFreeDates(specialist.id)" class="btn d-block w-100 d-sm-inline-block btn-light">Записаться</button>
              </div>
            </div>
            <ModalWindow :show="show">
              <form @submit.prevent="registerToSpecialist" class="text-center">
                <label for="inputGroupSelect05">Выберите дату</label>
                <select v-model="current_date" class="custom-select" id="inputGroupSelect05" aria-label="Example select with button addon">
                  <option v-for="(value, name, index) in date" :value="[value, name]">{{ name }}</option>
                </select>
                <template v-if="current_date !== ''">
                  <label class="mt-3" for="inputGroupSelect04">Выберите промежуток</label>
                  <select v-model="time_slot" class="custom-select" id="inputGroupSelect04" aria-label="Example select with button addon">
                    <option v-for="time_slot in current_date[0]" :value="time_slot.id">{{ time_slot.start }} - {{ time_slot.end }}</option>
                  </select>
                </template>
                <button class="btn btn-primary float-right mt-2" type="submit">Register</button>
                <button @click="show=false; specialist_id=''" class="btn btn-danger float-left mt-2">Close</button>
              </form>
            </ModalWindow>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ModalWindow from "@/components/ModalWindow";
import axios from 'axios'
export default {
  components: {
    ModalWindow
  },
  name: 'Index',
  data() {
    return {
      specialists: [],
      date: [],
      show: false,
      current_date: '',
      specialist_id: '',
      time_slot: '',
      services: [],
      selected: ''
    }
  },
  methods: {
    async fetchSpecialists() {
      if (this.selected) {
        const response = await axios.get(`http://127.0.0.1:8000/api/specialist/list/?service=${this.selected}`);
        this.specialists = response.data;
      } else {
        const response = await axios.get('http://127.0.0.1:8000/api/specialist/list/');
        this.specialists = response.data;
      }
    },
    async getFreeDates(specialist_id) {
      this.show = true;
      const response = await axios.get(`http://127.0.0.1:8000/api/date-work/${specialist_id}/`);
      this.date = response.data;
      this.specialist_id = specialist_id;
    },
    async registerToSpecialist() {
      const formData = {
        date: this.current_date[1],
        time_slot: this.time_slot,
        specialist: this.specialist_id
      }
      await axios.post('http://127.0.0.1:8000/api/create/', formData);
      this.show = false;
    },
    async getServiceList() {
      const response = await axios.get('http://127.0.0.1:8000/api/service/list/');
      this.services = response.data;
    }
  },
  mounted() {
    this.fetchSpecialists()
    this.getServiceList()
  },
  watch: {
    'selected': {
      handler: 'fetchSpecialists',
      immediate: true
    }
  }
}
</script>

<style scoped>
body{
  background:#f5f5f5;
  margin-top:20px;}

.filter-result .job-box {
  -webkit-box-shadow: 0 0 35px 0 rgba(130, 130, 130, 0.2);
  box-shadow: 0 0 35px 0 rgba(130, 130, 130, 0.23);
  border-radius: 10px;
  padding: 10px 35px;
}

ul {
  list-style: none;
}

.list-disk li {
  list-style: none;
  margin-bottom: 12px;
}

.list-disk li:last-child {
  margin-bottom: 0;
}

.job-box .img-holder {
  height: 65px;
  width: 65px;
  background-color: #4e63d7;
  background-image: -webkit-gradient(linear, left top, right top, from(rgba(78, 99, 215, 0.9)), to(#5a85dd));
  background-image: linear-gradient(to right, rgba(78, 99, 215, 0.9) 0%, #5a85dd 100%);
  font-family: "Open Sans", sans-serif;
  color: #fff;
  font-size: 22px;
  font-weight: 700;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-pack: center;
  -ms-flex-pack: center;
  justify-content: center;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  border-radius: 65px;
}

.job-overview .job-detail ul {
  margin-bottom: 28px;
}

.job-overview .job-detail ul li {
  opacity: 0.75;
  font-weight: 600;
  margin-bottom: 15px;
}

.job-overview .job-detail ul li i {
  font-size: 20px;
  position: relative;
  top: 1px;
}

.job-content ul li {
  font-weight: 600;
  opacity: 0.75;
  border-bottom: 1px solid #ccc;
  padding: 10px 5px;
}

@media (min-width: 768px) {
  .job-content ul li {
    border-bottom: 0;
    padding: 0;
  }
}

.job-content ul li i {
  font-size: 20px;
  position: relative;
  top: 1px;
}
.mb-30 {
  margin-bottom: 30px;
}
</style>