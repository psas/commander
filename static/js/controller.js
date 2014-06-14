var cmdr = angular.module('cmdr', []);

cmdr.controller('cmdrButtons', function ($scope) {
    $scope.fire = function (cmd) {
        console.log("send command");
    };
});
