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

CarsController.$inject = ['$filter', '$scope', '$state', '$timeout', 'Case', 'HLFilters', 'LocalStorage',
    'Settings', 'User', 'UserTeams'];
function CarsController($filter, $scope, $state, $timeout, Case, HLFilters, LocalStorage,
                            Settings, User, UserTeams) {
    var vm = this;

    vm.storage = new LocalStorage('brand');
   

    init();
    _setupWatchers();

    //////

    function init() {
        // This timeout is needed because by loading from LocalStorage isn't fast enough.
        $timeout(function() {
            //初始化的一些动作
        }, 50);
    }

    function _setupWatchers() {
        /**
         * 一组变量onchange监听
         * 
         */
        $scope.$watchGroup([
            'vm.var1',
            'vm.var2',
            'vm.varn',
        ], function() {
            //都会执行的函数1();
            //都会执行的函数2();
        });

        /**
         * 数组集合onchange的监听
         */
        $scope.$watchCollection('vm.table.visibility', function() {
            //都会执行的函数1();
        });

        /**
         *单一变量onchange监听
         */
        $scope.$watch('vm.filterList', function() {
            //都会执行的函数1();
        }, true);
    }

}
