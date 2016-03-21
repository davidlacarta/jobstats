var app = angular.module("jobstats_app", []);

app.config(function ($interpolateProvider, $httpProvider) {
    // conflict django templates {{}}
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    // json post
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    // request.is_ajax():
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});

app.controller('provinces_ctr',function($scope,$http){
    $scope.key_prov = "programador";
    $scope.search = function(){
        $('#jobs_prov').trigger('input');
        $('.progress.provinces').show()
        $http.get('/search', { params: { search : $scope.key_prov }})
            .success(function(response){
                $scope.prov_sal = angular.fromJson(response.prov_sal);
                $scope.prov_op = angular.fromJson(response.prov_op);
                $scope.prov_count = angular.fromJson(response.prov_count);
                $('.progress.provinces').hide()
            })
            .error(function(response) {
                console.log(response)
            });
    };
});

app.controller('jobs_ctr',function($scope,$http){
    $scope.key_jobs = "java,camarero";
    $scope.province = "Madrid";
    $scope.search = function(){
        $('#jobs_jobs').trigger('input');
        $('#province').trigger('input');
        $('.progress.jobs').show()
        $http.get('/search', { params: { search : $scope.key_jobs, province : $scope.province }})
            .success(function(response){
                $scope.jobs_sal = angular.fromJson(response.jobs_sal);
                $scope.jobs_op = angular.fromJson(response.jobs_op);
                $scope.jobs_count = angular.fromJson(response.jobs_count);
                $('.progress.jobs').hide();
            })
            .error(function(response) {
                console.log(response);
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

var provinces = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('key'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: {
        url: '/provinces', 
        ttl: 10,
        transform: function(list) {
            return list.province;
        }
    }
});

provinces.initialize();

$('#province').typeahead({
  hint: true,
  highlight: true,
  minLength: 1
},
{
  name: 'provinces',
  displayKey: 'key',
  valueKey: 'key',
  source: provinces.ttAdapter()
});

$('.progress').hide();
$('#jobs_jobs').val($('#jobs_jobs').prop('defaultValue'));
$('#jobs_prov').val($('#jobs_prov').prop('defaultValue'));
