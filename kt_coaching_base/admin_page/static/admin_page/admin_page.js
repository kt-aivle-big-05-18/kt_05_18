document.addEventListener('DOMContentLoaded', (event) => {
    // 성별 데이터
    const genderCounts = JSON.parse(document.getElementById('gender_counts').textContent);
    const genderLabels = genderCounts.map(item => item.gender);
    const genderData = genderCounts.map(item => item.gender_count);

    const ctxGender = document.getElementById('gender_Chart').getContext('2d');
    new Chart(ctxGender, {
        type: 'bar',
        data: {
            labels: genderLabels,
            datasets: [{
                data: genderData,
                backgroundColor: [
                    'rgba(231, 84, 128, 0.6)',
                    'rgba(0, 128, 128, 0.6)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false,
                },
                title: {
                    display: true,
                    text: '성별 비율'
                },
                datalabels: {
                    display: true,
                    color: '#000',
                    font: {
                        size: 16,
                        weight: 'bold'
                    },
                    formatter: (value, context) => {
                        return context.chart.data.labels[context.dataIndex] + ': ' + value;
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true
                },
                y: {
                    beginAtZero: true
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });

    // 연령대 데이터
    const ageCounts = JSON.parse(document.getElementById('age_counts').textContent);
    const ageLabels = ageCounts.map(item => item.age_group);
    const ageData = ageCounts.map(item => item.age_group_count);

    const ctxAge = document.getElementById('age_Chart').getContext('2d');
    new Chart(ctxAge, {
        type: 'bar',
        data: {
            labels: ageLabels,
            datasets: [{
                data: ageData,
                backgroundColor: 'rgba(143, 185, 219, 0.6)',
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false,
                },
                title: {
                    display: true,
                    text: '선택한 연령대',
                },
                datalabels: {
                    display: true,
                    color: '#000',
                    font: {
                        size: 16,
                        weight: 'bold',
                    },
                    formatter: (value, context) => {
                        return context.chart.data.labels[context.dataIndex] + ': ' + value;
                    },
                },
            },
            scales: {
                x: {
                    beginAtZero: true,
                },
                y: {
                    beginAtZero: true,
                },
            },
            animation: {
                animateScale: true,
                animateRotate: true,
            },
        },
    });

   // Rank 데이터
   const rankCounts = JSON.parse(document.getElementById('rank_counts').textContent);
   const rankLabels = rankCounts.map(item => item.rank);
   const rankData = rankCounts.map(item => item.rank_count);
   const rankColors = [
       'rgba(143, 170, 220, 1)',
       'rgba(244, 177, 131, 1)',
       'rgba(169, 209, 142, 1)',
       'rgba(255, 217, 102, 1)',
       'rgba(250, 166, 178, 1)',
       'rgba(167, 226, 225, 1)',
       'rgba(193, 167, 226, 1)',
   ];

   const ctxRank = document.getElementById('rank_Chart').getContext('2d');
   new Chart(ctxRank, {
       type: 'pie',
       data: {
           labels: rankLabels,
           datasets: [{
               data: rankData,
               backgroundColor: rankColors,
           }]
       },
       options: {
           responsive: true,
           plugins: {
               title: {
                   display: true,
                   text: 'Rank 비율'
               },
               datalabels: {
                   display: true,
                   color: '#000',
                   font: {
                       size: 16,
                       weight: 'bold'
                   },
                   formatter: (value, context) => {
                       return context.chart.data.labels[context.dataIndex] + ': ' + value;
                   }
               }
           }
       }
   });

   // Department 데이터
   const departmentCounts = JSON.parse(document.getElementById('department_counts').textContent);
   const departmentLabels = departmentCounts.map(item => item.department);
   const departmentData = departmentCounts.map(item => item.department_count);
   const departmentColors = [
        'rgba(143, 170, 220, 1)',
        'rgba(244, 177, 131, 1)',
        'rgba(169, 209, 142, 1)',
        'rgba(255, 217, 102, 1)',
        'rgba(250, 166, 178, 1)',
        'rgba(167, 226, 225, 1)',
        'rgba(193, 167, 226, 1)',
   ];

   const ctxDepartment = document.getElementById('department_Chart').getContext('2d');
   new Chart(ctxDepartment, {
       type: 'pie',
       data: {
           labels: departmentLabels,
           datasets: [{
               data: departmentData,
               backgroundColor: departmentColors,
           }]
       },
       options: {
           responsive: true,
           plugins: {
               title: {
                   display: true,
                   text: 'Department 비율'
               },
               datalabels: {
                   display: true,
                   color: '#000',
                   font: {
                       size: 16,
                       weight: 'bold'
                   },
                   formatter: (value, context) => {
                       return context.chart.data.labels[context.dataIndex] + ': ' + value;
                   }
               }
           }
       }
   });

   // Topic Label 데이터
   const topicLabelCounts = JSON.parse(document.getElementById('topic_label_counts').textContent);
   const topicLabelLabels = topicLabelCounts.map(item => item.topic_label);
   const topicLabelData = topicLabelCounts.map(item => item.topic_label_count);
   const topicLabelColors = [
        'rgba(143, 170, 220, 1)',
        'rgba(244, 177, 131, 1)',
        'rgba(169, 209, 142, 1)',
        'rgba(255, 217, 102, 1)',
        'rgba(250, 166, 178, 1)',
        'rgba(167, 226, 225, 1)',
        'rgba(193, 167, 226, 1)',
    ];

   const ctxTopicLabel = document.getElementById('topic_label_Chart').getContext('2d');
   new Chart(ctxTopicLabel, {
       type: 'pie',
       data: {
           labels: topicLabelLabels,
           datasets: [{
               data: topicLabelData,
               backgroundColor: topicLabelColors,
           }]
       },
       options: {
           responsive: true,
           plugins: {
               title: {
                   display: true,
                   text: 'Topic Label 비율'
               },
               datalabels: {
                   display: true,
                   color: '#000',
                   font: {
                       size: 16,
                       weight: 'bold'
                   },
                   formatter: (value, context) => {
                       return context.chart.data.labels[context.dataIndex] + ': ' + value;
                   }
               }
           }
       }
   });
});