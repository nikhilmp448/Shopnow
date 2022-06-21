$(document).ready(function () {
    
});
  var c_config = {
      type: 'pie',
      data: {
        datasets: [{
          data: {{ data1|safe }},
          backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          ],
          borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1 ,
          label: 'Customer'
        }],
        labels: {{ data1_label|safe }}
      },
      options: {
        responsive: true
      }
    };

    var o_config = {
        type: 'pie',
        data: {
          datasets: [{
            data: {{ odata|safe }},
            backgroundColor: [
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
            ],
            borderColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)'
              ],
              borderWidth: 1 ,
            label: 'Orders'
          }],
          labels: {{ olabels|safe }}
        },
        options: {
          responsive: true
        }
      };



    window.onload = function() {
        var c_ctx = document.getElementById('myChart').getContext('2d');
        window.myPie1 = new Chart(c_ctx, c_config);

        var o_ctx = document.getElementById('order-chart').getContext('2d');
            window.myPie2 = new Chart(o_ctx, o_config);
        };

