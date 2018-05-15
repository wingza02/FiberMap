<template>
    <div>
      <div class="example" id='chart'>
        <h3>Select Date</h3>
        <datepicker id='chart1' placeholder="Select Date" v-model="vModelExample" v-on:selected="Gengraph" ></datepicker>
      <!-- <p>{{ vModelExample }}</p> -->
    </div>

    <div class="example" id='chart'>
      <h3>Months</h3>
      <datepicker id='chart1' :minimumView="'month'" :maximumView="'month'" :format="'MMMM yyyy'" placeholder="Select Month" v-on:selected="Gengraphmonth"  ></datepicker>
    </div>

    <div class="example" id='chart'>
      <h3>Years</h3>
      <datepicker id='chart1' :minimumView="'year'" :maximumView="'year'" :format="'yyyy'" placeholder="Select Year" v-on:selected="Gengraphyear"  ></datepicker>
    </div>

    <canvas id="planet-chart"></canvas>
    </div>
</template>

<script>
import moment,{ months } from 'moment';
import Datepicker from 'vuejs-datepicker';

export default {
  components: {
    Datepicker,
  },
  props: ['data', 'chartData','id'],
  data() {
    return {
      info: null,
      Modelmonth: null,
      chart: null,
      vModelExample: moment.now( ) 
    }
  },
  methods: {
    renewGraph () {
      this.info = null
      this.Modelmonth = null
      if(this.chart != null) {
        this.chart.destroy()
      }
      this.vModelExample = moment.now( ) 
    },
    startGraph(eiei) {
      console.log(eiei)
      var labelstart = ["00.00","01.00","02.00","03.00","04.00","05.00","06.00","07.00","08.00","09.00","10.00",
                      "11.00","12.00","13.00","14.00","15.00","16.00","17.00","18.00","19.00","20.00","21.00","22.00","23.00"];
    const planetChartData = {
            type: 'line',
            data: {
              labels: labelstart,
              datasets: [
                { // one line graph
                  label: 'CPU USED(%)',
                  type: 'line',
                  data: [],
                  backgroundColor: [
                    'rgba(54,73,93,.5)', // Blue
                    'rgba(54,73,93,.5)',
                    'rgba(54,73,93,.5)',
                    'rgba(54,73,93,.5)',
                    'rgba(54,73,93,.5)',
                    'rgba(54,73,93,.5)',
                    'rgba(54,73,93,.5)',
                    'rgba(54,73,93,.5)'
                  ],
                  borderColor: [
                    '#36495d',
                    '#36495d',
                    '#36495d',
                    '#36495d',
                    '#36495d',
                    '#36495d',
                    '#36495d',
                    '#36495d',
                  ],
                  borderWidth: 3
                }
                
              ]
            },
            options: {
              responsive: true,
              lineTension: 1,
              scales: {
                yAxes: [{
                  ticks: {
                    beginAtZero: true,
                    padding: 20,
                  }
                }]
              }
            }
          }
          // console.log(response.data);
          this.createChart('planet-chart', planetChartData);
    // this.axios
    //     .get("https://fibermap.herokuapp.com/getallcpu")
    //     .then(response => {
    //       this.info = response.data;
    //       this.Gengraph()
    //     })
        // this.info = [{"id": 2,"device_id": 1,"cpu": "5","timestamp": "2018-03-31 04:50:46"}]
        this.info = eiei
        this.Gengraph()
    },
  createChart(chartId, chartData) {
    const ctx = document.getElementById(chartId);
    const myChart = new Chart(ctx, {
      type: chartData.type,
      data: chartData.data,
      options: chartData.options,
    });
    this.chart = myChart
    }
  ,
  updateData(data) {
    this.chart.data.datasets[0].data = data;
    this.chart.update();
  },
  updatelabel(label){
    this.chart.data.labels = label;
    this.chart.update();
  },
  Gengraph(e) {
          console.log(e)
          var datepick = moment(e);
          var monthpick = moment(e);
          var yearpick = moment(e);
          // var monthpickplus = monthpick.month() +1;
          console.log(datepick.date())
          console.log(monthpick.month())
          // console.log(monthpickplus)
          console.log(yearpick.year())
          // function isDate(element) {
          //   return moment(element.timestamp).date() == 31 && moment(element.timestamp).hour() == 13 && 
          //   moment(element.timestamp).minute() == 50  ;
          // }
          // var filtered = response.data.filter(isDate);
          //Device == 1
          
          var devictest = this.id;
          function isDevice(element) {
            return element.device_id == devictest ;
          }
          var filtereddevice = this.info.filter(isDevice);
          //console.log(filtereddevice)
          // function inDay31(element) {
          //   return moment(element.timestamp).date() == 31 ;
          // }
          // var hours13 = response.data.filter(inDay31);
          // //console.log(hours13)
          // var hr13 = hours13.map((hours13) => hours13.cpu)
          // //console.log(hr13)
          // var sumhr13 = 0;
          // var hhr13 = hr13.map(Number)
          // //var arrayOfNumbers = arrayOfStrings.map(Number);
          // for(var i in hhr13){ 
          //     if(hr13[i] != "NOSUCHINSTANCE"){
          //       sumhr13 += hhr13[i];
          //     }
          //    }
          // var avghr13 = sumhr13/(hr13.length) 
          // console.log(avghr13)
          var In1day = []; // all data in each hr
          var In1dayhr = []; // all avg cpu in each hr
          var In1dayhrr = []; // all cpu in each hr
          //filter day/month/year
          function inDaymonthyear(element) {
            return moment(element.timestamp).date() == datepick.date() && moment(element.timestamp).month() == monthpick.month() &&
            moment(element.timestamp).year() == yearpick.year() ;
          }
          var Daymonthyear = filtereddevice.filter(inDaymonthyear);
          var daymonyear = Daymonthyear.map((Daymonthyear) => Daymonthyear.cpu)
          //filter each hr
          for(var i=0; i < 24 ; i++){
              function inHr(element) {
                return moment(element.timestamp).hour() == i ;
              }
              In1day[i] = Daymonthyear.filter(inHr);
              
          }
          //Filter month 
          function inMonth(element) {
            return moment(element.timestamp).month() == monthpick.month() ;
          }
         
         //Avg cpu each hr
          for(var i=0; i < 24 ; i++){ //loop 24hr
            if(In1day[i].length !=0){      
              var aa = In1day[i].map(Inday => parseInt(Inday.cpu))
              In1dayhrr.push(aa);// push cpu in array of cpu in each hr
                var sumaa = 0;
                for(var k=0; k<aa.length;k++){ //loop in each array to sum cpu
                  sumaa += aa[k]; 
                  
                }
                sumaa = sumaa/aa.length ; 
                In1dayhr.push(sumaa); //push Avg cpu in array of cpu in each hr
              }
            else{
              In1dayhrr[i] = 0;
              In1dayhr[i] = 0;
            } 
          }
          // console.log(sumaa)
          console.log(In1dayhrr)
          console.log(In1dayhr)
          
          //console.log(Day31)
          //console.log(day31)
          // var sumhr13 = 0;
          // var hhr13 = hr13.map(Number)
          
          // for(var i in hhr13){ 
          //     if(hr13[i] != "NOSUCHINSTANCE"){
          //       sumhr13 += hhr13[i];
          //     }
          //    }
          // var avghr13 = sumhr13/(hr13.length) 
          // console.log(avghr13)
          // var cpu = response.data.map((filtered) => filtered.cpu) 
          // var cpu = filtered.map((filtered) => filtered.cpu) 
          // var time = filtered.map((filtered) => filtered.timestamp)
          //console.log(cpu)
          //console.log(time)
          
          var label = ["00.00","01.00","02.00","03.00","04.00","05.00","06.00","07.00","08.00","09.00","10.00",
                      "11.00","12.00","13.00","14.00","15.00","16.00","17.00","18.00","19.00","20.00","21.00","22.00","23.00"];
          this.updatelabel(label) //update label
          this.updateData(In1dayhr)
          
          
        },
    Gengraphmonth(m) {
          var devictest = this.id;
          console.log(m)
          // var datepick = moment(e);
          var monthpick = moment(m);
          var yearpick = moment(m);
          // var yearpick = moment(e);
          // var monthpickplus = monthpick.month() +1;
          // console.log(datepick.date())
          console.log(monthpick.month())
          // console.log(monthpickplus)
          // console.log(yearpick.year())
          // function isDate(element) {
          //   return moment(element.timestamp).date() == 31 && moment(element.timestamp).hour() == 13 && 
          //   moment(element.timestamp).minute() == 50  ;
          // }
          // var filtered = response.data.filter(isDate);
          //Device == 1
          
          
          function isDevice(element) {
            return element.device_id == devictest ;
          }
          var filtereddevice = this.info.filter(isDevice);
          //console.log(filtereddevice)
          // function inDay31(element) {
          //   return moment(element.timestamp).date() == 31 ;
          // }
          // var hours13 = response.data.filter(inDay31);
          // //console.log(hours13)
          // var hr13 = hours13.map((hours13) => hours13.cpu)
          // //console.log(hr13)
          // var sumhr13 = 0;
          // var hhr13 = hr13.map(Number)
          // //var arrayOfNumbers = arrayOfStrings.map(Number);
          // for(var i in hhr13){ 
          //     if(hr13[i] != "NOSUCHINSTANCE"){
          //       sumhr13 += hhr13[i];
          //     }
          //    }
          // var avghr13 = sumhr13/(hr13.length) 
          // console.log(avghr13)
          var In1month = []; // all data in each month
          var In1day = []; // all avg cpu in each day
          var In1dayy = []; // all cpu in each day
          //filter day/month/year
          function inDaymonth(element) {
            return moment(element.timestamp).month() == monthpick.month() && moment(element.timestamp).year() == yearpick.year();
          }
          var Daymonth = filtereddevice.filter(inDaymonth);
         
          console.log(Daymonth)
         
          var month31 = [0,2,4,6,7,9,11];
          var month30 = [3,5,8,10];
          var month28 = [1];
          if(month31.includes(monthpick.month())){
            for(var i=0; i < 31 ; i++){
              function inDay(element) {
                return moment(element.timestamp).date() == i+1 ;
              }
              In1month[i] = Daymonth.filter(inDay).map((In1month) => In1month.cpu); //map cpu in each day --> array
              
            }
            for(var i=0; i < 31 ; i++){ //loop 24hr
              if(In1month[i].length !=0){      
                var aa = In1month[i].map(Inmonth => parseInt(Inmonth))
                In1dayy.push(aa);// push cpu in array of cpu in each hr
                  var sumaa = 0;
                  for(var k=0; k<aa.length;k++){ //loop in each array to sum cpu
                    sumaa += aa[k]; 
                    
                  }
                  sumaa = sumaa/aa.length ; 
                  In1day.push(sumaa); //push Avg cpu in array of cpu in each hr
                }
              else{
                In1dayy[i] = 0;
                In1day[i] = 0;
              }   
            }
            var label = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31];
          }
          else if(month30.includes(monthpick.month())){
            for(var i=0; i < 30 ; i++){
              function inDay(element) {
                return moment(element.timestamp).date() == i+1 ;
              }
              In1month[i] = Daymonth.filter(inDay).map((In1month) => In1month.cpu); //map cpu in each day --> array
              
            }
            for(var i=0; i < 30 ; i++){ //loop 24hr
              if(In1month[i].length !=0){      
                var aa = In1month[i].map(Inmonth => parseInt(Inmonth))
                In1dayy.push(aa);// push cpu in array of cpu in each hr
                  var sumaa = 0;
                  for(var k=0; k<aa.length;k++){ //loop in each array to sum cpu
                    sumaa += aa[k]; 
                    
                  }
                  sumaa = sumaa/aa.length ; 
                  In1day.push(sumaa); //push Avg cpu in array of cpu in each hr
                }
              else{
                In1dayy[i] = 0;
                In1day[i] = 0;
              } 
            }
            var label = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30];
          }
          else if(month28.includes(monthpick.month())){
            for(var i=0; i < 28 ; i++){
              function inDay(element) {
                return moment(element.timestamp).date() == i+1 ;
              }
              In1month[i] = Daymonth.filter(inDay).map((In1month) => In1month.cpu); //map cpu in each day --> array
              
            }
            for(var i=0; i < 28 ; i++){ //loop 24hr
              if(In1month[i].length !=0){      
                var aa = In1month[i].map(Inmonth => parseInt(Inmonth))
                In1dayy.push(aa);// push cpu in array of cpu in each hr
                  var sumaa = 0;
                  for(var k=0; k<aa.length;k++){ //loop in each array to sum cpu
                    sumaa += aa[k]; 
                    
                  }
                  sumaa = sumaa/aa.length ; 
                  In1day.push(sumaa); //push Avg cpu in array of cpu in each hr
                }
              else{
                In1dayy[i] = 0;
                In1day[i] = 0;
              } 
            }
            var label = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28];
          }
          
          console.log(In1month)
          // var daymonth = In1month.map((In1month) => In1month.cpu)
         
          
         
         //Avg cpu each day
          // for(var i=0; i < 31 ; i++){ //loop 24hr
          //   if(In1month[i].length !=0){      
          //     var aa = In1month[i].map(Inmonth => parseInt(Inmonth))
          //     In1dayy.push(aa);// push cpu in array of cpu in each hr
          //       var sumaa = 0;
          //       for(var k=0; k<aa.length;k++){ //loop in each array to sum cpu
          //         sumaa += aa[k]; 
                  
          //       }
          //       sumaa = sumaa/aa.length ; 
          //       In1day.push(sumaa); //push Avg cpu in array of cpu in each hr
          //     }
          //   else{
          //     In1dayy[i] = 0;
          //     In1day[i] = 0;
          //   } 
          // }
          // console.log(sumaa)
          console.log(In1dayy)
          console.log(In1day)
          
          //console.log(Day31)
          //console.log(day31)
          // var sumhr13 = 0;
          // var hhr13 = hr13.map(Number)
          
          // for(var i in hhr13){ 
          //     if(hr13[i] != "NOSUCHINSTANCE"){
          //       sumhr13 += hhr13[i];
          //     }
          //    }
          // var avghr13 = sumhr13/(hr13.length) 
          // console.log(avghr13)
          // var cpu = response.data.map((filtered) => filtered.cpu) 
          // var cpu = filtered.map((filtered) => filtered.cpu) 
          // var time = filtered.map((filtered) => filtered.timestamp)
          //console.log(cpu)
          //console.log(time)
          
          this.updatelabel(label) //update label
          this.updateData(In1day) //update data (month)
          
          
        },

  Gengraphyear(n){
        var devictest = this.id;
        var yearpick = moment(n);
        console.log(yearpick.year())    
 
        function isDevice(element) { //filter device
            return element.device_id == devictest ; 
          }
        var filtereddevice = this.info.filter(isDevice);
        var In1year = []; // all data in each year
        var In1month = []; // all avg cpu in each month
        var In1monthh = []; // all cpu in each month
        function inyear(element) {
            return moment(element.timestamp).year() == yearpick.year(); //filter year
          }
          var Yeardevice = filtereddevice.filter(inyear); //filter device_id && year
          // var daymonth = Daymonth.map((Daymonth) => Daymonth.cpu) // map 
          console.log(Yeardevice)
          var monpick = moment(n);
          for(var i=0; i < 12 ; i++){
              function inMonth(element) {
                return moment(element.timestamp).month() == i ;
              }
              In1year[i] = Yeardevice.filter(inMonth).map((In1year) => In1year.cpu); //map cpu in each month --> array
              
          }
          
          console.log(In1year)
          for(var i=0; i < 12 ; i++){ //loop 24hr
            if(In1year[i].length !=0){      
              var aa = In1year[i].map(Inmonth => parseInt(Inmonth))
              In1monthh.push(aa);// push cpu in array of cpu in each hr
                var sumaa = 0;
                for(var k=0; k<aa.length;k++){ //loop in each array to sum cpu
                  sumaa += aa[k]; 
                  
                }
                sumaa = sumaa/aa.length ; 
                In1month.push(sumaa); //push Avg cpu in array of cpu in each hr
              }
            else{
              In1monthh[i] = 0;
              In1month[i] = 0;
            } 
          }
          // console.log(sumaa)
          console.log(In1monthh)
          console.log(In1month)
          var label = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
          this.updatelabel(label) //update label
          this.updateData(In1month) //update data (year)
  }
  }
}
</script>

<style>

#chart1 {
    text-align: center;
    padding: .75em .5em;
    font-size: 100%;
    border: 1px solid #ccc;
    width: 100%
}
#chart1 {
    height: 2.5em;
    text-align: center;
}
#chart {
    background: #f2f2f2;
    border: 1px solid #ddd;
    text-align: center;
    /* padding: 0em 1em 1em; */
    /* margin-bottom: 2em; */
    /* width: 25%; */
    
}

</style>
