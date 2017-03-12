angular.module('app.cars').config(carConfig); 

carConfig.$inject = ['$stateProvider'];
function carConfig($stateProvider) {
    $stateProvider.state('base.cars', {
        url: '/cars',
        views: {
            '@': {
                templateUrl: 'cars/controllers/index.html',
                controller: CarsController,
                controllerAs: 'vm',
            },
        },
        ncyBreadcrumb: {
            label: 'Cars',
        },
    });
}

angular.module('app.cars').controller('CarsController', CarsController);

CarsController.$inject = ['$scope'];
function CarsController($scope) {
    var vm = this;
    vm.price_level='all';
    init();
    _setupWatchers();

    //////

    function init() {
    }

    function load_data(){

    }

    function _setupWatchers() {
        /**
         * 一组变量onchange监听
         * 
         */
        $scope.$watchGroup([
            'vm.price_level'
        ], function() {
            //都会执行的函数1();
            //都会执行的函数2();
        });

        /**
         *单一变量onchange监听
         */
        $scope.$watch('vm.price_level', function() {
            //都会执行的函数1();
            load_data();
        }, true);
    }

    vm.change_price_class=function(val){
        alert("get class called");
        vm.price_level_class_all="";
        vm.price_level_class_0="";
        vm.price_level_class_1="";
        vm.price_level_class_2="";
        vm.price_level_class_3="";
        vm.price_level_class_4="";
        vm.price_level_class_5="";
        switch(val){
            case '0':vm.price_level_class_0="act";break;
            case '1':vm.price_level_class_1="act";break;
            case '2':vm.price_level_class_2="act";break;
            case '3':vm.price_level_class_3="act";break;
            case '4':vm.price_level_class_4="act";break;
            case '5':vm.price_level_class_5="act";break;
            case 'all':vm.price_level_class_all="act";break;
        }
    }

}
