import Vue from 'vue'
import Router from 'vue-router'

// Containers
import Full from '@/containers/Full'

// Views
import Dashboard from '@/views/Dashboard'
import Charts from '@/views/Charts'
import Widgets from '@/views/Widgets'

import FiberMap from '@/views/Map'
import RealPath from '@/views/RealPath'
import MapToReal from '@/views/MapToReal'
import NodeFiber from '@/views/NodeFiber'
import Config from '@/views/Configuration'
import Setting from '@/views/Setting'

import ChartReport from '@/views/ChartReport'


// Views - ConfigComponents
import AddSwitch from '@/views/config_components/AddSwitch'
import EditSwitch from '@/views/config_components/EditSwitch'
import AddPath from '@/views/config_components/AddPath'
import EditPath from '@/views/config_components/EditPath'
import AddUser from '@/views/config_components/AddUser'
import EditUser from '@/views/config_components/EditUser'
import ChangePass from '@/views/config_components/ChangePass'
import AddNode from '@/views/config_components/AddNode'
import EditNode from '@/views/config_components/EditNode'
import AddNodeConnect from '@/views/config_components/AddNodeConnect'
import AddNodePath from '@/views/config_components/AddNodePath'
import EditNodePath from '@/views/config_components/EditNodePath'
import AddOID from '@/views/config_components/AddOID'

// Views - Components
import Buttons from '@/views/components/Buttons'
import SocialButtons from '@/views/components/SocialButtons'
import Cards from '@/views/components/Cards'
import Forms from '@/views/components/Forms'
import Modals from '@/views/components/Modals'
import Switches from '@/views/components/Switches'
import Tables from '@/views/components/Tables'

// Views - Icons
import FontAwesome from '@/views/icons/FontAwesome'
import SimpleLineIcons from '@/views/icons/SimpleLineIcons'

// Views - Pages
import Page404 from '@/views/pages/Page404'
import Page500 from '@/views/pages/Page500'
import Login from '@/views/pages/Login'
import Register from '@/views/pages/Register'

Vue.use(Router)

export default new Router({
  mode: 'hash', // Demo is living in GitHub.io, so required!
  linkActiveClass: 'open active',
  scrollBehavior: () => ({ y: 0 }),
  routes: [
    {
      path: '/',
      redirect: '/dashboard',
      name: 'Home',
      component: Full,
      children: [
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: Dashboard,
          meta: { requiresAuth: true }
        },
        {
          path: 'map',
          name: 'Map',
          component: FiberMap,
          meta: { requiresAuth: true }
        },
        {
          path: 'realpath',
          name: 'RealPath',
          component: RealPath,
          meta: { requiresAuth: true }
        },
        {
          path: 'nodefiber',
          name: 'NodeFiber',
          component: NodeFiber,
          meta: { requiresAuth: true }
        },
        {
          path: 'maptoreal',
          name: 'MapToReal',
          component: MapToReal,
          meta: { requiresAuth: true }
        },
        //  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        {
          path: 'config',
          name: 'Config',
          component: Config,
          meta: { requiresAuth: true }
        },
        {
          path: 'config/addswitch',
          name: 'AddSwitch',
          component: AddSwitch,
          meta: { requiresAuth: true }
        },
        {
          path: 'config/editswitch',
          name: 'EditSwitch',
          component: EditSwitch,
          meta: { requiresAuth: true }
        },
        {
          path: 'config/addpath',
          name: 'AddPath',
          component: AddPath,
          meta: { requiresAuth: true }
        },
        {
          path: 'config/editpath',
          name: 'EditPath',
          component: EditPath,
          meta: { requiresAuth: true }
        },
        {
          path: 'config/adduser',
          name: 'AddUser',
          component: AddUser,
          meta: { requiresAuth: true }
        },
        {
          path: 'config/edituser',
          name: 'EditUser',
          component: EditUser,
          meta: { requiresAuth: true }
        },
        {
          path: 'config/changepass',
          name: 'ChangePass',
          component: ChangePass,
          meta: { requiresAuth: true }
        },
        {
          path: 'config/addnode',
          name: 'AddNode',
          component: AddNode,
          meta: { requiresAuth: true }
        },
        {
          path: 'config/editnode',
          name: 'EditNode',
          component: EditNode,
          meta: { requiresAuth: true }
        },
        {
          path: 'config/addnodeconnect',
          name: 'AddNodeConnect',
          component: AddNodeConnect,
          meta: { requiresAuth: true }
        },
        {
          path: 'config/addnodepath',
          name: 'AddNodePath',
          component: AddNodePath,
          meta: { requiresAuth: true }
        },
        {
          path: 'config/editnodepath',
          name: 'EditNodePath',
          component: EditNodePath,
          meta: { requiresAuth: true }
        },
        //  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        {
          path: 'setting',
          name: 'Setting',
          component: Setting,
          meta: { requiresAuth: true }
        },
        {
          path: 'setting/addoid',
          name: 'AddOID',
          component: AddOID,
          meta: { requiresAuth: true }
        },
        //  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        {
          path: 'charts',
          name: 'Charts',
          component: Charts
        },
        {
          path: 'report',
          name: 'report',
          component: ChartReport
        },
        {
          path: 'widgets',
          name: 'Widgets',
          component: Widgets
        },
        {
          path: 'components',
          redirect: '/components/buttons',
          name: 'Components',
          component: {
            render (c) { return c('router-view') }
          },
          children: [
            {
              path: 'buttons',
              name: 'Buttons',
              component: Buttons
            },
            {
              path: 'social-buttons',
              name: 'Social Buttons',
              component: SocialButtons
            },
            {
              path: 'cards',
              name: 'Cards',
              component: Cards
            },
            {
              path: 'forms',
              name: 'Forms',
              component: Forms
            },
            {
              path: 'modals',
              name: 'Modals',
              component: Modals
            },
            {
              path: 'switches',
              name: 'Switches',
              component: Switches
            },
            {
              path: 'tables',
              name: 'Tables',
              component: Tables
            }
          ]
        },
        {
          path: 'icons',
          redirect: '/icons/font-awesome',
          name: 'Icons',
          component: {
            render (c) { return c('router-view') }
          },
          children: [
            {
              path: 'font-awesome',
              name: 'Font Awesome',
              component: FontAwesome
            },
            {
              path: 'simple-line-icons',
              name: 'Simple Line Icons',
              component: SimpleLineIcons
            }
          ]
        }
      ]
    },
    {
      path: '/pages',
      redirect: '/pages/404',
      name: 'Pages',
      component: {
        render (c) { return c('router-view') }
      },
      children: [
        {
          path: '404',
          name: 'Page404',
          component: Page404
        },
        {
          path: '500',
          name: 'Page500',
          component: Page500
        },
        {
          path: 'login',
          name: 'Login',
          component: Login
        },
        {
          path: 'register',
          name: 'Register',
          component: Register
        }
      ]
    }
  ]
})
