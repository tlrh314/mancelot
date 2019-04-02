(function () {
    describe('Service: apiClient test suite', function () {

        beforeEach(module('psonocli', function ($translateProvider) {

            $translateProvider.translations('en', {});
        }));

        var $httpBackend, cryptoLibrary;

        beforeEach(inject(function($injector){
            // unwrap necessary services
            $httpBackend = $injector.get('$httpBackend');
            cryptoLibrary = $injector.get('cryptoLibrary');

            spyOn(cryptoLibrary, "encrypt_data").and.callFake(function(json_data, session_secret_key) {
                return JSON.parse(json_data);
            });
            $httpBackend.when('GET', "view/datastore.html").respond({});
        }));

        it('apiClient exists', inject(function (apiClient) {
            expect(apiClient).toBeDefined();
        }));

        it('ínfo', inject(function (apiClient) {

            $httpBackend.when('GET', "https://www.psono.pw/server/info/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.info()).toBeDefined();

            $httpBackend.flush();
        }));

        it('login', inject(function (apiClient) {

            var login_info = 'a-login_info';
            var login_info_nonce = 'a-login_info_nonce';
            var public_key = 'a-public_key';

            $httpBackend.when('POST', "https://www.psono.pw/server/authentication/login/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);
                    expect(data.login_info).toEqual(login_info);
                    expect(data.login_info_nonce).toEqual(login_info_nonce);
                    expect(data.public_key).toEqual(public_key);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.login(login_info, login_info_nonce, public_key)).toBeDefined();

            $httpBackend.flush();
        }));

        it('ga_verify', inject(function (apiClient) {

            var token = 'a-token';
            var ga_token = 'a-ga_token';
            var session_secret_key = 'a-session_secret_key';

            $httpBackend.when('POST', "https://www.psono.pw/server/authentication/ga-verify/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.ga_token).toEqual(ga_token);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.ga_verify(token, ga_token, session_secret_key)).toBeDefined();

            $httpBackend.flush();
        }));

        it('yubikey_otp_verify', inject(function (apiClient) {

            var token = 'a-token';
            var yubikey_otp = 'a-yubikey_otp';
            var session_secret_key = 'a-session_secret_key';

            $httpBackend.when('POST', "https://www.psono.pw/server/authentication/yubikey-otp-verify/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.yubikey_otp).toEqual(yubikey_otp);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.yubikey_otp_verify(token, yubikey_otp, session_secret_key)).toBeDefined();

            $httpBackend.flush();
        }));

        it('activate_token', inject(function (apiClient) {

            var token = 'a-token';
            var verification = 'a-verification';
            var verification_nonce = 'a-verification_nonce';
            var session_secret_key = 'a-session_secret_key';

            $httpBackend.when('POST', "https://www.psono.pw/server/authentication/activate-token/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.verification).toEqual(verification);
                    expect(data.verification_nonce).toEqual(verification_nonce);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.activate_token(token, verification, verification_nonce, session_secret_key)).toBeDefined();

            $httpBackend.flush();
        }));

        it('get_sessions', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';

            $httpBackend.when('GET', "https://www.psono.pw/server/authentication/sessions/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.get_sessions(token, session_secret_key)).toBeDefined();

            $httpBackend.flush();
        }));

        it('logout', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';

            $httpBackend.when('POST', "https://www.psono.pw/server/authentication/logout/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    // will fail for everything that is no ISO date and return NAN which is not bigger than 0
                    expect(Date.parse(data.request_time) > 0).toBeTruthy();

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.logout(token, session_secret_key)).toBeDefined();

            $httpBackend.flush();
        }));

        it('logout other session', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var session_id = '82dc7d4b-1078-4df4-86b4-9deaccb75de9';

            $httpBackend.when('POST', "https://www.psono.pw/server/authentication/logout/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(data.session_id).toEqual(session_id);
                    // will fail for everything that is no ISO date and return NAN which is not bigger than 0
                    expect(Date.parse(data.request_time) > 0).toBeTruthy();

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.logout(token, session_secret_key, session_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('register', inject(function (apiClient) {

            var email = 'a-email';
            var username = 'a-username';
            var authkey = 'a-authkey';
            var public_key = 'a-public_key';
            var private_key = 'a-private_key';
            var private_key_nonce = 'a-private_key_nonce';
            var secret_key = 'a-secret_key';
            var secret_key_nonce = 'a-secret_key_nonce';
            var user_sauce = 'a-user_sauce';
            var base_url = 'a-base_url';

            $httpBackend.when('POST', "https://www.psono.pw/server/authentication/register/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(data.email).toEqual(email);
                    expect(data.username).toEqual(username);
                    expect(data.authkey).toEqual(authkey);
                    expect(data.public_key).toEqual(public_key);
                    expect(data.private_key).toEqual(private_key);
                    expect(data.private_key_nonce).toEqual(private_key_nonce);
                    expect(data.secret_key).toEqual(secret_key);
                    expect(data.secret_key_nonce).toEqual(secret_key_nonce);
                    expect(data.user_sauce).toEqual(user_sauce);
                    expect(data.base_url).toEqual(base_url);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.register(email, username, authkey, public_key, private_key, private_key_nonce, secret_key, secret_key_nonce, user_sauce, base_url)).toBeDefined();

            $httpBackend.flush();
        }));

        it('verify_email', inject(function (apiClient) {

            var activation_code = 'a-activation_code';

            $httpBackend.when('POST', "https://www.psono.pw/server/authentication/verify-email/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(data.activation_code).toEqual(activation_code);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.verify_email(activation_code)).toBeDefined();

            $httpBackend.flush();
        }));

        it('update_user', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var email = 'a-email';
            var authkey = 'a-authkey';
            var authkey_old = 'a-authkey_old';
            var private_key = 'a-private_key';
            var private_key_nonce = 'a-private_key_nonce';
            var secret_key = 'a-secret_key';
            var secret_key_nonce = 'a-secret_key_nonce';
            var user_sauce = 'a-user_sauce';

            $httpBackend.when('PUT', "https://www.psono.pw/server/user/update/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.email).toEqual(email);
                    expect(data.authkey).toEqual(authkey);
                    expect(data.authkey_old).toEqual(authkey_old);
                    expect(data.private_key).toEqual(private_key);
                    expect(data.private_key_nonce).toEqual(private_key_nonce);
                    expect(data.secret_key).toEqual(secret_key);
                    expect(data.secret_key_nonce).toEqual(secret_key_nonce);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.update_user(token, session_secret_key, email, authkey, authkey_old, private_key, private_key_nonce, secret_key, secret_key_nonce, user_sauce)).toBeDefined();

            $httpBackend.flush();
        }));

        it('write_recoverycode', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var recovery_authkey = 'a-recovery_authkey';
            var recovery_data = 'a-recovery_data';
            var recovery_data_nonce = 'a-recovery_data_nonce';
            var recovery_sauce = 'a-recovery_sauce';

            $httpBackend.when('POST', "https://www.psono.pw/server/recoverycode/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.recovery_authkey).toEqual(recovery_authkey);
                    expect(data.recovery_data).toEqual(recovery_data);
                    expect(data.recovery_data_nonce).toEqual(recovery_data_nonce);
                    expect(data.recovery_sauce).toEqual(recovery_sauce);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.write_recoverycode(token, session_secret_key, recovery_authkey, recovery_data, recovery_data_nonce, recovery_sauce)).toBeDefined();

            $httpBackend.flush();
        }));

        it('enable_recoverycode ', inject(function (apiClient) {

            var username = 'a-username';
            var recovery_authkey = 'a-recovery_authkey';

            $httpBackend.when('POST', "https://www.psono.pw/server/password/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(data.username).toEqual(username);
                    expect(data.recovery_authkey).toEqual(recovery_authkey);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.enable_recoverycode(username, recovery_authkey)).toBeDefined();

            $httpBackend.flush();
        }));

        it('set_password  ', inject(function (apiClient) {

            var username = 'a-username';
            var recovery_authkey = 'a-recovery_authkey';
            var update_data = 'a-update_data';
            var update_data_nonce = 'a-update_data_nonce';

            $httpBackend.when('PUT', "https://www.psono.pw/server/password/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(data.username).toEqual(username);
                    expect(data.recovery_authkey).toEqual(recovery_authkey);
                    expect(data.update_data).toEqual(update_data);
                    expect(data.update_data_nonce).toEqual(update_data_nonce);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.set_password (username, recovery_authkey, update_data, update_data_nonce)).toBeDefined();

            $httpBackend.flush();
        }));

        it('read_datastore', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var datastore_id = 'a-datastore_id';

            $httpBackend.when('GET', "https://www.psono.pw/server/datastore/a-datastore_id/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.read_datastore(token, session_secret_key, datastore_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('create_datastore', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var type = 'a-type';
            var description = 'a-description';
            var encrypted_data = 'a-encrypted_data';
            var encrypted_data_nonce = 'a-encrypted_data_nonce';
            var is_default = 'a-is_default';
            var encrypted_data_secret_key = 'a-encrypted_data_secret_key';
            var encrypted_data_secret_key_nonce = 'a-encrypted_data_secret_key_nonce';

            $httpBackend.when('PUT', "https://www.psono.pw/server/datastore/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.type).toEqual(type);
                    expect(data.description).toEqual(description);
                    expect(data.data).toEqual(encrypted_data);
                    expect(data.data_nonce).toEqual(encrypted_data_nonce);
                    expect(data.is_default).toEqual(is_default);
                    expect(data.secret_key).toEqual(encrypted_data_secret_key);
                    expect(data.secret_key_nonce).toEqual(encrypted_data_secret_key_nonce);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.create_datastore(token, session_secret_key, type, description, encrypted_data, encrypted_data_nonce, is_default, encrypted_data_secret_key, encrypted_data_secret_key_nonce)).toBeDefined();

            $httpBackend.flush();
        }));

        it('delete_datastore', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var datastore_id = 'a-datastore-id';
            var authkey = 'a-authkey';

            $httpBackend.when('DELETE', "https://www.psono.pw/server/datastore/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.datastore_id).toEqual(datastore_id);
                    expect(data.authkey).toEqual(authkey);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.delete_datastore(token, session_secret_key, datastore_id, authkey)).toBeDefined();

            $httpBackend.flush();
        }));

        it('write_datastore', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var datastore_id = 'a-datastore_id';
            var encrypted_data = 'a-encrypted_data';
            var encrypted_data_nonce = 'a-encrypted_data';
            var encrypted_data_secret_key = 'a-encrypted_data_secret_key';
            var encrypted_data_secret_key_nonce = 'a-encrypted_data_secret_key_nonce';

            $httpBackend.when('POST', "https://www.psono.pw/server/datastore/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.datastore_id).toEqual(datastore_id);
                    expect(data.data).toEqual(encrypted_data);
                    expect(data.data_nonce).toEqual(encrypted_data_nonce);
                    expect(data.secret_key).toEqual(encrypted_data_secret_key);
                    expect(data.secret_key_nonce).toEqual(encrypted_data_secret_key_nonce);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.write_datastore(token, session_secret_key, datastore_id, encrypted_data, encrypted_data_nonce,
                encrypted_data_secret_key, encrypted_data_secret_key_nonce)).toBeDefined();

            $httpBackend.flush();
        }));

        it('read_secret', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var secret_id = 'a-secret_id';

            $httpBackend.when('GET', "https://www.psono.pw/server/secret/a-secret_id/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.read_secret(token, session_secret_key, secret_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('create_secret', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var encrypted_data = 'a-datastore_id';
            var encrypted_data_nonce = 'a-encrypted_data';
            var link_id = 'a-link_id';
            var parent_datastore_id = 'a-parent_datastore_id';
            var parent_share_id = 'a-parent_share_id';

            $httpBackend.when('PUT', "https://www.psono.pw/server/secret/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.data).toEqual(encrypted_data);
                    expect(data.data_nonce).toEqual(encrypted_data_nonce);
                    expect(data.link_id).toEqual(link_id);
                    expect(data.parent_datastore_id).toEqual(parent_datastore_id);
                    expect(data.parent_share_id).toEqual(parent_share_id);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.create_secret(token, session_secret_key, encrypted_data, encrypted_data_nonce, link_id, parent_datastore_id, parent_share_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('write_secret', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var secret_id = 'a-secret_id';
            var encrypted_data = 'a-encrypted_data';
            var encrypted_data_nonce = 'a-encrypted_data_nonce';

            $httpBackend.when('POST', "https://www.psono.pw/server/secret/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.secret_id).toEqual(secret_id);
                    expect(data.data).toEqual(encrypted_data);
                    expect(data.data_nonce).toEqual(encrypted_data_nonce);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.write_secret(token, session_secret_key, secret_id, encrypted_data, encrypted_data_nonce)).toBeDefined();

            $httpBackend.flush();
        }));

        it('move_secret_link', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var link_id = 'a-link_id';
            var new_parent_share_id = 'a-new_parent_share_id';
            var new_parent_datastore_id = 'a-new_parent_datastore_id';

            $httpBackend.when('POST', "https://www.psono.pw/server/secret/link/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.link_id).toEqual(link_id);
                    expect(data.new_parent_share_id).toEqual(new_parent_share_id);
                    expect(data.new_parent_datastore_id).toEqual(new_parent_datastore_id);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.move_secret_link(token, session_secret_key, link_id, new_parent_share_id, new_parent_datastore_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('delete_secret_link', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var link_id = 'a-link_id';

            $httpBackend.when('DELETE', "https://www.psono.pw/server/secret/link/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.link_id).toEqual(link_id);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.delete_secret_link(token, session_secret_key, link_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('read_share', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var share_id = 'a-share_id';

            $httpBackend.when('GET', "https://www.psono.pw/server/share/a-share_id/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.read_share(token, session_secret_key, share_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('read_shares', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';

            $httpBackend.when('GET', "https://www.psono.pw/server/share/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.read_shares(token, session_secret_key)).toBeDefined();

            $httpBackend.flush();
        }));

        it('create_share', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var encrypted_data = 'a-encrypted_data';
            var encrypted_data_nonce = 'a-encrypted_data_nonce';
            var key = 'a-key';
            var key_nonce = 'a-key_nonce';
            var parent_share_id = 'a-parent_share_id';
            var parent_datastore_id = 'a-parent_datastore_id';
            var link_id = 'a-link_id';

            $httpBackend.when('POST', "https://www.psono.pw/server/share/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.data).toEqual(encrypted_data);
                    expect(data.data_nonce).toEqual(encrypted_data_nonce);
                    expect(data.key).toEqual(key);
                    expect(data.key_nonce).toEqual(key_nonce);
                    expect(data.parent_share_id).toEqual(parent_share_id);
                    expect(data.parent_datastore_id).toEqual(parent_datastore_id);
                    expect(data.link_id).toEqual(link_id);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.create_share(token, session_secret_key, encrypted_data, encrypted_data_nonce, key, key_nonce, parent_share_id,
                parent_datastore_id, link_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('write_share', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var share_id = 'a-share_id';
            var encrypted_data = 'a-encrypted_data';
            var encrypted_data_nonce = 'a-encrypted_data_nonce';

            $httpBackend.when('PUT', "https://www.psono.pw/server/share/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.share_id).toEqual(share_id);
                    expect(data.data).toEqual(encrypted_data);
                    expect(data.data_nonce).toEqual(encrypted_data_nonce);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.write_share(token, session_secret_key, share_id, encrypted_data, encrypted_data_nonce)).toBeDefined();

            $httpBackend.flush();
        }));

        it('read_share_rights', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var share_id = 'a-share_id';

            $httpBackend.when('GET', "https://www.psono.pw/server/share/rights/a-share_id/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.read_share_rights(token, session_secret_key, share_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('read_share_rights_overview', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';

            $httpBackend.when('GET', "https://www.psono.pw/server/share/right/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.read_share_rights_overview(token, session_secret_key)).toBeDefined();

            $httpBackend.flush();
        }));

        it('create_share_right', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var encrypted_title = 'a-encrypted_title';
            var encrypted_title_nonce = 'a-encrypted_title_nonce';
            var encrypted_type = 'a-encrypted_type';
            var encrypted_type_nonce = 'a-encrypted_type_nonce';
            var share_id = 'a-share_id';
            var user_id = 'a-user_id';
            var group_id = undefined;
            var key = 'a-key';
            var key_nonce = 'a-key_nonce';
            var read = 'a-read';
            var write = 'a-write';
            var grant = 'a-grant';

            $httpBackend.when('PUT', "https://www.psono.pw/server/share/right/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.title).toEqual(encrypted_title);
                    expect(data.title_nonce).toEqual(encrypted_title_nonce);
                    expect(data.type).toEqual(encrypted_type);
                    expect(data.type_nonce).toEqual(encrypted_type_nonce);
                    expect(data.share_id).toEqual(share_id);
                    expect(data.user_id).toEqual(user_id);
                    expect(data.key).toEqual(key);
                    expect(data.key_nonce).toEqual(key_nonce);
                    expect(data.read).toEqual(read);
                    expect(data.write).toEqual(write);
                    expect(data.grant).toEqual(grant);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.create_share_right(token, session_secret_key, encrypted_title, encrypted_title_nonce, encrypted_type, encrypted_type_nonce, share_id,
                user_id, group_id, key, key_nonce, read, write, grant)).toBeDefined();

            $httpBackend.flush();
        }));

        it('update_share_right', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var share_id = 'a-share_id';
            var user_id = 'a-user_id';
            var read = 'a-read';
            var write = 'a-write';
            var grant = 'a-grant';
            var group_id;

            $httpBackend.when('POST', "https://www.psono.pw/server/share/right/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.share_id).toEqual(share_id);
                    expect(data.user_id).toEqual(user_id);
                    expect(data.read).toEqual(read);
                    expect(data.write).toEqual(write);
                    expect(data.grant).toEqual(grant);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.update_share_right(token, session_secret_key, share_id,
                user_id, group_id, read, write, grant)).toBeDefined();

            $httpBackend.flush();
        }));

        it('delete_share_right', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var user_share_right_id = 'a-usershare_right_id';
            var group_share_right_id = 'a-groupshare_right_id';

            $httpBackend.when('DELETE', "https://www.psono.pw/server/share/right/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.user_share_right_id).toEqual(user_share_right_id);
                    expect(data.group_share_right_id).toEqual(group_share_right_id);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.delete_share_right(token, session_secret_key, user_share_right_id, group_share_right_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('read_share_rights_inherit_overview', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';

            $httpBackend.when('GET', "https://www.psono.pw/server/share/right/inherit/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.read_share_rights_inherit_overview(token, session_secret_key)).toBeDefined();

            $httpBackend.flush();
        }));

        it('accept_share_right', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var share_right_id = 'a-share_right_id';
            var key = 'a-key';
            var key_nonce = 'a-key_nonce';

            $httpBackend.when('POST', "https://www.psono.pw/server/share/right/accept/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.share_right_id).toEqual(share_right_id);
                    expect(data.key).toEqual(key);
                    expect(data.key_nonce).toEqual(key_nonce);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.accept_share_right(token, session_secret_key, share_right_id, key, key_nonce)).toBeDefined();

            $httpBackend.flush();
        }));

        it('decline_share_right', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var share_right_id = 'a-share_right_id';

            $httpBackend.when('POST', "https://www.psono.pw/server/share/right/decline/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.share_right_id).toEqual(share_right_id);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.decline_share_right(token, session_secret_key, share_right_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('get_users_public_key', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var user_id = 'a-user_id';
            var user_username = 'a-user_username';

            $httpBackend.when('POST', "https://www.psono.pw/server/user/search/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.user_id).toEqual(user_id);
                    expect(data.user_username).toEqual(user_username);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.search_user(token, session_secret_key, user_id, user_username)).toBeDefined();

            $httpBackend.flush();
        }));

        it('create_ga', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var title = 'a-title';

            $httpBackend.when('PUT', "https://www.psono.pw/server/user/ga/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.title).toEqual(title);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.create_ga(token, session_secret_key, title)).toBeDefined();

            $httpBackend.flush();
        }));

        it('read_ga', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';

            $httpBackend.when('GET', "https://www.psono.pw/server/user/ga/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));


                    // return answer
                    return [200, {}];
                });

            expect(apiClient.read_ga(token, session_secret_key)).toBeDefined();

            $httpBackend.flush();
        }));

        it('delete_ga', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var google_authenticator_id = 'a-google_authenticator_id';

            $httpBackend.when('DELETE', "https://www.psono.pw/server/user/ga/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.google_authenticator_id).toEqual(google_authenticator_id);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.delete_ga(token, session_secret_key, google_authenticator_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('create_yubikey_otp', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var title = 'a-title';
            var yubikey_otp = 'a-yubikey_otp';

            $httpBackend.when('PUT', "https://www.psono.pw/server/user/yubikey-otp/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.title).toEqual(title);
                    expect(data.yubikey_otp).toEqual(yubikey_otp);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.create_yubikey_otp(token, session_secret_key, title, yubikey_otp)).toBeDefined();

            $httpBackend.flush();
        }));

        it('read_yubikey_otp', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';

            $httpBackend.when('GET', "https://www.psono.pw/server/user/yubikey-otp/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));


                    // return answer
                    return [200, {}];
                });

            expect(apiClient.read_yubikey_otp(token, session_secret_key)).toBeDefined();

            $httpBackend.flush();
        }));

        it('delete_yubikey_otp', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var yubikey_otp_id = 'a-yubikey_otp_id';

            $httpBackend.when('DELETE', "https://www.psono.pw/server/user/yubikey-otp/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.yubikey_otp_id).toEqual(yubikey_otp_id);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.delete_yubikey_otp(token, session_secret_key, yubikey_otp_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('create_share_link', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var link_id = 'a-link_id';
            var share_id = 'a-share_id';
            var parent_share_id = 'a-parent_share_id';
            var parent_datastore_id = 'a-parent_datastore_id';

            $httpBackend.when('PUT', "https://www.psono.pw/server/share/link/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.link_id).toEqual(link_id);
                    expect(data.share_id).toEqual(share_id);
                    expect(data.parent_share_id).toEqual(parent_share_id);
                    expect(data.parent_datastore_id).toEqual(parent_datastore_id);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.create_share_link(token, session_secret_key, link_id, share_id, parent_share_id, parent_datastore_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('move_share_link', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var link_id = 'a-link_id';
            var new_parent_share_id = 'a-new_parent_share_id';
            var new_parent_datastore_id = 'a-new_parent_datastore_id';

            $httpBackend.when('POST', "https://www.psono.pw/server/share/link/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.link_id).toEqual(link_id);
                    expect(data.new_parent_share_id).toEqual(new_parent_share_id);
                    expect(data.new_parent_datastore_id).toEqual(new_parent_datastore_id);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.move_share_link(token, session_secret_key, link_id, new_parent_share_id, new_parent_datastore_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('delete_share_link', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var link_id = 'a-link_id';

            $httpBackend.when('DELETE', "https://www.psono.pw/server/share/link/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.link_id).toEqual(link_id);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.delete_share_link(token, session_secret_key, link_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('read_group_specific', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var group_id = 'a-group_id';

            $httpBackend.when('GET', "https://www.psono.pw/server/group/a-group_id/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.read_group(token, session_secret_key, group_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('read_group_all', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';

            $httpBackend.when('GET', "https://www.psono.pw/server/group/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.read_group(token, session_secret_key)).toBeDefined();

            $httpBackend.flush();
        }));

        it('create_group', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var name = 'a-name';
            var secret_key = 'a-secret_key';
            var secret_key_nonce = 'a-secret_key_nonce';
            var private_key = 'a-private_key';
            var private_key_nonce = 'a-private_key_nonce';
            var public_key = 'a-public_key';

            $httpBackend.when('PUT', "https://www.psono.pw/server/group/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.name).toEqual(name);
                    expect(data.secret_key).toEqual(secret_key);
                    expect(data.secret_key).toEqual(secret_key);
                    expect(data.secret_key_nonce).toEqual(secret_key_nonce);
                    expect(data.private_key).toEqual(private_key);
                    expect(data.private_key_nonce).toEqual(private_key_nonce);
                    expect(data.public_key).toEqual(public_key);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.create_group(token, session_secret_key, name, secret_key, secret_key_nonce, private_key, private_key_nonce, public_key)).toBeDefined();

            $httpBackend.flush();
        }));

        it('update_group', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var group_id = 'a-group_id';
            var name = 'a-name';

            $httpBackend.when('POST', "https://www.psono.pw/server/group/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.group_id).toEqual(group_id);
                    expect(data.name).toEqual(name);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.update_group(token, session_secret_key, group_id, name)).toBeDefined();

            $httpBackend.flush();
        }));

        it('delete_group', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var group_id = 'a-group_id';

            $httpBackend.when('DELETE', "https://www.psono.pw/server/group/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.group_id).toEqual(group_id);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.delete_group(token, session_secret_key, group_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('read_group_rights_specific', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var group_id = 'a-group_id';

            $httpBackend.when('GET', "https://www.psono.pw/server/group/rights/a-group_id/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.read_group_rights(token, session_secret_key, group_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('read_group_rights_all', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';

            $httpBackend.when('GET', "https://www.psono.pw/server/group/rights/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.read_group_rights(token, session_secret_key)).toBeDefined();

            $httpBackend.flush();
        }));

        it('create_membership', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var group_id = 'a-group_id';
            var user_id = 'a-user_id';
            var secret_key = 'a-secret_key';
            var secret_key_nonce = 'a-secret_key_nonce';
            var secret_key_type = 'a-secret_key_type';
            var private_key = 'a-private_key';
            var private_key_nonce = 'a-private_key_nonce';
            var private_key_type = 'a-private_key_type';
            var group_admin = 'a-group_admin';

            $httpBackend.when('PUT', "https://www.psono.pw/server/membership/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.group_id).toEqual(group_id);
                    expect(data.user_id).toEqual(user_id);
                    expect(data.secret_key).toEqual(secret_key);
                    expect(data.secret_key_nonce).toEqual(secret_key_nonce);
                    expect(data.secret_key_type).toEqual(secret_key_type);
                    expect(data.private_key).toEqual(private_key);
                    expect(data.private_key_nonce).toEqual(private_key_nonce);
                    expect(data.private_key_type).toEqual(private_key_type);
                    expect(data.group_admin).toEqual(group_admin);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.create_membership(token, session_secret_key, group_id, user_id, secret_key,
                secret_key_nonce,secret_key_type, private_key, private_key_nonce, private_key_type, group_admin)).toBeDefined();

            $httpBackend.flush();
        }));

        it('update_membership', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var membership_id = 'a-membership_id';
            var group_admin = 'a-group_admin';

            $httpBackend.when('POST', "https://www.psono.pw/server/membership/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.membership_id).toEqual(membership_id);
                    expect(data.group_admin).toEqual(group_admin);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.update_membership(token, session_secret_key, membership_id, group_admin)).toBeDefined();

            $httpBackend.flush();
        }));

        it('delete_membership', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var membership_id = 'a-membership_id';

            $httpBackend.when('DELETE', "https://www.psono.pw/server/membership/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.membership_id).toEqual(membership_id);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.delete_membership(token, session_secret_key, membership_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('accept_membership', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var membership_id = 'a-membership_id';

            $httpBackend.when('POST', "https://www.psono.pw/server/membership/accept/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.membership_id).toEqual(membership_id);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.accept_membership(token, session_secret_key, membership_id)).toBeDefined();

            $httpBackend.flush();
        }));

        it('decline_membership', inject(function (apiClient) {

            var token = 'a-token';
            var session_secret_key = 'a-session_secret_key';
            var membership_id = 'a-membership_id';

            $httpBackend.when('POST', "https://www.psono.pw/server/membership/decline/").respond(
                function(method, url, data, headers, params) {
                    // Validate request parameters:
                    data = JSON.parse(data);

                    expect(headers.Authorization).toEqual('Token ' + token);
                    expect(headers['Authorization-Validator']).toEqual(jasmine.any(String));

                    expect(data.membership_id).toEqual(membership_id);

                    // return answer
                    return [200, {}];
                });

            expect(apiClient.decline_membership(token, session_secret_key, membership_id)).toBeDefined();

            $httpBackend.flush();
        }));

    });

}).call();
