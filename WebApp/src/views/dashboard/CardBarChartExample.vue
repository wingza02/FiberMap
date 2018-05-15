<script>
import { Bar, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

// const brandPrimary = '#20a8d8'
// const datasets = [
//   {
//     label: 'My First dataset',
//     backgroundColor: brandPrimary,
//     borderColor: 'rgba(255,255,255,.55)',
//     data: [65, 59, 84, 84, 51, 55, 40]
//   }
// ]

export default {
  extends: Bar,
  mixins: [reactiveProp],
  props: ['data', 'chartData'],
  mounted () {
    this.renderChart({
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      datasets: this.data
    }, {
      maintainAspectRatio: true,
      responsive: true,
      legend: {
        display: true
      },
      scales: {
        xAxes: [{
          gridLines: {
            color: 'black',
            zeroLineColor: 'transparent'
          },
          ticks: {
            fontSize: 12,
            fontColor: 'black'
          }
        }],
        yAxes: [{
          display: true,
          ticks: {
            display: true,
            // min: Math.min.apply(Math, datasets[0].data) - 5,
            min: 0,
            max: 100
          }
        }]
      },
      elements: {
        line: {
          borderWidth: 2
        },
        point: {
          radius: 4,
          hitRadius: 10,
          hoverRadius: 4
        }
      }
    })
  }
}
</script>
