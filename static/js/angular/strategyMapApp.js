/**
 * Created by kyle on 2/7/14.
 */
var strategyMapApp = angular.module('strategyMapApp', ['textAngular']).config(function($interpolateProvider){
        $interpolateProvider.startSymbol('{[').endSymbol(']}');
});



strategyMapApp.controller('StrategyMapCtrl', function($scope, $http){
    var csrftoken = document.getElementById('csrftoken').value;
    $scope.change = function(mapping){
        alert(csrftoken);
        mapping.nonwtf_csrf_token = csrftoken;
        alert(JSON.stringify(mapping));
        $http.post('/strategymap',mapping);
        $('#mappingsaved').fadeIn(1200).fadeOut(800)
    };

    $scope.textAngularOpts = {};
});

strategyMapApp.directive('ckEditor', function() {
  return {
    require: '?ngModel',
    link: function(scope, elm, attr, ngModel) {
//      var ck = CKEDITOR.replace(elm[0]);
        var ck = elm[0];
        ck.css('contenteditable');

      if (!ngModel) return;

      ck.on('pasteState', function() {
        scope.$apply(function() {
          ngModel.$setViewValue(ck.getData());
        });
      });

      ngModel.$render = function(value) {
        ck.setData(ngModel.$viewValue);
      };
    }
  };
});