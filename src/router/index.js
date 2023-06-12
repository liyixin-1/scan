import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/* Router Modules */
import chartsRouter from './modules/charts'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    noCache: true                if set true, the page will no be cached(default is false)
    affix: true                  if set true, the tag will affix in the tags-view
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path(.*)',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/auth-redirect',
    component: () => import('@/views/login/auth-redirect'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        component: () => import('@/views/dashboard/index'),
        name: 'Dashboard',
        meta: { title: '首页', icon: 'dashboard', affix: true }
      }
    ]
  },
  {
    path: '/guide',
    component: Layout,
    redirect: '/guide/index',
    children: [
      {
        path: 'index',
        component: () => import('@/views/guide/index'),
        name: '引导',
        meta: { title: '引导', icon: 'guide', noCache: true }
      }
    ]
  },
  {
    path: '/404',
    component: () => import('@/views/error-page/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/error-page/401'),
    hidden: true
  }
]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  {
    path: '/newpasswd',
    component: Layout,
    children: [
      {
        path: 'index',
        name: '修改密码',
        component: () => import('@/views/newpasswd/index'),
        meta: { title: '密码修改', icon: 'form', roles: ['admin', 'editor'] }
      }
    ]
  },
  {
    path: '/port',
    component: Layout,
    children: [
      {
        path: 'index',
        name: '端口扫描',
        component: () => import('@/views/port/index'),
        meta: { title: '端口扫描', icon: 'form', roles: ['admin', 'editor'] }
      }
    ]
  },
  {
    path: '/ping',
    component: Layout,
    children: [
      {
        path: 'newtask',
        name: 'newtask',
        component: () => import('@/views/ping/index'),
        meta: { title: '主机存活扫描', icon: 'table', roles: ['admin', 'editor'] }
      }
    ]
  },
  {
    path: '/domain',
    component: Layout,
    children: [
      {
        path: 'task',
        name: 'task',
        component: () => import('@/views/domain/index'),
        meta: { title: '子目录爆破', icon: 'table', roles: ['admin', 'editor'] }
      }
    ]
  },
  {
    path: '/attack',
    component: Layout,
    redirect: '/attack',
    name: 'attack',
    meta: { title: '泛洪攻击', icon: 'el-icon-s-help', roles: ['admin', 'editor'] },
    children: [
      {
        path: 'syn',
        name: 'syn',
        component: () => import('@/views/attack/syn/index'),
        meta: { title: 'SYN攻击', icon: 'table', roles: ['admin', 'editor'] }
      },
      {
        path: 'fin',
        name: 'fin',
        component: () => import('@/views/attack/fin/index'),
        meta: { title: 'FIN攻击', icon: 'table', roles: ['admin', 'editor'] }
      },
      {
        path: 'mac',
        name: 'mac',
        component: () => import('@/views/attack/mac/index'),
        meta: { title: 'MAC攻击', icon: 'table', roles: ['admin', 'editor'] }
      },
      {
        path: 'icmp',
        name: 'icmp',
        component: () => import('@/views/attack/icmp/index'),
        meta: { title: 'ICMP攻击', icon: 'table', roles: ['admin', 'editor'] }
      }
    ]
  },
  {
    path: '/user',
    component: Layout,
    children: [
      {
        path: 'usermanage',
        name: '登录用户管理',
        component: () => import('@/views/user/index'),
        meta: { title: '登录用户管理', icon: 'table', roles: ['admin'] }
      }
    ]
  },

  /** when your routing map is too long, you can split it into small modules **/
  // chartsRouter,

  /*{
    path: '/excel',
    component: Layout,
    redirect: '/excel/export-excel',
    name: 'Excel',
    meta: {
      title: 'Excel',
      icon: 'excel'
    },
    children: [
      {
        path: 'export-excel',
        component: () => import('@/views/excel/export-excel'),
        name: 'ExportExcel',
        meta: { title: 'Export Excel' }
      },
      {
        path: 'export-selected-excel',
        component: () => import('@/views/excel/select-excel'),
        name: 'SelectExcel',
        meta: { title: 'Export Selected' }
      },
      {
        path: 'export-merge-header',
        component: () => import('@/views/excel/merge-header'),
        name: 'MergeHeader',
        meta: { title: 'Merge Header' }
      },
      {
        path: 'upload-excel',
        component: () => import('@/views/excel/upload-excel'),
        name: 'UploadExcel',
        meta: { title: 'Upload Excel' }
      }
    ]
  },

  {
    path: '/pdf',
    component: Layout,
    redirect: '/pdf/index',
    children: [
      {
        path: 'index',
        component: () => import('@/views/pdf/index'),
        name: 'PDF',
        meta: { title: 'PDF', icon: 'pdf' }
      }
    ]
  },
  {
    path: '/pdf/download',
    component: () => import('@/views/pdf/download'),
    hidden: true
  },*/

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
