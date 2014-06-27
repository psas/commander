var cmdr = angular.module('cmdr', []);

cmdr.controller('cmdrButtons', function ($scope, $http) {

    $scope.test = false;
    $scope.background = "#fff";

    $scope.settest = function () {
        $scope.test = !$scope.test;
        $scope.background = $scope.test ? "#ecc" : "#fff";
    };

    $scope.fire = function (e, cmd) {
        e.srcElement.disabled = true


        if ($scope.test) {
            cmd = '/TEST' + cmd;
        }

        console.log("Command"+cmd);
        var request = $http({
            method: "post",
            url: cmd
        }).success(function (d) {
            e.srcElement.disabled = false;
        });
    };

});
