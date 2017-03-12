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
        }, true);
    }

}
