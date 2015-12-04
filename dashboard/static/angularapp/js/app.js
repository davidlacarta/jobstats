var app = angular.module("instantsearch", []);

app.config(function ($interpolateProvider, $httpProvider) {
    // conflict django templates {{}}
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    // json post
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    // request.is_ajax():
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

    preloader = new $.materialPreloader({
        position: 'top',
        height: '5px',
        col_1: '#159756',
        col_2: '#da4733',
        col_3: '#3b78e7',
        col_4: '#fdba2c',
        fadeIn: 200,
        fadeOut: 200
    });
});

app.controller('someCtrl',function($scope,$http){
    $scope.search = function(){
        preloader.on();
        $('#error').fadeOut(200);
        $('#items').fadeOut(200);
        return $http.get('/search', { params: { search : $scope.keywords }})
            .success(function(response){
                $scope.items = angular.fromJson(response.items);
                $scope.summary = angular.fromJson(response.summary);
                $('#items').fadeIn(200);
                preloader.off();
            })
            .error(function(response) {
                preloader.off();
                $('#error').fadeIn(200);
                $('#items').fadeOut(200);
            });
    };
});

app.directive('myEnter', function () {
    return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if(event.which === 13) {
                scope.$apply(function (){
                    scope.$eval(attrs.myEnter);
                });

                event.preventDefault();
            }
        });
    };
});