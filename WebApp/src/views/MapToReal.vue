<template>
  <div id="app">
    <!-- map -->
    <gmap-map :center="center" 
    @zoom_changed="updateZoom" 
    @center_changed="updateCenter"
    :zoom="zoom"
    mapTypeId="hybrid"
    style="width: 100%; height: 550px; float: left;">
    
<!-- Marker+InfoWindow @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ -->
    <gmap-info-window :options="infoOptions" :position="infoWindowPos" :opened="infoWinOpen" @closeclick="infoWinOpen=false" v-if="infoMarker">
        Name: {{infoContent.name}}<br>
        <!-- IP: {{infoContent.ip}}<br> -->
        <p v-if="infoContent.uptime=='0:00:00'">Status: Down <br> Uptime: 0:00:00 Hours</p>
        <p v-else>Status: Up <br> Uptime: {{ infoContent.uptime }} Hours</p>
        <a href="#" @click="zoomMap(infoWindowPos,'marker')">Zoom</a> <font v-if="user.isLogin==true&&user.isAdmin==true">|| </font>
        <font v-if="user.isLogin==true&&user.isAdmin==true"><a href="#" data-toggle="modal" data-target="#graphCPU" @click="getCPU(infoContent)">Graph</a> || </font>
        <a href="#" @click="backToMap()">Back</a> <!--|| <a data-toggle="modal" data-target="#myModal">History</a> -->
    </gmap-info-window> 
    <gmap-marker
      :key="index"
      v-for="(m, index) in filterData"
      :title="m.name"
      :position="m.position"
      :clickable="true"
      :draggable="false"
      :icon="m.image"
      @click="toggleInfoWindow(m,index)"
    ></gmap-marker>

    <gmap-marker
      :key="index"
      v-for="(m, index) in markers"
      :title="m.name"
      :position="m.position"
      :clickable="true"
      :draggable="false"
      :icon="image1.url"
      @click="toggleInfoWindow(m,index)">
      </gmap-marker>

    <gmap-info-window  :options="infoOptions" :position="infoWindowPos" :opened="infoWinOpen" @closeclick="infoWinOpen=false" v-if="infoPolyline">
        From: {{ infoContent.A }} - {{ infoContent.port_A }} <br>
        To: {{ infoContent.B }} - {{ infoContent.port_B }} <br>
        Status: {{ infoContent.linestatus }}<br>
        ------------------------------------------------------------------ <br>
        Distance of Fiber: {{ infoline.distance }} Meter<br>
        Distance in Gmap: {{ infoline.gmap_distance }} Meter<br>
        Type: {{ infoline.type }}<br>
        Core Number: {{ infoline.core_number }} Core<br>
        ------------------------------------------------------------------ <br>
        <a href="#" @click="zoomMap(infoWindowPos,'line')">Zoom</a> || 
        <a href="#" data-toggle="modal" data-target="#History" @click="loadHistory('All Time')">History</a> || 
        <font v-if="user.isLogin==true&&user.isAdmin==true"><a href="#" data-toggle="modal" data-target="#Problem">จุดขาด</a> ||</font> 
        <font v-if="user.isLogin==true&&user.isAdmin==true"><a href="#" data-toggle="modal" data-target="#graphBW" @click="getBandwidth(infoContent)">Graph</a> || </font> 
        <a href="#" @click="routeStreetView">Street View</a> || 
        <a href="#" @click="backToMap()">Back</a>
    </gmap-info-window> 
    <gmap-polyline
      v-for="(pl,index) in connects" 
      :key="index" 
      :path="pl.path" 
      :options="{geodesic:true, strokeColor:pl.linecolor ,strokeWeight:4, icons: [{icon: pl.icon, offset: pl.broken_percentile}]}"
      @click="toggleInfoWindow2(pl,index,1)"
      @mousemove="posMouse">
    </gmap-polyline>
    
    </gmap-map>

    <div v-show="false" style="display: inline-block; margin-left: 10px; width: 30%">
      <div id="bigBoxs">
        <!-- <input v-model="search" type="text" /> -->
        <!-- </div> -->
        <!-- <div class="col-md-6 col-md-offset-6" > -->
        <h2>Status :
          <!-- <input type="submit" class="btn btn-default" @click="checkStatus('all')" value="All"/>
          <input type="submit" class="btn btn-default" @click="checkStatus('up')" value="Up"/>
          <input type="submit" class="btn btn-default" @click="checkStatus('down')" value="Down"/> -->
        <div class="btn-group">
          <input type="submit" class="btn btn-default" @click="showByStatus('all')" value="All"/>
          <input type="submit" class="btn btn-default" @click="showByStatus('updown',1)" value="Up"/>
          <input type="submit" class="btn btn-default" @click="showByStatus('updown',0)" value="Down"/>
        </div>
        </h2>
        <!-- </div> -->
        <!-- <div class="col-md-6 col-md-offset-6" > -->
        <h2>Layer :
          <!-- <button class="btn btn-default" type="submit">All</button>
          <button class="btn btn-default" type="submit">Core-End</button>
          <button class="btn btn-default" type="submit">Core-Core</button> -->
          <div class="btn-group">
            <input type="submit" class="btn btn-default" @click="showLayer('all')" value="All"/>
            <input type="submit" class="btn btn-default" @click="showLayer('coretocore')" value="Core-Core"/>
            <input type="submit" class="btn btn-info dropdown-toggle" data-toggle="dropdown" value="Zone"/>
            <ul class="dropdown-menu dropdown-menu-right">
              <li><a @click="showLayer('zone',1)">COM</a></li>
              <li><a @click="showLayer('zone',2)">ENG</a></li>
              <li><a @click="showLayer('zone',5)">AGR</a></li>
              <li><a @click="showLayer('zone',4)">MED</a></li>
              <li><a @click="showLayer('zone',33)">MAE-HEA</a></li>
            </ul>   
          </div>
        </h2>
        <h2>Filtered By :
          <!-- <button class="btn btn-default" type="submit">All</button>
          <button class="btn btn-default" type="submit">Core-End</button>
          <button class="btn btn-default" type="submit">Core-Core</button> -->
          <div class="btn-group">
            <input type="submit" class="btn btn-default" @click="showTable('switch')" value="Switch"/>
            <input type="submit" class="btn btn-default" @click="showTable('line')" value="Optical Fiber"/>
          </div>
        </h2>
        <vue-good-table v-if="isTableMarker"
          :columns="columns"
          :rows="filterData"
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

      <div class="modal" id="History" tabindex="-1" role="dialog" aria-labelledby="History" aria-hidden="true" style="width: 82%;">
        <div class="modal-dialog" role="document">
          <div class="modal-content" style="width: 150%;">
            <div class="modal-header">
              <h2 class="modal-title" id="History">History : {{ this.dateHistory }}</h2>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
                <button type="button" class="btn btn-info" @click="filterHistory(-1,'Last 1 Month')">1 Month</button> || 
                <button type="button" class="btn btn-primary" @click="filterHistory(-3,'Last 3 Months')">3 Months</button> || 
                <button type="button" class="btn btn-info" @click="filterHistory(-6,'Last 6 Months')">6 Months</button> ||
                <button type="button" class="btn btn-primary" @click="filterHistory(-12,'Last 1 Year')">1 Year</button> || 
                <button type="button" class="btn btn-info" @click="loadHistory('All Time')">All Time</button> --- 
                <input type="date" name="bday" v-model="fDate"> - <input type="date" name="bday" v-model="tDate">
                <button type="button" class="btn btn-primary" @click="filterHistory2()">Search</button> <hr>
              <div v-for="(h,index) in history" :key="index">
                <h4>{{ h.broken_time }} - Distance: {{ h.distance }} m - 
                  <font v-if="h.status_broken==0" color="green">ซ่อมแล้ว (ยืนยันโดย {{ h.approved_by }}) - {{ h.timestamp }}</font>
                  <font v-if="h.status_broken==1" color="red">รอการซ่อมแซม (แจ้งโดย {{ h.approved_by }})</font>
                  <font v-if="h.status_broken==2" color="Gray">กำลังดำเนินการ (แจ้งโดย {{ h.approved_by }})</font>
                  <font v-if="h.status_broken==3" color="Orange">รอการยืนยัน (แจ้งโดย {{ h.approved_by }})</font>
                  <font v-if="h.status_broken==1&&user.isLogin==true&&h.status==1">
                    <label class="checkbox-inline" v-if="user.isAdmin==false"><input v-model="chkBroken" type="radio" name="chkbroken" id="chkbroken" value="2">รับรู้แล้ว</label> 
                    <label class="checkbox-inline" v-if="user.isAdmin==false"><input v-model="chkBroken" type="radio" name="chkbroken" id="chkbroken" value="3">ซ่อมเสร็จแล้ว</label> 
                    <label class="checkbox-inline" v-if="user.isAdmin==true"><input v-model="chkBroken" type="radio" name="chkbroken" id="chkbroken" value="0">ยืนยันการซ่อม</label>
                    <button type="submit" class="btn btn-primary" @click="checkBroken(index)">ยืนยัน</button>
                  </font>
                  <font v-if="h.status_broken==2&&user.isLogin==true&&h.status==1">
                    <label class="checkbox-inline" v-if="user.isAdmin==false"><input v-model="chkBroken" type="radio" name="chkbroken" id="chkbroken" value="3">ซ่อมเสร็จแล้ว</label> 
                    <label class="checkbox-inline" v-if="user.isAdmin==true"><input v-model="chkBroken" type="radio" name="chkbroken" id="chkbroken" value="0">ยืนยันการซ่อม</label>
                    <button type="submit" class="btn btn-primary" @click="checkBroken(index)">ยืนยัน</button>
                  </font>
                  <font v-if="h.status_broken==3&&user.isLogin==true&&user.isAdmin==true&&h.status==1">
                    <label class="checkbox-inline" v-if="user.isAdmin==true"><input v-model="chkBroken" type="radio" name="chkbroken" id="chkbroken" value="0">ยืนยันการซ่อม</label>
                    <button type="submit" class="btn btn-primary" @click="checkBroken(index)">ยืนยัน</button>
                  </font>
                </h4>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-primary" @click="downloadHistory(history)">Export History</button>
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="modal" id="Problem" tabindex="-1" role="dialog" aria-labelledby="Problem" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h2 class="modal-title" id="Problem">รายงานตำแหน่งที่สายขาด</h2>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <h3>จุดขาดอยู่ที่ตำแหน่ง <input v-model="distance" type="text" placeholder="ระยะทางที่สายชำรุด"/> เมตร <button type="button" class="btn btn-primary" data-dismiss="modal" @click="saveHistory">Add</button></h3>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      </div>

      <modal v-show="showModal" @close="showModal = false">
        <h3 slot="header">
          <p v-if="showCPU==true">{{ infoContent.name }} </p> 
          <p v-if="showBW==true">From: {{infoContent.B}} - To: {{infoContent.A}}</p>
          
        </h3>
        <h3 slot="body">
          <div v-show="showCPU"><chart-report ref="chartCPU" :id="infoContent.id" ></chart-report></div>
          <div v-show="showBW"><chart-b-w ref="chartBW"></chart-b-w></div>
        </h3>
      </modal>
    </div>
</template>

<script>
import CardLine1ChartExample from './dashboard/CardLine1ChartExample'
import CardLine2ChartExample from './dashboard/CardLine2ChartExample'
import CardLine3ChartExample from './dashboard/CardLine3ChartExample'
import CardBarChartExample from './dashboard/CardBarChartExample'
import MainChartExample from './dashboard/MainChartExample'
import SocialBoxChartExample from './dashboard/SocialBoxChartExample'
import CalloutChartExample from './dashboard/CalloutChartExample'
import { Callout } from '../components/'
import funcJS from '../function.js'
import modal from './modal'
import ChartReport from './ChartReport'
import ChartBW from './ChartBW'

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
  name: 'dashboard',
  components: {
    ChartReport,
    ChartBW,
    modal,
    Callout,
    CardLine1ChartExample,
    CardLine2ChartExample,
    CardLine3ChartExample,
    CardBarChartExample,
    MainChartExample,
    SocialBoxChartExample,
    CalloutChartExample
  },
  data () {
    return {
      image: {
        // url: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png'
      },
      image1: {
        url: 'http://fibermap.cmu.ac.th/img/me.png'
      },
      goldStar: {
        path: 'M-0.1,0a0.1,0.1 0 1,0 0.2,0a0.1,0.1 0 1,0 -0.2,0 M-6.5,0a6.5,6.5 0 1,0 13,0a6.5,6.5 0 1,0 -13,0',
        strokeColor: 'gold',
        strokeWeight: 3
      },
      broke_distance: 105,
      percentile: ['0%', '100%'],
      zoom: 16,
      center: { lat: parseFloat(this.$route.query.lat), lng: parseFloat(this.$route.query.lng) },
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
      markers: [
        {
          position: {
            lat: 47.376332,
            lng: 8.547511
          },
          infoText: 'Marker 1'
        },
        {
          position: {
            lat: 47.374592,
            lng: 8.548867
          },
          infoText: 'Marker 2'
        },
        {
          position: {
            lat: 47.379592,
            lng: 8.549867
          },
          infoText: 'Marker 3'
        }
      ],
      plPath: [
        { lat: 18.7956453, lng: 98.952812 },
        { lat: 18.7982302, lng: 98.9491877 },
        { lat: 18.8004538, lng: 98.9504027 },
        { lat: 18.7932254, lng: 98.9562057 },
        { lat: 18.7956453, lng: 98.952812 }
      ],
      lineColor: 'RED',
      ppath: [
        {
          path: [
            { lat: 18.803528, lng: 98.952944 },
            { lat: 18.803289, lng: 98.952839 },
            { lat: 18.803622, lng: 98.951974 },
            { lat: 18.801703, lng: 98.951205 },
            { lat: 18.800288, lng: 98.951428 },
            { lat: 18.799764, lng: 98.951980 },
            { lat: 18.799236, lng: 98.951806 },
            { lat: 18.798836, lng: 98.951308 },
            { lat: 18.79685, lng: 98.951251 },
            { lat: 18.79674, lng: 98.951974 },
            { lat: 18.796134, lng: 98.951974 },
            { lat: 18.796137, lng: 98.951652 }
          ]
        },
        {
          path: [
            { lat: 18.7982302, lng: 98.9491877 },
            { lat: 18.7956453, lng: 98.952812 }
          ]
        },
        {
          path: [
            { lat: 18.8004538, lng: 98.9504027 }
            // { lat: 18.7982302, lng: 98.9491877 }
          ]
        },
        {
          path: [
            { lat: 18.7932254, lng: 98.9562057 },
            { lat: 18.7932254, lng: 98.9562057 }
          ]
        }
      ],
      plvisible: true,
      switchs: [],
      connects: [],
      search: '',
      columns: [
        {
          label: 'Name',
          field: 'name',
          filterable: false
        },
        {
          label: 'Status',
          field: 'status',
          type: 'string',
          html: false,
          filterable: false
        },
        {
          label: 'Uptime',
          field: 'uptime',
          type: 'number',
          html: false,
          filterable: false
        }
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
          field: 'linestatus',
          html: false,
          filterable: false
        }
      ],
      isTableLine: false,
      distance: '',
      history: [{ comment: '' }],
      dateHistory: 'All Time',
      fDate: '',
      tDate: '',
      myLocation: '',
      cpu_usage: [],
      datacollection: null,
      showModal: false,
      date_usage: [],
      user: [],
      infoline: [],
      showCPU: false,
      showBW: false
    }
  },
  methods: {
    hellojs: funcJS.hello,
    variant (value) {
      let $variant
      if (value <= 25) {
        $variant = 'info'
      } else if (value > 25 && value <= 50) {
        $variant = 'success'
      } else if (value > 50 && value <= 75) {
        $variant = 'warning'
      } else if (value > 75 && value <= 100) {
        $variant = 'danger'
      }
      return $variant
    },
    imageMarker() {
      for (let i=0; i<this.switchs.length; i++) {
        // console.log(this.switchs[i].status)
        if(this.switchs[i].status == 'Up' || this.switchs[i].uptime != 0 || this.switchs[i].uptime != '0:00:00') {
          this.switchs[i].image = 'http://fibermap.cmu.ac.th/img/up.png'
        }
        if(this.switchs[i].status == 'Down' || this.switchs[i].uptime == 0 || this.switchs[i].uptime == '0:00:00') {
          this.switchs[i].image = 'http://fibermap.cmu.ac.th/img/down.png'
        }
      }
    },
    showBroken () {
      // console.log(this.connects)
      // this.goldStar.path = 'M-0.1,0a0.1,0.1 0 1,0 0.2,0a0.1,0.1 0 1,0 -0.2,0 M-6.5,0a6.5,6.5 0 1,0 13,0a6.5,6.5 0 1,0 -13,0'
      // this.goldStar.strokeColor = 'blue'
      // this.goldStar.strokeWeight = 3
      this.axios
        .get('https://fibermap.herokuapp.com/getbroken')
        .then(response => {
          this.broke_distance = response.data
          // console.log(this.broke_distance.length)
          for (var i = 0; i < this.broke_distance.length; i++) {
            for (var j = 0; j < this.connects.length; j++) {
              if (this.broke_distance[i].line_id === this.connects[j].id) {
                this.connects[j]['broke_distance'] = this.broke_distance[i].distance
                this.connects[j]['icon'] = {'path': 'M-0.1,0a0.1,0.1 0 1,0 0.2,0a0.1,0.1 0 1,0 -0.2,0 M-6.5,0a6.5,6.5 0 1,0 13,0a6.5,6.5 0 1,0 -13,0', 'strokeColor': 'gold', 'strokeWeight': 3}
              } else if (this.connects[j].broke_distance === undefined) {
                this.connects[j]['broke_distance'] = 0
                this.connects[j]['icon'] = {'path': '', 'strokeColor': 'gold', 'strokeWeight': 3}
              }
            }
          }
          this.calDistance()
        })
    },
    calDistance () {
      // console.log(this.connects[0])
      var distance = 0
      for (var i = 0; i < this.connects[0].path.length - 1; i++) {
        distance = distance + this.getDistance(this.connects[0].path[i].lat, this.connects[0].path[i].lng, this.connects[0].path[i + 1].lat, this.connects[0].path[i + 1].lng)
      }
      this.percentile = ((this.connects[0].broke_distance / 1000) * 100) / distance
      this.percentile = this.percentile.toString() + '%'
      this.connects[0]['broken_percentile'] = this.percentile
      // console.log(this.connects[x])
      // console.log(this.connects[1].broke_distance)
    },
    getDistance (slat, slng, flat, flng) {
      var R = 6371
      var dLat = (flat - slat) * (Math.PI / 180)
      var dLng = (flng - slng) * (Math.PI / 180)
      var a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(slat * (Math.PI / 180)) * Math.cos(flat * (Math.PI / 180)) *
        Math.sin(dLng / 2) * Math.sin(dLng / 2)
      var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
      var d = R * c
      return d
      // console.log(d)
    },
    checkBroken (index) {
      // console.log(this.chkBroken)
      // console.log(this.history[index].id)
      // console.log(this.history[index].distance)
      this.axios.get('https://fibermap.herokuapp.com/updatehistory', {
        params: {
          id: this.history[index].id,
          line_id: this.history[index].line_id,
          distance: this.history[index].distance,
          broken_time: this.history[index].broken_time,
          status_broken: parseInt(this.chkBroken),
          userid: this.user.id,
          A: this.infoContent.A,
          B: this.infoContent.B
        }
      })
        .then(response => {
          this.loadHistory('All Time')
        })
    },
    saveHistory () {
      if(this.infoline.gmap_distance == null) {
        alert('Please add real path before add break point.')
      } else {
        if (this.distance >= this.infoline.gmap_distance) {
          alert('Please input distance less then Gmap distance.')
        } else {
          this.axios.get('https://fibermap.herokuapp.com/savehistory', {
            params: {
              id: this.infoContent.id,
              A: this.infoContent.A,
              B: this.infoContent.B,
              distance: this.distance,
              userid: this.user.id
            }
          })
          .then(response => {
            window.alert('Added break point.')
            this.$router.go(this.$router.currentRoute)
            this.distance = ''
          })
        }
      }
    },
    loadHistory (dateString) {
      this.dateHistory = dateString
      this.axios
        .get('https://fibermap.herokuapp.com/loadhistory', {
          params: {
            id: this.infoContent.id
          }
        })
        .then(response => {
          this.history = response.data.data
          this.chkBroken = null
        })
    },
    filterHistory (value, dateString) {
      this.dateHistory = dateString
      this.axios
        .get('https://fibermap.herokuapp.com/filterhistory', {
          params: {
            id: this.infoContent.id,
            date: value
          }
        })
        .then(response => {
          this.history = response.data.data
          this.dateHistory = response.data.date.fromDate + ' - ' + response.data.date.toDate
        })
    },
    filterHistory2 () {
      this.dateHistory = this.fDate + ' - ' + this.tDate
      this.axios
        .get('https://fibermap.herokuapp.com/filterhistory2', {
          params: {
            id: this.infoContent.id,
            fromDate: this.fDate,
            toDate: this.tDate
          }
        })
        .then(response => {
          this.history = response.data
          this.dateHistory = this.fDate + ' - ' + this.tDate
        })
    },
    downloadHistory (history) {
      let broken
      let distance
      let status
      let fixed
      let user
      if (history.length !== 0) {
        for (let i = 0; i < history.length; i++) {
          if (broken === undefined) {
            broken = history[i].broken_time.toString()
            distance = history[i].distance.toString() + ' m'
            user = history[i].approved_by.toString()
            if (parseInt(history[i].status_broken) === 0) {
              status = 'ซ่อมแซมแล้ว'
              fixed = history[i].timestamp.toString()
            } else if (parseInt(history[i].status_broken) === 1) {
              status = 'รอการซ่อมแซม'
              fixed = '-'
            } else if (parseInt(history[i].status_broken) === 2) {
              status = 'กำลังดำเนินการ'
              fixed = '-'
            } else if (parseInt(history[i].status_broken) === 3) {
              status = 'รอการยืนยัน'
              fixed = '-'
            }
          } else {
            broken = broken + '\n' + history[i].broken_time.toString()
            distance = distance + '\n' + history[i].distance.toString() + ' m'
            user = user + '\n' + history[i].approved_by.toString()
            if (parseInt(history[i].status_broken) === 0) {
              status = status + '\n' + 'ซ่อมแซมแล้ว'
              fixed = fixed + '\n' + history[i].timestamp.toString()
            } else if (parseInt(history[i].status_broken) === 1) {
              status = status + '\n' + 'รอการซ่อมแซม'
              fixed = fixed + '\n' + '-'
            } else if (parseInt(history[i].status_broken) === 2) {
              status = status + '\n' + 'กำลังดำเนินการ'
              fixed = fixed + '\n' + '-'
            } else if (parseInt(history[i].status_broken) === 3) {
              status = status + '\n' + 'รอการยืนยัน'
              fixed = fixed + '\n' + '-'
            } 
          }
        }
        let docDefinition = {
          content: [
            {text: 'History [' + this.dateHistory + ']', style: 'header', fontSize: 30},
            history[0].comment,
            {
              layout: 'lightHorizontalLines', // optional
              table: {
                // headers are automatically repeated if the table spans over multiple pages
                // you can declare how many rows should be treated as headers
                headerRows: 1,
                widths: [ 'auto', 'auto', 'auto', 'auto', 'auto' ],

                body: [
                  [ 'วันที่ขาด', 'ระยะที่ขาด', 'สถานะ', 'วันที่ซ่อมแซม', 'ผู้แจ้ง/ผู้ยืนยัน' ],
                  [ broken, distance, status, fixed, user ]
                ]
              }
            }
          ],
          defaultStyle: {
            font: 'THSarabunNew',
            fontSize: 18
          }
        }
        pdfMake.createPdf(docDefinition).download(history[0].comment + ' [' + this.dateHistory + '].pdf')
      } else {
        window.alert('สายยังไม่เคยชำรุด')
      }
    },
    showLayer (value, e) {
      if (value === 'all') {
        this.getSwitch()
        this.getConnect()
      }
      if (value === 'coretocore') {
        this.switchs = []
        this.connects = []
        this.axios
          .get('https://fibermap.herokuapp.com/showlayerRP')
          .then(response => {
            this.switchs = response.data[0].switch
            this.connects = response.data[0].connect
            this.showBroken()
          })
      }
      if (value === 'zone') {
        this.switchs = []
        this.connects = []
        this.axios
          .get('https://fibermap.herokuapp.com/showzoneRP', {
            params: {
              zone: e
            }
          })
          .then(response => {
            for (let i = 0; i < response.data[0].switch.length; i++) {
              if (e === response.data[0].switch[i].id) {
                this.center = response.data[0].switch[i].position
              }
            }
            this.switchs = response.data[0].switch
            this.connects = response.data[0].connect
            this.showBroken()
          })
      }
    },
    backToMap () {
      this.$router.go(-1)
    },
    zoomMap (pos, obj) {
      if (obj === 'marker') {
        this.center = pos
        this.zoom = 18
      } else if (obj === 'line') {
        this.center = pos
        this.zoom = 17
      }
    },
    updateZoom (zoom) {
      // console.log(zoom)
      this.zoom = zoom
    },
    updateCenter (center) {
      this.center = {
        lat: center.lat(),
        lng: center.lng()
      }
    },
    routeStreetView () {
      // location.href = 'http://maps.google.com/maps?q=&layer=c&cbll=' + this.mousePos.lat + ',' + this.mousePos.lng
      window.open('http://maps.google.com/maps?q=&layer=c&cbll=' + this.mousePos.lat + ',' + this.mousePos.lng, '_blank')
    },
    posMouse (pos) {
      this.mousePos = {
        lat: pos.latLng.lat(),
        lng: pos.latLng.lng()
      }
    },
    showTable (value) {
      // console.log(value)
      if (value === 'switch') {
        this.isTableMarker = true
        this.isTableLine = false
      } else if (value === 'line') {
        this.isTableMarker = false
        this.isTableLine = true
      }
    },
    showByStatus (value, e) {
      // console.log(value)
      // console.log(e)
      if (value === 'all') {
        this.getSwitch()
        this.getConnect()
      }
      if (value === 'updown') {
        if (e === 1) {
          this.switchs = []
          this.connects = []
        }
        this.axios
          .get('https://fibermap.herokuapp.com/showbystatusRP', {
            params: {
              status: e
            }
          })
          .then(response => {
            // console.log(response.data[0].switch);
            this.switchs = response.data[0].switch
            this.connects = response.data[0].connect
          })
      }
    },
    toggleInfoWindow (marker, idx) {
      this.infoOptions.pixelOffset.height = -20
      this.infoWindowPos = marker.position
      this.infoContent = marker
      this.center = marker.position
      this.infoWinOpen = true
      this.currentMidx = idx
      this.infoMarker = true
      this.infoPolyline = false
    },
    toggleInfoWindow2 (line, idx, e) {
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
      this.getInfoline(line.id)
    },
    getMapToRealpath () {
      this.axios
        .get('https://fibermap.herokuapp.com/realpathbyid', {
          params: {
            lineid: this.$route.query.lineid
          }
        })
        .then(response => {
          this.switchs = response.data[0].switch
          this.connects = response.data[0].connect
          this.imageMarker()
          this.showBroken()
          // console.log(this.switchs)
        })
    },
    getInfoline (lineid) {
      this.axios
        .get('https://fibermap.herokuapp.com/getinfoline', {
          params: {
            line_id : lineid
          }
        })
        .then(response => {
          // console.log(response.data)
          this.infoline = response.data
        })
    },
    getCPU (value) {
      console.log(value)
      this.axios.get('https://fibermap.herokuapp.com/getcpu', {
        params: {
          device_id: value.id
        }
      })
      .then(response => {
        this.showBW = false
        this.showCPU = true
        if(this.showCPU == true) {
          this.cpu_usage = response.data
          this.$refs.chartCPU.renewGraph()
          this.$refs.chartCPU.startGraph(this.cpu_usage)
        }
        this.showModal = true  
      })
    },
    getBandwidth (value) {
      console.log(value)

      this.axios.get('https://fibermap.herokuapp.com/getallbw', {
        params: {
          name: value.A,
          type_port: value.port_A
        }
      })
      .then(response => {
        this.showBW = true
        this.showCPU = false
        if (this.showBW == true) {
          this.bandwidth_usage = response.data
          this.$refs.chartBW.renewGraph()
          this.$refs.chartBW.startGraph(this.bandwidth_usage)
        }
        this.showModal = true    
      })
    },
    fillData (val, date) {
      this.datacollection = {
        labels: date,
        datasets: [
          {
            label: 'CPU Usage (%)',
            backgroundColor: '#f87979',
            data: val
          }
        ]
      }
    },
    filterChart (val) {
      if (val === 0) {
        this.fillData(this.cpu_usage.day.cpu, this.date_usage.day.time)
      } else if (val === 1) {
        this.fillData(this.cpu_usage.month.cpu, this.date_usage.month.time)
      } else if (val === 2) {
        this.fillData(this.cpu_usage.year.cpu, this.date_usage.year.time)
      }
    },
    getDataUser () {
      this.user.id = sessionStorage.getItem('iduser')
      this.user.username = sessionStorage.getItem('username')
      this.user.firstname = sessionStorage.getItem('firstname')
      this.user.lastname = sessionStorage.getItem('lastname')
      this.user.tel = sessionStorage.getItem('tel')
      this.user.email = sessionStorage.getItem('email')
      this.user.isAdmin = sessionStorage.getItem('isAdmin') === 'true'
      this.user.isLogin = sessionStorage.getItem('isLogin') === 'true'
    }
  },
  created: function () {
    this.getMapToRealpath()
    this.getDataUser()
    // var eiei = this.$route.query.lineid
    // console.log(parseInt(eiei))
    // console.log(this.$route)
  },
  computed: {
    filterData () {
      return this.switchs.filter(sw => {
        return sw.name.match(this.search)
      })
    }
  },
  mounted: function () {
    if (navigator.geolocation) {
      var self = this
      navigator.geolocation.getCurrentPosition(function (position) {
        self.myLocation = position.coords
        self.markers[0].position.lat = position.coords.latitude
        self.markers[0].position.lng = position.coords.longitude
        // console.log(position.coords.latitude)
        // console.log(position.coords.longitude)
        // console.log(self.myLocation)
      })
    }
  }
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