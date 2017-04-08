angular.module('app.brand').config(brandConfig); 

brandConfig.$inject = ['$stateProvider'];
function brandConfig($stateProvider) {
    $stateProvider.state('base.brand', {
        url: '/brand',
        views: {
            '@': {
                templateUrl: 'brand/controllers/index.html',
                controller: BrandController,
                controllerAs: 'vm',
            },
        },
        ncyBreadcrumb: {
            label: 'Brand',
        },
    });
}

angular.module('app.brand').controller('BrandController', BrandController);

BrandController.$inject = ['$scope', 'BrandService'];
function BrandController($scope, BrandService) {
    var vm = this;


    init();
    _setupWatchers();

    //////

    function init() {
        vm.city_id=1;//TODO
        vm.table = {
            page: 1,  // Current page of pagination: 1-index.
            pageSize: 5,  // Number of items per page.
            totalItems: 0 // Total number of items.
        };
    }

    function _setupWatchers(){
        /**
         * 一组变量onchange监听
         * 
         */
        $scope.$watchGroup([
            'vm.table.page',
            'vm.brand'
        ], function() {
            //都会执行的函数1();
            //都会执行的函数2();
            load_data();
        });
    }

    function load_data(){
        BrandService.getBrandActs({
            city_id:vm.city_id, 
            brand:vm.brand,
            page_index:vm.table.page,
            page_size:vm.table.pageSize
        }, function(response_data){
            vm.acts = response_data.acts;
            vm.table.items = response_data.acts;
            vm.table.totalItems = response_data.cnt;
            vm.table.page = response_data.page_index;
        });
    }


    vm.brand_classes=[];
    for(var i=0;i<173;i++){
        vm.brand_classes.push("");
    }
    vm.change_brand=function(val){
        vm.brand=val;
        if(val==""){
            vm.brand_class_all='cur';
        }else{
            vm.brand_class_all="";
        }
        
        for(var i=0;i<173;i++){
            vm.brand_classes[i]="";
        }

        vm.brand_classes[val]="cur";
    }
    vm.class_initial = function(initial){
        if(vm.brand_initial==initial){
            return "red_bor";
        }
        return "";
    };

}
