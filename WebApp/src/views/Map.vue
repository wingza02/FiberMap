<template>
  <div id="app">
    <!-- <nav class="navbar navbar-inverse navbar-fixed-top">
        <div class="container-fluid">
      <div class="navbar-header">
        <a class="navbar-brand" href="#"><h4>Fiber Map</h4></a>
      </div>
      <ul class="nav navbar-nav">
        <li class="active"><a href="#"><h4>Monitor</h4></a></li>
        <li><a href="#"><h4>Real Path</h4></a></li>
      </ul>
      <ul class="nav navbar-nav navbar-right">
        <li><a href="#"><h4><span class="glyphicon glyphicon-log-in"></span> Login</h4></a></li>
      </ul>
    </div>
     </nav> -->
   
    <!-- map -->
    <gmap-map :center="center" @zoom_changed="updateZoom" @center_changed="updateCenter" :zoom="zoom" style="width: 65%; height: 550px; float: left;">

<!-- Marker+InfoWindow @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ -->
    <gmap-info-window :options="infoOptions" :position="infoWindowPos" :opened="infoWinOpen" @closeclick="infoWinOpen=false" v-if="infoMarker">
        Name: {{infoContent.name}}<br>
        <font v-if="user.isAdmin==true">IP: {{ infoContent.ip }} </font>
        <!-- IP: {{infoContent.ip}}<br> -->
        <p v-if="infoContent.uptime=='0:00:00'">Status: Down <br> Uptime: 0:00:00 Hours</p>
        <p v-else>Status: Up <br> Uptime: {{ infoContent.uptime }} Hours</p>
        <a href="#" @click="zoomMap(infoWindowPos,'marker')">Zoom</a> <font v-if="user.isLogin==true&&user.isAdmin==true">|| </font>
        <font v-if="user.isLogin==true&&user.isAdmin==true"><a href="#" data-toggle="modal" data-target="#graphCPU" @click="getCPU(infoContent)">Graph</a> </font> <!--|| <a data-toggle="modal" data-target="#myModal">History</a> -->
    </gmap-info-window> 
    <gmap-marker
      :key="index"
      v-for="(m, index) in switchs"
      :title="m.name"
      :position="m.position"
      :clickable="true"
      :draggable="false"
      :icon="m.image"
      @click="toggleInfoWindow(m,index)"
    ></gmap-marker>


    <!-- <gmap-polyline
      :key="index"
      v-for="(p, index) in connects"
      :position="p.position"
      :path="p.path"
      :clickable="true"
      @click="toggleInfoWindow(pl,i)"
    ></gmap-polyline> -->
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
        <a href="#" @click="focusLine(infoContent.id)">Focus</a> || 
        <a href="#" @click="unfocusLine()">UnFocus</a> || 
        <a href="#" @click="toRealpath()">RealPath</a> 
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


    <div style="display: inline-block; margin-left: 10px; width: 30%; height:100%">
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

      <!-- <div class="modal" id="graphCPU" tabindex="-1" role="dialog" aria-labelledby="graphCPU" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h2 class="modal-title" id="graphCPU">CPU Graph</h2>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <div v-show="showCPU"><chart-report id="2020" ref="chartCPU" :id="infoContent.id" ></chart-report></div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      </div>

      <div class="modal" id="graphBW" tabindex="-1" role="dialog" aria-labelledby="graphBW" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h2 class="modal-title" id="graphBW">Bandwidth Graph</h2>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <div v-show="showBW"><chart-b-w id="eiei" ref="chartBW"></chart-b-w></div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      </div> -->

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
        url:''
      },
      zoom: 16,
      center: { lat: 18.79686, lng: 98.9537475 },
      mousePos: { lat: 18.79686, lng: 98.9537475 },
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
      chkBroken: 1,
      cpu_usage: [],
      bandwidth_usage: [],
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
          // console.log(response.data)
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
        this.axios
          .get('https://fibermap.herokuapp.com/showlayer')
          .then(response => {
            // console.log(response.data[0].switch);
            this.switchs = response.data[0].switch
            this.connects = response.data[0].connect
            this.imageMarker()
          })
      }
      if (value === 'zone') {
        // console.log(e)
        this.axios
          .get('https://fibermap.herokuapp.com/showzone', {
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
            // console.log(response.data[0])
            this.switchs = response.data[0].switch
            this.connects = response.data[0].connect
            this.imageMarker()
          })
      }
    },
    focusLine (value) {
      this.axios
        .get('https://fibermap.herokuapp.com/connectbyid', {
          params: {
            id: value
          }
        })
        .then(response => {
          // console.log(response.data[0].switch)
          this.switchs = response.data[0].switch
          this.connects = response.data[0].connect
          this.imageMarker()
        })
    },
    unfocusLine () {
      this.getSwitch()
      this.getConnect()
    },
    toRealpath () {
      // console.log(this.$route)
      // this.$route.go(1)
      let hostname
      let protocol = location.protocol
      if (location.hostname === 'localhost') {
        hostname = location.host
      } else {
        hostname = location.hostname
      }
      location.href = '' + protocol + '//' + hostname + '/#/maptoreal?lineid=' + this.infoContent.id + '&lat=' + this.mousePos.lat + '&lng=' + this.mousePos.lng
      // console.log(this.infoContent.id)
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
        this.axios
          .get('https://fibermap.herokuapp.com/showbystatus', {
            params: {
              status: e
            }
          })
          .then(response => {
            // console.log(response.data[0].switch);
            this.switchs = response.data[0].switch
            this.connects = response.data[0].connect
            this.imageMarker()
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
        midLat = (line.path[0].lat + line.path[1].lat) / 2
        midLng = (line.path[0].lng + line.path[1].lng) / 2
        this.center = { lat: midLat, lng: midLng }
      }
      // console.log(line.id)
      this.infoWindowPos = { lat: midLat, lng: midLng }
      this.infoContent = line
      this.infoWinOpen = true
      this.currentMidx = idx
      this.infoPolyline = true
      this.infoMarker = false
      this.getInfoline(line.id)
    },
    getSwitch () {
      this.axios
        .get('https://fibermap.herokuapp.com/getswitch')
        .then(response => {
          // console.log(response.data[0].name)
          this.switchs = response.data
          this.imageMarker()
        })
    },
    getConnect () {
      this.axios
        .get('https://fibermap.herokuapp.com/connect')
        .then(response => {
          // console.log(response.data)
          this.connects = response.data
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
    this.getSwitch()
    this.getConnect()
    this.getDataUser()
  },
  computed: {
    filterData () {
      return this.switchs.filter(sw => {
        return sw.name.match(this.search)
      })
    }
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

