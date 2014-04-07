/**
 * Created by Kyle on 3/23/14.
 */
var tasksApp = angular.module('tasksApp', ['textAngular']);

tasksApp.controller('TaskCtrl', function ($scope, $http) {
  $http.get('/refreshtasks').success(function(data) {
    $scope.tasks = data;
    });
   $scope.new = function(post){
//       alert(JSON.stringify(post));
        $http.post('/addtask',post);
        $http.get('/refreshtasks').success(function(data) {
            $scope.entries = data;
    });
  };
    $scope.update = function(entry){
        $http.post('/updatetask',entry);
            $http.get('/refreshtasks').success(function(data) {
                $scope.entries = data;
    });
    };
    $scope.deletetask = function(task){
        $http.post('/deletetask/'+task.id);
        $http.get('/refreshtasks').success(function(data) {
            $scope.entries = data;
        });
    };
    $scope.refreshtasks = function(){
        $http.get('/refreshtasks').success(function(data) {
                $scope.tasks = data;
        }).error(function(){alert('oops')});
    };

});
