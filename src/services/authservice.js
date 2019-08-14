import decode from 'jwt-decode';

const accessToken = 'accessToken';

export default class AuthService {

    constructor(domain) {
        this.domain = domain || 'http://localhost:8080';
        this.fetch = this.fetch.bind(this);
        this.getProfile = this.getProfile.bind(this);
    }

    login = (username, password) => {
        return this.fetch(`${this.domain}/auth/jwtoken/`, {
            method: 'POST',
            body: JSON.stringify({
                username,
                password
            })
        }).then(res => {
            this.setToken(res.token);
            return Promise.resolve(res);
        });
    };

    loggedIn() {
        const token = this.getToken();
        return !!token && !this.isTokenExpired(token);
    }

    isTokenExpired(token) {
        try {
            const decoded = decode(token);
            if (decoded.exp < Date.now() / 1000) {
                return true;
            }
        }
        catch (err) {
            return false;
        }
    }

    setToken(idToken) {
        localStorage.setItem(accessToken, idToken);
    }

    getToken() {
        return localStorage.getItem(accessToken);
    }

    logout() {
        localStorage.removeItem(accessToken);
    }

    getProfile = () => decode(this.getToken())

    fetch = (url, options) => {

        const headers = {
            Accept: 'application/json',
            'Content-Type': 'application/json'
        };

        if (this.loggedIn()) {
            headers.Authorization = `Bearer ${this.getToken()}`;
        }

        return fetch(url, {
            headers,
            ...options
        })
            .then(this._checkStatus)
            .then(response => response.json());
    }

    _checkStatus(response) {
        if (response.status >= 200 && response.status < 300) {
            return response;
        } else {
            const error = new Error(response.statusText);
            error.response = response;
            throw error;
        }
    }
}