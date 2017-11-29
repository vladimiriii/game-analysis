/*---------------------------------------
Presentation
---------------------------------------*/
var bgColor = '#F8F8F8',
    lineColor = '#586e75',
    chartWidth = 960;

var pct_format = '<span style="color:{point.color}">\u25CF</span><b>{series.name}</b>: {point.y:.1f}%<br>'
var int_format = '<span style="color:{point.color}">\u25CF</span><b>{series.name}</b>: {point.y:,.0f}<br>'
var dec_format = '<span style="color:{point.color}">\u25CF</span><b>{series.name}</b>: {point.y:.2f}<br>'


$(document).ready(function(){
    chartWidth = $(window).width() * 0.8;
    loadCharts();

});

function loadCharts() {

        // Daily Installs
        var series = [
            {"name": "IOS", "data": dailyInstallData['IOS']},
            {"name": "Android", "data": dailyInstallData['Android']},
            {"name": "FireOS", "data": dailyInstallData['FireOS']},
            {"name": "WebGL", "data": dailyInstallData['WebGL']}
        ];
        drawAreaChart("dailyInstalls", dailyInstallData['Date'], series, "Installs", true, int_format);

        // Installs by Country
        series = [{"name": "Installs", "data": installsByCountry['Installs']}];
        drawColumnChart("installsByCountry", installsByCountry['Countries'], series, "Installs", false, int_format);

        // Daily Active Users
        series = [
            {"name": "IOS", "data": dailyActiveUsers['IOS']},
            {"name": "Android", "data": dailyActiveUsers['Android']},
            {"name": "FireOS", "data": dailyActiveUsers['FireOS']},
            {"name": "WebGL", "data": dailyActiveUsers['WebGL']}
        ];
        drawAreaChart("dailyActiveUsers", dailyActiveUsers['Date'], series, "Users", true, int_format);

        // Day N Retention Any
        series = [
            {"name": "Day 1", "data": dayNRetentionAny['Day 1 (%)'].map(convertToPct)},
            {"name": "Day 7", "data": dayNRetentionAny['Day 7 (%)'].map(convertToPct)},
            {"name": "Day 14", "data": dayNRetentionAny['Day 14 (%)'].map(convertToPct)},
            {"name": "Day 21", "data": dayNRetentionAny['Day 21 (%)'].map(convertToPct)},
            {"name": "Day 28", "data": dayNRetentionAny['Day 28 (%)'].map(convertToPct)}
        ];
        drawLineChart("dayNRetentionAny", dayNRetentionAny['Date'], series, "Retention Rate (%)", true, pct_format);

        // Day N Retention Install
        series = [
            {"name": "Day 1", "data": dayNRetentionInstall['Day 1 (%)'].map(convertToPct)},
            {"name": "Day 7", "data": dayNRetentionInstall['Day 7 (%)'].map(convertToPct)},
            {"name": "Day 14", "data": dayNRetentionInstall['Day 14 (%)'].map(convertToPct)},
            {"name": "Day 21", "data": dayNRetentionInstall['Day 21 (%)'].map(convertToPct)},
            {"name": "Day 28", "data": dayNRetentionInstall['Day 28 (%)'].map(convertToPct)}
        ];
        drawLineChart("dayNRetentionInstall", dayNRetentionInstall['Date'], series, "Retention Rate (%)", true, pct_format);

        // More than a Day
        series = [
            {"name": "IOS", "data": moreThanADay['IOS'].map(convertToPct)},
            {"name": "Android", "data": moreThanADay['Android'].map(convertToPct)},
            {"name": "FireOS", "data": moreThanADay['FireOS'].map(convertToPct)},
            {"name": "WebGL", "data": moreThanADay['WebGL'].map(convertToPct)},
            {"name": "Overall", "data": moreThanADay['Total'].map(convertToPct)}
        ];
        drawLineChart("moreThanADay", moreThanADay['Date'], series, "% of All Users", true, pct_format);
        var chart = $('#moreThanADay').highcharts();
        chart.series[0].hide();
        chart.series[1].hide();
        chart.series[2].hide();
        chart.series[3].hide();

        // Daily Rounds
        series = [
            {"name": "IOS", "data": dailyRounds['IOS']},
            {"name": "Android", "data": dailyRounds['Android']},
            {"name": "Overall", "data": dailyRounds['Overall']}
        ];
        drawLineChart("dailyRounds", dailyRounds['Date'], series, "Avg. games per day", true, dec_format);

        // Purchases over time
        series = [
            {"name": "Product A", "data": purchasesOverTime['Product A']},
            {"name": "Product B", "data": purchasesOverTime['Product B']},
            {"name": "Product C", "data": purchasesOverTime['Product C']},
            {"name": "Product D", "data": purchasesOverTime['Product D']}
        ];
        drawAreaChart("purchasesOverTime", purchasesOverTime['Date'], series, "Amount", true, int_format);

        // Revenue Per User over time
        series = [
            {"name": "ARPDAU", "data": revenuePerUser['ARPDAU']},
            {"name": "ARPPU", "data": revenuePerUser['ARPPU']}
        ];
        drawLineChart("revenuePerUser", revenuePerUser['Date'], series, "Amount per User", true, dec_format);
        var chart = $('#revenuePerUser').highcharts();
        chart.series[1].hide();

        // Revenue by Country
        series = [
            {"name": "Revenue", "data": revenuePerInstall['total']['Sum']}
        ];
        format = "<b>{series.name}</b>: {point.y:.0f}";
        drawColumnChart("revenueByCountry", revenuePerInstall['total']['Country'], series, "Total Revenue", false, int_format);

        // Revenue by Country - Normalized
        series = [
            {"name": "Revenue per Install", "data": revenuePerInstall['normalized']['Revenue Per Install']}
        ];
        drawColumnChart("revenuePerInstall", revenuePerInstall['normalized']['Country'], series, "Revenue per Install", false, dec_format);

        // Update chart colors
        chart = $('#revenuePerInstall').highcharts();
        for (var i = 0; i < 10; i++) {
            chart.series[0].data[i].update({
                color: 'rgb(144, 237, 125)'
            });
        };
        for (var i = 11; i < 21; i++) {
            chart.series[0].data[i].update({
                color: 'rgb(247, 163, 92)'
            });
        };

        // Player Types
        series = [
            {"name": "IOS", "data": spendingTypes['users']['IOS']},
            {"name": "Android", "data": spendingTypes['users']['Android']},
            {"name": "FireOS", "data": spendingTypes['users']['FireOS']}
        ];
        drawStackedColumnChart("spendingTypesUsers", spendingTypes['users']['Category'], series, "Users", true, int_format);

        // Player Types
        series = [
            {"name": "IOS", "data": spendingTypes['revenue']['IOS']},
            {"name": "Android", "data": spendingTypes['revenue']['Android']},
            {"name": "FireOS", "data": spendingTypes['revenue']['FireOS']}
        ];
        drawStackedColumnChart("spendingTypesRevenue", spendingTypes['revenue']['Category'], series, "Revenue", true, int_format);

        /*----------------------------------------
        Game Structure
        ----------------------------------------*/
        // Missions by Version
        series = [
            {"name": "Mission Completed", "data": missionStats['version']['Completes'].map(convertToPct)},
            {"name": "Mission Failed", "data": missionStats['version']['Fails'].map(convertToPct)},
            {"name": "Mission Abandoned", "data": missionStats['version']['Abandons'].map(convertToPct)}
        ];
        drawStackedColumnChart("missionsByVersion", missionStats['version']['Version'], series, "% of Starts", true, pct_format);

        // Version Overlap
        series = [
            {"name": "Version 1.1.0", "data": missionStats['versionOverlap']['v1.1.0']},
            {"name": "Version 1.0.6", "data": missionStats['versionOverlap']['v1.0.6']},
            {"name": "Version 1.0.5", "data": missionStats['versionOverlap']['v1.0.5']},
            {"name": "Version 1.0.3", "data": missionStats['versionOverlap']['v1.0.3']},
            {"name": "Version 1.0.1", "data": missionStats['versionOverlap']['v1.0.1']}
        ];
        drawAreaChart("versionOverlap", missionStats['versionOverlap']['Date'], series, "Events", true, int_format);

        // Version Level Spread
        series = [
            {"name": "Version 1.0.1", "data": missionStats['versionSpread']['1.0.1'].map(convertToPct)},
            {"name": "Version 1.0.3", "data": missionStats['versionSpread']['1.0.3'].map(convertToPct)},
            {"name": "Version 1.0.6", "data": missionStats['versionSpread']['1.0.6'].map(convertToPct)},
            {"name": "Version 1.1.0", "data": missionStats['versionSpread']['1.1.0'].map(convertToPct)}
        ];
        drawLineChart("versionSpread", missionStats['versionSpread']['Levels'], series, "% of events", true, pct_format);

        // Hardest Levels
        series = [
            {"name": "Failure Rate", "data": levelStats['hardest']['Failure Rate'].map(convertToPct)}
        ];
        drawColumnChart("mostFailed", levelStats['hardest']['Level'], series, "Failure Rate", false, pct_format);

        chart = $('#mostFailed').highcharts();
        chart.series[0].data[0].update({ color: 'rgb(247, 163, 92)' });
        chart.series[0].data[3].update({ color: 'rgb(247, 163, 92)' });
        chart.series[0].data[6].update({ color: 'rgb(247, 163, 92)' });

        // User Drop Off
        series = [
            {"name": "Drop-Off Rate", "data": levelStats['dropoff']['User Drop-off'].map(convertToPct)}
        ];
        drawColumnChart("biggestDropOff", levelStats['dropoff']['Level'], series, "Drop-Off Rate", false, pct_format);

        chart = $('#biggestDropOff').highcharts();
        chart.series[0].data[0].update({ color: 'rgb(247, 163, 92)' });
        chart.series[0].data[1].update({ color: 'rgb(247, 163, 92)' });
        chart.series[0].data[6].update({ color: 'rgb(247, 163, 92)' });
        chart.series[0].data[5].update({ color: 'rgb(144, 237, 125)' });

        // User Drop Off by Level
        series = [
            {"name": "Users", "data": levelStats['dropOffTop100']['Users']}
        ];
        drawLineChart("dropOffByLevel", levelStats['dropOffTop100']['Level'], series, "Users", false, int_format);

        // Conversions by Level
        series = [
            {"name": "Users", "data": levelStats['levelRevenue']['Users']}
        ];
        drawColumnChart("firstPurchases", levelStats['levelRevenue']['Last Level Attempted'], series, "Users", false, int_format);

        chart = $('#firstPurchases').highcharts();
        chart.series[0].data[0].update({ color: 'rgb(144, 237, 125)' });
        chart.series[0].data[1].update({ color: 'rgb(247, 163, 92)' });
        chart.series[0].data[2].update({ color: 'rgb(247, 163, 92)' });
        chart.series[0].data[4].update({ color: 'rgb(247, 163, 92)' });

        // Coin Economy
        series = [
            {"name": "Coin Balance", "data": coinEconomy['Net Balance']}
        ];
        drawColumnChart("coinEconomy", coinEconomy['eventDate'], series, "Coins", false, int_format);

        /*----------------------------------------
        Marketing
        ----------------------------------------*/
        // Model Results
        series = [
            {"name": "Accuracy", "data": modelResults['Accuracy'].map(convertToPct)},
            {"name": "Recall", "data": modelResults['Recall'].map(convertToPct)},
            {"name": "Precision", "data": modelResults['Precision'].map(convertToPct)},
            {"name": "F1 Score", "data": modelResults['F1 Score'].map(convertToPct)}
        ];
        drawLineChart("modelResults", modelResults['Threshold'], series, "Score", true, pct_format);

        // Campaign Timing
        series = [
            {"name": "Campaign Users", "data": campaignData['timing']['Campaign Users']},
            {"name": "Non-Campaign Users", "data": campaignData['timing']['Non-Campaign Users']}

        ];
        drawAreaChart("campaignTiming", campaignData['timing']['Date'], series, "Users", true, int_format);
        chart = $('#campaignTiming').highcharts();
        chart.series[1].hide();

        // Top Campaigns
        series = [
            {"name": "Users", "data": campaignData['topCampaigns']['Users']},
            {"name": "Revenue", "data": campaignData['topCampaigns']['Revenue']}
        ];
        drawColumnChart("topCampaigns", campaignData['topCampaigns']['Campaign ID'], series, "Revenue/Users", true, int_format);



};

function convertToPct(x) {
    if (x == null) {
        return null
    } else {
        return Math.round(x * 10000)/100;
    };
};

function drawLineChart(div, xCats, data, label, legend, tooltip) {

    $('#' + div).highcharts({
		title: {
			text: "",
		},
        chart: {
			backgroundColor: "", // Background color
			className: 'modalLine',
            width: chartWidth,
            zoomType: 'xy'
        },
		xAxis: {
			lineColor: lineColor,
			tickColor: lineColor,
			categories: xCats, // list of index values
			labels: {
				style: {
					color: lineColor
				}
			}
		},
		yAxis: {
			title: {
				text: label,
				style: {
					color: lineColor
				}
			},
			labels: {
				style: {
					color: lineColor
				}
			},
			gridLineColor: lineColor,
			gridLineDashStyle: 'ShortDot',
			plotLines: [{
				value: 0,
				width: 1,
			}]
		},
        tooltip: {
            headerFormat: '<b>{point.x}</b><br>',
            pointFormat: tooltip
        },
		legend: {
			enabled: legend
		},
		series: data

	});
}

function drawColumnChart(div, xCats, data, label, legend, tooltip) {
    $('#' + div).highcharts({
        chart: {
            type: 'column',
            backgroundColor: "",
            width: chartWidth,
            zoomType: 'xy'
        },
        title: {
            text: ""
        },
        xAxis: {
            categories: xCats,
            labels: {
                style: {
                    color: "black"
                }
            }
        },
        yAxis: {
            title: {
                text: label,
                style: {
                    color: lineColor
                }
            },
            labels: {
                style: {
                    color: lineColor
                }
            },
        },
        legend: {
            enabled: legend
        },
        tooltip: {
            headerFormat: '<b>{point.x}</b><br>',
            shared: true,
            pointFormat: tooltip
        },
        series: data
    });
};


function drawStackedColumnChart(div, xCats, data, label, legend, tooltip) {
    $('#' + div).highcharts({
        chart: {
            type: 'column',
            backgroundColor: "",
            width: chartWidth,
            zoomType: 'xy'
        },
        title: {
            text: ""
        },
        xAxis: {
            categories: xCats,
            labels: {
                style: {
                    color: "black"
                }
            }
        },
        yAxis: {
            title: {
                text: label,
                style: {
                    color: lineColor
                }
            },
            labels: {
                style: {
                    color: lineColor
                }
            },
        },
        plotOptions: {
        column: {
            stacking: 'normal',
            dataLabels: {
                enabled: true,
                color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
                }
            }
        },
        legend: {
            enabled: legend
        },
        tooltip: {
            headerFormat: '<b>{point.x}</b><br>',
            shared: true,
            pointFormat: tooltip
        },
        series: data
    });
};


function drawAreaChart(div, xCats, data, label, legend, tooltip) {
    $('#' + div).highcharts({
        chart: {
            type: 'area',
            backgroundColor: "",
            width: chartWidth
        },
        title: {
            text: ""
        },
        xAxis: {
            categories: xCats,
            labels: {
                style: {
                    color: "black"
                }
            }
        },
        yAxis: {
            title: {
                text: label,
                style: {
                    color: lineColor
                }
            },
            labels: {
                style: {
                    color: lineColor
                }
            },
        },
        plotOptions: {
        area: {
            stacking: 'normal',
            lineColor: lineColor,
            lineWidth: 1,
            marker: {
                lineWidth: 1,
                lineColor: lineColor
            }
        }
    },
        legend: {
            enabled: legend
        },
        tooltip: {
            headerFormat: '<b>{point.x}</b><br>',
            split: true,
            pointFormat: tooltip
        },
        series: data
    });
}
