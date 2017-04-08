angular.module('app.brand.services').factory('BrandService', BrandService);

BrandService.$inject = ['$http'];
function BrandService($http) {
    return {
        getBrandActs:function(condition, callback, error_callback){
             $http.post(
                '/api/acts/by_brand',
                {
                    brand_id:condition.brand,
                    lid:condition.city_id,
                    page_index:condition.page_index,
                    page_size:condition.page_size
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
        }
    };
}
