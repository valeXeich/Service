<template>
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
                  <table class="table">
                    <thead>
                    <tr>
                      <th>Специалист</th>
                      <th>Услуга</th>
                      <th>Дата</th>
                      <th>Время</th>
                    </tr>
                    </thead>
                    <tbody v-if="appointments.length">
                    <tr v-for="appointment in appointments">
                      <td>
                        {{ appointment.specialist.first_name }} {{ appointment.specialist.last_name }}
                      </td>
                      <td>{{ appointment.specialist.service }}</td>
                      <td>{{ appointment.date }}</td>
                      <td>
                        {{ appointment.time_slot.start }} - {{ appointment.time_slot.end }}
                      </td>
                    </tr>
                    </tbody>
                  </table>
                  <h4 v-if="!appointments.length" class="text-center">Список постов пуст</h4>
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
  name: "ClientProfile",
  data() {
    return {
      appointments: [],
      total: [],
      next: [],
      previous: [],
      current_page: 0,
      check: null,
      first_name: '',
      last_name: ''
    }
  },
  methods: {
    async appointmentList() {
      const response = await axios.get('http://127.0.0.1:8000/api/client/appointment/list/');
      this.appointments = response.data;
    },
    async userInfo() {
      const response = await axios.get('http://127.0.0.1:8000/auth/users/me/');
      this.first_name = response.data.first_name;
      this.last_name = response.data.last_name;
      await this.appointmentList();
    }
  },
  mounted() {
    this.userInfo()
  }
}
</script>

<style scoped>
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
.panel .panel-body .table tbody .action-list{
  padding: 0;
  margin: 0;
  list-style: none;
}
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