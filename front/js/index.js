$(".form_datetime").datetimepicker({
    weekStart: 1,
    todayBtn: 1,
    autoclose: 1,
    todayHighlight: 1,
    startView: 2,
    forceParse: 0
});

$("#serial_record").bootstrapTable({
    pagination: true,
    search: true,
    sidePagination: "client"
});

function row_style(row, index) {
    if (row.type == "市价买")
        return { classes: "danger" };
    else
        return { classes: "active"};
}

function begin() {
    $("#nonsense").slideUp("slow");
    $("#stop_btn").slideDown("slow");
    $(".site-wrapper").css("height", "10%");
    $("#main_info").slideDown("slow");
    update_data();
    window.setInterval("update_data()", 1000 * 60);
}

function update_data() {
    //获取流水数据
    $.ajax({
        url: "http://123.207.20.248:8080/cgi-bin/getTrans.py",
        data: {},
        cache: false,
        async: true,
        type: "POST",
        dataType: "json",
        success: function(data) {
            $("#serial_record").bootstrapTable("load", data["trans"]);
        }
    });
    //获取资产数据
    $.ajax({
        url: "http://123.207.20.248:8080/cgi-bin/getAccount.py",
        data: {},
        cache: false,
        async: false,
        type: "POST",
        dataType: "json",
        success: function(data) {
            var balance = data["Balance"].toString().split(".");
            if (balance.length < 2) {
                balance[1] = "00";
            }
            while (balance[1].length < 2) {
                balance[1] += "0";
            }
            var bitcoin = data["Stocks"].toString().split(".");
            if (bitcoin.length < 2) {
                bitcoin[1] = "0000";
            }
            while (bitcoin[1].length < 4) {
                bitcoin[1] += "0";
            }
            var profit = data["Profit"].toString().split(".");
            if (profit.length < 2) {
                profit[1] = "00";
            }
            while (profit[1].length < 2) {
                profit[1] += "0";
            }
            var netAsset = data["NetAsset"].toString().split(".");
            if (netAsset.length < 2) {
                netAsset[1] = "00";
            }
            while (netAsset[1].length < 2) {
                netAsset[1] += "0";
            }
            $("#balance_int").html(balance[0]);
            $("#balance_decimal").html("." + balance[1].slice(0, 2));
            $("#bitcoin_int").html(bitcoin[0]);
            $("#bitcoin_decimal").html("." + bitcoin[1].slice(0, 4));
            $("#netAsset_int").html(netAsset[0]);
            $("#netAsset_decimal").html("." + netAsset[1].slice(0, 2));
            $("#profit_int").html(profit[0]);
            $("#profit_decimal").html("." + profit[1].slice(0, 2));
        }
    });
    //获取K线数据
    get_k_lines();
}


function get_k_lines() {
    var period = "0";
    //var url = "http://123.207.20.248:8080/cgi-bin/interface/getKLines.py?period=" + period;
    var url = "/cgi-bin/getKLines.py?period=" + period;
    $.getJSON(url, function(result) {
        var rawData = [];
        rawData = result["recs"];
        new_data = splitData(rawData);
        draw_k_lines(new_data);
    });

}

function splitData(rawData) {
    var categoryData = [];
    var values = []
    for (var i = 0; i < rawData.length; i++) {
        categoryData.push(rawData[i].splice(0, 1)[0]);
        values.push(rawData[i])
    }
    return {
        categoryData: categoryData,
        values: values
    };
}

function calculateMA(new_data, dayCount) {
    var result = [];
    for (var i = 0, len = new_data.values.length; i < len; i++) {
        if (i < dayCount) {
            result.push('-');
            continue;
        }
        var sum = 0;
        for (var j = 0; j < dayCount; j++) {
            sum += new_data.values[i - j][1];
        }
        result.push(sum / dayCount);
    }
    return result;
}

function draw_k_lines(new_data) {
    var k = echarts.init($("#chart")[0]);
    var option = {
        title: {
            text: '火币网比特币指数',
            left: 0
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            }
        },
        legend: {
            data: ['1分钟K线', 'MA5', 'MA10', 'MA20', 'MA30']
        },
        grid: {
            left: '10%',
            right: '10%',
            bottom: '15%'
        },
        xAxis: {
            type: 'category',
            data: new_data.categoryData,
            scale: true,
            boundaryGap: false,
            axisLine: { onZero: false },
            splitLine: { show: false },
            splitNumber: 20,
            min: 'dataMin',
            max: 'dataMax'
        },
        yAxis: {
            scale: true,
            splitArea: {
                show: true
            }
        },
        dataZoom: [{
                type: 'inside',
                start: 50,
                end: 100
            },
            {
                show: true,
                type: 'slider',
                y: '90%',
                start: 50,
                end: 100
            }
        ],
        series: [{
                name: '1分钟K线',
                type: 'candlestick',
                data: new_data.values,
                markPoint: {
                    label: {
                        normal: {
                            formatter: function(param) {
                                return param != null ? Math.round(param.value) : '';
                            }
                        }
                    },
                    data: [{
                            name: 'XX标点',
                            coord: ['2013/5/31', 2300],
                            value: 2300,
                            itemStyle: {
                                normal: { color: 'rgb(41,60,85)' }
                            }
                        },
                        {
                            name: 'highest value',
                            type: 'max',
                            valueDim: 'highest'
                        },
                        {
                            name: 'lowest value',
                            type: 'min',
                            valueDim: 'lowest'
                        },
                        {
                            name: 'average value on close',
                            type: 'average',
                            valueDim: 'close'
                        }
                    ],
                    tooltip: {
                        formatter: function(param) {
                            return param.name + '<br>' + (param.data.coord || '');
                        }
                    }
                },
                markLine: {
                    symbol: ['none', 'none'],
                    data: [
                        [{
                                name: 'from lowest to highest',
                                type: 'min',
                                valueDim: 'lowest',
                                symbol: 'circle',
                                symbolSize: 10,
                                label: {
                                    normal: { show: false },
                                    emphasis: { show: false }
                                }
                            },
                            {
                                type: 'max',
                                valueDim: 'highest',
                                symbol: 'circle',
                                symbolSize: 10,
                                label: {
                                    normal: { show: false },
                                    emphasis: { show: false }
                                }
                            }
                        ],
                        {
                            name: 'min line on close',
                            type: 'min',
                            valueDim: 'close'
                        },
                        {
                            name: 'max line on close',
                            type: 'max',
                            valueDim: 'close'
                        }
                    ]
                }
            },
            {
                name: 'MA5',
                type: 'line',
                data: calculateMA(new_data, 5),
                smooth: true,
                lineStyle: {
                    normal: { opacity: 0.5 }
                }
            },
            {
                name: 'MA10',
                type: 'line',
                data: calculateMA(new_data, 10),
                smooth: true,
                lineStyle: {
                    normal: { opacity: 0.5 }
                }
            },
            {
                name: 'MA20',
                type: 'line',
                data: calculateMA(new_data, 20),
                smooth: true,
                lineStyle: {
                    normal: { opacity: 0.5 }
                }
            },
            {
                name: 'MA30',
                type: 'line',
                data: calculateMA(new_data, 30),
                smooth: true,
                lineStyle: {
                    normal: { opacity: 0.5 }
                }
            },

        ]
    };
    k.setOption(option);
}
