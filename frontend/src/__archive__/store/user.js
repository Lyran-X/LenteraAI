import { defineStore } from 'pinia';
import axiosClient from '@/axios';
import router from '@/router/index.ts';
import Swal from 'sweetalert2';

const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
  }),

  actions: {
    async fetchUser() {
      try {
        const { data } = await axiosClient.get('/api/user');
        this.user = data;
      } catch (error) {
        this.user = null;
        throw error;
      }
    },

    async logout(showAlert = false) {
      try {
        await axiosClient.post('/logout');
      } catch (error) {
        console.warn('Logout error, Continue deleting local data.');
      } finally {
        this.user = null;
        localStorage.removeItem('user');
        localStorage.removeItem('token');

        if (showAlert) {
          Swal.fire({
            icon: 'info',
            title: 'You are out',
            text: 'Access to this page is not allowed while logged in.',
            timer: 1500,
            showConfirmButton: false,
          });
        }

        router.push({ name: 'Landing' });
      }
    },

    setUser(userData) {
      this.user = userData;
    },
  },
});

export default useUserStore;
