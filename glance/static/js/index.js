
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
        selectedSerial: '',
    },
    methods: {
        setSelectedSerial: function(selectedSerial){
        var self = this;
        self.selectedSerial = selectedSerial;
        console.log(selectedSerial);
        get('/api/get-all-orders/',{ serial: self.selectedSerial}
            ).then(function(res) {
        self.orderData.orders = res.results;});
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
            console.log(self.serialData);
        });
        // 获取会员的直接订单
        get('/api/get-all-orders/', {
            serial: userSerial
        }).then(function(res) {
            self.orderData.orders = res.results;
            console.log(self.orderData.orders);
        });
    }
});
