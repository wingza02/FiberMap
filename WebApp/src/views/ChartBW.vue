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
    <canvas id="eieichart"></canvas>
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
    startGraph(data) {
      var labelstart = ["00.00","01.00","02.00","03.00","04.00","05.00","06.00","07.00","08.00","09.00","10.00",
                      "11.00","12.00","13.00","14.00","15.00","16.00","17.00","18.00","19.00","20.00","21.00","22.00","23.00"];
    const planetChartData = {
            type: 'line',
            data: {
              labels: labelstart,
              datasets: [
                { // one line graph
                  label: 'Upload(Mbps)',
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
                },
                { // another line graph
                    label: 'Download(Mbps)',
                    data: [],
                    backgroundColor: [
                    'rgba(71, 183,132,.5)', // Green
                    ],
                    borderColor: [
                    '#47b784',
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
          this.createChart('eieichart', planetChartData);
    // this.axios
    //     .get("https://fibermap.herokuapp.com/getallbw", {
    //       params: {
    //         name: "VSS_COM.cm.edu",
    //         type_port: "GigabitEthernet1/3/10"
    //       }
    //     })
        // .then(response => {
          this.info = data;
          this.Gengraph()
        // })
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
  updateData1(data) {
    this.chart.data.datasets[0].data = data;
    this.chart.update();
  },
  updateData2(data) {
    this.chart.data.datasets[1].data = data;
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
          
          
        
          
          // function inDay31(element) {
          //   return moment(element.timestamp).date() == 31 ;
          // }
          
          var bwinput = []; // all data in each hr
          var bwoutput = [];
          var bwinputhr = []; // all avg cpu in each hr
          var bwinputhrr = []; // all cpu in each hr
          var bwoutputhr = []; // all avg cpu in each hr
          var bwoutputhrr = []; // all cpu in each hr
          //filter day/month/year
          function inDaymonthyear(element) {
            return moment(element.timestamp).date() == datepick.date() && moment(element.timestamp).month() == monthpick.month() &&
            moment(element.timestamp).year() == yearpick.year() ;
          }
          var BWindaymonthyear = this.info.filter(inDaymonthyear);
          var BWindaymonthyeartest = this.info.filter(inDaymonthyear);
        //   var inbounddaymonyear = BWindaymonthyear.map((BWindaymonthyear) => BWindaymonthyear.inbound)
        //   var outbounddaymonyear = BWindaymonthyear.map((BWindaymonthyear) => BWindaymonthyear.outbound)
          var BWinminus = [];
          var BWoutminus = [];
          console.log(BWindaymonthyear)
        //   console.log(inbounddaymonyear)
            for(var i=0; i < BWindaymonthyear.length -1 ;i++){
                var newObj = BWindaymonthyear[i]
                var x = ((parseInt(BWindaymonthyeartest[i+1].inbound)-parseInt(BWindaymonthyeartest[i].inbound))*8)/(1000000)
                newObj.inpututilization = x
                BWinminus.push(newObj)
            }
        console.log(BWinminus)
            for(var i=0; i < BWindaymonthyear.length -1 ;i++){
                var newObj = BWindaymonthyear[i]
                var x = ((parseInt(BWindaymonthyeartest[i+1].outbound)-parseInt(BWindaymonthyeartest[i].outbound))*8)/(1000000)
                newObj.outpututilization = x
                BWoutminus.push(newObj)
            }
            // console.log(BWoutminus)
            
          //filter each hr
          for(var i=0; i < 24 ; i++){
              function inHr(element) {
                return moment(element.timestamp).hour() == i ;
              }
              bwinput[i] = BWoutminus.filter(inHr).map((bwinput) => bwinput.inpututilization);
              bwoutput[i] = BWoutminus.filter(inHr).map((bwoutput) => bwoutput.outpututilization);
          }
          
            console.log(bwinput)
            console.log(bwoutput)
            
            // console.log(inbounddaymonyear)
          //Filter month 
        //   function inMonth(element) {
        //     return moment(element.timestamp).month() == monthpick.month() ;
        //   }
         
         for(var i=0; i < 24 ; i++){ //loop 24hr
            if(bwinput[i].length !=0){      
              var aa = bwinput[i].map(Inmonth => Inmonth)
              bwinputhrr.push(aa);// push cpu in array of cpu in each hr
                var sumaa = 0;
                for(var k=0; k<aa.length;k++){ //loop in each array to sum cpu
                  sumaa += aa[k]; 
                  
                }
                sumaa = (sumaa/aa.length)/1000 ; 
                // sumaa = (sumaa*8*100)/(1000000*)
                bwinputhr.push(sumaa); //push Avg cpu in array of cpu in each hr
              }
            else{
              bwinputhrr[i] = 0;
              bwinputhr[i] = 0;
            } 
          }
        //   console.log(bwinputhrr)
          console.log(bwinputhr)
          for(var i=0; i < 24 ; i++){ //loop 24hr
            if(bwoutput[i].length !=0){      
              var aa = bwoutput[i].map(Inmonth => Inmonth)
              bwoutputhrr.push(aa);// push cpu in array of cpu in each hr
                var sumaa = 0;
                for(var k=0; k<aa.length;k++){ //loop in each array to sum cpu
                  sumaa += aa[k]; 
                  
                }
                sumaa = (sumaa/aa.length)/1000 ;
                // sumaa = (sumaa*8*100)/(1000000*)
                bwoutputhr.push(sumaa); //push Avg cpu in array of cpu in each hr
              }
            else{
              bwoutputhrr[i] = 0;
              bwoutputhr[i] = 0;
            } 
          }
        //   console.log(bwinputhrr)
          console.log(bwoutputhr)
         //Avg cpu each hr
        //   for(var i=0; i < 24 ; i++){ //loop 24hr
        //     if(bwIn1day[i].length !=0){      
        //       var aa = bwIn1day[i].map(Inday => parseInt(Inday.cpu))
        //       bwIn1dayhrr.push(aa);// push cpu in array of cpu in each hr
        //         var sumaa = 0;
        //         for(var k=0; k<aa.length;k++){ //loop in each array to sum cpu
        //           sumaa += aa[k]; 
                  
        //         }
        //         sumaa = sumaa/aa.length ; 
        //         In1dayhr.push(sumaa); //push Avg cpu in array of cpu in each hr
        //       }
        //     else{
        //       In1dayhrr[i] = 0;
        //       In1dayhr[i] = 0;
        //     } 
        //   }
        
          // console.log(sumaa)
        //   console.log(In1dayhrr)
        //   console.log(In1dayhr)
          
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
          this.updateData1(bwinputhr)
          this.updateData2(bwoutputhr)
          
        },
  Gengraphmonth(m) {
          
          console.log(m)
          // var datepick = moment(e);
          var monthpick = moment(m);
          var yearpick = moment(m);
          // var yearpick = moment(e);
          // var monthpickplus = monthpick.month() +1;
          // console.log(datepick.date())
          console.log(monthpick.month())
          
          // function isDate(element) {
          //   return moment(element.timestamp).date() == 31 && moment(element.timestamp).hour() == 13 && 
          //   moment(element.timestamp).minute() == 50  ;
          // }
          // var filtered = response.data.filter(isDate);
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
        //   var In1month = []; // all data in each month
        //   var In1day = []; // all avg cpu in each day
        //   var In1dayy = []; // all cpu in each day
            var bwinput = []; // all data in each hr
            var bwoutput = [];
            var bwinputhr = []; // all avg cpu in each hr
            var bwinputhrr = []; // all cpu in each hr
            var bwoutputhr = []; // all avg cpu in each hr
            var bwoutputhrr = []; // all cpu in each hr
          //filter day/month/year
          function inDaymonth(element) {
            return moment(element.timestamp).month() == monthpick.month() && moment(element.timestamp).year() == yearpick.year();
          }
          var BWindaymonthyear = this.info.filter(inDaymonth);
          var BWindaymonthyeartest = this.info.filter(inDaymonth);
            var BWinminus = [];
            var BWoutminus = [];
          console.log(BWindaymonthyear)
        //   console.log(inbounddaymonyear)
            for(var i=0; i < BWindaymonthyear.length -1 ;i++){
                var newObj = BWindaymonthyear[i]
                var x = ((parseInt(BWindaymonthyeartest[i+1].inbound)-parseInt(BWindaymonthyeartest[i].inbound))*8)/(1000000)
                newObj.inpututilization = x
                BWinminus.push(newObj)
            }
        console.log(BWinminus)
            for(var i=0; i < BWindaymonthyear.length -1 ;i++){
                var newObj = BWindaymonthyear[i]
                var x = ((parseInt(BWindaymonthyeartest[i+1].outbound)-parseInt(BWindaymonthyeartest[i].outbound))*8)/(1000000)
                newObj.outpututilization = x
                BWoutminus.push(newObj)
            }
        //   var Daymonth = filtereddevice.filter(inDaymonth);
         
        //   console.log(Daymonth)
         
          var month31 = [0,2,4,6,7,9,11];
          var month30 = [3,5,8,10];
          var month28 = [1];
          if(month31.includes(monthpick.month())){
            for(var i=0; i < 31 ; i++){
              function inHr(element) {
                return moment(element.timestamp).hour() == i ;
              }
              bwinput[i] = BWoutminus.filter(inHr).map((bwinput) => bwinput.inpututilization);
              bwoutput[i] = BWoutminus.filter(inHr).map((bwoutput) => bwoutput.outpututilization);
            }
            for(var i=0; i < 31 ; i++){ //loop 24hr
                if(bwinput[i].length !=0){      
                var aa = bwinput[i].map(Inmonth => Inmonth)
                bwinputhrr.push(aa);// push cpu in array of cpu in each hr
                    var sumaa = 0;
                    for(var k=0; k<aa.length;k++){ //loop in each array to sum cpu
                    sumaa += aa[k]; 
                    
                    }
                    sumaa = (sumaa/aa.length)/1000 ; 
                    // sumaa = (sumaa*8*100)/(1000000*)
                    bwinputhr.push(sumaa); //push Avg cpu in array of cpu in each hr
                }
                else{
                bwinputhrr[i] = 0;
                bwinputhr[i] = 0;
                } 
             }
        //   console.log(bwinputhrr)
        //   console.log(bwinputhr)
            for(var i=0; i < 31 ; i++){ //loop 24hr
                if(bwoutput[i].length !=0){      
                var aa = bwoutput[i].map(Inmonth => Inmonth)
                bwoutputhrr.push(aa);// push cpu in array of cpu in each hr
                    var sumaa = 0;
                    for(var k=0; k<aa.length;k++){ //loop in each array to sum cpu
                    sumaa += aa[k]; 
                    
                    }
                    sumaa = (sumaa/aa.length)/1000 ;
                    // sumaa = (sumaa*8*100)/(1000000*)
                    bwoutputhr.push(sumaa); //push Avg cpu in array of cpu in each hr
                }
                else{
                bwoutputhrr[i] = 0;
                bwoutputhr[i] = 0;
                } 
            }
                var label = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31];
          }
          
          
          // var daymonth = In1month.map((In1month) => In1month.cpu)
         
         
          else if(month30.includes(monthpick.month())){
            for(var i=0; i < 30 ; i++){
              function inHr(element) {
                return moment(element.timestamp).hour() == i ;
              }
              bwinput[i] = BWoutminus.filter(inHr).map((bwinput) => bwinput.inpututilization);
              bwoutput[i] = BWoutminus.filter(inHr).map((bwoutput) => bwoutput.outpututilization);
            }
            for(var i=0; i < 30 ; i++){ //loop 24hr
                if(bwinput[i].length !=0){      
                var aa = bwinput[i].map(Inmonth => Inmonth)
                bwinputhrr.push(aa);// push cpu in array of cpu in each hr
                    var sumaa = 0;
                    for(var k=0; k<aa.length;k++){ //loop in each array to sum cpu
                    sumaa += aa[k]; 
                    
                    }
                    sumaa = (sumaa/aa.length)/1000 ; 
                    // sumaa = (sumaa*8*100)/(1000000*)
                    bwinputhr.push(sumaa); //push Avg cpu in array of cpu in each hr
                }
                else{
                bwinputhrr[i] = 0;
                bwinputhr[i] = 0;
                } 
             }
        //   console.log(bwinputhrr)
        //   console.log(bwinputhr)
            for(var i=0; i < 30 ; i++){ //loop 24hr
                if(bwoutput[i].length !=0){      
                var aa = bwoutput[i].map(Inmonth => Inmonth)
                bwoutputhrr.push(aa);// push cpu in array of cpu in each hr
                    var sumaa = 0;
                    for(var k=0; k<aa.length;k++){ //loop in each array to sum cpu
                    sumaa += aa[k]; 
                    
                    }
                    sumaa = (sumaa/aa.length)/1000 ;
                    // sumaa = (sumaa*8*100)/(1000000*)
                    bwoutputhr.push(sumaa); //push Avg cpu in array of cpu in each hr
                }
                else{
                bwoutputhrr[i] = 0;
                bwoutputhr[i] = 0;
                } 
            }
                var label = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30];
          }
          
          else if(month28.includes(monthpick.month())){
            for(var i=0; i < 28 ; i++){
              function inHr(element) {
                return moment(element.timestamp).hour() == i ;
              }
              bwinput[i] = BWoutminus.filter(inHr).map((bwinput) => bwinput.inpututilization);
              bwoutput[i] = BWoutminus.filter(inHr).map((bwoutput) => bwoutput.outpututilization);
            }
            for(var i=0; i < 28 ; i++){ //loop 24hr
                if(bwinput[i].length !=0){      
                var aa = bwinput[i].map(Inmonth => Inmonth)
                bwinputhrr.push(aa);// push cpu in array of cpu in each hr
                    var sumaa = 0;
                    for(var k=0; k<aa.length;k++){ //loop in each array to sum cpu
                    sumaa += aa[k]; 
                    
                    }
                    sumaa = (sumaa/aa.length)/1000 ; 
                    // sumaa = (sumaa*8*100)/(1000000*)
                    bwinputhr.push(sumaa); //push Avg cpu in array of cpu in each hr
                }
                else{
                bwinputhrr[i] = 0;
                bwinputhr[i] = 0;
                } 
            }
        //   console.log(bwinputhrr)
        //   console.log(bwinputhr)
            for(var i=0; i < 28 ; i++){ //loop 24hr
                if(bwoutput[i].length !=0){      
                var aa = bwoutput[i].map(Inmonth => Inmonth)
                bwoutputhrr.push(aa);// push cpu in array of cpu in each hr
                    var sumaa = 0;
                    for(var k=0; k<aa.length;k++){ //loop in each array to sum cpu
                    sumaa += aa[k]; 
                    
                    }
                    sumaa = (sumaa/aa.length)/1000 ;
                    // sumaa = (sumaa*8*100)/(1000000*)
                    bwoutputhr.push(sumaa); //push Avg cpu in array of cpu in each hr
                }
                else{
                bwoutputhrr[i] = 0;
                bwoutputhr[i] = 0;
                } 
            }
                var label = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28];
          }
            console.log(bwinputhr)
            this.updatelabel(label)
            this.updateData1(bwinputhr)
            this.updateData2(bwoutputhr)
           
        //   this.updatelabel(label) //update label
        //   this.updateData(In1day) //update data (month)
          
        },
  Gengraphyear(n){
        
        var yearpick = moment(n);
        console.log(yearpick.year())    
 
            var bwinput = []; // all data in each hr
            var bwoutput = [];
            var bwinputhr = []; // all avg cpu in each hr
            var bwinputhrr = []; // all cpu in each hr
            var bwoutputhr = []; // all avg cpu in each hr
            var bwoutputhrr = []; // all cpu in each hr
          //filter day/month/year
          function inyear(element) {
            return moment(element.timestamp).year() == yearpick.year();
          }
          var BWindaymonthyear = this.info.filter(inyear);
          var BWindaymonthyeartest = this.info.filter(inyear);
            var BWinminus = [];
            var BWoutminus = [];
        for(var i=0; i < BWindaymonthyear.length -1 ;i++){
                var newObj = BWindaymonthyear[i]
                var x = ((parseInt(BWindaymonthyeartest[i+1].inbound)-parseInt(BWindaymonthyeartest[i].inbound))*8)/(1000000)
                newObj.inpututilization = x
                BWinminus.push(newObj)
            }
        console.log(BWinminus)
            for(var i=0; i < BWindaymonthyear.length -1 ;i++){
                var newObj = BWindaymonthyear[i]
                var x = ((parseInt(BWindaymonthyeartest[i+1].outbound)-parseInt(BWindaymonthyeartest[i].outbound))*8)/(1000000)
                newObj.outpututilization = x
                BWoutminus.push(newObj)
            }
            
        for(var i=0; i < 12 ; i++){
              function inHr(element) {
                return moment(element.timestamp).month() == i ;
              }
              bwinput[i] = BWoutminus.filter(inHr).map((bwinput) => bwinput.inpututilization);
              bwoutput[i] = BWoutminus.filter(inHr).map((bwoutput) => bwoutput.outpututilization);
            }
        
        for(var i=0; i < 12 ; i++){ //loop 24hr
            if(bwinput[i].length !=0){      
              var aa = bwinput[i].map(Inmonth => Inmonth)
              bwinputhrr.push(aa);// push cpu in array of cpu in each hr
                var sumaa = 0;
                for(var k=0; k<aa.length;k++){ //loop in each array to sum cpu
                  sumaa += aa[k]; 
                  
                }
                sumaa = (sumaa/aa.length)/1000 ; 
                // sumaa = (sumaa*8*100)/(1000000*)
                bwinputhr.push(sumaa); //push Avg cpu in array of cpu in each hr
              }
            else{
              bwinputhrr[i] = 0;
              bwinputhr[i] = 0;
            } 
          }
        //   console.log(bwinputhrr)
          console.log(bwinputhr)
          for(var i=0; i < 12 ; i++){ //loop 24hr
            if(bwoutput[i].length !=0){      
              var aa = bwoutput[i].map(Inmonth => Inmonth)
              bwoutputhrr.push(aa);// push cpu in array of cpu in each hr
                var sumaa = 0;
                for(var k=0; k<aa.length;k++){ //loop in each array to sum cpu
                  sumaa += aa[k]; 
                  
                }
                sumaa = (sumaa/aa.length)/1000 ;
                // sumaa = (sumaa*8*100)/(1000000*)
                bwoutputhr.push(sumaa); //push Avg cpu in array of cpu in each hr
              }
            else{
              bwoutputhrr[i] = 0;
              bwoutputhr[i] = 0;
            } 
          }
            var label = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
            this.updatelabel(label)
            this.updateData1(bwinputhr)
            this.updateData2(bwoutputhr)
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
