import Vue from 'vue'
import Router from 'vue-router'
import PostList from '@/components/PostList'
import PostReader from '@/components/PostReader'
import PostWriter from '@/components/PostWriter'
import UserCreate from '@/components/UserCreate'
import UserLogin from '@/components/UserLogin'

Vue.use(Router)

export default new Router({
  mode: 'history',
  linkActiveClass: 'open active',
  scrollBehavior: () => ({ y: 0 }),
  routes: [
    {
      path: '/',
      name: 'PostList',
      component: PostList,
      meta: {
        label: 'Posts'
      }
    },
    {
      path: '/tags/:tags',
      name: 'PostListByTags',
      label: 'Posts',
      component: PostList,
      meta: {
        label: 'Posts'
      }
    },
    {
      path: '/write/:id?',
      name: 'PostWriter',
      component: PostWriter,
      meta: {
        label: 'Write'
      }
    },
    {
      path: '/read/:slug',
      name: 'PostReader',
      component: PostReader,
      meta: {
        label: 'Read'
      }
    },
    {
      path: '/register',
      name: 'UserCreate',
      component: UserCreate,
      meta: {
        label: 'Create User'
      }
    },
    {
      path: '/login',
      name: 'UserLogin',
      component: UserLogin,
      meta: {
        label: 'Login'
      }
    },
    // Compatibility redirect for my old Django blog permalinks
    {
      path: '/:year(\\d{4})/:month([a-z]{3})/:day(\\w{1,2})/:slug',
      redirect: to => {
        return {name: 'PostReader', params: {slug: to.params.slug}}
      }
    }
  ]
})
