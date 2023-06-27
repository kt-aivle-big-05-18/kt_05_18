// 차트그리기
// 파이차트
$(document).ready(function() {
    // var perspective = {{Perspective}};
    // var respect = {{Respect}};
    // var recognition = {{Recognition}};
    // var negation = {{Negation}};
    // var feedback = {{Feedback}};
    
    var context = $('#pie_chart')[0].getContext('2d');
    var myChart = new Chart(context, {
      type: 'pie',
      data: {
        labels: ['관점 변화', '존중', '인정', '부정', '판단'],
        datasets: [{
          label: '점수',
          fill: false,
          data: [21, 19, 17, 34, 23],
          backgroundColor: [
            '#E9FFFF',
            '#F0F0F0',
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
          ],
          borderColor: [
            '#2FC4CE',
            '#919191',
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
          ],
          borderWidth: 1
        }]
      },
      options: {
        // indexAxis: 'y',
        scales: {
          xAxes: [{
            ticks: {
              beginAtZero: true
            }
          }],
        }
      }
    });
  });