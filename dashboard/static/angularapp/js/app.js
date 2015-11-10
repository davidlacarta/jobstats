var app = angular.module("instantsearch", []);

app.config(function ($interpolateProvider, $httpProvider) {
    // conflict django templates {{}}
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    // json post
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    // request.is_ajax():
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
})

app.controller('someCtrl',function($scope,$http){
    $scope.search = function(){
        console.log($scope.keywords)
        return $http.get('/offers', { params: { search : $scope.keywords }})
            .success(function(response){
                $scope.items = angular.fromJson(response.search_offers);
            })
            .error(function(response) {
                console.log("No data found..");
            });
    };
});