let vue = new Vue({
    el: '#app',
    data: {
        day1: {},
        day2: '',
        day3: '',
        day4: '',
        day5: '',
    },
    methods: {
        update: function (event) {
            value = event.target.value;
            this.info = value;
            console.log(value);
        }
    }
});
vue.day1 = {'name': 'Jueves', 'sunrise':'07:15', 'sunset':'21:10'};
vue.day2 = 'Viernes';
vue.day3 = 'Sábado';
vue.day4 = 'Domingo';
vue.day5 = 'Lunes';