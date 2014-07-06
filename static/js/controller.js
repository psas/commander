var cmdr = angular.module('cmdr', []);

cmdr.controller('cmdrButtons', function ($scope, $http) {

    // Init
    $scope.test = false;
    $scope.background = "#fff";
    $scope.busy = false;
    $scope.responses = [];

    // Test Mode button
    $scope.settest = function () {
        $scope.test = !$scope.test;
        $scope.background = $scope.test ? "#ecc" : "#fff";
    };

    // Clear the history
    $scope.clearHistory = function () {
        $scope.responses = [];
    };

    // Fire!
    $scope.fire = function (cmd, title) {

        // We fired a command, wait for response (diable other commands)
        $scope.busy = true;

        // Record local timestamp
        var time = new Date()
        var H = time.getHours();
        var M = time.getMinutes();
        var S = time.getSeconds();
        if (H   < 10) H = "0"+H;
        if (M < 10) M = "0"+M;
        if (S < 10) S = "0"+S;
        $scope.responses.push({'time': H+':'+M+':'+S, 'cmd': title, 'response': "pending..." });

        // Angular takes a few ms to push changes (probably at the end of this function call?). Update scroll after it gets there
        window.setTimeout(function () {
            var table = document.getElementById('history');
            table.scrollTop = table.scrollHeight;
        }, 5);

        // Use test server if in test mode
        if ($scope.test) {
            cmd = '/TEST' + cmd;
        }

        // Make HTTP request
        var request = $http({ method: "post", url: cmd }).
        success(function (d) {
            if (d.result == 'success')
                $scope.responses[$scope.responses.length - 1].response = d.data;
            else
                $scope.responses[$scope.responses.length - 1].response = d.result + " (" + d.reason + ")";
            $scope.busy = false;
        }).
        error(function (d) {
            $scope.responses[$scope.responses.length - 1].response = "Failed to contact CMDR server!";
            $scope.busy = false;
        });
    };
});
