<template>
  <div>
    <div class="text-center">
      <form class="form-signin" @submit.prevent="submitForm">
        <h1 class="h3 mb-3 mt-3 font-weight-normal">Пожалуйста укажите логин и пароль</h1>
        <input id="inputUsername" class="form-control" placeholder="Логин" required="" v-model="login">
        <input type="password" id="inputPassword" class="form-control mt-2" placeholder="Пароль" required="" v-model="password">
        <button class="btn mt-2 btn-lg btn-primary btn-block" type="submit">Войти</button>
      </form>
      <div class="alert alert-danger mt-2" role="alert" v-if="errors.length">
        <p v-for="error in errors" :key="error">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Login",
  data() {
    return {
      login: '',
      password: '',
      errors: []
    }
  },
  methods: {
    async submitForm() {
      const formData = {
        username: this.login,
        password: this.password
      }
      try {
        const response = await axios.post('http://127.0.0.1:8000/auth/token/login/', formData);
        const token = response.data.auth_token;
        localStorage.setItem('token', token);
        axios.defaults.headers.common['Authorization'] = 'Token ' + token;
        await this.getUserInfo();
        window.location.href = "/";
      } catch (e) {
        this.errors.push('Введены некорректные данные');
        this.login = '';
        this.password = '';
      }
    },
    async getUserInfo() {
      const response = await axios.get('http://127.0.0.1:8000/auth/users/me/');
      if (response.data.status === 'client') {
        localStorage.setItem('client', 'client');
      }
      if (response.data.is_staff === true) {
        localStorage.setItem('admin', 'admin');
      }
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