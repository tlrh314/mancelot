(function(angular) {
    'use strict';

    /**
     * @ngdoc controller
     * @name psonocli.controller:RegisterCtrl
     * @requires $scope
     * @requires $route
     * @requires $filter
     * @requires psonocli.managerDatastoreUser
     * @requires psonocli.browserClient
     * @requires psonocli.helper
     *
     * @description
     * Controller for the registration view
     */
    angular.module('psonocli').controller('RegisterCtrl', ['$scope', '$route', '$filter', 'managerDatastoreUser', 'browserClient', 'helper',
        function ($scope, $route, $filter, managerDatastoreUser, browserClient, helper) {

            $scope.select_server = select_server;
            $scope.changing = changing;
            $scope.register = register;

            activate();

            function activate() {
                var onSuccess = function(config) {

                    // TODO interpret "allow_custom_server"
                    // TODO check last visited server for "preselection"

                    /* Server selection with preselection */
                    $scope.servers = config['backend_servers'];
                    $scope.filtered_servers = $scope.servers;
                    $scope.selected_server = $scope.servers[0];
                    $scope.selected_server_title = $scope.selected_server.title;
                    $scope.selected_server_url = $scope.selected_server.url;
                    if ($scope.selected_server.domain) {
                        $scope.selected_server_domain = $scope.selected_server.domain;
                    } else {
                        $scope.selected_server_domain = helper.get_domain($scope.selected_server.url);
                    }
                };

                var onError = function() {

                };

                browserClient.get_config().then(onSuccess, onError);

                /* preselected values */
                // $scope.registerFormEmail = "register@saschapfeiffer.com";
                // $scope.registerFormUsername = "register";
                // $scope.registerFormPassword = "myPassword";
                // $scope.registerFormPasswordRepeat = "myPassword";

                browserClient.get_base_url().then(function(base_url){
                    $scope.base_url = base_url;
                });
            }

            /**
             * @ngdoc
             * @name psonocli.controller:RegisterCtrl#select_server
             * @methodOf psonocli.controller:RegisterCtrl
             *
             * @description
             * Select a server from the offered choices
             *
             * @param {object} server The selected server
             */
            function select_server(server) {
                //triggered when selecting an server
                $scope.selected_server = server;
                $scope.selected_server_title = server.title;
                $scope.selected_server_url = server.url;
                if (server.domain) {
                    $scope.selected_server_domain = server.domain;
                } else {
                    $scope.selected_server_domain = helper.get_domain(server.url);
                }
            }

            /**
             * @ngdoc
             * @name psonocli.controller:RegisterCtrl#changing
             * @methodOf psonocli.controller:RegisterCtrl
             *
             * @description
             * Triggered automatically once someone types something into the "Server" Field
             *
             * @param {url} url The typed url
             */
            function changing (url) {
                //triggered when typing an url
                $scope.selected_server = {title: url, url: url};
                $scope.selected_server_url = url;
                $scope.selected_server_domain = helper.get_domain(url);
                $scope.filtered_servers = $filter('filter')($scope.servers, {url: url});
            }

            /**
             * @ngdoc
             * @name psonocli.controller:RegisterCtrl#register
             * @methodOf psonocli.controller:RegisterCtrl
             *
             * @description
             * Triggered once someone clicks the register button
             *
             * @param {email} email The email one wants to register with
             * @param {string} username The username one wants to register with
             * @param {string} password The password one wants to register with
             * @param {string} password2 The password repeated
             */
            function register(email, username, password, password2) {


                $scope.errors = [];
                $scope.msgs = [];
                var test_result;

                function onError() {
                    alert("Error, should not happen.");
                }

                function onRequestReturn(data) {
                    if (data.response === "success") {
                        $scope.success = true;
                        $scope.msgs.push('Successful, check your e-mail.');
                    } else {
                        // handle server is offline
                        if (data.error_data === null) {
                            $scope.errors.push('Server offline.');
                            return;
                        }

                        // server is not offline and returned some errors
                        for (var property in data.error_data) {
                            if (!data.error_data.hasOwnProperty(property)) {
                                continue;
                            }
                            for (var i = 0; i < data.error_data[property].length; i++) {
                                $scope.errors.push(data.error_data[property][i]);
                            }
                        }
                    }
                }

                if (email === undefined || password === undefined || password2 === undefined || username === undefined) {
                    return;
                }

                test_result = helper.is_valid_password(password, password2);
                if (test_result !== true) {
                    $scope.errors.push(test_result);
                    return;
                }

                test_result = helper.is_valid_email(email);
                if (test_result !== true) {
                    $scope.errors.push("Invalid Email provided");
                    return;
                }

                username = helper.form_full_username(username, $scope.selected_server_domain);

                test_result = helper.is_valid_username(username);
                if (test_result !== true) {
                    $scope.errors.push(test_result);
                    return;
                }

                // TODO forbid weak and poor passwords

                managerDatastoreUser.register(email, username, password, angular.copy($scope.selected_server))
                    .then(onRequestReturn, onError);
            }
        }]
    );
}(angular));