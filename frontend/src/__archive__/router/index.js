import { createRouter, createWebHistory } from 'vue-router';
import useUserStore from '@/store/user';
import Swal from 'sweetalert2';

import Landing from '../landing_project/Landing.vue';
import Login from '../landing_project/auth/Login.vue';
import Register from '../landing_project/auth/Register.vue';
import ForgotPassword from '../landing_project/auth/ForgotPassword.vue';
import NotFound from '../landing_project/pages/NotFound.vue';
import TermsOfUse from '../landing_project/pages/TermsOfUse.vue';
import PrivacyPolicy from '../landing_project/pages/PrivacyPolicy.vue';
import Supports from '../landing_project/pages/Supports.vue';
//import FAQs from '../landing_project/pages/FAQs.vue';
//import Contact from '../landing_project/pages/Contact.vue';
//import Blogs from '../landing_project/pages/Blogs.vue';
//import BlogDetail from '../landing_project/pages/BlogDetail.vue';
//import Careers from '../landing_project/pages/Careers.vue';
//import Portfolios from '../landing_project/pages/Portfolios.vue';

import DashboardContent from '../dashboard_project/views/Home/DashboardContent.vue';
import Profile from '../dashboard_project/views/DropMenu/Profile.vue';
import Orders from '../dashboard_project/views/DropMenu/Orders.vue';
import LearningPath from '../dashboard_project/contents/LearningPath/LearningPath.vue';
import Subscription from '../dashboard_project/contents/Langganan/Langganan.vue';
import Program from '../dashboard_project/contents/Program/Program.vue';;
import Impact from '../dashboard_project/contents/Capaian/Capaian.vue';
import Reward from '../dashboard_project/contents/Reward/Reward.vue';

const routes = [
  { path: '/', name: 'Landing', component: Landing },
  { path: '/login', name: 'Login', component: Login, meta: { layout: 'landing' } },
  { path: '/register', name: 'Register', component: Register },
  { path: '/forgot-password', name: 'ForgotPassword', component: ForgotPassword },
  { path: '/terms', name: 'TermsOfUse', component: TermsOfUse },
  { path: '/privacy', name: 'PrivacyPolicy', component: PrivacyPolicy },
  { path: '/supports', name: 'Supports', component: Supports },
  //{ path: '/faqs', name: 'FAQs', component: FAQs },
 // { path: '/contact', name: 'Contact', component: Contact },
  //{ path: '/blogs', name: 'Blogs', component: Blogs },
 // { path: '/careers', name: 'Careers', component: Careers },
 // { path: '/portfolios', name: 'Portfolios', component: Portfolios },
//  { path: '/blogs/:id', name: 'BlogDetail', component: BlogDetail },

  {
    path: '/dashboard',
    meta: { layout: 'dashboard' },
    children: [
      { path: '', name: 'DashboardHome', component: DashboardContent },
      { path: 'academy/progress', name: 'AcademyProgress', component: () => import('@/dashboard_project/views/academy/progress/Progress.vue') },
      { path: 'academy/subscription', name: 'AcademySubscription', component: () => import('@/dashboard_project/views/academy/Langganan/Subscription.vue') },
      { path: 'challenge/followed', name: 'ChallengeFollowed', component: () => import('@/dashboard_project/views/challenge/ChallengeContent/Followed.vue') },
      { path: 'challenge/myapps', name: 'ChallengeMyApps', component: () => import('@/dashboard_project/views/challenge/Aplikasi/MyApps.vue') },
      { path: 'challenge/referral', name: 'ChallengeReferral', component: () => import('@/dashboard_project/views/challenge/Referral/Referral.vue') },
      { path: 'event/registered', name: 'EventRegistered', component: () => import('@/dashboard_project/views/event/Registered.vue') },
      { path: 'event/history', name: 'EventHistory', component: () => import('@/dashboard_project/views/event/History.vue') },
      { path: 'job/applications', name: 'JobApplications', component: () => import('@/dashboard_project/views/job/Lamaran/MyApplications.vue') },
      { path: 'job/manage', name: 'JobManage', component: () => import('@/dashboard_project/views/job/Manage/ManageJobs.vue') },
    ]
  },
  { path: '/profile', name: 'Profile', component: Profile, meta: { layout: 'content' } },
  { path: '/orders', name: 'Orders', component: Orders, meta: { layout: 'content' } },
  {
    path: '/settings', meta: { layout: 'content' }, children: [
      { path: 'profile', name: 'SettingsProfile', component: () => import('@/dashboard_project/views/settings/Profile/Profile.vue') },
      { path: 'personal', name: 'SettingsPersonal', component: () => import('@/dashboard_project/views/settings/Personal/Personal.vue') },
      { path: 'portfolio', name: 'SettingsPortfolio', component: () => import('@/dashboard_project/views/settings/Portfolio/Portfolio.vue') },
      { path: 'account', name: 'SettingsAccount', component: () => import('@/dashboard_project/views/settings/Account/Account.vue') },
      { path: 'academy', name: 'SettingsAcademy', component: () => import('@/dashboard_project/views/settings/Academy/Academy.vue') },
      { path: 'subscription-email', name: 'SettingsSubscriptionEmail', component: () => import('@/dashboard_project/views/settings/Subscript/SubscriptionEmail.vue') }
    ]
  },
  {
    path: '/learning',
    component: () => import('../dashboard_project/contents/LearningPath/LearningPath.vue'),
    meta: { layout: 'content' },
    children: [
      {
        path: '',
        name: 'LearningPlaceholder',
        component: () => import('@/dashboard_project/contents/LearningPath/Placeholder.vue')
      },
      {
        path: ':slug',
        name: 'DetailKelas',
        component: () => import('../dashboard_project/contents/LearningPath/DetailKelas.vue')
      },

      {
        path: ':slug/materi/:id',
        name: 'MateriDetail',
        component: () => import('../dashboard_project/contents/LearningPath/MateriDetail.vue'),
        meta: { hideNavbar: true } 
      },
      
    ]
  },

  {
    path: '/subscription',
    component: () => import('@/dashboard_project/contents/Langganan/Langganan.vue'),
    meta: { layout: 'content' },
    children: [
      {
        path: '',
        name: 'SubscriptionHome',
        component: () => import('@/dashboard_project/contents/Langganan/Langganan.vue') // atau bisa pakai Placeholder kalau tidak ingin rekursif
      },
      {
        path: 'pembayaran',
        name: 'SubscriptionPembayaran',
        component: () => import('@/dashboard_project/contents/Langganan/Pembayaran.vue'),
      }
    ]
  },
  
  
  { path: '/program', name: 'Program', component: Program, meta: { layout: 'content' } },
  { path: '/impact', name: 'Impact', component: Impact, meta: { layout: 'content' } },
  { path: '/rewards', name: 'Rewards', component: Reward, meta: { layout: 'content' } },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
  
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach(async (to, from, next) => {
  const store = useUserStore();
  const isProtectedRoute =
    to.path.startsWith('/dashboard') ||
    ['/profile', '/orders', '/learningpath', '/subscription', '/program', '/impact', '/rewards'].includes(to.path) ||
    to.path.startsWith('/settings');

  const isPublicPage =
    ['/', '/login', '/register', '/forgot-password', '/terms', '/privacy', '/supports', '/faqs', '/contact', '/blogs', '/careers', '/portfolios'].includes(to.path) ||
    to.path.startsWith('/blogs/');

  if (isProtectedRoute) {
    try {
      if (!store.user) {
        await store.fetchUser();
      }
      if (!store.user) {
        return next({ name: 'Landing' });
      }
    } catch (error) {
      return next({ name: 'Landing' });
    }
  }

  if (store.user && isPublicPage) {
    const result = await Swal.fire({
      title: 'Access Public Pages',
      text: 'If you access this page, you will be automatically logged out. Continue?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Continue',
      cancelButtonText: 'Cancelled'
    });

    if (result.isConfirmed) {
      await store.logout(true);
      return next(to.fullPath);
    } else {
      return next(false);
    }
  }

  next();
});

export default router;
