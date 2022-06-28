<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
    <button class="navbar-toggler" type="button" data-toggle="collapse"
            data-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
          <a href="/" class="nav-link">Главная</a>
        </li>
      </ul>
      <form class="form-inline my-2 my-lg-0">
        <input type="text" class="form-control mr-sm-2" placeholder="Поиск" aria-label="Поиск">
        <button class="btn btn-outline-success my-2 my-sm-0 mr-2" type="submit">Поиск</button>
      </form>
      <router-link v-if="!isAuthenticated" :to='`/login`' class="btn btn-outline-light mr-2">Вход</router-link>
      <router-link v-if="!isAuthenticated" :to='`/sign-up`' class="btn btn-outline-light mr-2">Регистрация</router-link>
      <router-link :to="`/client`" v-if="isAuthenticated && status==='client'" class="navbar-text mr-2">Профиль</router-link>
      <router-link :to="`/specialist/${slug}`" v-if="isAuthenticated && status==='specialist'" class="navbar-text mr-2">Профиль</router-link>
      <router-link v-if="isAdmin" to="/admin">Admin panel</router-link>
      <button v-if="isAuthenticated" @click.prevent="logout" class="btn btn-outline-light">Выход</button>
    </div>
  </nav>
</template>

<script>
import axios from "axios";
export default {
  name: "my-header",
  data() {
    return {
      isAuthenticated: this.$store.state.isAuthenticated,
      slug: '',
      status: '',
      isAdmin: this.$store.state.admin
    }
  },
  methods: {
    async logout() {
      await axios.post('http://127.0.0.1:8000/auth/token/logout/');
      localStorage.removeItem('token');
      localStorage.removeItem('client');
      localStorage.removeItem('admin');
      window.location.href = "/";
    },
    async userInfo() {
      const response = await axios.get('http://127.0.0.1:8000/auth/users/me/');
      this.slug = response.data.slug;
      this.status = response.data.status;
    }
  },
  mounted() {
    if (localStorage.getItem('token')) {
      this.userInfo();
    }
  },
}
</script>

<style scoped>

</style>