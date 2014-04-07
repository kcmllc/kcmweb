/**
 * Created by kyle on 2/7/14.
 */
var journalEntryApp = angular.module('journalEntryApp', ['textAngular']);

journalEntryApp.controller('JournalEntryCtrl', function ($scope, $http) {
  $http.get('/journalentries').success(function(data) {
    $scope.entries = data;

    });
   $scope.new = function(post){
//       alert(JSON.stringify(post));
        $http.post('/journal',post);
        $http.get('/journalentries').success(function(data) {
            $scope.entries = data;
    });
  };
    $scope.update = function(entry){
        $http.post('/journal',entry);
            $http.get('/journalentries').success(function(data) {
                $scope.entries = data;
    });
    };
    $scope.delete = function(entry){
        $http.delete('/journal/'+entry._id.$oid);
        $http.get('/journalentries').success(function(data) {
            $scope.entries = data;
        });
    };

});