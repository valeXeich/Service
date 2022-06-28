<template>
  <link rel="stylesheet" type="text/css" href="//netdna.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css">
  <hr>
  <div class="container bootstrap snippets bootdey">
    <div class="alert alert-danger mt-2" role="alert" v-if="errors.length">
      <p  class="text-center" v-for="error in errors">{{ error }}</p>
    </div>
    <div class="alert alert-success mt-2" role="alert" v-if="success.length">
      <p  class="text-center" v-for="succ in success">{{ succ }}</p>
    </div>
    <h4 class="text-center">Чтобы изменять расписания выберете день недели</h4>
    <div class="row">
      <div class="col-lg-12">
        <div class="main-box no-header clearfix">
          <div class="main-box-body clearfix">
            <div class="table-responsive">
              <table class="table user-list">
                <thead>
                <tr>
                  <th><span>Specialist</span></th>
                  <th><span>Location</span></th>
                  <th class="text-center"><span>Service</span></th>
                  <th><span>Day of week</span></th>
                  <th>1 Time slot</th>
                  <th>2 Time slot</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="specialist in specialists">
                  <td>
                    <a href="#">{{ specialist.first_name }} {{ specialist.last_name }}</a>
                  </td>
                  <td>
                    {{ specialist.location }}
                  </td>
                  <td class="text-center">
                    {{ specialist.service }}
                  </td>
                  <td>
                    <select v-model="selected[specialist.id]" class="custom-select">
                      <option :key="name" v-for="(value, name) in days" :value="name">{{ value }}</option>
                    </select>
                  </td>
                  <td style="width: 23%;">
                    <form>
                      <input
                          max="22:00"
                          v-if="getTimeSlot(specialist.schedules) != null"
                          id="firstTimeSlotStart"
                          :value="getTimeSlot(specialist.schedules).start"
                          type="time"
                          class="form-control-sm"
                      >
                      <input
                          max="22:00"
                          v-else
                          type="time"
                          class="form-control-sm"
                          id="firstTimeSlotStart"
                      >
                      <input
                          max="23:59"
                          v-if="getTimeSlot(specialist.schedules) != null"
                          id="firstTimeSlotEnd"
                          :value="getTimeSlot(specialist.schedules).end"
                          type="time"
                          class="form-control-sm ml-2"
                      >
                      <input
                          v-else type="time"
                          class="form-control-sm ml-2"
                          id="firstTimeSlotEnd"
                      >
                      <a
                          @click.prevent="updateFirstTimeSlot(specialist.schedules, specialist.id, false)"
                          class="line ml-2"
                          href="#"
                      >
                        Update
                      </a>
                      <a
                          @click.prevent="createSchedule(specialist.id, false)"
                          class="line ml-2"
                          href="#"
                      >
                        Create
                      </a>
                    </form>
                  </td>
                  <td style="width: 28%;">
                    <form>
                      <input
                          v-if="getSecondTimeSlot(specialist.schedules) != null"
                          id="secondTimeSlotStart"
                          :value="getSecondTimeSlot(specialist.schedules).start"
                          type="time"
                          class="form-control-sm"
                      >
                      <input
                          v-else
                          :value="getSecondTimeSlot(specialist.schedules)"
                          id="secondTimeSlotStart"
                          type="time"
                          class="form-control-sm"
                      >
                      <input
                          v-if="getSecondTimeSlot(specialist.schedules) != null"
                          id="secondTimeSlotEnd"
                          :value="getSecondTimeSlot(specialist.schedules).end"
                          type="time"
                          class="form-control-sm ml-2"
                      >
                      <input
                          v-else
                          :value="getSecondTimeSlot(specialist.schedules)"
                          id="secondTimeSlotEnd"
                          type="time"
                          class="form-control-sm ml-2"
                      >
                      <a
                          @click.prevent="updateSecondTimeSlot(specialist.schedules, specialist.id, true)"
                          class="line ml-2"
                          href="#"
                      >
                        Update
                      </a>
                      <a
                          @click.prevent="deleteSchedule(specialist.schedules, specialist.id, true)"
                          class="line ml-2" href="#"
                      >
                        Remove
                      </a>
                      <a
                          @click.prevent="createSchedule(specialist.id, true)"
                          class="line ml-2"
                          href="#"
                      >
                        Create
                      </a>
                    </form>
                  </td>
                </tr>
                </tbody>
              </table>
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
  name: "AdminPanel",
  data() {
    return {
      specialists: [],
      location: [],
      services: [],
      days: {
        'monday': 'Понедельник',
        'tuesday': 'Вторник',
        'wednesday': 'Среда',
        'thursday': 'Четверг',
        'friday': 'Пятница',
        'saturday': 'Суббота',
        'sunday': 'Воскресенье'
      },
      selected: [],
      first_time_slot_start: '',
      first_time_slot_end: '',
      second_time_slot_start: '',
      second_time_slot_end: '',
      errors: [],
      success: [],
    }
  },
  methods: {
    async fetchSpecialists() {
      const response = await axios.get('http://127.0.0.1:8000/api/specialist/list/');
      this.specialists = response.data;
    },
    async getLocationList() {
      const response = await axios.get('http://127.0.0.1:8000/api/location/list/');
      this.location = response.data;
    },
    async getService() {
      const response = await axios.get('http://127.0.0.1:8000/api/service/list/');
      this.services = response.data;
    },
    getScheduleId(schedules, specialist_id, is_second_schedule) {
      for (let schedule of schedules) {
        for (let selecte in this.selected) {
          if (is_second_schedule === true) {
            if (schedule.day_of_week === this.selected[selecte] && specialist_id == schedule.specialist && schedule.is_second_schedule === true) {
              return {'id': schedule.id, 'is_second_schedule': schedule.is_second_schedule, 'parent': schedule.second_schedule}
            }
          } else if (is_second_schedule === false) {
            if (schedule.day_of_week === this.selected[selecte] && specialist_id == schedule.specialist && schedule.is_second_schedule === false) {
              return {'id': schedule.id, 'is_second_schedule': schedule.is_second_schedule}
            }
          }
        }
      }
    },
    getTimeSlot(schedules) {
      if (this.selected.length > 0) {
        for (let schedule of schedules) {
          for (let selecte in this.selected) {
            if (schedule.day_of_week === this.selected[selecte] && schedule.is_second_schedule === false && schedule.specialist == selecte) {
              return {'start': schedule.start_schedule, 'end': schedule.end_schedule}
            }
          }
        }
      }
    },
    getSecondTimeSlot(schedules) {
      if (this.selected.length > 0) {
        for (let schedule of schedules) {
          for (let selecte in this.selected) {
            if (schedule.day_of_week === this.selected[selecte] && schedule.is_second_schedule === true && schedule.specialist == selecte) {
              return {'start': schedule.start_schedule, 'end': schedule.end_schedule}
            }
          }
        }
      }
    },
    async updateFirstTimeSlot(schedules, specialist_id, is_second_schedule) {
      const first_start = document.getElementById('firstTimeSlotStart').value;
      const first_end = document.getElementById('firstTimeSlotEnd').value;
      const scheduleInfo =  this.getScheduleId(schedules, specialist_id, is_second_schedule);
      const formData = {
        start_schedule: first_start,
        end_schedule: first_end
      }
      try {
        await axios.patch(`http://127.0.0.1:8000/api/schedule/update/${scheduleInfo.id}/`, formData);
        this.success.push('was updated');
      } catch (e) {
        this.errors.push('nothing to update');
      }
    },
    async updateSecondTimeSlot(schedules, specialist_id, is_second_schedule) {
      const second_start = document.getElementById('secondTimeSlotStart').value;
      const second_end = document.getElementById('secondTimeSlotEnd').value;
      const scheduleInfo =  this.getScheduleId(schedules, specialist_id, is_second_schedule);
      const formData = {
        start_schedule: second_start,
        end_schedule: second_end
      }
      try {
        await axios.patch(`http://127.0.0.1:8000/api/schedule/update/${scheduleInfo.id}/`, formData);
        this.success.push('was updated');
      } catch (e) {
        this.errors.push('nothing to update');
      }
    },
    async deleteSchedule(schedules, specialist_id, is_second_schedule) {
      const scheduleInfo =  this.getScheduleId(schedules, specialist_id, is_second_schedule);
      try {
        await axios.delete(`http://127.0.0.1:8000/api/schedule/delete/${scheduleInfo.id}`);
        this.success.push('Time slot was delete');
      } catch (e) {
        this.errors.push('nothing to delete');
      }
    },
    async createSchedule(specialist_id, is_second_schedule) {
      if (is_second_schedule) {
        const second_start = document.getElementById('secondTimeSlotStart').value;
        const second_end = document.getElementById('secondTimeSlotEnd').value;
        if (second_start == '' || second_end == '') {
          this.errors.push('Поле пустое либо уже создано');
          const err = Error('Поле пустое либо уже создано');
        }
        const formData = {
          day_of_week: this.selected[specialist_id],
          specialist: specialist_id,
          start_schedule: second_start,
          end_schedule: second_end,
          is_second_schedule: is_second_schedule
        }
        try {
          await axios.post('http://127.0.0.1:8000/api/specialist/schedule/create/', formData);
          this.success.push('Time slot was created');
        } catch (e) {
          this.errors = [];
          this.errors.push(e.response.data.time[0]);
        }
      } else {
        const first_start = document.getElementById('firstTimeSlotStart').value;
        const first_end = document.getElementById('firstTimeSlotEnd').value;
        if (first_start == '' || first_start == '') {
          this.errors.push('Поле пустое либо уже создано');
          const err = Error('Поле пустое либо уже создано');
        }
        const formData = {
          day_of_week: this.selected[specialist_id],
          start_schedule: first_start,
          end_schedule: first_end,
          is_second_schedule: is_second_schedule
        }
        try {
          await axios.post('http://127.0.0.1:8000/api/specialist/schedule/create/', formData);
          this.success.push('Time slot was created');
        } catch (e) {
          this.errors = [];
          this.errors.push(e.response.data.time[0]);
        }
      }
    }
  },
  mounted() {
    this.fetchSpecialists()
    this.getLocationList()
    this.getService()
  },
}
</script>

<style scoped>

.line {
  color: black;
}

.line:hover {
  text-decoration: underline;
}

body{
  background:#eee;
}
.main-box.no-header {
  padding-top: 20px;
}
.main-box {
  background: #FFFFFF;
  -webkit-box-shadow: 1px 1px 2px 0 #CCCCCC;
  -moz-box-shadow: 1px 1px 2px 0 #CCCCCC;
  -o-box-shadow: 1px 1px 2px 0 #CCCCCC;
  -ms-box-shadow: 1px 1px 2px 0 #CCCCCC;
  box-shadow: 1px 1px 2px 0 #CCCCCC;
  margin-bottom: 16px;
  -webikt-border-radius: 3px;
  -moz-border-radius: 3px;
  border-radius: 3px;
}

a {
  color: #3498db;
  outline: none!important;
}
.user-list tbody td>img {
  position: relative;
  max-width: 50px;
  float: left;
  margin-right: 15px;
}

.table thead tr th {
  text-transform: uppercase;
  font-size: 0.875em;
}
.table thead tr th {
  border-bottom: 2px solid #e7ebee;
}
.table tbody tr td:first-child {
  font-size: 1.125em;
  font-weight: 300;
}
.table tbody tr td {
  font-size: 0.875em;
  vertical-align: middle;
  border-top: 1px solid #e7ebee;
  padding: 12px 8px;
}
a:hover{
  text-decoration:none;
}

</style>