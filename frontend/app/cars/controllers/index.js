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

CarsController.$inject = ['$scope', 'CarService'];
function CarsController($scope, CarService) {
    //alert("yes");
    var vm = this;
    
    
    init();
    _setupWatchers();

    //////

    function init() {
        vm.price_level='';

        vm.table = {
            page: 1,  // Current page of pagination: 1-index.
            pageSize: 24,  // Number of items per page.
            totalItems: 0 // Total number of items.
        };
    }

    function load_data(){
        CarService.getCars({
            price:vm.price_level,
            size:vm.size, 
            brand:vm.brand,
            displacement:vm.displacement,
            gearbox:vm.gearbox,
            country:vm.country,
            page_index:vm.table.page,
            page_size:vm.table.pageSize
        }, function(response_data){
            vm.cars = response_data.cars;
            vm.table.items = response_data.cars;
            vm.table.totalItems = response_data.cnt;
            vm.table.page = response_data.page_index;
        });
    }

    function _setupWatchers() {
        /**
         * 一组变量onchange监听
         * 
         */
        $scope.$watchGroup([
            'vm.price_level',
            'vm.size',
            'vm.displacement',
            'vm.gearbox',
            'vm.country',
            'vm.table.page',
            'vm.brand'
        ], function() {
            load_data();
            //vm.table.page=1;
        });

        /**
         *单一变量onchange监听
         */
        $scope.$watch('vm.table.page', function() {
            //都会执行的函数1();
           //load_data();
        }, true);
    }

    vm.change_price=function(val){
        vm.price_level=val;
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
            case '':vm.price_level_class_all="act";break;
        }
    }

    vm.change_size=function(val){
        vm.size=val;
        vm.size_class_all="";
        vm.size_class_0="";
        vm.size_class_1="";
        vm.size_class_2="";
        vm.size_class_3="";
        vm.size_class_4="";
        vm.size_class_5="";
        vm.size_class_6="";
        vm.size_class_7="";
        vm.size_class_8="";
        switch(val){
            case '0':vm.size_class_0="act";break;
            case '1':vm.size_class_1="act";break;
            case '2':vm.size_class_2="act";break;
            case '3':vm.size_class_3="act";break;
            case '4':vm.size_class_4="act";break;
            case '5':vm.size_class_5="act";break;
            case '6':vm.size_class_6="act";break;
            case '7':vm.size_class_7="act";break;
            case '8':vm.size_class_8="act";break;
            case '':vm.size_class_all="act";break;
        }
    }

    vm.change_displacement=function(val){
        vm.displacement=val;
        vm.displacement_class_all="";
        vm.displacement_class_1="";
        vm.displacement_class_2="";
        vm.displacement_class_3="";
        vm.displacement_class_4="";
        vm.displacement_class_5="";
        vm.displacement_class_6="";
        vm.displacement_class_7="";
        vm.displacement_class_8="";
        vm.displacement_class_9="";
        switch(val){
            case 1:vm.displacement_class_1="act";break;
            case 2:vm.displacement_class_2="act";break;
            case 3:vm.displacement_class_3="act";break;
            case 4:vm.displacement_class_4="act";break;
            case 5:vm.displacement_class_5="act";break;
            case 6:vm.displacement_class_6="act";break;
            case 7:vm.displacement_class_7="act";break;
            case 8:vm.displacement_class_8="act";break;
            case 9:vm.displacement_class_9="act";break;
            case '':vm.displacement_class_all="act";break;
        }
    }

    vm.change_gearbox=function(val){
        vm.gearbox=val;
        vm.gearbox_class_all="";
        vm.gearbox_class_0="";
        vm.gearbox_class_1="";
        vm.gearbox_class_2="";
        vm.gearbox_class_3="";
        vm.gearbox_class_4="";

        switch(val){
            case '0':vm.gearbox_class_0="act";break;
            case '1':vm.gearbox_class_1="act";break;
            case '2':vm.gearbox_class_2="act";break;
            case '3':vm.gearbox_class_3="act";break;
            case '4':vm.gearbox_class_4="act";break;
            case '':vm.gearbox_class_all="act";break;
        }
    }

    vm.change_country=function(val){
        vm.country=val;
        vm.country_class_all="";
        vm.country_class_0="";
        vm.country_class_1="";
        vm.country_class_2="";
        vm.country_class_3="";
        vm.country_class_4="";
        vm.country_class_5="";
        vm.country_class_6="";
        vm.country_class_7="";
        switch(val){
            case '0':vm.country_class_0="act";break;
            case '1':vm.country_class_1="act";break;
            case '2':vm.country_class_2="act";break;
            case '3':vm.country_class_3="act";break;
            case '4':vm.country_class_4="act";break;
            case '5':vm.country_class_5="act";break;
            case '6':vm.country_class_6="act";break;
            case '7':vm.country_class_7="act";break;
            case '':vm.country_class_all="act";break;
        }
    }

    vm.brand_classes=[];
    for(var i=0;i<173;i++){
        vm.brand_classes.push("");
    }
    vm.change_brand=function(val){
        vm.brand=val;
        if(val==""){
            vm.brand_class_all='act';
        }else{
            vm.brand_class_all="";
        }
        
        for(var i=0;i<173;i++){
            vm.brand_classes[i]="";
        }

        vm.brand_classes[val]="act";
    }

    vm.set_hot=function(){

    }

}
