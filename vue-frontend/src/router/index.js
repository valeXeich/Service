
import {createRouter, createWebHistory} from "vue-router";
import store from "@/store";
import Index from "@/pages/Index";
import Login from "@/pages/Login";
import SignUp from "@/pages/SignUp";
import SpecialistProfile from "@/pages/SpecialistProfile";
import ClientProfile from "@/pages/ClientProfile";
import AdminPanel from "@/pages/AdminPanel";


const routes = [
    {
        path: '/',
        component: Index
    },
    {
        path: '/login',
        component: Login
    },
    {
        path: '/sign-up',
        component: SignUp
    },
    {
        path: '/specialist/:slug',
        component: SpecialistProfile
    },
    {
        path: '/client',
        component: ClientProfile,
        beforeEnter: (to, from, next) => {
            console.log(store.state.client)
                if(store.state.client === false) {
                    console.log('Вы не клиент')
                    next(false);
                } else {
                    next();
                }
            }
    },
    {
        path: '/admin',
        component: AdminPanel,
        beforeEnter: (to, from, next) => {
            console.log(store.state.client)
                if(store.state.admin === false) {
                    console.log('Вы не admin')
                    next(false);
                } else {
                    next();
                }
            }
    },
]

const router = createRouter({
    routes,
    history: createWebHistory(process.env.BASE_URL)
})

export default router;