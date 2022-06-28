import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: false,
    token: '',
    client: false,
    admin: false
  },
  getters: {
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('token')) {
        state.token = localStorage.getItem('token')
        state.isAuthenticated = true
      } else {
        state.token = ''
        state.isAuthenticated = false
      }
      if (localStorage.getItem('client')) {
        state.client = true
      }
      if (localStorage.getItem('admin')) {
        state.admin =true
      }
    },
  },
  actions: {
  },
  modules: {
  }
})
