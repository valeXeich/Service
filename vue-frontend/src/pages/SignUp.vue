<template>
  <div class="text-center">
    <form @submit.prevent="submitForm" class="form-signin">
      <h1 class="h3 mb-3 mt-3 font-weight-normal">Для регистрации укажите имя пользователя и пароль</h1>
      <input pattern="[a-Za-z]" id="inputUsername" class="form-control" placeholder="Логин" required="" v-model="username">
      <input id="inputfirsName" class="form-control mt-2" placeholder="Имя" required="" v-model="first_name">
      <input id="inputlastName" class="form-control mt-2" placeholder="Фамилия" required="" v-model="last_name">
      <select v-model="status" class="custom-select mt-2">
        <option selected value="client">Клиент</option>
        <option value="specialist">Специалист</option>
      </select>
      <div v-if="status==='specialist'">
        <label>Укажите вашу услугу, её длительность и место проведения этой услуги</label>
        <input v-model="service" class="form-control" placeholder="Название вашей услуги">
        <input v-model="service_time" type="time" class="form-control mt-2" >
        <input v-model="street" class="form-control mt-2" placeholder="Улица">
      </div>
      <input type="password" id="inputPassword" class="form-control mt-2" placeholder="Пароль" required="" v-model="password">
      <input type="password" id="ReInputPassword" class="form-control mt-2" placeholder="Повторите пароль" required="" v-model="password2">
      <button class="btn mt-2 btn-lg btn-primary btn-block" type="submit">Регистрация</button>
    </form>
    <div class="alert alert-danger mt-2" role="alert" v-if="errors.length">
      <p v-for="error in errors" :key="error">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "SignUp",
  data() {
    return {
      username: '',
      password: '',
      password2: '',
      status: 'client',
      first_name: '',
      last_name: '',
      errors: [],
      success: '',
      service: '',
      service_time: '',
      street: ''
    }
  },
  methods: {
    async submitForm() {
      let formData = {
        username: this.username,
        password: this.password,
        status: this.status,
        first_name: this.first_name,
        last_name: this.last_name,
        service_title: this.service,
        service_time: this.service_time,
        location: this.street
      }
      await axios.post('http://127.0.0.1:8000/auth/users/', formData);
      await this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.form-signin {
  margin-left: 700px;
  margin-right: 700px;
}

.alert {
  margin-left: 700px;
  margin-right: 700px;
}
</style>