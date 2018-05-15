<script>
import { Line, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  extends: Line,
  mixins: [reactiveProp],
  props: ['data', 'options', 'chartData'],
  mounted () {
    // this.chartData is created in the mixin.
    // If you want to pass options please create a local options object
    this.renderChart(this.chartData, {
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
      }
    })
  }
}
</script>
