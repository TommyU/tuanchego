angular.module('app.applybrand').config(applyBrandConfig); 

applyBrandConfig.$inject = ['$stateProvider'];
function applyBrandConfig($stateProvider) {
    $stateProvider.state('base.applybrand', {
        url: '/applybrand',
        views: {
            '@': {
                templateUrl: 'apply_brand/controllers/index.html',
                controller: ApplyBrandController,
                controllerAs: 'vm',
            },
        },
        ncyBreadcrumb: {
            label: 'Apply Brand',
        },
    });
}

angular.module('app.applybrand').controller('ApplyBrandController', ApplyBrandController);

ApplyBrandController.$inject = ['$filter', '$scope', '$state', '$timeout', 'Case', 'HLFilters', 'LocalStorage',
    'Settings', 'User', 'UserTeams'];
function ApplyBrandController($filter, $scope, $state, $timeout, Case, HLFilters, LocalStorage,
                            Settings, User, UserTeams) {
    var vm = this;

    vm.storage = new LocalStorage('applybrand');
   

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
