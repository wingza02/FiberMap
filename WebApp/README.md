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
Fix 18/12/2018<br>
how to fix error<br>
1.comment or delete about firebase - firebase and vuefire (in package.json and main.js)<br>
2.change bootstrap and jquery cdn in index.html (cdn is in bootstrap web)<br>
3.import BootstrapVue from 'bootstrap-vue' and Vue.use(BootstrapVue) (optional) <br>
4. "node-sass": "" (in package.json)<br>
5.npm install node-sass sass-loader (if you dont npm i then let npm i than 5 command)<br>
<br>
how to fix stuck when drag map<br>
delete @center_changed="updateCenter" in gmap-map
_____________________________________________________________
