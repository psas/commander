var cmdr = angular.module('cmdr', []);

cmdr.controller('cmdrButtons', function ($scope, $http) {

    $scope.test = false;
    $scope.background = "#fff";

    $scope.settest = function () {
        $scope.test = !$scope.test;
        $scope.background = $scope.test ? "#ecc" : "#fff";
    };

    $scope.responses = [];

    $scope.clearHistory = function () {
        $scope.responses = [];
    };

    $scope.fire = function (e, cmd, title) {
        e.target.disabled = true;

        var time = new Date()
        var H = time.getHours();
        var M = time.getMinutes();
        var S = time.getSeconds();
        $scope.responses.push({'time': H+':'+M+':'+S, 'cmd': title, 'response': "pending..." });

        if ($scope.test) {
            cmd = '/TEST' + cmd;
        }

        var request = $http({
            method: "post",
            url: cmd
        }).success(function (d) {
            if (d.result == 'success') {
                $scope.responses[$scope.responses.length - 1].response = d.data;
            }
            else {
                $scope.responses[$scope.responses.length - 1].response = d.result + " (" + d.reason + ")";
            }
            e.target.disabled = false;
        });
    };

});
