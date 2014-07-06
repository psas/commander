var cmdr = angular.module('cmdr', []);

cmdr.controller('cmdrButtons', function ($scope, $http) {

    // Init
    $scope.test = false;
    $scope.background = "#fff";
    $scope.busy = false;

    $scope.settest = function () {
        $scope.test = !$scope.test;
        $scope.background = $scope.test ? "#ecc" : "#fff";
    };

    $scope.responses = [];

    $scope.clearHistory = function () {
        $scope.responses = [];
    };

    $scope.fire = function (cmd, title) {
        $scope.busy = true;

        var time = new Date()
        var H = time.getHours();
        var M = time.getMinutes();
        var S = time.getSeconds();
        if (H   < 10) H = "0"+H;
        if (M < 10) M = "0"+M;
        if (S < 10) S = "0"+S;
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
            $scope.busy = false;
        }).error(function (d) {
            $scope.responses[$scope.responses.length - 1].response = "Failed to contact CMDR server!";
            $scope.busy = false;
        });
    };

});
