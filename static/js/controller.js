var cmdr = angular.module('cmdr', []);

cmdr.controller('cmdrButtons', function ($scope, $http) {

    $scope.fire = function (e, cmd) {
        $scope.loading = true;
        e.srcElement.disabled = true
        console.log("Command"+cmd);

        var request = $http({
            method: "post",
            url: cmd
        }).success(function (d) {
            e.srcElement.disabled = false;
        });
    };

});
