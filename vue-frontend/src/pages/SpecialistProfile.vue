<template xmlns="http://www.w3.org/1999/html">
  <div class="container">
    <div class="main-body mt-4">
      <div class="row gutters-sm">
        <div class="col-md-4 mb-3">
          <div class="card">
            <div class="card-body">
              <div class="d-flex flex-column align-items-center text-center">
                <div class="img-holder ml-mr-md-4 mb-md-0 mb-4 mx-auto mx-md-0 d-md-none d-lg-flex">
                  {{ first_name.slice(0, 1) }}{{ last_name.slice(0, 1) }}
                </div>
                <div>
                </div>
                <div class="mt-3">
                  <h4 class="text-center">{{ first_name }} {{ last_name }}</h4>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-8">
          <div class="row">
            <div class="col-md-offset-1 col-md-12">
              <div class="panel">
                <div class="panel-body table-responsive">
                  <template v-if="is_specialist">
                    <h4 class="text-center">Список записанных клиентов</h4>
                    <table class="table">
                      <thead>
                      <tr>
                        <th>Клиент</th>
                        <th>Отрезок</th>
                        <th>Дата</th>
                      </tr>
                      </thead>
                      <tbody>
                      <tr v-for="appointment in appoinments">
                        <td>{{ appointment.client.first_name }} {{ appointment.client.last_name }}</td>
                        <td>
                          {{ appointment.time_slot.start.slice(0, 5) }} - {{ appointment.time_slot.end.slice(0, 5) }}
                        </td>
                        <td>{{ appointment.date }}</td>
                      </tr>
                      </tbody>
                    </table>
                  </template>
                  <h4 v-if="is_specialist" class="text-center indent">Расписание</h4>
                  <h4 v-else class="text-center">Расписание</h4>
                  <table class="table">
                    <thead>
                    <tr>
                      <th>День</th>
                      <th>1 промежуток</th>
                      <th>2 промежуток</th>
                      <th>Удалить</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="schedule in schedules">
                      <template v-if="!schedule.is_second_schedule">
                        <td>{{ schedule.day_of_week }}</td>
                        <td>{{ schedule.start_schedule.slice(0, 5) }} - {{ schedule.end_schedule.slice(0, 5) }}</td>
                        <td v-if="schedule.second_schedule===null">
                          <form @submit.prevent="createSecondSchedule(schedule.day_of_week)">
                            От: <input
                              :min="schedule.end_schedule.slice(0, 5)"
                              max="22:00"
                              class="mr-4 form-control-sm"
                              v-model="second_start_schedule"
                              type="time"
                          >
                            До: <input
                              :min="schedule.end_schedule.slice(0, 5)"
                              max="23:59"
                              class="form-control-sm"
                              v-model="second_end_schedule"
                              type="time"
                          >
                            <button type="submit" class="btn btn-success btn-sm ml-2">+</button>
                          </form>
                        </td>
                        <td v-if="schedule.second_schedule">
                          {{ schedule.second_schedule.start_schedule.slice(0, 5) }} - {{ schedule.second_schedule.end_schedule.slice(0, 5) }}
                        </td>
                        <td>
                          <button @click.prevent="deleteSchedule(schedule.id)" class="btn btn-sm btn-danger ml-2">
                            <i class="fa fa-times"></i>
                          </button>
                        </td>
                      </template>
                    </tr>
                    </tbody>
                  </table>
                  <h4 class="text-center indent">Добавить расписание</h4>
                  <form @submit.prevent="createSchedule" v-if="Object.keys(days).length">
                    <select v-model="day_of_week" class="custom-select">
                      <option disabled value="">Выберите день недели</option>
                      <option v-for="(value, name) in days" :value="name">{{ value }}</option>
                    </select>
                    <div class="text-center mt-2">
                      От: <input
                        max="22:00"
                        class="mr-4 form-control-sm"
                        v-model="start_schedule"
                        type="time"
                    >
                      До: <input
                        :min="start_schedule"
                        max="23:59"
                        class="form-control-sm"
                        v-model="end_schedule"
                        type="time"
                    >
                    </div>
                    <button
                        v-if="!day_of_week || !start_schedule || !end_schedule"
                        disabled
                        class="btn btn-primary" type="submit"
                    >
                      Создать
                    </button>
                    <button v-else class="btn btn-primary" type="submit">Создать</button>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SpecialistProfile",
  data() {
    return {
      days: {
        'monday': 'Понедельник',
        'tuesday': 'Вторник',
        'wednesday': 'Среда',
        'thursday': 'Четверг',
        'friday': 'Пятница',
        'saturday': 'Суббота',
        'sunday': 'Воскресенье'
      },
      second_days: {
        'monday': 'Понедельник',
        'tuesday': 'Вторник',
        'wednesday': 'Среда',
        'thursday': 'Четверг',
        'friday': 'Пятница',
        'saturday': 'Суббота',
        'sunday': 'Воскресенье'
      },
      day_of_week: '',
      start_schedule: '',
      end_schedule: '',
      second_start_schedule: '',
      second_end_schedule: '',
      schedules: [],
      created: false,
      first_name: '',
      last_name: '',
      appoinments: [],
      is_specialist: false
    }
  },
  methods: {
    async getAppointments() {
      const response = await axios.get(
          `http://127.0.0.1:8000/api/specialist/appointment/list/${this.$route.params.slug}/`
      );
      this.appoinments = response.data;
    },
    async deleteSchedule(schedule_id) {
      await axios.delete(`http://127.0.0.1:8000/api/schedule/delete/${schedule_id}`);
      this.created = true;
    },
    async createSchedule() {
      const formData = {
        day_of_week: this.day_of_week,
        start_schedule: this.start_schedule,
        end_schedule: this.end_schedule
      }
      await axios.post('http://127.0.0.1:8000/api/specialist/schedule/create/', formData);
      this.created = true;
      this.start_schedule = '';
      this.end_schedule = '';
    },
    async specialistInfo() {
      const response = await axios.get(`http://127.0.0.1:8000/api/user/info/${this.$route.params.slug}/`);
      this.first_name = response.data.first_name;
      this.last_name = response.data.last_name;
    },
    async userInfo() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/auth/users/me/');
        if (response.data.status == 'specialist') {
          this.is_specialist = true;
          await this.this.getAppointments();
        }
      } catch (e) {
        console.log('error');
      }
    },
    async createSecondSchedule(day) {
      const eng_day = this.getObjectKey(this.second_days, day);
      const formData = {
        day_of_week: eng_day,
        start_schedule: this.second_start_schedule,
        end_schedule: this.second_end_schedule
      }
      await axios.post('http://127.0.0.1:8000/api/specialist/schedule/create/', formData);
      this.start_schedule = '';
      this.end_schedule = '';
      this.created = true;
    },
    async getSchedule() {
      const response = await axios.get(
          `http://127.0.0.1:8000/api/specialist/schedule/list/${this.$route.params.slug}/`
      );
      this.schedules = response.data;
      for (let schedule of this.schedules) {
        let key = this.getObjectKey(this.days, schedule.day_of_week)
        if (key) {
          delete this.days[key];
        }
      }
      this.created = false;
    },
    getObjectKey(obj, value) {
      return Object.keys(obj).find(key => obj[key] === value);
    }
  },
  mounted() {
    this.specialistInfo()
    this.userInfo()
  },
  watch: {
    'created': {
      handler: 'getSchedule',
      immediate: true
    }
  }
}
</script>

<style scoped>

.indent {
  margin-top: 50px;
}

.img-holder {
  height: 90px;
  width: 90px;
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

.container { position: relative; }

.panel{
  font-family: 'Raleway', sans-serif;
  padding: 0;
  border: none;
  box-shadow: 0 0 10px rgba(0,0,0,0.08);
}

.panel .panel-heading .form-horizontal label{
  color: #fff;
  margin-right: 10px;
}

.panel .panel-body{
  padding: 0;
  border-radius: 0;
}
.panel .panel-body .table thead tr th{
  color: #fff;
  background: #8D8D8D;
  font-size: 17px;
  font-weight: 700;
  padding: 12px;
  border-bottom: none;
}
.panel .panel-body .table thead tr th:nth-of-type(1){ width: 120px; }
.panel .panel-body .table thead tr th:nth-of-type(3){ width: 50%; }
.panel .panel-body .table tbody tr td{
  color: #555;
  background: #fff;
  font-size: 15px;
  font-weight: 500;
  padding: 13px;
  vertical-align: middle;
  border-color: #e7e7e7;
}
.panel .panel-body .table tbody tr:nth-child(odd) td{ background: #f5f5f5; }
.panel .panel-body .table tbody .action-list li{ display: inline-block; }
.panel .panel-body .table tbody .action-list li a{
  color: #fff;
  font-size: 13px;
  line-height: 28px;
  height: 28px;
  width: 33px;
  padding: 0;
  border-radius: 0;
  transition: all 0.3s ease 0s;
}
.panel .panel-body .table tbody .action-list li a:hover{ box-shadow: 0 0 5px #ddd; }
</style>