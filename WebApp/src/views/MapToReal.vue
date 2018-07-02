<template>
  <div id="app">

<!-- Map -->
    <gmap-map :center="center" @zoom_changed="updateZoom" @center_changed="updateCenter" :zoom="zoom" mapTypeId="hybrid" style="width: 100%; height: 550px; float: left;">

      <gmap-info-window :options="infoOptions" :position="infoWindowPos" :opened="infoWinOpen" @closeclick="infoWinOpen=false" v-if="infoMarker">
        Name: {{infoContent.name}}<br>
        <font v-if="user.isAdmin==true">IP: {{ infoContent.ip }} </font> <br>
        <font v-if="user.isAdmin==true">Model: {{ infoContent.model }} </font> <br>
        <font v-if="infoContent.uptime=='0:00:00'">Status: Down <br> Uptime: 0:00:00 Hours</font>
        <font v-else>Status: Up <br> Uptime: {{ infoContent.uptime }} Hours</font>
        <p>Comment: {{this.showHistorySW}}</p>
        <a href="#" @click="zoomMap(infoWindowPos,'marker')">Zoom</a> <font v-if="user.isLogin==true&&user.isAdmin==true">|| </font>
        <font v-if="user.isLogin==true&&user.isAdmin==true"> <a href="#" data-toggle="modal" data-target="#HistorySW">History</a> || </font>
        <font v-if="user.isLogin==true&&user.isAdmin==true"> <a href="#" data-toggle="modal" data-target="#ProblemSW">Comment</a>  </font>
        <!-- <font v-if="user.isLogin==true&&user.isAdmin==true"><a href="#" data-toggle="modal" data-target="#graphCPU" @click="getCPU(infoContent)">Graph</a> </font>  -->
      </gmap-info-window>

<!-- Switch Marker -->
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

<!-- My Location Marker -->
      <gmap-marker
        :position="myLocation"
        :clickable="false"
        :draggable="false"
        :icon="image1.url">
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
        <!-- <font v-if="user.isLogin==true&&user.isAdmin==true"><a href="#" data-toggle="modal" data-target="#graphBW" @click="getBandwidth(infoContent)">Graph</a> || </font>  -->
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

<!-- Modal History Path -->
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

<!-- Modal Add Point Break Path--> 
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

<!-- Modal Comment Switch -->
      <div class="modal" id="ProblemSW" tabindex="-1" role="dialog" aria-labelledby="ProblemSW" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h2 class="modal-title" id="ProblemSW">Comment Switch : {{infoContent.name}}</h2>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <h3>
                <label for="comment">Comment:</label>
                <textarea class="form-control" rows="5" id="comment" v-model="commentSW"></textarea>
                <button type="button" class="btn btn-primary" data-dismiss="modal" @click="saveHistorySW" style="float: right;">Add</button>
              </h3>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            </div>
          </div>
        </div>

<!-- Modal History Switch -->
      </div><div class="modal" id="HistorySW" tabindex="-1" role="dialog" aria-labelledby="HistorySW" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h2 class="modal-title" id="HistorySW">History Switch : {{infoContent.name}}</h2>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <h3 v-for="(h,index) in historySW" :key="h.id">{{h.register_time}} - {{h.comment}} - {{h.approved_by}}</h3>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      </div>

<!-- Modal Graph CPU & Bandwidth -->
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
// Import other function from .. file
import modal from './modal'
import ChartReport from './ChartReport'
import ChartBW from './ChartBW'

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
  name: 'MapToReal',
  components: {
    ChartReport,
    ChartBW,
    modal
  },
  data () {
    return {
      image: {
        // url: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png'
      },
      image1: {
        url: 'http://fibermap.cmu.ac.th/img/me.png'
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
      switchs: [],
      connects: [],
      distance: '',
      history: [{ comment: '' }],
      dateHistory: 'All Time',
      fDate: '',
      tDate: '',
      chkBroken: 1,
      commentSW: '',
      historySW: [],
      showHistorySW: '',
      myLocation: {'lat': 0, 'lng': 0},
      showModal: false,
      user: [],
      infoline: [],
      showCPU: false,
      showBW: false
    }
  },
  methods: {
    imageMarker() {                                       // Change Image Marker
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
    showBroken () {                                       // Show Break point on Map
      this.axios
        .get('https://fibermap-api.cmu.ac.th/getbroken', {
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
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
    calDistance () {                                       // Calculate polyline distance on Map
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
    getDistance (slat, slng, flat, flng) {                                       // Get distance between 2 point
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
    saveHistorySW () {                                       // Save comment switch
      // console.log(this.infoContent.id)
      this.axios.get('https://fibermap-api.cmu.ac.th/savehistorysw', {
        params: {
          id: this.infoContent.id,
          comment: this.commentSW.toString(),
          userid: this.user.id
        },
        headers: {'Authorization': sessionStorage.getItem('token')}
      })
      .then(response => {
        window.alert('Added comment for this switch.')
        this.$router.go(this.$router.currentRoute)
        this.commentSW = ''
      })
    },
    loadHistorySW () {                                       // Load comment switch
      this.axios
        .get('https://fibermap-api.cmu.ac.th/loadhistorysw', {
          params: {
            id: this.infoContent.id
          },
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          // console.log(response.data.data)
          this.historySW = response.data.data
          if(this.historySW.length != 0) {
            this.showHistorySW = this.historySW[0].comment
          }
          else {
            this.showHistorySW = ''
          }
        })
    },
    checkBroken (index) {                                       // Update status of path in history modal
      // console.log(this.chkBroken)
      // console.log(this.history[index].id)
      // console.log(this.history[index].distance)
      this.axios.get('https://fibermap-api.cmu.ac.th/updatehistory', {
        params: {
          id: this.history[index].id,
          line_id: this.history[index].line_id,
          distance: this.history[index].distance,
          broken_time: this.history[index].broken_time,
          status_broken: parseInt(this.chkBroken),
          userid: this.user.id,
          A: this.infoContent.A,
          B: this.infoContent.B
        },
        headers: {'Authorization': sessionStorage.getItem('token')}
      })
        .then(response => {
          this.loadHistory('All Time')
        })
    },
    saveHistory () {                                       // Save history path
      if(this.infoline.gmap_distance == null) {
        alert('Please add real path before add break point.')
      } else {
        if (this.distance >= this.infoline.gmap_distance) {
          alert('Please input distance less then Gmap distance.')
        } else {
          this.axios.get('https://fibermap-api.cmu.ac.th/savehistory', {
            params: {
              id: this.infoContent.id,
              A: this.infoContent.A,
              B: this.infoContent.B,
              distance: this.distance,
              userid: this.user.id
            },
            headers: {'Authorization': sessionStorage.getItem('token')}
          })
          .then(response => {
            window.alert('Added break point.')
            this.$router.go(this.$router.currentRoute)
            this.distance = ''
          })
        }
      }
    },
    loadHistory (dateString) {                                       // Load history path
      this.dateHistory = dateString
      this.axios
        .get('https://fibermap-api.cmu.ac.th/loadhistory', {
          params: {
            id: this.infoContent.id
          },
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          this.history = response.data.data
          this.chkBroken = null
        })
    },
    filterHistory (value, dateString) {                                       // Filter history by button
      this.dateHistory = dateString
      this.axios
        .get('https://fibermap-api.cmu.ac.th/filterhistory', {
          params: {
            id: this.infoContent.id,
            date: value
          },
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          this.history = response.data.data
          this.dateHistory = response.data.date.fromDate + ' - ' + response.data.date.toDate
        })
    },
    filterHistory2 () {                                       // Filter history by range in calendar
      this.dateHistory = this.fDate + ' - ' + this.tDate
      this.axios
        .get('https://fibermap-api.cmu.ac.th/filterhistory2', {
          params: {
            id: this.infoContent.id,
            fromDate: this.fDate,
            toDate: this.tDate
          },
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          this.history = response.data
          this.dateHistory = this.fDate + ' - ' + this.tDate
        })
    },
    downloadHistory (history) {                                       // Download history to pdf
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
    showLayer (value, e) {                                       // Filter by Layer on top of table
      if (value === 'all') {                                       // All
        this.getSwitch()
        this.getConnect()
      }
      if (value === 'coretocore') {                                       // core-core
        this.switchs = []
        this.connects = []
        this.axios
          .get('https://fibermap-api.cmu.ac.th/showlayerRP', {
            headers: {'Authorization': sessionStorage.getItem('token')}
          })
          .then(response => {
            this.switchs = response.data[0].switch
            this.connects = response.data[0].connect
            this.showBroken()
          })
      }
      if (value === 'zone') {                                       // zone
        this.switchs = []
        this.connects = []
        this.axios
          .get('https://fibermap-api.cmu.ac.th/showzoneRP', {
            params: {
              zone: e
            },
            headers: {'Authorization': sessionStorage.getItem('token')}
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
    backToMap () {                                       // Go to previous page
      this.$router.go(-1)
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
    showByStatus (value, e) {                                       // Filter by status
      // console.log(value)
      // console.log(e)
      if (value === 'all') {                                       // All
        this.getSwitch()
        this.getConnect()
      }
      if (value === 'updown') {                                       // Up or Down
        if (e === 1) {
          this.switchs = []
          this.connects = []
        }
        this.axios
          .get('https://fibermap-api.cmu.ac.th/showbystatusRP', {
            params: {
              status: e
            },
            headers: {'Authorization': sessionStorage.getItem('token')}
          })
          .then(response => {
            // console.log(response.data[0].switch);
            this.switchs = response.data[0].switch
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
      this.loadHistorySW()
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
      this.getInfoline(line.id)
    },
    getMapToRealpath () {                                       // Get switch and polyline from DB
      this.axios
        .get('https://fibermap-api.cmu.ac.th/realpathbyid', {
          params: {
            lineid: this.$route.query.lineid
          },
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          this.switchs = response.data[0].switch
          this.connects = response.data[0].connect
          this.imageMarker()
          this.showBroken()
        })
    },
    getInfoline (lineid) {                                       // Get information for that path
      this.axios
        .get('https://fibermap-api.cmu.ac.th/getinfoline', {
          params: {
            line_id : lineid
          },
          headers: {'Authorization': sessionStorage.getItem('token')}
        })
        .then(response => {
          // console.log(response.data)
          this.infoline = response.data
        })
    },
    getCPU (value) {                                       // Show Graph CPU
      console.log(value)
      this.axios.get('https://fibermap-api.cmu.ac.th/getcpu', {
        params: {
          device_id: value.id
        },
        headers: {'Authorization': sessionStorage.getItem('token')}
      })
      .then(response => {
        this.showBW = false
        this.showCPU = true
        if(this.showCPU == true) {
          this.$refs.chartCPU.renewGraph()
          this.$refs.chartCPU.startGraph(response.data)
        }
        this.showModal = true  
      })
    },
    getBandwidth (value) {                                       // Show Graph Bandwidth
      this.axios.get('https://fibermap-api.cmu.ac.th/getallbw', {
        params: {
          name: value.A,
          type_port: value.port_A
        },
        headers: {'Authorization': sessionStorage.getItem('token')}
      })
      .then(response => {
        this.showBW = true
        this.showCPU = false
        if (this.showBW == true) {
          this.$refs.chartBW.renewGraph()
          this.$refs.chartBW.startGraph(response.data)
        }
        this.showModal = true    
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
    this.getMapToRealpath()
    this.getDataUser()
    // var eiei = this.$route.query.lineid
    // console.log(parseInt(eiei))
    // console.log(this.$route)
  },
  mounted: function () {                                       // Run these function when stay in page
    if (navigator.geolocation) {
      var self = this
      navigator.geolocation.getCurrentPosition(function (position) {
        self.myLocation.lat = position.coords.latitude
        self.myLocation.lng = position.coords.longitude
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