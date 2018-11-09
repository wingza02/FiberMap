# core-ui

> Open Source Admin Template

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run e2e tests
npm run e2e

# run all tests
npm test
```

For detailed explanation on how things work, checkout the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

_____________________________________________________________
Fix 11/9/2018
how to fix error
1.comment about firebase
2.change bootstrap and jquery cdn in index.html
3.import BootstrapVue from 'bootstrap-vue'
4.npm install node-sass sass-loader

how to fix stuck when drag map
  delete @center_changed="updateCenter" in <gmap-map> 
_____________________________________________________________
