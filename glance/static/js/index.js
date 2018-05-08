
function get(url, data) {
    return $.ajax({
        type: "get",
        url: url,
        dataType: "json",
        data: data
    }).done(function(res) {
        return res;
    });
}

function filterMonthlyData(data){
    var filteredAry = data.filter(function(e) { return e.num_of_buyers !== 0 })
    // var filteredAry = data.filter(e => e.num_of_buyers !== 0)
    return filteredAry;
}

// 获取用户serial
var userSerial = $('#serial').text();

var glanceData = new Vue({
    el: 'body',
    data: {
        msg: '',
        alertType: 'success',
        serialData: {
            serials: []
        },
        orderData: {
            orders: []
        },
        monthlyData: {
            months: []
        },
        selectedSerial: '',
    },
    methods: {
        setSelectedSerial: function(selectedSerial){
            var self = this;
            self.selectedSerial = selectedSerial.serial;
            get('/api/get-all-orders/',{ serial: self.selectedSerial}
                ).then(function(res) {
            self.orderData.orders = res.results;});

            get('/api/get-monthly-data/', { serial: self.selectedSerial
            }).then(function(res) {
                self.monthlyData.months = filterMonthlyData(res.results);
                console.log(self.monthlyData.months);
            });
        }
    },
    created: function() {
        var self = this;
        console.log(userSerial);
        // 获取会员的次级会员
        get('/api/sub-serials/', {
            serial: userSerial
        }).then(function(res) {
            self.serialData.serials = res.results;

            console.log(self.serialData.serials);
        });
        // 获取会员的直接订单
        get('/api/get-all-orders/', {
            serial: userSerial
        }).then(function(res) {
            self.orderData.orders = res.results;
            console.log(self.orderData.orders);
        });
        // 获取会员的月度汇总
        get('/api/get-monthly-data/', {
            serial: userSerial
        }).then(function(res) {
            self.monthlyData.months = filterMonthlyData(res.results);
            console.log(self.monthlyData.months);
        });
    }
});
