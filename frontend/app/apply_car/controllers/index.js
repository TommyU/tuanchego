angular.module('app.applycar').config(applyCarConfig); 

applyCarConfig.$inject = ['$stateProvider'];
function applyCarConfig($stateProvider) {
    $stateProvider.state('base.applycar', {
        url: '/applycar',
        views: {
            '@': {
                templateUrl: 'apply_car/controllers/index.html',
                controller: ApplyCarController,
                controllerAs: 'vm',
            },
        },
        ncyBreadcrumb: {
            label: 'Apply Car',
        },
    });
}

angular.module('app.applycar').controller('ApplyCarController', ApplyCarController);

ApplyCarController.$inject = ['$filter', '$scope', '$state', '$timeout', 'Case', 'HLFilters', 'LocalStorage',
    'Settings', 'User', 'UserTeams'];
function ApplyCarController($filter, $scope, $state, $timeout, Case, HLFilters, LocalStorage,
                            Settings, User, UserTeams) {
    var vm = this;

    vm.storage = new LocalStorage('applycar');
   

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
