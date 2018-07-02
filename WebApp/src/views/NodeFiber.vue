<template>
  <div id="app">

<!-- Map -->
    <gmap-map :center="center" @zoom_changed="updateZoom" @center_changed="updateCenter" :zoom="zoom" mapTypeId="hybrid" style="width: 65%; height: 550px; float: left;">
    
      <gmap-info-window :options="infoOptions" :position="infoWindowPos" :opened="infoWinOpen" @closeclick="infoWinOpen=false" v-if="infoMarker">
        Name: {{infoContent.name}}<br>
        --------------------------- <br>
        <a href="#" @click="zoomMap(infoWindowPos,'marker')">Zoom</a> <!-- <font v-if="user.isLogin==true&&user.isAdmin==true">|| </font> -->
        <!--|| <a data-toggle="modal" data-target="#myModal">History</a> -->
      </gmap-info-window>

      <gmap-marker
        :key="index"
        v-for="(m, index) in nodes"
        :title="m.name"
        :position="m.position"
        :clickable="true"
        :draggable="false"
        :icon="image.url"
        @click="toggleInfoWindow(m,index)"
      ></gmap-marker>

      <gmap-info-window :options="infoOptions" :position="infoWindowPos" :opened="infoWinOpen" @closeclick="infoWinOpen=false" v-if="infoPolyline">
        From: {{ infoContent.A }} <br>
        To: {{ infoContent.B }} <br>
        Status: {{ infoContent.status }}<br>
        ------------------------------------------------------------------ <br>
        <a href="#" @click="zoomMap(infoWindowPos,'line')">Zoom</a> || 
        <a href="#" @click="focusLine(infoContent.id)">Focus</a> || 
        <a href="#" @click="unfocusLine()">UnFocus</a> || 
        <a href="#" @click="routeStreetView">Street View</a>
      </gmap-info-window> 

      <gmap-polyline
        v-for="(pl,index) in connects" 
        :key="index" 
        :path="pl.path" 
        :options="{geodesic:true, strokeColor:pl.linecolor ,strokeWeight:4}"
        @click="toggleInfoWindow2(pl,index,1)"
        @mousemove="posMouse">
      </gmap-polyline>
      
    </gmap-map>

<!-- Table And Filter -->
    <div style="display: inline-block; margin-left: 10px; width: 30%">
      <div id="bigBoxs">
        <h2>Status :
        <div class="btn-group">
          <input type="submit" class="btn btn-default" @click="showByStatus('all')" value="All"/>
          <input type="submit" class="btn btn-default" @click="showByStatus('status',1)" value="Main"/>
          <input type="submit" class="btn btn-default" @click="showByStatus('status',0)" value="Simulate"/>
        </div>
        </h2>
        <h2>Layer :
          <div class="btn-group">
            <input type="submit" class="btn btn-default" @click="showLayer('all')" value="All"/>
            <input type="submit" class="btn btn-default" @click="showLayer('coretocore')" value="Core-Core"/>
            <input type="submit" class="btn btn-info dropdown-toggle" data-toggle="dropdown" value="Zone"/>
            <ul class="dropdown-menu dropdown-menu-right">
              <li><a @click="showLayer('zone','COM')">COM</a></li>
              <li><a @click="showLayer('zone','ENG')">ENG</a></li>
              <li><a @click="showLayer('zone','AGR')">AGR</a></li>
              <li><a @click="showLayer('zone','MED')">MED</a></li>
              <li><a @click="showLayer('zone','MAEHEA')">MAE-HEA</a></li>
            </ul>   
          </div>
        </h2>
        <h2>Filtered By :
          <div class="btn-group">
            <input type="submit" class="btn btn-default" @click="showTable('node')" value="Node"/>
            <input type="submit" class="btn btn-default" @click="showTable('line')" value="Optical Fiber"/>
          </div>
        </h2>
        <vue-good-table v-if="isTableMarker"
          :columns="columns"
          :rows="nodes"
          :paginate="true"
          :lineNumbers="false"
          :globalSearch="true"
          :onClick="toggleInfoWindow"/>
          <vue-good-table v-if="isTableLine"
          :columns="columnsLine"
          :rows="connects"
          :paginate="true"
          :lineNumbers="false"
          :globalSearch="true"
          :onClick="toggleInfoWindow2"/>
        </div>
      </div>

    </div>
</template>

<script>
// Import make pdf and thai font
import pdfMake from 'pdfmake/build/pdfmake'
import pdfFonts from 'pdfmake/build/vfs_fonts'
pdfMake.vfs = pdfFonts.pdfMake.vfs
pdfMake.fonts = {
  THSarabunNew: {
    normal: 'THSarabunNew.ttf',
    bold: 'THSarabunNew-Bold.ttf',
    italics: 'THSarabunNew-Italic.ttf',
    bolditalics: 'THSarabunNew-BoldItalic.ttf'
  },
  Roboto: {
    normal: 'Roboto-Regular.ttf',
    bold: 'Roboto-Medium.ttf',
    italics: 'Roboto-Italic.ttf',
    bolditalics: 'Roboto-MediumItalic.ttf'
  }
}

export default {
  name: 'NodeFiber',
  data () {
    return {
      i:0,
      image: {
        url: 'https://fibermap-v2.cmu.ac.th/img/gmap.png'
      },
      zoom: 16,
      center: { lat: 18.79686, lng: 98.9537475 },
      mousePos: { lat: 18.796861024696568, lng: 98.95122811930116 },
      infoContent: '',
      infoMarker: false,
      infoPolyline: false,
      infoWindowPos: {
        lat: 0,
        lng: 0
      },
      infoWinOpen: false,
      currentMidx: null,
      infoOptions: {
        pixelOffset: {
          width: 0,
          height: -35
        }
      },
      nodes: [],
      connects: [],
      core_sw: [],
      columns: [
        {
          label: 'Name',
          field: 'name',
          filterable: false
        },
        // {
        //   label: 'Status',
        //   field: 'status',
        //   type: 'string',
        //   html: false,
        //   filterable: false
        // },
        // {
        //   label: 'Uptime',
        //   field: 'uptime',
        //   type: 'number',
        //   html: false,
        //   filterable: false
        // }
      ],
      isTableMarker: true,
      columnsLine: [
        {
          label: 'From',
          field: 'A',
          filterable: false
        },
        {
          label: 'To',
          field: 'B',
          filterable: false
        },
        {
          label: 'Status',
          field: 'status',
          html: false,
          filterable: false
        }
      ],
      isTableLine: false,
      user: [],
    }
  },
  methods: {
    showLayer (value, e, num) {                                       // Filter by Layer on top of table
      if (value === 'all') {                                       // All
        this.getNode()
        this.getConnect()
      }
      if (value === 'coretocore') {                                       // Core-Core
        this.nodes = []
        this.connects = []
        this.axios
          .get('https://fibermap-api.cmu.ac.th/showlayerNP', {
            headers: {'Authorization': sessionStorage.getItem('token')}
          })
          .then(response => {
            // console.log(response.data[0].node);
            this.nodes = response.data[0].node
            this.connects = response.data[0].connect
          })
      }
      if (value === 'zone') {                                       // Zone
        this.nodes = []
        this.connects = []
        // console.log(e)
        this.axios
          .get('https://fibermap-api.cmu.ac.th/showzoneNP', {
            params: {
              zone: e
            },
            headers: {'Authorization': sessionStorage.getItem('token')}
          })
          .then(response => {
            // console.log(response.data[0])
            for (let i = 0; i < response.data[0].node.length; i++) {
              if (e == response.data[0].node[i].zone && response.data[0].node[i].is_core==1) {
                this.center = response.data[0].node[i].position
              }
            }
            this.nodes = response.data[0].node
            this.connects = response.data[0].connect
          })
      }
    },
    focusLine (value) {                                       // Focus Path
      this.axios
        .get('https://fibermap-api.cmu.ac.th/nodepathbyid', {
          params: {
            lineid: value
          },
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
        //   console.log(response.data[0])
          this.nodes = response.data[0].node
          this.connects = response.data[0].connect
        })
    },
    unfocusLine () {                                       // Unfocus Path
      this.getNode()
      this.getConnect()
    },
    zoomMap (pos, obj) {                                       // Zoom Map
      if (obj === 'marker') {
        this.center = pos
        this.zoom = 18
      } else if (obj === 'line') {
        this.center = pos
        this.zoom = 17
      }
    },
    updateZoom (zoom) {                                       // Update Map for new zoom value
      // console.log(zoom)
      this.zoom = zoom
    },
    updateCenter (center) {                                       // Update Map for new center value
      this.center = {
        lat: center.lat(),
        lng: center.lng()
      }
    },
    routeStreetView () {                                       // Link to StreetView on google map site
      window.open('http://maps.google.com/maps?q=&layer=c&cbll=' + this.mousePos.lat + ',' + this.mousePos.lng, '_blank')
    },
    posMouse (pos) {                                       // Mouse Position
      this.mousePos = {
        lat: pos.latLng.lat(),
        lng: pos.latLng.lng()
      }
    },
    showTable (value) {                                       // use for switch table filter between device and line
      // console.log(value)
      if (value === 'node') {
        this.isTableMarker = true
        this.isTableLine = false
      } else if (value === 'line') {
        this.isTableMarker = false
        this.isTableLine = true
      }
    },
    showByStatus (value, e) {                                       // Filter by status
      // console.log(value)
      // console.log(e)
      if (value === 'all') {                                       // All
        this.getNode()
        this.getConnect()
      }
      if (value === 'status') {                                       // Up or Down
        if (e === 1) {
          this.nodes = []
          this.connects = []
        }
        this.axios
          .get('https://fibermap-api.cmu.ac.th/showbystatusNP', {
            params: {
              status: e
            },
            headers: {'Authorization': sessionStorage.getItem('token')}
          })
          .then(response => {
            // console.log(response.data[0]);
            this.nodes = response.data[0].node
            this.connects = response.data[0].connect
          })
      }
    },
    toggleInfoWindow (marker, idx) {                                       // Toggle infowindow Marker
      this.infoOptions.pixelOffset.height = -20
      this.infoWindowPos = marker.position
      this.infoContent = marker
      this.center = marker.position
      this.infoWinOpen = true
      this.currentMidx = idx
      this.infoMarker = true
      this.infoPolyline = false
    },
    toggleInfoWindow2 (line, idx, e) {                                       // Toggle infowindow Line
      this.infoOptions.pixelOffset.height = 0
      if (e === 1) {
        var midLat = this.mousePos.lat
        var midLng = this.mousePos.lng
      } else {
        if ((line.path.length % 2) === 0) {
          midLat = (line.path[line.path.length / 2].lat)
          midLng = (line.path[line.path.length / 2].lng)
        } else {
          midLat = (line.path[line.path.length / 2 - 0.5].lat + line.path[line.path.length / 2 + 0.5].lat) / 2
          midLng = (line.path[line.path.length / 2 - 0.5].lng + line.path[line.path.length / 2 + 0.5].lng) / 2
        }
        this.center = { lat: midLat, lng: midLng }
      }
      // console.log(line.path.length)
      this.infoWindowPos = { lat: midLat, lng: midLng }
      this.infoContent = line
      this.infoWinOpen = true
      this.currentMidx = idx
      this.infoPolyline = true
      this.infoMarker = false
    },
    getNode () {                                       // Get node from DB
      this.axios
        .get('https://fibermap-api.cmu.ac.th/getnode', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          // console.log(response.data[0].name)
          this.nodes = response.data
        })
    },
    getConnect () {                                       // Get polyline path from DB
      this.axios
        .get('https://fibermap-api.cmu.ac.th/getnodepath', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          this.connects = response.data
          // console.log(this.connects[0].path)
          // console.log(this.connects)
        })
    },
    getCoreNode () {                                       // Get core node from DB
      this.axios
        .get('https://fibermap-api.cmu.ac.th/getcorenode', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          // console.log(response.data[0].name)
          this.core_sw = response.data
        })
    },
    getDataUser () {                                       // Auth user for each page
      this.user.id = sessionStorage.getItem('iduser')
      this.user.username = sessionStorage.getItem('username')
      this.user.firstname = sessionStorage.getItem('firstname')
      this.user.lastname = sessionStorage.getItem('lastname')
      this.user.tel = sessionStorage.getItem('tel')
      this.user.email = sessionStorage.getItem('email')
      this.user.isAdmin = sessionStorage.getItem('isAdmin') === 'true'
      this.user.isLogin = sessionStorage.getItem('isLogin') === 'true'
      
      this.axios.post('https://fibermap-api.cmu.ac.th/checktoken', {
        token : sessionStorage.getItem('token')
      })
      .then(response => {
        if(response.data.status == 'timeout') {
          this.$router.push({name: 'Login'})
        }
      })
    }
  },
  created: function () {                                       // Run these function when start page
    this.getNode()
    this.getConnect()
    this.getCoreNode()
    this.getDataUser()
  },
}
</script>

<style>
a:hover {
  color: red;
  cursor: pointer;
}
a:link {
  cursor: pointer
}
</style>