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
        e.srcElement.disabled = true

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
            console.log(d.result);
            $scope.responses[$scope.responses.length - 1].response = d.result;
            RET = "IT WORKS"
            //$scope.responses.push({'time': "1", 'cmd': "Command"+cmd, 'response': d.result});
            //console.log(JSON.parse(d));
            e.srcElement.disabled = false;
        });
    };

});
