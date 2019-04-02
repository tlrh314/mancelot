(function(angular) {
    'use strict';

    /**
     * @ngdoc controller
     * @name psonocli.controller:OtherSessionsCtrl
     * @requires $rootScope
     * @requires $scope
     * @requires $routeParams
     * @requires psonocli.managerDatastoreUser
     * @requires psonocli.helper
     *
     * @description
     * Controller for the Sessions tab in the "Others" menu
     */
    angular.module('psonocli').controller('OtherSessionsCtrl', ['$rootScope', '$scope', '$routeParams', 'managerDatastoreUser', 'helper', 'languagePicker', 'DTOptionsBuilder', 'DTColumnDefBuilder',
        function ($rootScope, $scope, $routeParams, managerDatastoreUser, helper, languagePicker, DTOptionsBuilder, DTColumnDefBuilder) {

            $scope.dtOptions = DTOptionsBuilder
                .newOptions()
                .withLanguageSource('translations/datatables.' + languagePicker.get_active_language_code() + '.json');

            $scope.dtColumnDefs = [
                DTColumnDefBuilder.newColumnDef(0),
                DTColumnDefBuilder.newColumnDef(1),
                DTColumnDefBuilder.newColumnDef(2),
                DTColumnDefBuilder.newColumnDef(3)
            ];

            $scope.delete_session = delete_session;

            $scope.sessions=[];

            activate();
            function activate() {
                managerDatastoreUser.get_sessions().then(function (sessions) {
                    $scope.sessions = sessions;
                });
            }

            /**
             * @ngdoc
             * @name psonocli.controller:OtherSessionsCtrl#delete_session
             * @methodOf psonocli.controller:OtherSessionsCtrl
             *
             * @description
             * deletes an open session with given session id
             *
             * @param {uuid} session_id The session id to delete
             */
            function delete_session(session_id) {

                var onSuccess = function () {
                    helper.remove_from_array($scope.sessions, session_id, function(session, session_id) {
                        return session['id'] === session_id;
                    });
                };
                var onError = function () {
                };

                managerDatastoreUser.delete_session(session_id).then(onSuccess, onError);
            }
        }]
    );
}(angular));