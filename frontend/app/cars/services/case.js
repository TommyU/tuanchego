angular.module('app.cars.services').factory('CarService', CarService);

CarService.$inject = ['$http'];
function CarService($http) {
    var _service ={
        getCars:function(searchConditions, callback, error_callback){
            $http.post(
                '/api/cars/',
                {
                    price:searchConditions.price,
                    size:searchConditions.size,
                    brand:searchConditions.brand,
                    displacement:searchConditions.displacement,
                    gearbox:searchConditions.gearbox,
                    country:searchConditions.country,
                    page_index:searchConditions.page_index,
                    page_size:searchConditions.page_size
                }
            ).then(
                function(response){
                    if(response.data.error==undefined){
                        callback(response.data);
                    }else{
                        console.log(response.data.error);
                        if(error_callback!=undefined){
                            error_callback(response.data);
                        }
                    }
                },
                function(response){

                }
            );
        },
    };
    return _service;
}
