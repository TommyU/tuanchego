angular.module('app.base').controller('headerController', headerController);

headerController.$inject = ['$scope','$rootScope'];
function headerController($scope, $rootScope) {
    $scope.$on('$includeContentLoaded', function() {
        Layout.initHeader(); // init header
    });
    /*$rootScope.$on('$stateChangeStart', 
	function(event, toState, toParams, fromState, fromParams){ 
	    // do something
	    if(toState!='base.home'){
	    	$scrop.navRegSlidVisible=false;
	    }else{
	    	$scrop.navRegSlidVisible=true;
	    }
	});*/
}
