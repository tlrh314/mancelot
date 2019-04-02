(function(angular) {
    'use strict';

    /**
     * @ngdoc controller
     * @name psonocli.controller:ModalShareNewEntryCtrl
     * @requires $scope
     * @requires $uibModalInstance
     * @requires psonocli.managerHost
     * @requires psonocli.shareBlueprint
     * @requires psonocli.browserClient
     * @requires psonocli.helper
     *
     * @description
     * Controller for the "New Entry" modal
     */
    angular.module('psonocli').controller('ModalShareNewEntryCtrl', ['$scope', '$uibModalInstance', 'managerHost',
        'shareBlueprint', 'browserClient', 'helper', 'parent', 'path', 'hide_advanced', 'hide_history',
        function ($scope, $uibModalInstance, managerHost,
                  shareBlueprint, browserClient, helper, parent, path, hide_advanced, hide_history) {

            $scope.reset = reset;
            $scope.save = save;
            $scope.cancel = cancel;

            $scope.parent = parent;
            $scope.path = path;
            $scope.name = '';
            $scope.content = '';
            $scope.isCollapsed = true;
            $scope.hide_advanced = hide_advanced;
            $scope.hide_history = hide_history;
            $scope.errors = [];
            $scope.bp = {
                all: shareBlueprint.get_blueprints(),
                selected: shareBlueprint.get_default_blueprint()
            };
            $scope.form_control = {'block_submit': true};

            activate();

            function activate() {
                var onSuccess = function(config) {

                    /* Server selection with preselection */
                    $scope.servers = config['backend_servers'];
                    $scope.filtered_servers = $scope.servers;
                    $scope.selected_server = managerHost.get_current_host();
                    $scope.selected_server_title = $scope.selected_server.title;
                    $scope.selected_server_url = $scope.selected_server.url;
                    $scope.selected_server_domain = helper.get_domain($scope.selected_server.url);
                };

                var onError = function() {

                };

                browserClient.get_config().then(onSuccess, onError);

                $scope.$watch('bp.selected', function(newValue, oldValue) {
                    if (typeof $scope.bp.selected.onNewModalOpen !== 'undefined') {
                        $scope.bp.selected.onNewModalOpen($scope.bp.selected);
                    }
                });
            }

            /**
             * Sets submitted to false
             */
            function reset() {
                $scope.submitted = false;
            }

            /**
             * Triggered once someone clicks the save button in the modal
             */
            function save() {
                $scope.errors = [];

                for (var i = 0; i < $scope.bp.selected.fields.length; i++) {
                    var field = $scope.bp.selected.fields[i];
                    if (field.hasOwnProperty("required")) {
                        if (field['required'] && field['value'] !== false && !field['value']) {
                            $scope.errors.push(field['title'] + '_IS_REQUIRED');
                            continue;
                        }
                    }
                    if (field.hasOwnProperty("type")) {
                        if (field['type'].toLowerCase() === 'url' && field['value'] && !helper.is_valid_url(field['value'])) {
                            $scope.errors.push('INVALID_URL_IN_' + field['title']);
                            continue;
                        }
                        if (field['type'].toLowerCase() === 'email' && field['value'] && !helper.is_valid_email(field['value'])) {
                            $scope.errors.push('INVALID_EMAIL_IN_' + field['title']);
                            continue;
                        }
                    }

                }

                if ($scope.errors.length > 0) {
                    return;
                }

                $uibModalInstance.close($scope.bp.selected);
            }

            /**
             * Triggered once someone clicks the cancel button in the modal
             */
            function cancel() {
                $uibModalInstance.dismiss('cancel');
            }
        }]
    );

}(angular));